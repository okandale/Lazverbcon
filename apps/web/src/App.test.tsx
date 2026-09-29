import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { App } from "./App";
import { defaults, requestFromMatch } from "./api/client";
import { parseSelection } from "./api/selection";
import type { Match } from "./api/client";

const entry = {
  id: "verb-0232",
  infinitive: "osinapu",
  verb_class: "TVE",
  english: "to speak",
  turkish: "konuşmak",
  variants: [{ form: "isinapams", dialects: ["AS"] }],
  source_row: 232,
  issues: [],
};
const features = {
  dialect: "AS",
  subject: "1sg",
  object: null,
  tense: "present",
  mood: "indicative",
  derivation: "none",
  applicative: false,
  causative: "none",
  optional_preverb: false,
};
const form = {
  spelling: "visinapam",
  frame: "Ergative",
  subject: "1sg",
  object: null,
  subject_pronoun: "ma",
  object_pronoun: "",
  rule: "tve_present",
};
const match = { entry, features, form } as Match;
const calls: Record<string, unknown>[] = [];

beforeEach(() => {
  localStorage.clear();
  calls.length = 0;
  window.history.replaceState(null, "", "/");
  vi.stubGlobal(
    "fetch",
    vi.fn(async (request: globalThis.Request) => {
      const url = new URL(request.url);
      let data: unknown;
      if (url.pathname.endsWith("/suggestions"))
        data = { suggestions: ["visinapam"] };
      else if (url.pathname.endsWith("/conjugation-options"))
        data = { dialects: ["AS"], options: {} };
      else if (url.pathname.endsWith("/conjugations")) {
        calls.push(await request.clone().json());
        data = {
          entry,
          source: "database",
          cells: [{ features, status: "ok", forms: [form] }],
        };
      } else if (url.pathname.endsWith("/reverse"))
        data = { match_type: "exact", total: 1, matches: [match] };
      else if (url.pathname.endsWith("/verbs"))
        data = { entries: [entry], total: 1 };
      else data = entry;
      return new globalThis.Response(JSON.stringify(data), {
        headers: { "Content-Type": "application/json" },
      });
    }),
  );
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

function mount() {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  render(
    <QueryClientProvider client={client}>
      <App />
    </QueryClientProvider>,
  );
}

describe("conjugator journeys", () => {
  it("shows forms and clears them when the selection changes", async () => {
    mount();
    await screen.findByText("visinapam");
    fireEvent.change(screen.getByLabelText("Tense"), {
      target: { value: "past" },
    });
    expect(screen.queryByText("visinapam")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: /Conjugate verb/ }));
    await waitFor(() => expect(calls.at(-1)?.tense).toBe("past"));
  });

  it("carries a reverse analysis into a valid conjugation request", async () => {
    mount();
    await screen.findByText("visinapam");
    fireEvent.click(screen.getByRole("tab", { name: /Find a verb/ }));
    fireEvent.change(screen.getByRole("combobox", { name: "Find a verb" }), {
      target: { value: "visinapam" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Find its verb ↗" }));
    fireEvent.click(
      await screen.findByRole("button", { name: "Explore this form →" }),
    );
    await waitFor(() => expect(calls.at(-1)?.subject).toBe("1sg"));
    expect(calls.at(-1)?.dialects).toEqual(["AS"]);
    expect(calls.at(-1)).not.toHaveProperty("dialect");
  });

  it("rejects an empty dialect selection without sending a request", async () => {
    mount();
    await screen.findByText("visinapam");
    for (const name of [
      "AŞ Ardeşen",
      "PZ Pazar",
      "FA Fındıklı · Arhavi",
      "HO Hopa",
    ]) {
      fireEvent.click(screen.getByRole("checkbox", { name }));
    }
    const count = calls.length;
    fireEvent.click(screen.getByRole("button", { name: /Conjugate verb/ }));
    expect(screen.getByRole("status").textContent).toContain(
      "Select at least one dialect",
    );
    expect(calls.length).toBe(count);
  });

  it("submits the potential optative through the regular controls", async () => {
    mount();
    await screen.findByText("visinapam");
    fireEvent.change(screen.getByLabelText("Mood"), {
      target: { value: "optative" },
    });
    fireEvent.change(screen.getByLabelText("Derivation"), {
      target: { value: "potential" },
    });
    fireEvent.click(screen.getByRole("button", { name: /Conjugate verb/ }));
    await waitFor(() =>
      expect(calls.at(-1)).toMatchObject({
        mood: "optative",
        derivation: "potential",
      }),
    );
  });

  it("restores a shared reverse search and language, then opens the analysis", async () => {
    window.history.replaceState(null, "", "/?reverse=visinapam&lang=tr");
    mount();
    fireEvent.click(
      await screen.findByRole("button", { name: "Bu çekimi incele →" }),
    );
    await waitFor(() => expect(calls.at(-1)?.subject).toBe("1sg"));
    const params = new URLSearchParams(window.location.search);
    expect(params.has("reverse")).toBe(false);
    expect(JSON.parse(params.get("selection")!).entry_id).toBe(entry.id);
  });

  it("shares a reverse search instead of a stale forward selection", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText },
    });
    mount();
    fireEvent.click(screen.getByRole("tab", { name: /Find a verb/ }));
    fireEvent.change(screen.getByRole("combobox", { name: "Find a verb" }), {
      target: { value: "visinapam" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Find its verb ↗" }));
    await screen.findByRole("button", { name: "Explore this form →" });
    fireEvent.click(screen.getByRole("button", { name: "Share ↗" }));
    const url = new URL(writeText.mock.calls[0][0]);
    expect(url.searchParams.get("reverse")).toBe("visinapam");
    expect(url.searchParams.has("selection")).toBe(false);
  });
});

it("validates shared selections and drops unrelated fields", () => {
  expect(parseSelection("{broken")).toEqual(defaults);
  expect(
    parseSelection(JSON.stringify({ entry_id: "verb-0232", dialects: "HO" })),
  ).toEqual(defaults);
  const selection = parseSelection(
    JSON.stringify({ ...defaults, dialects: ["HO"], unknown: true }),
  );
  expect(selection.dialects).toEqual(["HO"]);
  expect(selection).not.toHaveProperty("unknown");
  expect(parseSelection(JSON.stringify(requestFromMatch(match)))).toEqual(
    requestFromMatch(match),
  );
});
