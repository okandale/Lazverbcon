import { expect, it } from "vitest";
import { feedbackContext } from "./feedbackContext";
it("turns a selection into readable context", () => {
  const selection = JSON.stringify({
    entry_id: "verb-0232",
    tense: "past_progressive",
    object: null,
  });
  const context = feedbackContext(
    "/conjugator?verb=osinapu&selection=" + encodeURIComponent(selection),
    "en",
  )!;
  expect(context.text).toContain("Verb: osinapu");
  expect(context.text).toContain("Tense: Past progressive");
  expect(context.text).toContain("Object: None");
  expect(context.text).not.toContain("%7B");
  expect(context.text).not.toContain("entry_id");
  expect(context.link).toMatch(/^\/conjugator\?selection=/);
});
it("rejects external links, malformed selections and arbitrary context", () => {
  for (const raw of [
    "https://example.com/conjugator",
    "javascript:alert(1)",
    "/api/status",
    "/conjugator?selection=broken",
    "x".repeat(3001),
  ])
    expect(feedbackContext(raw, "en")).toBeNull();
});
