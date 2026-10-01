/** Browser queries over a published catalog. No morphology rules run here. */
import type { components } from "./schema";
type Entry = components["schemas"]["Entry"];
type Features = components["schemas"]["Features"];
type Form = components["schemas"]["Form"];
type Selection = components["schemas"]["ConjugationRequest"];
type Match = components["schemas"]["Match"];
type Value = string | boolean | null;
type Problem = [string, string];
type Bounds = [string, string, string][];
type Ref = [number, number, number];
type Exact = [string, string, Ref[]];
type Alias = [string, string[]];
type Chunk = {
  forms: string[][];
  requests: Record<string, number[]>;
  unsupported: Record<string, Problem>;
};
type Manifest = {
  schema_version: number;
  feature_fields: (keyof Features)[];
  form_fields: (keyof Form)[];
  dimensions: Value[][];
  forward: Record<string, Record<string, string>>;
  indexes: Record<"exact" | "alternate" | "broad", Bounds>;
  casefold: Record<string, string>;
  whitespace: string;
  alternates: [string, string][];
};
type Validation = {
  reasons: (Problem | null)[];
  tables: string[];
  entries: Record<
    string,
    {
      table: number;
      dialects: Features["dialect"][];
      prefixes: Record<string, string[]>;
    }
  >;
};

// SQLite orders Unicode text by code point, unlike JS's UTF-16 default sort.
function compare(a: string, b: string): number {
  const left = Array.from(a),
    right = Array.from(b);
  for (let i = 0; i < Math.min(left.length, right.length); i++) {
    const difference = left[i].codePointAt(0)! - right[i].codePointAt(0)!;
    if (difference) return difference;
  }
  return left.length - right.length;
}
function canonical(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value !== null && typeof value === "object") {
    return `{${Object.entries(value)
      .sort(([a], [b]) => compare(a, b))
      .map(([key, val]) => `${JSON.stringify(key)}:${canonical(val)}`)
      .join(",")}}`;
  }
  return JSON.stringify(value);
}
function indexOf(bounds: Bounds, key: string): number {
  let low = 0,
    high = bounds.length;
  while (low < high) {
    const middle = (low + high) >>> 1;
    if (compare(bounds[middle][1], key) < 0) low = middle + 1;
    else high = middle;
  }
  return low;
}

export class StaticCatalog {
  private cache = new Map<string, { value: unknown; bytes: number }>();
  private pending = new Map<string, Promise<unknown>>();
  private bytes = 0;
  constructor(
    private root: string,
    private fetchFile: typeof fetch = (...args) => globalThis.fetch(...args),
  ) {}

