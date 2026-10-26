import React from "react";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";
import { Results } from "./Results";
import type { Response } from "../../api/client";
const data = {
  entry: {},
  source: "database",
  cells: [
    {
      features: { dialect: "AS" },
      status: "ok",
      forms: [
        {
          subject: "1sg",
          object: "3sg",
          subject_pronoun: "ma",
          object_pronoun: "heyas",
          spelling: "visinapam",
        },
      ],
    },
    {
      features: { dialect: "HO" },
      status: "unsupported",
      forms: [],
      reason: "dialect_unavailable",
      message: "No principal part",
    },
  ],
} as Response;
afterEach(cleanup);
it("shows the translated subject and hides Laz pronouns and the implicit object", () => {
  render(<Results data={data} language="en" object={null} />);
  expect(screen.getByRole("cell", { name: "I" })).toBeTruthy();
  expect(screen.getByText("visinapam")).toBeTruthy();
  expect(screen.queryByText("ma")).toBeNull();
  expect(screen.queryByText("heyas")).toBeNull();
  expect(screen.queryByRole("columnheader", { name: "Object" })).toBeNull();
  expect(screen.queryByText(/Some combinations/)).toBeNull();
});
it("distinguishes explicitly requested objects with translated labels", () => {
  render(<Results data={data} language="tr" object="all" />);
  expect(screen.getByRole("cell", { name: "Ben" })).toBeTruthy();
  expect(screen.getByRole("cell", { name: "O" })).toBeTruthy();
});
