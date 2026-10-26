// @vitest-environment node
import { readFile } from "node:fs/promises";
import { expect, it } from "vitest";
import { guides } from "./keyboards";
it("includes installation, system activation and typing instructions for every platform", () => {
  expect(guides.windows.steps.length).toBeGreaterThanOrEqual(9);
  expect(guides.mac.steps.length).toBeGreaterThanOrEqual(9);
  expect(guides.android.steps.map((s) => s.body.en).join(" ")).toContain(
    "Enable Keyman as system-wide keyboard",
  );
  expect(guides.iphone.steps.map((s) => s.body.en).join(" ")).toContain(
    "Add New Keyboard",
  );
  expect(guides.iphone.steps.map((s) => s.body.en).join(" ")).toContain(
    "globe key",
  );
  expect(guides.phone.optional?.length).toBeGreaterThan(0);
});
it("has the source screenshot and bilingual text for each guide step", async () => {
  for (const guide of Object.values(guides)) {
    const steps = [
      ...guide.steps,
      ...(guide.optional ?? []).flatMap((section) => section.steps),
    ];
    for (const step of steps) {
      expect(
        step.title.en && step.title.tr && step.body.en && step.body.tr,
      ).toBeTruthy();
      if (step.image)
        expect(
          (
            await readFile(
              new URL(
                `../../public/images/keyboard/${step.image}`,
                import.meta.url,
              ),
            )
          ).length,
        ).toBeGreaterThan(0);
    }
  }
});
