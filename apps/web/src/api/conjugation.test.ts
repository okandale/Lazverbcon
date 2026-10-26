import { afterEach, expect, it, vi } from "vitest";
import { defaults, defaultsForEntry } from "./client";
import type { Entry, Response } from "./client";
import {
  conjugateSelection,
  mergeDefaultObjectResults,
  selectionOptions,
} from "./conjugation";

const entry: Entry = {
  id: "verb-0232",
  infinitive: "osinapu",
  english: "to speak",
  turkish: "konuşmak",
  verb_class: "TVE",
  source_row: 232,
  issues: [],
  variants: [{ form: "isinapams", dialects: ["AS", "PZ", "FA"] }],
};
const base: Response = {
  entry,
  source: "database",
  cells: [
    {
      features: {
        dialect: "AS",
        subject: "1sg",
        object: null,
        tense: "present",
        mood: "indicative",
        derivation: "none",
        applicative: false,
        causative: "none",
        optional_preverb: false,
        optional_prefix: "none",
      },
      status: "not_generated",
      forms: [],
    },
  ],
};
const implicit: Response = {
  ...base,
  cells: [
    {
      ...base.cells[0],
      features: { ...base.cells[0].features, object: "3sg" },
      status: "ok",
      forms: [
        {
          spelling: "visinapam",
          frame: "Ergative",
          subject: "1sg",
          object: "3sg",
          subject_pronoun: "ma",
          object_pronoun: "heyas",
          rule: "editorial",
        },
      ],
    },
  ],
};
afterEach(() => vi.unstubAllGlobals());
it("starts with None and only the entry's available dialects", () => {
  expect(defaults.object).toBeNull();
  expect(defaultsForEntry(entry)).toMatchObject({
    object: null,
    dialects: ["AS", "PZ", "FA"],
  });
});
it("finds an implicit O3SG form when the objectless request has no row", () => {
  const result = mergeDefaultObjectResults(base, implicit);
  expect(result.cells[0].status).toBe("ok");
  expect(result.cells[0].forms?.[0].spelling).toBe("visinapam");
  expect(result.cells[0].features.object).toBeNull();
});
it("retains distinct objectless forms and removes duplicate spellings for None", () => {
  const objectless = {
    ...base,
    cells: [
      {
        ...base.cells[0],
        status: "ok" as const,
        forms: [
          { ...implicit.cells[0].forms![0], object: null },
          {
            ...implicit.cells[0].forms![0],
            object: null,
            spelling: "alternative",
          },
        ],
      },
    ],
  };
  expect(
    mergeDefaultObjectResults(objectless, implicit).cells[0].forms?.map(
      (f) => f.spelling,
    ),
  ).toEqual(["visinapam", "alternative"]);
});
it("expands only None; an explicit object remains an exact request", async () => {
  const objects: unknown[] = [];
  vi.stubGlobal(
    "fetch",
    vi.fn(async (request: globalThis.Request) => {
      const body = await request.json();
      objects.push(body.object);
      return new globalThis.Response(
        JSON.stringify(body.object === null ? base : implicit),
        { headers: { "Content-Type": "application/json" } },
      );
    }),
  );
  expect((await conjugateSelection(defaults)).cells[0].status).toBe("ok");
  expect(objects).toEqual([null, "3sg"]);
  objects.length = 0;
  await conjugateSelection({ ...defaults, object: "2sg" });
  expect(objects).toEqual(["2sg"]);
});
it("keeps the None option available for an attested implicit object", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn(async (request: globalThis.Request) => {
      const { object } = await request.json();
      return new globalThis.Response(
        JSON.stringify({
          dialects: ["AS"],
          options: {
            object: [
              {
                value: null,
                enabled: false,
                reason: "missing",
                reason_code: "not_generated",
              },
              {
                value: "3sg",
                enabled: object === "3sg",
                reason: null,
                reason_code: null,
              },
            ],
            tense: [
              {
                value: "present",
                enabled: object === "3sg",
                reason: null,
                reason_code: null,
              },
            ],
          },
        }),
        { headers: { "Content-Type": "application/json" } },
      );
    }),
  );
  const options = await selectionOptions(defaults);
  expect(options.options.object[0]).toMatchObject({
    value: null,
    enabled: true,
    reason: null,
  });
  expect(options.options.tense[0].enabled).toBe(true);
});

it("keeps a real implicit-query failure visible when neither request returns forms", () => {
  const failed = {
    ...implicit,
    cells: [
      {
        ...implicit.cells[0],
        status: "error" as const,
        forms: [],
        reason: "engine_failure",
        message: "Engine failed",
      },
    ],
  };
  expect(mergeDefaultObjectResults(base, failed).cells[0]).toMatchObject({
    status: "error",
    reason: "engine_failure",
  });
});
