// @vitest-environment node
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { StaticCatalog } from "./static";

const fixture = process.env.LAZ_ADMIN_STATIC_TEST_DIR;
describe.skipIf(!fixture)("approved editorial export", () => {
  it("uses approved exceptions for forward lookup, options, reverse and suggestions", async () => {
    const selection = JSON.parse(
      await readFile(resolve(fixture, "selection.json"), "utf8"),
    );
    const catalog = new StaticCatalog(
      "/data",
      async (url) =>
        new Response(
          await readFile(resolve(fixture, "data", String(url).slice(6))),
        ),
    );
    const result = await catalog.conjugate(selection);
    expect(result.cells[0].status).toBe("ok");
    expect(result.cells[0].forms[0]).toMatchObject({
      spelling: "author-exception",
      subject_pronoun: "reviewed-subject",
      object_pronoun: "reviewed-object",
    });
    const options = await catalog.options(selection);
    expect(options.options.object.find((v) => v.value === "2sg").enabled).toBe(
      true,
    );
    expect(
      options.options.optional_prefix.find((v) => v.value === "ko").enabled,
    ).toBe(true);
    const initialOptions = await catalog.options({
      entry_id: selection.entry_id,
    });
    expect(
      initialOptions.options.object.find((v) => v.value === "2sg").enabled,
    ).toBe(true);
    expect(
      initialOptions.options.optional_prefix.find((v) => v.value === "ko")
        .enabled,
    ).toBe(true);
    expect((await catalog.reverse("author-exception")).total).toBe(1);
    expect((await catalog.suggestions("author")).suggestions).toEqual([
      "author-exception",
    ]);
    expect((await catalog.reverse("private-draft")).total).toBe(0);
    const absent = await catalog.conjugate({ ...selection, subject: "2sg" });
    expect(absent.cells[0].status).toBe("unsupported");
  });
});
