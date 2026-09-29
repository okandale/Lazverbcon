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
    screen.getByRole("link", { name: "Fiiller" }).getAttribute("href"),
  ).toBe("/verbs?lang=tr");
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
it("does not display placeholders or Hopa phrases as another dialect", () => {
  mount("/resources/phrase-guide/ardesen");
  expect(screen.getByRole("heading", { level: 1 }).textContent).toContain(
    "Ardeşen",
  );
  expect(screen.getByText(/don’t yet have reviewed Ardeşen/)).toBeTruthy();
  expect(screen.queryByText("İya muǩos ren?")).toBeNull();
});
it("prepares feedback with context without submitting to an external service", async () => {
  const fetch = vi.fn();
  vi.stubGlobal("fetch", fetch);
  mount(
    "/feedback?context=" + encodeURIComponent("/conjugator?selection=example"),
  );
  fireEvent.change(screen.getByLabelText("Form or text to review"), {
    target: { value: "test form" },
  });
  fireEvent.change(screen.getByLabelText("Suggested correction"), {
    target: { value: "correct form" },
  });
  fireEvent.change(screen.getByLabelText("Dialect, example or explanation"), {
    target: { value: "Hopa example" },
  });
  fireEvent.click(screen.getByRole("button", { name: "Prepare email →" }));
  const href = screen
    .getByRole("link", { name: "Open email app ↗" })
    .getAttribute("href")!;
  const body = new URL(href).searchParams.get("body");
  expect(body).toContain("Hopa example");
  expect(body).toContain("/conjugator?selection=example");
  expect(body).toContain("correct form");
  expect(fetch).not.toHaveBeenCalled();
  expect(screen.getByText("Nothing has been sent yet.")).toBeTruthy();
  fireEvent.change(screen.getByLabelText("Form or text to review"), {
    target: { value: "changed" },
  });
  expect(screen.queryByRole("link", { name: "Open email app ↗" })).toBeNull();
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
            },
            {
              id: "verb-0002",
              infinitive: "test",
              turkish: "iki",
              english: "two",
              verb_class: "TVM",
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
