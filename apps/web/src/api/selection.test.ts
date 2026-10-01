import { expect, it } from "vitest";
import { defaults } from "./client";
import { parseSelection } from "./selection";

it("round trips explicit prefix selections", () => {
  const selected = { ...defaults, optional_prefix: "do" };
  expect(parseSelection(JSON.stringify(selected))).toEqual(selected);
});

it("keeps old boolean links and rejects conflicting prefix choices", () => {
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
  ).toEqual(defaults);
});
