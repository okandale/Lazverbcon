import React, { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api, requireData } from "../../api/client";
import type { Match } from "../../api/client";
import { dialectNames, labels, names } from "../../i18n";
import type { Language } from "../../i18n";
import { CharacterBar } from "../CharacterBar";

export function ReverseSearch({
  language,
  onSelect,
  initialQuery = "",
  onSearch,
}: {
  language: Language;
  onSelect: (match: Match) => void;
  initialQuery?: string;
  onSearch: (query: string) => void;
}) {
  const t = labels[language];
  const n = names[language];
  const input = useRef<HTMLInputElement>(null);
  const [reverseText, setReverseText] = useState(initialQuery);
  const [reverseQuery, setReverseQuery] = useState(initialQuery);
  const [reversePage, setReversePage] = useState(0);
  const [prefix, setPrefix] = useState("");
  useEffect(() => {
    const timer = setTimeout(() => setPrefix(reverseText.trim()), 200);
    return () => clearTimeout(timer);
  }, [reverseText]);
  const suggestions = useQuery({
    queryKey: ["suggestions", prefix],
    enabled: prefix.length > 1,
    queryFn: async ({ signal }) =>
      requireData(
        await api.GET("/api/v1/reverse/suggestions", {
          params: { query: { q: prefix } },
          signal,
        }),
      ),
  });
  const reverse = useQuery({
    queryKey: ["reverse", reverseQuery, reversePage],
    enabled: !!reverseQuery,
    queryFn: async ({ signal }) =>
      requireData(
        await api.GET("/api/v1/reverse", {
          params: {
            query: {
              q: reverseQuery,
              limit: 20,
              offset: reversePage * 20,
            },
          },
          signal,
        }),
      ),
  });
  return (
    <section className="panel reverse-panel">
      <p className="eyebrow">
        LAZURİ → {language === "en" ? "MEANING" : "ANLAM"}
      </p>
      <h2>{t.reverseTitle}</h2>
      <form
        className="reverse-form"
        onSubmit={(e) => {
          e.preventDefault();
          setReverseQuery(reverseText.trim());
          onSearch(reverseText.trim());
          setReversePage(0);
        }}
      >
        <input
          ref={input}
          aria-label={t.reverse}
          placeholder={t.reverseHint}
          value={reverseText}
          onChange={(e) => setReverseText(e.target.value)}
          required
          maxLength={200}
          list="reverse-suggestions"
        />
        <datalist id="reverse-suggestions">
          {suggestions.data?.suggestions.map((word) => (
            <option key={word} value={word} />
          ))}
        </datalist>
        <button className="primary">{t.find} ↗</button>
      </form>
      <CharacterBar
        value={reverseText}
        onChange={setReverseText}
        input={input}
      />
      {reverse.isFetching && <p>{t.loading}</p>}
      {reverse.error && <p role="alert">{reverse.error.message}</p>}
      {reverse.data && (
        <>
          <p className="muted">
            {reverse.data.total} {t.matches}
            {reverse.data.match_type !== "none" &&
              ` · ${t[reverse.data.match_type]}`}
          </p>
          {reverse.data.total === 0 && <p>{t.noMatches}</p>}
          <div className="reverse-list">
            {reverse.data.matches.map((match, i) => (
              <article className="match" key={i}>
                <div>
                  <h3>{match.form.spelling}</h3>
                  <p>
                    {match.entry.infinitive} ·{" "}
                    {language === "en"
                      ? match.entry.english
                      : match.entry.turkish}
                  </p>
                  <small>
                    {dialectNames[match.features.dialect]} ·{" "}
                    {n[match.features.tense]} · {n[match.features.mood]} ·{" "}
                    {n[match.features.subject]}
                    {match.features.object && ` → ${n[match.features.object]}`}
                    {` · ${n[match.entry.verb_class]}`}
                    {match.features.derivation !== "none" &&
                      ` · ${n[match.features.derivation]}`}
                    {match.features.applicative && ` · ${t.applicative}`}
                    {match.features.causative !== "none" &&
                      ` · ${t.causative}: ${n[match.features.causative]}`}
                    {match.features.optional_preverb && ` · ${t.optional}`}
                  </small>
                </div>
                <button onClick={() => onSelect(match)}>{t.open} →</button>
              </article>
            ))}
          </div>
          <div className="pagination">
            <button
              disabled={!reversePage}
              onClick={() => setReversePage(reversePage - 1)}
            >
              ← {t.previous}
            </button>
            <span>{reversePage + 1}</span>
            <button
              disabled={(reversePage + 1) * 20 >= reverse.data.total}
              onClick={() => setReversePage(reversePage + 1)}
            >
              {t.next} →
            </button>
          </div>
        </>
      )}
    </section>
  );
}
