import React from "react";
import { afterEach, expect, it, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReverseSearch } from "./ReverseSearch";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

function mount() {
  const onSearch = vi.fn();
  const queries: string[] = [];
  vi.stubGlobal(
    "fetch",
    vi.fn(async (request: Request) => {
      const url = new URL(request.url);
      const suggestions = url.pathname.endsWith("/suggestions");
      if (suggestions) queries.push(url.searchParams.get("q")!);
      return new Response(
        JSON.stringify(
          suggestions
            ? { suggestions: ["doviguram", "doviguramt"] }
            : { matches: [], total: 0, match_type: "none" },
        ),
        {
          headers: { "Content-Type": "application/json" },
        },
      );
    }),
  );
  render(
    <QueryClientProvider
      client={
        new QueryClient({ defaultOptions: { queries: { retry: false } } })
      }
    >
      <ReverseSearch language="en" onSearch={onSearch} onSelect={vi.fn()} />
    </QueryClientProvider>,
  );
  const input = screen.getByRole("combobox", { name: "Find a verb" });
  fireEvent.focus(input);
  fireEvent.change(input, { target: { value: "dovi" } });
  return { input, onSearch, queries };
}

it("shows suggestions and fills a clicked form before searching", async () => {
  const { input, onSearch, queries } = mount();
  const option = await screen.findByRole("option", { name: "doviguram" });
  expect(input.getAttribute("aria-expanded")).toBe("true");
  expect(queries).toEqual(["dovi"]);
  fireEvent.pointerDown(option);
  fireEvent.click(option);
  expect((input as HTMLInputElement).value).toBe("doviguram");
  expect(screen.queryByRole("listbox")).toBeNull();
  expect(onSearch).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole("button", { name: "Find its verb ↗" }));
  expect(onSearch).toHaveBeenCalledWith("doviguram");
});

it("supports arrow keys, Enter to fill, and Escape to dismiss", async () => {
  const { input, onSearch } = mount();
  await screen.findByRole("listbox");
  fireEvent.keyDown(input, { key: "ArrowUp" });
  const last = screen.getByRole("option", { name: "doviguramt" });
  expect(last.getAttribute("aria-selected")).toBe("true");
  expect(input.getAttribute("aria-activedescendant")).toBe(last.id);
  fireEvent.keyDown(input, { key: "Escape" });
  expect(screen.queryByRole("listbox")).toBeNull();
  expect(input.hasAttribute("aria-activedescendant")).toBe(false);
  fireEvent.keyDown(input, { key: "ArrowDown" });
  fireEvent.keyDown(input, { key: "Enter" });
  expect((input as HTMLInputElement).value).toBe("doviguram");
  expect(onSearch).not.toHaveBeenCalled();
  expect(screen.queryByRole("listbox")).toBeNull();
});

it("hides stale suggestions immediately when the prefix changes or is cleared", async () => {
  const { input, queries } = mount();
  await screen.findByRole("listbox");
  fireEvent.keyDown(input, { key: "ArrowDown" });
  fireEvent.change(input, { target: { value: "dog" } });
  expect(screen.queryByRole("listbox")).toBeNull();
  await screen.findByRole("listbox");
  expect(queries).toEqual(["dovi", "dog"]);
  expect(input.hasAttribute("aria-activedescendant")).toBe(false);
  fireEvent.change(input, { target: { value: "" } });
  expect(screen.queryByRole("listbox")).toBeNull();
});

it("dismisses on blur and keeps late results closed until focus returns", async () => {
  const { input, queries } = mount();
  fireEvent.blur(input);
  await waitFor(() => expect(queries).toEqual(["dovi"]));
  expect(screen.queryByRole("listbox")).toBeNull();
  fireEvent.focus(input);
  await screen.findByRole("listbox");
});

it("resets the input, results, suggestions and shared query", async () => {
  const { input, onSearch } = mount();
  await screen.findByRole("listbox");
  fireEvent.click(screen.getByRole("button", { name: "Find its verb ↗" }));
  await screen.findByText(/0 analyses/);
  fireEvent.click(screen.getByRole("button", { name: "Reset" }));
  expect((input as HTMLInputElement).value).toBe("");
  expect(screen.queryByText(/0 analyses/)).toBeNull();
  expect(screen.queryByRole("listbox")).toBeNull();
  expect(onSearch).toHaveBeenLastCalledWith("");
});
