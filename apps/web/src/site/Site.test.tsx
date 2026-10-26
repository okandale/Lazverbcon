import { beforeEach, afterEach, expect, it, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Site } from "./Site";
import { phrases, vocabulary } from "./phrases";

beforeEach(() => {
  localStorage.clear();
  window.history.replaceState(null, "", "/");
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
function mount(path: string) {
  window.history.replaceState(null, "", path);
  render(
    <QueryClientProvider
      client={
        new QueryClient({ defaultOptions: { queries: { retry: false } } })
      }
    >
      <Site />
    </QueryClientProvider>,
  );
}
it("keeps the language across public page links and explicit shared links", () => {
  mount("/");
  fireEvent.click(screen.getByRole("button", { name: "TR" }));
  expect(document.documentElement.lang).toBe("tr");
  expect(localStorage.getItem("lazuri-language")).toBe("tr");
  expect(
    screen.getByRole("link", { name: "Fiil çekimi" }).getAttribute("href"),
  ).toBe("/conjugator?lang=tr");
  cleanup();
  mount("/about");
  expect(screen.getByRole("heading", { level: 1 }).textContent).toBe(
    "Bir fiil. Birçok ses.",
  );
  cleanup();
  mount("/about?lang=en");
  expect(document.documentElement.lang).toBe("en");
});
it("restores phrase categories, vocabulary, copy and browser back state", async () => {
  const copy = vi.fn().mockResolvedValue(undefined);
  Object.defineProperty(navigator, "clipboard", {
    configurable: true,
    value: { writeText: copy },
  });
  mount("/resources/phrase-guide/hopa?category=hotel");
  expect(screen.getByText("Oda giğunan-i?")).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "At the market" }));
  expect(new URLSearchParams(window.location.search).get("category")).toBe(
    "market",
  );
  fireEvent.click(screen.getByText("Words to use in this phrase"));
  expect(screen.getByText("Domatisi/Ǩaǩa")).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "Copy: İya muǩos ren?" }));
  await waitFor(() => expect(copy).toHaveBeenCalledWith("İya muǩos ren?"));
  window.history.replaceState(
    null,
    "",
    "/resources/phrase-guide/hopa?category=pharmacy",
  );
  fireEvent(window, new PopStateEvent("popstate"));
  expect(screen.getByText("Tiş ǯǩuni şeni ç̌ami minon")).toBeTruthy();
  expect(Object.values(phrases).flat()).toHaveLength(24);
  expect(vocabulary).toHaveLength(12);
});
it.each(["pazar", "ardesen", "findikli-arhavi"])(
  "preserves the unfinished %s guide without substituting Hopa translations",
  (dialect) => {
    mount(`/resources/phrase-guide/${dialect}`);
    expect(screen.getByText("Translation pending")).toBeTruthy();
    expect(screen.getByText("How much is this?")).toBeTruthy();
    expect(screen.getByText("...")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "At the pharmacy" }));
    expect(screen.getByText("I need medicine for a headache")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "At the restaurant" }));
    expect(screen.getByText("I’m vegetarian")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "At the hotel" })).toBeNull();
    expect(screen.queryByText("İya muǩos ren?")).toBeNull();
  },
);
it("shows readable feedback context and only offers email after delivery fails", () => {
  mount(
    "/feedback?context=" +
      encodeURIComponent(
        "/conjugator?verb=osinapu&selection=" +
          encodeURIComponent(
            JSON.stringify({
              entry_id: "verb-0232",
              tense: "past",
              object: null,
            }),
          ),
      ),
  );
  fireEvent.click(screen.getByText("Included page and selection"));
  expect(screen.getByText("osinapu")).toBeTruthy();
  expect(screen.getByText("Past")).toBeTruthy();
  expect(
    screen
      .getByRole("link", { name: "Open this selection" })
      .getAttribute("href"),
  ).toContain("/conjugator?selection=");
  expect(screen.queryByText("Prepare email instead")).toBeNull();
  expect(screen.queryByRole("link", { name: "Open email app ↗" })).toBeNull();
  expect(screen.getByRole("main").textContent).not.toContain("%7B");
});
it("links homographs to their own entries and resets directory paging on search", async () => {
  const requests: URL[] = [];
  vi.stubGlobal(
    "fetch",
    vi.fn(async (request: Request) => {
      const url = new URL(request.url);
      requests.push(url);
      return new Response(
        JSON.stringify({
          total: 31,
          entries: [
            {
              id: "verb-0001",
              infinitive: "test",
              turkish: "bir",
              english: "one",
              verb_class: "TVE",
              variants: [{ form: "test", dialects: ["AS"] }],
            },
            {
              id: "verb-0002",
              infinitive: "test",
              turkish: "iki",
              english: "two",
              verb_class: "TVM",
              variants: [{ form: "test", dialects: ["AS"] }],
            },
          ],
        }),
        { headers: { "Content-Type": "application/json" } },
      );
    }),
  );
  mount("/verbs");
  const links = await screen.findAllByRole("link", { name: "test ↗" });
  expect(
    links.map(
      (a) =>
        JSON.parse(
          new URL(a.getAttribute("href")!, location.origin).searchParams.get(
            "selection",
          )!,
        ).entry_id,
    ),
  ).toEqual(["verb-0001", "verb-0002"]);
  fireEvent.click(screen.getByRole("button", { name: "Next →" }));
  await waitFor(() =>
    expect(requests.at(-1)?.searchParams.get("offset")).toBe("30"),
  );
  fireEvent.change(screen.getByLabelText("Search verbs"), {
    target: { value: "changed" },
  });
  await waitFor(() =>
    expect(requests.at(-1)?.searchParams.get("q")).toBe("changed"),
  );
  expect(requests.at(-1)?.searchParams.get("offset")).toBe("0");
});
it("offers recovery for an unmapped old verb link and a genuine not-found page", () => {
  mount("/v2/verb/123/TVE");
  expect(
    screen
      .getByRole("link", { name: "Search the verbs →" })
      .getAttribute("href"),
  ).toContain("/verbs");
  cleanup();
  mount("/does-not-exist");
  expect(screen.getByText("404")).toBeTruthy();
});

it("keeps the verb directory out of home cards and global navigation", () => {
  mount("/");
  expect(screen.queryByRole("link", { name: /06 Verb list/ })).toBeNull();
  expect(screen.queryByRole("link", { name: "Verbs" })).toBeNull();
  expect(
    screen
      .getAllByRole("link")
      .filter((a) => a.classList.contains("resource-card")),
  ).toHaveLength(5);
});

it("opens the nested verb list for a legacy trailing-slash directory link", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn(
      async () =>
        new Response(JSON.stringify({ entries: [], total: 0 }), {
          headers: { "Content-Type": "application/json" },
        }),
    ),
  );
  mount("/verbs/");
  expect(
    await screen.findByRole("textbox", { name: "Search verbs" }),
  ).toBeTruthy();
  expect(
    screen
      .getByRole("tab", { name: "Verb list" })
      .getAttribute("aria-selected"),
  ).toBe("true");
  expect(
    screen
      .getByRole("link", { name: "Conjugator" })
      .getAttribute("aria-current"),
  ).toBe("page");
});
