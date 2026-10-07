import { expect, it } from "vitest";
import { defaults } from "./client";
import { parseSelection } from "./selection";

it("round trips explicit prefix selections", () => {
  const selected = { ...defaults, optional_prefix: "do" };
  expect(parseSelection(JSON.stringify(selected))).toEqual(selected);
});

it("keeps typed prefix selections for data-driven validation", () => {
  expect(
    parseSelection(JSON.stringify({ ...defaults, optional_preverb: true })),
  ).toMatchObject({ optional_preverb: true, optional_prefix: "none" });
  expect(
    parseSelection(
      JSON.stringify({
        ...defaults,
        optional_preverb: true,
        optional_prefix: "ko",
      }),
    ),
  ).toMatchObject({ optional_preverb: true, optional_prefix: "ko" });
});

it("round trips admin-created entry IDs and rejects paths", () => {
  const selected = { ...defaults, entry_id: "entry-123abc" };
  expect(parseSelection(JSON.stringify(selected))).toEqual(selected);
  expect(
    parseSelection(JSON.stringify({ ...selected, entry_id: "../private" })),
  ).toEqual(defaults);
});
