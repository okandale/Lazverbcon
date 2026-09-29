import { Lexicon } from "./features/lexicon/Lexicon";
import { ReverseSearch } from "./features/reverse/ReverseSearch";
import { Results } from "./features/conjugation/Results";
import React, { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api, defaults, requireData, requestFromMatch } from "./api/client";
import type { Dialect, Match, Request } from "./api/client";
import { dialectNames, labels, names } from "./i18n";
import { parseSelection } from "./api/selection";
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
  const [tab, setTab] = useState<"conjugate" | "reverse">(() =>
    reverseQuery ? "reverse" : "conjugate",
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
    enabled: !!selected.data,
    queryFn: async ({ signal }) =>
      requireData(
        await api.POST("/api/v1/conjugation-options", { body: draft, signal }),
      ),
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
    enabled: submitted !== null,
    queryFn: async ({ signal }) =>
      requireData(
        await api.POST("/api/v1/conjugations", { body: submitted!, signal }),
      ),
  });
  function update<K extends keyof Request>(key: K, value: Request[K]) {
    setDraft((previous) => ({ ...previous, [key]: value }));
    setSubmitted(null);
    setNotice("");
  }
  function choose(id: string) {
    setDraft({ ...defaults, entry_id: id });
    setSubmitted(null);
    setNotice("");
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
    if (tab === "reverse") url.searchParams.set("reverse", reverseQuery);
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
          <p className="explorer-links">
            <a href={localLink("/verbs", language)}>
              {language === "en"
                ? "Browse all verbs →"
                : "Tüm fiilleri incele →"}
            </a>
          </p>
          <div className="tabs" role="tablist" aria-label={t.source}>
            <button
              role="tab"
              aria-selected={tab === "conjugate"}
              onClick={() => setTab("conjugate")}
            >
              {t.conjugate}
              <span>↗</span>
            </button>
            <button
              role="tab"
              aria-selected={tab === "reverse"}
              onClick={() => setTab("reverse")}
            >
              {t.reverse}
              <span>↙</span>
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
                      <div className="field-grid">
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
                        {select("subject", ["all", ...people])}
                        {select("object", ["", "all", ...people])}
                      </div>
                      <fieldset className="dialects">
                        <legend>{t.dialects}</legend>
                        {dialects.map((d) => (
                          <label
                            key={d}
                            className={
                              draft.dialects?.includes(d) ? "checked" : ""
                            }
                          >
                            <input
                              type="checkbox"
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
                        <div className="field-grid">
                          {select("derivation", [
                            "none",
                            "potential",
                            "passive",
                          ])}
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
                          <label className="check">
                            <input
                              type="checkbox"
                              checked={draft.optional_preverb ?? false}
                              onChange={(e) =>
                                update("optional_preverb", e.target.checked)
                              }
                            />
                            {t.optional}
                          </label>
                        </div>
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
                          onClick={() => choose(draft.entry_id)}
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
                                  `${c.features.dialect} · ${f.subject_pronoun}${f.object ? ` → ${f.object_pronoun}` : ""}: ${f.spelling}`,
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
                    <Results data={results.data} language={language} />
                  )
                )}
              </section>
            </div>
          </div>
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
                    : `/conjugator?selection=${encodeURIComponent(JSON.stringify(submitted ?? draft))}`,
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
