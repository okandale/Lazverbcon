// @vitest-environment node
// Generated expected responses come from FastAPI, not from the static adapter.
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { StaticCatalog, createStaticFetch } from "./static";

const fixture = process.env.LAZ_STATIC_TEST_DIR;
describe.skipIf(!fixture)("published static catalog", () => {
  it("matches the API for verbs, options, cells, reverse search and suggestions", async () => {
    const data = resolve(process.env.LAZ_STATIC_DATA ?? `${fixture}/data`);
    const cases = JSON.parse(
      await readFile(resolve(fixture, "cases.json"), "utf8"),
    );
    const fetched = new Set();
    const fetchFile = async (url) => {
      expect(url).toMatch(/^\/static\//);
      const file = String(url).slice("/static/".length);
      fetched.add(file);
      return new Response(await readFile(resolve(data, file)));
    };
    const transport = createStaticFetch("/static", fetchFile);
    for (const test of cases) {
      const response = await transport(
        new Request(`http://static.test${test.path}`, {
          method: test.method,
          ...(test.body
            ? {
                body: JSON.stringify(test.body),
                headers: { "Content-Type": "application/json" },
              }
            : {}),
        }),
      );
      expect(
        await response.json(),
        `${test.path} ${JSON.stringify(test.body)}`,
      ).toEqual(test.expected);
    }
    expect([...fetched].some((file) => file.startsWith("exact/"))).toBe(true);
    expect([...fetched].some((file) => file.startsWith("verbs/"))).toBe(true);
  }, 120000);

  it("does not download the catalog for a verb directory query, and retries failures", async () => {
    const calls = [];
    let fail = true;
    const catalog = new StaticCatalog("/static", async (url) => {
      calls.push(url);
      if (fail) return new Response("unavailable", { status: 503 });
      return new Response(
        await readFile(
          resolve(
            process.env.LAZ_STATIC_DATA ?? `${fixture}/data`,
            String(url).slice(8),
          ),
        ),
      );
    });
    await expect(catalog.verbs()).rejects.toThrow("could not be loaded");
    // Let both parallel failed fetches settle before retrying.
    await new Promise((resolve) => setTimeout(resolve, 0));
    fail = false;
    expect((await catalog.verbs()).total).toBeGreaterThan(0);
    expect(new Set(calls)).toEqual(
      new Set(["/static/entries.json", "/static/manifest.json"]),
    );
  });

  it("rejects HTML returned for a missing data file", async () => {
    const catalog = new StaticCatalog(
      "/static",
      async () => new Response("<!doctype html>"),
    );
    await expect(catalog.entry("verb-0026")).rejects.toThrow(
      "published data is unavailable",
    );
  });
});
