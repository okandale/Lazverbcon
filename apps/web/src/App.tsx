import { Lexicon } from "./features/lexicon/Lexicon";
import { ReverseSearch } from "./features/reverse/ReverseSearch";
import { Results } from "./features/conjugation/Results";
import React, { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  api,
  defaults,
  defaultsForEntry,
  requireData,
  requestFromMatch,
} from "./api/client";
import type { Dialect, Entry, Match, Request } from "./api/client";
import { dialectNames, labels, names } from "./i18n";
import { parseSelection } from "./api/selection";
import { conjugateSelection, selectionOptions } from "./api/conjugation";
import { VerbDirectory } from "./site/VerbDirectory";
import { restrictionText } from "./restrictions";
import { Header, Footer, localLink, useLanguage } from "./site/shared";

const dialects = Object.keys(dialectNames) as Dialect[];
const people = ["1sg", "2sg", "3sg", "1pl", "2pl", "3pl"];

function initialRequest(): Request {
  const params = new URLSearchParams(window.location.search);
  return parseSelection(params.get("selection"));
}

export function App() {
  const [language, setLanguage] = useLanguage();
  const t = labels[language];
  const n = names[language];
  const [reverseQuery, setReverseQuery] = useState(() =>
    (new URLSearchParams(window.location.search).get("reverse") ?? "").slice(
      0,
      200,
    ),
  );
  const [tab, setTab] = useState<"conjugate" | "reverse" | "verbs">(() =>
    window.location.pathname.replace(/\/+$/, "") === "/verbs" ||
    new URLSearchParams(window.location.search).get("view") === "verbs"
      ? "verbs"
      : reverseQuery
        ? "reverse"
        : "conjugate",
  );
  const [draft, setDraft] = useState<Request>(initialRequest);
  const [submitted, setSubmitted] = useState<Request | null>(initialRequest);
  const [notice, setNotice] = useState("");
  useEffect(() => {
    document.documentElement.lang = language;
    document.title = `${language === "en" ? "Verb explorer" : "Fiil çekimi"} · Lazuri`;
  }, [language]);
  const selected = useQuery({
    queryKey: ["entry", draft.entry_id],
    enabled: tab === "conjugate",
    queryFn: async ({ signal }) =>
      requireData(
        await api.GET("/api/v1/verbs/{entry_id}", {
          params: { path: { entry_id: draft.entry_id } },
          signal,
        }),
      ),
  });
  const capabilities = useQuery({
    queryKey: ["options", draft],
    enabled: tab === "conjugate" && !!selected.data,
    queryFn: ({ signal }) => selectionOptions(draft, signal),
  });
  const selectionNotes = [
    ...new Set(
      Object.entries(capabilities.data?.options ?? {}).flatMap(
        ([field, choices]) =>
          choices
            .filter(
              (choice) =>
                choice.value === draft[field as keyof Request] &&
                !choice.enabled,
            )
            .map((choice) =>
              restrictionText(choice.reason_code, choice.reason, language),
            )
            .filter(Boolean),
      ),
    ),
  ];
  const results = useQuery({
    queryKey: ["conjugations", submitted],
    enabled: submitted !== null && tab === "conjugate",
    queryFn: ({ signal }) => conjugateSelection(submitted!, signal),
  });
  function update<K extends keyof Request>(key: K, value: Request[K]) {
    setDraft((previous) => ({ ...previous, [key]: value }));
    setSubmitted(null);
    setNotice("");
  }
  function choose(entry: Entry) {
    setDraft(defaultsForEntry(entry));
    setSubmitted(null);
    setNotice("");
  }
  function switchTab(value: "conjugate" | "reverse" | "verbs") {
    setTab(value);
    const url = new URL(window.location.href);
    url.pathname = "/conjugator";
    url.searchParams.delete("view");
    url.searchParams.delete("reverse");
    if (value === "verbs") url.searchParams.set("view", "verbs");
    if (value === "reverse" && reverseQuery)
      url.searchParams.set("reverse", reverseQuery);
    window.history.replaceState(null, "", url);
  }
  function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!draft.dialects?.length) {
      setNotice(t.selectDialect);
      return;
    }
    setSubmitted({ ...draft });
    const url = new URL(window.location.href);
    url.searchParams.delete("reverse");
    url.searchParams.delete("view");
    url.searchParams.set("selection", JSON.stringify(draft));
    window.history.replaceState(null, "", url);
    setNotice("");
  }
  async function copy(text: string, message: string) {
    try {
      await navigator.clipboard.writeText(text);
      setNotice(message);
    } catch {
      setNotice(
        language === "en"
          ? "Copy is unavailable in this browser."
          : "Bu tarayıcıda kopyalama kullanılamıyor.",
      );
    }
  }
  function share() {
    const url = new URL(window.location.href);
    url.pathname = "/conjugator";
    url.search = "";
    url.searchParams.set("lang", language);
    if (tab === "verbs") url.searchParams.set("view", "verbs");
    else if (tab === "reverse") url.searchParams.set("reverse", reverseQuery);
    else url.searchParams.set("selection", JSON.stringify(draft));
    void copy(url.toString(), t.shared);
  }
  function openMatch(match: Match) {
    const request = requestFromMatch(match);
    setDraft(request);
    setSubmitted(request);
    setTab("conjugate");
    const url = new URL(window.location.href);
    url.searchParams.delete("reverse");
    url.searchParams.delete("view");
    url.searchParams.set("selection", JSON.stringify(request));
    window.history.replaceState(null, "", url);
  }
  function select(
    field: "tense" | "mood" | "derivation" | "subject" | "object" | "causative",
    values: string[],
  ) {
    return (
      <label className="field" key={field}>
        <span>{t[field]}</span>
        <select
          value={draft[field] ?? ""}
          onChange={(e) => update(field, (e.target.value || null) as never)}
        >
          {values.map((value) => (
            <option key={value} value={value}>
              {value === "" ? t.none : value === "all" ? t.all : n[value]}
            </option>
          ))}
        </select>
      </label>
    );
  }

  return (
    <>
      <Header language={language} setLanguage={setLanguage} />
      <main id="main">
        <section className="intro">
          <p className="eyebrow">LAZVERBCON / LAZURİ NENA</p>
          <h1>{t.title}</h1>
          <p>{t.intro}</p>
          <div className="tabs" role="tablist" aria-label={t.source}>
            <button
              role="tab"
              aria-selected={tab === "conjugate"}
              onClick={() => switchTab("conjugate")}
            >
              {t.conjugate}
              <span>↗</span>
            </button>
            <button
              role="tab"
              aria-selected={tab === "reverse"}
              onClick={() => switchTab("reverse")}
            >
              {t.reverse}
              <span>↙</span>
            </button>
            <button
              role="tab"
              aria-selected={tab === "verbs"}
              onClick={() => switchTab("verbs")}
            >
              {language === "en" ? "Verb list" : "Fiil listesi"}
            </button>
          </div>
        </section>
        {tab === "conjugate" ? (
          <div className="workspace">
            <Lexicon
              language={language}
              selectedId={draft.entry_id}
              onSelect={choose}
            />
            <div className="main-column">
              <section className="panel controls">
                {selected.error ? (
                  <p role="alert">{selected.error.message}</p>
                ) : (
                  <>
                    <div className="verb-heading">
                      <div>
                        <p className="eyebrow">
                          {selected.data
                            ? n[selected.data.verb_class]
                            : "LAZURİ"}
                        </p>
                        <h2>{selected.data?.infinitive ?? "…"}</h2>
                        <p>
                          {selected.data &&
                            (language === "en"
                              ? selected.data.english
                              : selected.data.turkish)}
                        </p>
                      </div>
                      <span className="verb-number">Aa</span>
                    </div>
                    <form onSubmit={submit}>
                      <div className="field-grid grammar-grid">
                        {select("tense", [
                          "present",
                          "past",
                          "future",
                          "past_progressive",
                          "present_perfect",
                        ])}
                        {select("mood", [
                          "indicative",
                          "optative",
                          "imperative",
                          "negative_imperative",
                        ])}
                        {select("derivation", ["none", "potential", "passive"])}
                      </div>
                      <div className="field-grid person-grid">
                        {select("subject", ["all", ...people])}
                        {select("object", ["", "all", ...people])}
                      </div>
                      <fieldset className="dialects">
                        <legend>{t.dialects}</legend>
                        {dialects.map((d) => (
                          <label
                            key={d}
                            title={
                              capabilities.data &&
                              !capabilities.data.dialects.includes(d)
                                ? language === "en"
                                  ? "No recorded forms for this dialect"
                                  : "Bu lehçe için kayıtlı çekim yok"
                                : undefined
                            }
                            className={
                              draft.dialects?.includes(d) ? "checked" : ""
                            }
                          >
                            <input
                              type="checkbox"
                              disabled={
                                !!capabilities.data &&
                                !capabilities.data.dialects.includes(d) &&
                                !draft.dialects?.includes(d)
                              }
                              aria-label={`${d === "AS" ? "AŞ" : d} ${dialectNames[d]}`}
                              checked={draft.dialects?.includes(d) ?? false}
                              onChange={(e) =>
                                update(
                                  "dialects",
                                  e.target.checked
                                    ? [...(draft.dialects ?? []), d]
                                    : draft.dialects?.filter((x) => x !== d),
                                )
                              }
                            />
                            <span>{d === "AS" ? "AŞ" : d}</span>
                            <small>{dialectNames[d]}</small>
                          </label>
                        ))}
                      </fieldset>
                      <details className="advanced">
                        <summary>
                          {t.more} <span>+</span>
                        </summary>
                        <fieldset className="option-group">
                          <legend>{t.markers}</legend>
                          <div className="field-grid">
                            {select("causative", ["none", "simple", "double"])}
                            <label className="check">
                              <input
                                type="checkbox"
                                checked={draft.applicative ?? false}
                                onChange={(e) =>
                                  update("applicative", e.target.checked)
                                }
                              />
                              {t.applicative}
                            </label>
                          </div>
                        </fieldset>
                        <fieldset className="option-group">
                          <legend>{t.prefixes}</legend>
                          <label className="field">
                            <span>{t.optional}</span>
                            <select
                              value={
                                draft.optional_preverb
                                  ? "legacy"
                                  : (draft.optional_prefix ?? "none")
                              }
                              onChange={(e) => {
                                setDraft((previous) => ({
                                  ...previous,
                                  optional_preverb: e.target.value === "legacy",
                                  optional_prefix:
                                    e.target.value === "legacy"
                                      ? "none"
                                      : (e.target.value as
                                          "none" | "ko" | "do"),
                                }));
                                setSubmitted(null);
                                setNotice("");
                              }}
                            >
                              <option value="none">{t.none}</option>
                              <option value="ko">ko</option>
                              <option value="do">do</option>
                              {draft.optional_preverb && (
                                <option value="legacy">
                                  {language === "en"
                                    ? "Previous setting"
                                    : "Önceki seçenek"}
                                </option>
                              )}
                            </select>
                          </label>
                        </fieldset>
                      </details>
                      {selectionNotes.length > 0 && (
                        <ul className="selection-notes">
                          {selectionNotes.map((note) => (
                            <li key={note}>{note}</li>
                          ))}
                        </ul>
                      )}
                      <div className="actions">
                        <button
                          type="submit"
                          className="primary"
                          disabled={results.isFetching || !selected.data}
                        >
                          {results.isFetching ? t.loading : t.generate}
                          <span>→</span>
                        </button>
                        <button
                          type="button"
                          className="text-button"
                          onClick={() => selected.data && choose(selected.data)}
                        >
                          {t.reset}
                        </button>
                      </div>
                    </form>
                  </>
                )}
              </section>
              <section className="panel results" aria-live="polite">
                <div className="section-title">
                  <h2>{t.forms}</h2>
                  {submitted && results.data && (
                    <button
                      className="text-button"
                      onClick={() =>
                        copy(
                          results
                            .data!.cells.flatMap((c) =>
                              (c.forms ?? []).map(
                                (f) =>
                                  `${c.features.dialect} · ${n[f.subject]}${submitted.object != null && f.object ? ` → ${n[f.object]}` : ""}: ${f.spelling}`,
                              ),
                            )
                            .join("\n"),
                          t.copied,
                        )
                      }
                    >
                      {t.copy} ↗
                    </button>
                  )}
                </div>
                {!submitted ? (
                  <div className="empty">
                    <span aria-hidden="true">✳</span>
                    <p>{t.empty}</p>
                  </div>
                ) : results.isPending ? (
                  <p>{t.loading}</p>
                ) : results.error ? (
                  <p role="alert">{results.error.message}</p>
                ) : (
                  results.data && (
                    <Results
                      data={results.data}
                      language={language}
                      object={submitted?.object}
                    />
                  )
                )}
              </section>
            </div>
          </div>
        ) : tab === "verbs" ? (
          <VerbDirectory language={language} embedded />
        ) : (
          <ReverseSearch
            language={language}
            onSelect={openMatch}
            initialQuery={reverseQuery}
            onSearch={(query) => {
              setReverseQuery(query);
              const url = new URL(window.location.href);
              url.searchParams.set("reverse", query);
              window.history.replaceState(null, "", url);
            }}
          />
        )}
        {notice && (
          <p className="notice" role="status">
            {notice}
          </p>
        )}
        <p className="page-note">
          <a
            href={localLink(
              "/feedback?context=" +
                encodeURIComponent(
                  tab === "reverse"
                    ? `/conjugator?reverse=${encodeURIComponent(reverseQuery)}`
                    : tab === "verbs"
                      ? "/conjugator?view=verbs"
                      : `/conjugator?verb=${encodeURIComponent(selected.data?.infinitive ?? "")}&selection=${encodeURIComponent(JSON.stringify(submitted ?? draft))}`,
                ),
              language,
            )}
          >
            {language === "en"
              ? "Report a form or suggest a correction →"
              : "Bir çekim bildirin veya düzeltme önerin →"}
          </a>
        </p>
      </main>
      <Footer language={language}>
        <button className="text-button" onClick={share}>
          {t.share} ↗
        </button>
      </Footer>
    </>
  );
}