  private async load<T>(path: string): Promise<T> {
    const cached = this.cache.get(path);
    if (cached) {
      this.cache.delete(path);
      this.cache.set(path, cached);
      return cached.value as T;
    }
    if (!this.pending.has(path)) {
      const promise = (async () => {
        const response = await this.fetchFile(`${this.root}/${path}`);
        if (!response.ok)
          throw new Error(
            "The published data could not be loaded. Check your connection and reload the page.",
          );
        const text = await response.text();
        let value: unknown;
        try {
          value = JSON.parse(text);
        } catch {
          throw new Error(
            "The published data is unavailable. Reload the page to get the latest release.",
          );
        }
        const bytes = text.length * 2;
        this.cache.set(path, { value, bytes });
        this.bytes += bytes;
        // Bound cached encoded data. Parsed objects add overhead, but we never
        // retain the entire catalog as users browse across verbs and searches.
        while (this.bytes > 12 * 1024 * 1024 && this.cache.size > 1) {
          const oldest = this.cache.keys().next().value!;
          this.bytes -= this.cache.get(oldest)!.bytes;
          this.cache.delete(oldest);
        }
        return value;
      })().finally(() => this.pending.delete(path));
      this.pending.set(path, promise);
    }
    return this.pending.get(path)! as Promise<T>;
  }
  private async manifest() {
    const manifest = await this.load<Manifest>("manifest.json");
    if (manifest.schema_version !== 1)
      throw new Error("This data release needs a newer app. Reload the page.");
    return manifest;
  }
  private normalize(value: string, m: Manifest): string {
    const chars = Array.from(value);
    while (chars.length && m.whitespace.includes(chars[0])) chars.shift();
    while (chars.length && m.whitespace.includes(chars.at(-1)!)) chars.pop();
    return chars
      .map((c) => m.casefold[c] ?? c)
      .join("")
      .normalize("NFC");
  }
  private strict(value: string, m: Manifest): string {
    const replacements = new Map(m.alternates);
    const pattern = new RegExp(
      m.alternates
        .map(([key]) => key)
        .sort((a, b) => b.length - a.length)
        .map((key) => key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
        .join("|"),
      "g",
    );
    return this.normalize(
      this.normalize(value, m).replace(pattern, (key) =>
        replacements.get(key)!,
      ),
      m,
    );
  }
  private code(f: Features, m: Manifest, base = false): number {
    let code = 0;
    for (let i = base ? 1 : 0; i < m.dimensions.length - (base ? 1 : 0); i++) {
      const index = m.dimensions[i].indexOf(f[m.feature_fields[i]] ?? null);
      if (index < 0) throw new Error("Invalid conjugation selection.");
      code = code * m.dimensions[i].length + index;
    }
    return code;
  }
  private features(code: number, m: Manifest): Features {
    const values: Value[] = [];
    for (let i = m.dimensions.length - 1; i >= 0; i--) {
      values[i] = m.dimensions[i][code % m.dimensions[i].length];
      code = Math.floor(code / m.dimensions[i].length);
    }
    return Object.fromEntries(
      m.feature_fields.map((field, i) => [field, values[i]]),
    ) as Features;
  }
  private form(row: string[], features: Features, m: Manifest): Form {
    return {
      ...Object.fromEntries(m.form_fields.map((field, i) => [field, row[i]])),
      subject: features.subject,
      object: features.object ?? null,
    } as Form;
  }
  private validate(
    id: string,
    f: Features,
    v: Validation,
    tables: string[],
    m: Manifest,
  ): Problem | null {
    if (f.optional_preverb && f.optional_prefix !== "none")
      return [
        "prefix_conflict",
        "Choose an explicit prefix or the legacy option, not both.",
      ];
    const entry = v.entries[id];
    if (!entry.dialects.includes(f.dialect))
      return [
        "dialect_unavailable",
        "This entry has no principal part in this dialect.",
      ];
    if (
      f.optional_prefix !== "none" &&
      !entry.prefixes[f.dialect].includes(f.optional_prefix)
    )
      return [
        "prefix_unavailable",
        "This prefix is not attested for this verb and dialect.",
      ];
    return v.reasons[tables[entry.table].charCodeAt(this.code(f, m, true))];
  }
  private expand(
    selection: Selection,
    dialects: Features["dialect"][],
    m: Manifest,
  ): Features[] {
    const subjects =
      selection.subject === "all"
        ? m.dimensions[1]
        : [selection.subject ?? "all"];
    const objects =
      selection.object === "all" ? m.dimensions[1] : [selection.object ?? null];
    return dialects.flatMap((dialect) =>
      subjects.flatMap((subject) =>
        objects.map(
          (object) =>
            ({
              dialect,
              subject,
              object,
              tense: selection.tense ?? "present",
              mood: selection.mood ?? "indicative",
              derivation: selection.derivation ?? "none",
              applicative: selection.applicative ?? false,
              causative: selection.causative ?? "none",
              optional_preverb: selection.optional_preverb ?? false,
              optional_prefix: selection.optional_prefix ?? "none",
            }) as Features,
        ),
      ),
    );
  }
  async verbs(q = "", limit = 30, offset = 0) {
    const [entries, m] = await Promise.all([
      this.load<Entry[]>("entries.json"),
      this.manifest(),
    ]);
    const key = this.normalize(q, m);
    const found = entries.filter((e) =>
      this.normalize(`${e.infinitive} ${e.english} ${e.turkish}`, m).includes(
        key,
      ),
    );
    return {
      entries: found.slice(offset, offset + limit),
      total: found.length,
    };
  }
  async entry(id: string) {
    const entry = (await this.load<Entry[]>("entries.json")).find(
      (e) => e.id === id,
    );
    if (!entry) throw new Error("Unknown verb entry.");
    return entry;
  }
  async conjugate(selection: Selection) {
    const [entry, m, v] = await Promise.all([
      this.entry(selection.entry_id),
      this.manifest(),
      this.load<Validation>("validation.json"),
    ]);
    const tables = v.tables.map((table) => atob(table));
    const features = this.expand(
      { ...selection, subject: selection.subject ?? "all" },
      [
        ...new Set(selection.dialects ?? m.dimensions[0]),
      ] as Features["dialect"][],
      m,
    );
    const cells = await Promise.all(
      features.map(async (f) => {
        const problem = this.validate(entry.id, f, v, tables, m);
        if (problem)
          return {
            features: f,
            status: "unsupported",
            forms: [],
            reason: problem[0],
            message: problem[1],
          };
        const filename = m.forward[entry.id]?.[f.dialect];
        const chunk = filename ? await this.load<Chunk>(filename) : undefined;
        const code = this.code(f, m);
        const rejected = chunk?.unsupported[code];
        if (rejected)
          return {
            features: f,
            status: "unsupported",
            forms: [],
            reason: rejected[0],
            message: rejected[1],
          };
        const rows = chunk?.requests[code];
        if (!rows)
          return {
            features: f,
            status: "not_generated",
            forms: [],
            reason: "not_generated",
            message:
              "This combination is not included in this database release.",
          };
        return {
          features: f,
          status: "ok",
          forms: rows.map((row) => this.form(chunk!.forms[row], f, m)),
          reason: null,
          message: null,
        };
      }),
    );
    return { entry, source: "database", cells };
  }
  async options(selection: Selection) {
    const [m, v] = await Promise.all([
      this.manifest(),
      this.load<Validation>("validation.json"),
      this.entry(selection.entry_id),
    ]);
    const tables = v.tables.map((table) => atob(table));
    const entry = v.entries[selection.entry_id];
    const dialect =
      selection.dialects?.find((d) => entry.dialects.includes(d)) ??
      entry.dialects[0];
    const options: Record<string, unknown[]> = {};
    for (let i = 1; i < m.feature_fields.length; i++) {
      const field = m.feature_fields[i];
      const values =
        field === "subject"
          ? ["all", ...m.dimensions[i]]
          : field === "object"
            ? [null, "all", ...m.dimensions[1]]
            : m.dimensions[i];
      options[field] = values.map((value) => {
        const candidate = {
          ...selection,
          subject: selection.subject ?? "all",
          [field]: value,
        } as Selection;
        const problems = this.expand(candidate, [dialect], m).map((f) =>
          this.validate(selection.entry_id, f, v, tables, m),
        );
        const problem = problems.includes(null) ? null : problems[0];
        return {
          value,
          enabled: problem === null,
          reason: problem?.[1] ?? null,
          reason_code: problem?.[0] ?? null,
        };
      });
    }
    return { dialects: entry.dialects, options };
  }
  private async indexed<T extends Exact | Alias>(
    bounds: Bounds,
    key: string,
  ): Promise<T | undefined> {
    const index = indexOf(bounds, key);
    if (index >= bounds.length || compare(bounds[index][0], key) > 0)
      return undefined;
    return (await this.load<T[]>(bounds[index][2])).find(
      (row) => row[0] === key,
    );
  }
  async suggestions(query: string, limit = 8) {
    const m = await this.manifest();
    const key = this.normalize(query, m);
    const suggestions: string[] = [];
    if (!key) return { suggestions };
    const bounds = m.indexes.exact;
    for (
      let i = indexOf(bounds, key);
      i < bounds.length && suggestions.length < limit;
      i++
    ) {
      if (compare(bounds[i][0], `${key}\u{10ffff}`) >= 0) break;
      for (const row of await this.load<Exact[]>(bounds[i][2])) {
        if (row[0].startsWith(key)) suggestions.push(row[1]);
        if (suggestions.length === limit) break;
      }
    }
    return { suggestions };
  }
  async reverse(query: string, limit = 50, offset = 0) {
    const m = await this.manifest();
    let exactRows: Exact[] = [];
    let match_type = "none";
    const strict = this.strict(query, m);
    for (const [tier, key] of [
      ["exact", this.normalize(query, m)],
      ["alternate", strict],
      ["broad", strict.replaceAll("k", "ǩ").replace(/ç(?!\u030c)/g, "ç̌")],
    ] as const) {
      if (tier === "exact") {
        const row = await this.indexed<Exact>(m.indexes.exact, key);
        if (row) exactRows = [row];
      } else {
        const aliases = await this.indexed<Alias>(m.indexes[tier], key);
        if (aliases) {
          for (const spelling of aliases[1]) {
            const row = await this.indexed<Exact>(m.indexes.exact, spelling);
            if (!row)
              throw new Error(
                "Incomplete published search index. Reload the page.",
              );
            exactRows.push(row);
          }
        }
      }
      if (exactRows.length) {
        match_type = tier;
        break;
      }
    }
    const entries = await this.load<Entry[]>("entries.json");
    const variants: { entry: Entry; features: Features; form: Form }[] = [];
    // Group references by file so a broad match does not repeatedly reload an
    // evicted file, and only one chunk is decoded at a time.
    const refsByFile = new Map<string, Ref[]>();
    for (const row of exactRows)
      for (const ref of row[2]) {
        const features = this.features(ref[1], m);
        const filename = m.forward[entries[ref[0]].id][features.dialect];
        if (!refsByFile.has(filename)) refsByFile.set(filename, []);
        refsByFile.get(filename)!.push(ref);
      }
    for (const [filename, refs] of refsByFile) {
      const chunk = await this.load<Chunk>(filename);
      for (const [entryIndex, code, formIndex] of refs) {
        const features = this.features(code, m);
        variants.push({
          entry: entries[entryIndex],
          features,
          form: this.form(chunk.forms[formIndex], features, m),
        });
      }
    }
    variants.sort(
      (a, b) =>
        compare(a.entry.id, b.entry.id) ||
        compare(
          canonical(m.feature_fields.map((k) => a.features[k])),
          canonical(m.feature_fields.map((k) => b.features[k])),
        ) ||
        compare(
          canonical(m.form_fields.map((k) => a.form[k])),
          canonical(m.form_fields.map((k) => b.form[k])),
        ),
    );
    const groups = new Map<string, Match>();
    for (const { entry, features, form } of variants) {
      const common = Object.fromEntries(
        Object.entries(features).filter(
          ([key]) =>
            !["dialect", "optional_preverb", "optional_prefix"].includes(key),
        ),
      );
      const key = canonical([
        entry.id,
        form.spelling,
        form.frame,
        form.rule,
        common,
      ]);
      if (!groups.has(key))
        groups.set(key, { entry, features, form, variants: [] });
      groups.get(key)!.variants.push({ features, form });
    }
    const matches = [...groups.values()].map((group) => {
      group.variants.sort(
        (a, b) =>
          Number(a.features.optional_preverb) -
            Number(b.features.optional_preverb) ||
          compare(a.features.optional_prefix, b.features.optional_prefix) ||
          compare(a.features.dialect, b.features.dialect) ||
          compare(canonical(a), canonical(b)),
      );
      return { ...group, ...group.variants[0] };
    });
    return {
      match_type,
      total: matches.length,
      matches: matches.slice(offset, offset + limit),
    };
  }
}

/** Preserve the typed UI contract; these calls never go to an API server. */
export function createStaticFetch(root: string, fetchFile?: typeof fetch) {
  const catalog = new StaticCatalog(root, fetchFile);
  return async (request: Request): Promise<Response> => {
    request.signal.throwIfAborted();
    const url = new URL(request.url);
    const q = url.searchParams.get("q") ?? "";
    const limit = Number(
      url.searchParams.get("limit") ??
        (url.pathname.endsWith("reverse") ? 50 : 30),
    );
    const offset = Number(url.searchParams.get("offset") ?? 0);
    let data: unknown;
    if (url.pathname === "/api/v1/verbs")
      data = await catalog.verbs(q, limit, offset);
    else if (url.pathname.startsWith("/api/v1/verbs/"))
      data = await catalog.entry(decodeURIComponent(url.pathname.slice(14)));
    else if (url.pathname === "/api/v1/conjugations")
      data = await catalog.conjugate(await request.json());
    else if (url.pathname === "/api/v1/conjugation-options")
      data = await catalog.options(await request.json());
    else if (url.pathname === "/api/v1/reverse/suggestions")
      data = await catalog.suggestions(q);
    else if (url.pathname === "/api/v1/reverse")
      data = await catalog.reverse(q, limit, offset);
    else throw new Error("Unsupported static operation.");
    request.signal.throwIfAborted();
    return Response.json(data);
  };
}
