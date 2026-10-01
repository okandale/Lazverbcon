import { afterEach, expect, it, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { Feedback } from "./Feedback";
import { sendFeedback } from "./feedbackDelivery";

vi.mock("./feedbackDelivery", () => ({ sendFeedback: vi.fn() }));
afterEach(() => {
  cleanup();
  vi.resetAllMocks();
});

function fill(language: "en" | "tr" = "en") {
  window.history.replaceState(
    null,
    "",
    "/feedback?context=%2Fconjugator%3Fselection%3Dexample",
  );
  const view = render(<Feedback language={language} />);
  const fields = screen.getAllByRole("textbox");
  ["doviba", "correction", "Hopa explanation"].forEach((value, i) =>
    fireEvent.change(fields[i], { target: { value } }),
  );
  return {
    ...view,
    fields,
    submit: screen.getByRole("button", {
      name: language === "en" ? "Send feedback" : "Geri bildirim gönder",
    }),
  };
}

it("sends context with the legacy fields, prevents duplicates and clears text only after success", async () => {
  let complete!: () => void;
  vi.mocked(sendFeedback).mockImplementation(
    () =>
      new Promise((resolve) => {
        complete = resolve;
      }),
  );
  const { fields, submit } = fill();
  fireEvent.click(submit);
  fireEvent.submit(submit.closest("form")!);
  expect(sendFeedback).toHaveBeenCalledTimes(1);
  expect(sendFeedback).toHaveBeenCalledWith(
    {
      incorrectWord: "doviba",
      correction: "correction",
      explanation:
        "Hopa explanation\n\nPage / selection: /conjugator?selection=example",
    },
    expect.any(AbortSignal),
  );
  expect((fields[0] as HTMLInputElement).value).toBe("doviba");
  expect((fields[0] as HTMLInputElement).disabled).toBe(true);
  complete();
  await screen.findByText("Feedback sent. Thank you.");
  expect((fields[0] as HTMLInputElement).value).toBe("");
});

it("preserves failed submissions and provides an email fallback and manual retry", async () => {
  vi.mocked(sendFeedback)
    .mockRejectedValueOnce(new Error("timeout"))
    .mockResolvedValueOnce(undefined);
  const { fields, submit } = fill();
  fireEvent.click(submit);
  await screen.findByRole("alert");
  expect((fields[0] as HTMLInputElement).value).toBe("doviba");
  expect(screen.queryByText("Nothing has been sent yet.")).toBeNull();
  const link = screen.getByRole("link", { name: "Open email app ↗" });
  expect(
    new URL(link.getAttribute("href")!).searchParams.get("body"),
  ).toContain("Hopa explanation");
  fireEvent.click(submit);
  await screen.findByText("Feedback sent. Thank you.");
  expect(sendFeedback).toHaveBeenCalledTimes(2);
});

it("supports Turkish success messages", async () => {
  vi.mocked(sendFeedback).mockResolvedValue(undefined);
  fireEvent.click(fill("tr").submit);
  await screen.findByText("Geri bildiriminiz gönderildi. Teşekkürler.");
});

it("cancels delivery when leaving the page", async () => {
  vi.mocked(sendFeedback).mockImplementation(
    (_data, signal) =>
      new Promise((_resolve, reject) => {
        signal.addEventListener("abort", () =>
          reject(new DOMException("Cancelled", "AbortError")),
        );
      }),
  );
  const { unmount, submit } = fill();
  fireEvent.click(submit);
  const signal = vi.mocked(sendFeedback).mock.calls[0][1];
  unmount();
  await waitFor(() => expect(signal.aborted).toBe(true));
});
