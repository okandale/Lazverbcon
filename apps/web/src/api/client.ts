import createClient from "openapi-fetch";
import type { components, paths } from "./schema";

export const api = createClient<paths>({
  baseUrl: window.location.origin,
  fetch: (request) => globalThis.fetch(request),
});
export type Entry = components["schemas"]["Entry"];
export type Request = components["schemas"]["ConjugationRequest"];
export type Response = components["schemas"]["ConjugationResponse"];
export type Match = components["schemas"]["Match"];
export type Dialect = components["schemas"]["Dialect"];

export const defaults: Request = {
  entry_id: "verb-0026",
  dialects: ["AS", "PZ", "FA", "HO"],
  subject: "all",
  object: null,
  tense: "present",
  mood: "indicative",
  derivation: "none",
  applicative: false,
  causative: "none",
  optional_preverb: false,
};

export async function requireData<T>(result: {
  data?: T;
  error?: unknown;
}): Promise<T> {
  if (result.data !== undefined) return result.data;
  const error = result.error as { detail?: unknown } | undefined;
  throw new Error(
    typeof error?.detail === "string"
      ? error.detail
      : "The request could not be completed.",
  );
}

export function requestFromMatch(match: Match): Request {
  const { dialect, ...features } = match.features;
  return { entry_id: match.entry.id, ...features, dialects: [dialect] };
}
