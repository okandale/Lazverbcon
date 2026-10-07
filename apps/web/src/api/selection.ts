import { defaults } from "./client";
import type { Request } from "./client";

const values = {
  subject: ["all", "1sg", "2sg", "3sg", "1pl", "2pl", "3pl"],
  object: [null, "all", "1sg", "2sg", "3sg", "1pl", "2pl", "3pl"],
  tense: ["present", "past", "future", "past_progressive", "present_perfect"],
  mood: ["indicative", "optative", "imperative", "negative_imperative"],
  derivation: ["none", "potential", "passive"],
  causative: ["none", "simple", "double"],
  optional_prefix: ["none", "ko", "do"],
};

/** Validate URL data before it reaches controls; API validation remains authoritative. */
export function parseSelection(encoded: string | null): Request {
  if (!encoded) return { ...defaults };
  try {
    const input: unknown = JSON.parse(encoded);
    if (!input || typeof input !== "object" || Array.isArray(input))
      return { ...defaults };
    const data = input as Record<string, unknown>;
    const result = { ...defaults } as Record<string, unknown>;
    if (
      typeof data.entry_id !== "string" ||
      !/^[A-Za-z0-9][A-Za-z0-9_-]{0,99}$/.test(data.entry_id)
    )
      return { ...defaults };
    result.entry_id = data.entry_id;
    for (const [field, allowed] of Object.entries(values)) {
      if (field in data) {
        if (!(allowed as unknown[]).includes(data[field]))
          return { ...defaults };
        result[field] = data[field];
      }
    }
    if ("dialects" in data) {
      if (
        !Array.isArray(data.dialects) ||
        data.dialects.length < 1 ||
        data.dialects.length > 4 ||
        data.dialects.some((d) => !["AS", "PZ", "FA", "HO"].includes(d))
      )
        return { ...defaults };
      result.dialects = [...new Set(data.dialects)];
    }
    for (const field of ["applicative", "optional_preverb"]) {
      if (field in data) {
        if (typeof data[field] !== "boolean") return { ...defaults };
        result[field] = data[field];
      }
    }
    return result as Request;
  } catch {
    return { ...defaults };
  }
}
