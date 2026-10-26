import { api, requireData } from "./client";
import type { Options, Request, Response } from "./client";

/** The original website's None choice searches objectless and implicit O3SG rows. */
export function mergeDefaultObjectResults(
  base: Response,
  implicit: Response,
): Response {
  return {
    ...base,
    cells: base.cells.map((cell): Response["cells"][number] => {
      const alternate = implicit.cells.find(
        (candidate) =>
          candidate.features.dialect === cell.features.dialect &&
          candidate.features.subject === cell.features.subject,
      );
      const supported = [cell, alternate].filter(
        (candidate) =>
          candidate?.status === "ok" && (candidate.forms?.length ?? 0) > 0,
      );
      if (!supported.length)
        return alternate?.status === "error" ? alternate : cell;
      const forms = supported.flatMap((candidate) => candidate?.forms ?? []);
      return {
        ...cell,
        status: "ok",
        reason: null,
        message: null,
        forms: forms.filter(
          (form, index) =>
            index ===
            forms.findIndex(
              (other) =>
                other.spelling === form.spelling &&
                other.frame === form.frame &&
                other.subject === form.subject,
            ),
        ),
      };
    }),
  };
}

export async function conjugateSelection(
  selection: Request,
  signal?: AbortSignal,
) {
  const fetch = async (body: Request) =>
    requireData(await api.POST("/api/v1/conjugations", { body, signal }));
  if (selection.object != null) return fetch(selection);
  const [base, implicit] = await Promise.all([
    fetch(selection),
    fetch({ ...selection, object: "3sg" }),
  ]);
  return mergeDefaultObjectResults(base, implicit);
}

export async function selectionOptions(
  selection: Request,
  signal?: AbortSignal,
): Promise<Options> {
  const fetch = async (body: Request) =>
    requireData(
      await api.POST("/api/v1/conjugation-options", { body, signal }),
    );
  if (selection.object != null) return fetch(selection);
  const [base, implicit] = await Promise.all([
    fetch(selection),
    fetch({ ...selection, object: "3sg" }),
  ]);
  return {
    ...base,
    options: Object.fromEntries(
      Object.entries(base.options).map(([field, choices]) => [
        field,
        choices.map((choice) => {
          const alternative = implicit.options[field]?.find(
            (other) =>
              other.value ===
              (field === "object" && choice.value === null
                ? "3sg"
                : choice.value),
          );
          const enabled =
            choice.enabled ||
            (!!alternative?.enabled &&
              (field !== "object" || choice.value === null));
          return enabled
            ? { ...choice, enabled: true, reason: null, reason_code: null }
            : choice;
        }),
      ]),
    ),
  };
}
