import React from "react";
import { afterEach, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { ReverseMatch } from "./ReverseMatch";
import { requestFromMatch } from "../../api/client";
import type { Match } from "../../api/client";

afterEach(cleanup);

const features: Match["features"] = {
  dialect: "AS",
  subject: "1sg",
  object: null,
  tense: "present",
  mood: "optative",
  derivation: "none",
  applicative: false,
  causative: "none",
  optional_preverb: false,
};
const form: Match["form"] = {
  spelling: "doviba",
  frame: "Nominative",
  subject: "1sg",
  object: null,
  subject_pronoun: "ma",
  object_pronoun: "",
  rule: "tvm_tense",
};
const match: Match = {
  entry: {
    id: "verb-0020",
    infinitive: "dobalu",
    english: "to flow, to leak",
    turkish: "akmak",
    verb_class: "TVM",
    variants: [],
    source_row: 20,
    issues: [],
  },
  features,
  form,
  variants: [
    { features, form },
    { features: { ...features, dialect: "PZ" }, form },
    { features: { ...features, dialect: "HO", optional_preverb: true }, form },
  ],
};

it("shows combined dialects and opens only dialects supporting the chosen setting", () => {
  const onSelect = vi.fn();
  render(<ReverseMatch match={match} language="en" onSelect={onSelect} />);
  expect(screen.getByText(/Ardeşen · Pazar · Hopa/)).toBeTruthy();
  // Collapsed details leave one primary action visible.
  fireEvent.click(screen.getByRole("button", { name: "Explore this form →" }));
  expect(requestFromMatch(onSelect.mock.calls[0][0])).toMatchObject({
    entry_id: "verb-0020",
    dialects: ["AS", "PZ"],
    optional_preverb: false,
  });
});

it("keeps a dialect requiring the optional preverb accessible in details", () => {
  const onSelect = vi.fn();
  render(<ReverseMatch match={match} language="en" onSelect={onSelect} />);
  fireEvent.click(screen.getByText("Dialects and options"));
  fireEvent.click(
    screen.getByRole("button", {
      name: "Explore this form: Hopa · Optional preverb",
    }),
  );
  expect(requestFromMatch(onSelect.mock.calls[0][0])).toMatchObject({
    dialects: ["HO"],
    optional_preverb: true,
  });
});

it("opens all grouped dialects when their optional-preverb setting agrees", () => {
  const group = {
    ...match,
    variants: match.variants.map((v) => ({
      ...v,
      features: { ...v.features, optional_preverb: false },
    })),
  };
  expect(requestFromMatch(group).dialects).toEqual(["AS", "PZ", "HO"]);
});
