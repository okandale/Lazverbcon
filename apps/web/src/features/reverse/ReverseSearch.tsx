import React, { useEffect, useId, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api, requireData } from "../../api/client";
import type { Match } from "../../api/client";
import { labels } from "../../i18n";
import type { Language } from "../../i18n";
import { CharacterBar } from "../CharacterBar";
import { ReverseMatch } from "./ReverseMatch";

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
  const input = useRef<HTMLInputElement>(null);
  const [reverseText, setReverseText] = useState(initialQuery);
  const [reverseQuery, setReverseQuery] = useState(initialQuery);
  const [reversePage, setReversePage] = useState(0);
  const [prefix, setPrefix] = useState("");
  const suggestionsId = useId();
  const [suggestionsOpen, setSuggestionsOpen] = useState(false);
  const [activeSuggestion, setActiveSuggestion] = useState(-1);
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
  // Hide the previous prefix's results immediately while the next query debounces.
  const words =
    prefix.length > 1 && prefix === reverseText.trim()
      ? (suggestions.data?.suggestions ?? [])
      : [];
  const showSuggestions = suggestionsOpen && words.length > 0;
  const changeText = (value: string) => {
    setReverseText(value);
    setSuggestionsOpen(true);
    setActiveSuggestion(-1);
  };
  const selectSuggestion = (word: string) => {
    setReverseText(word);
    setSuggestionsOpen(false);
    setActiveSuggestion(-1);
  };
  useEffect(() => {
    if (showSuggestions && activeSuggestion >= 0) {
      document
        .getElementById(`${suggestionsId}-${activeSuggestion}`)
        ?.scrollIntoView?.({ block: "nearest" });
    }
  }, [activeSuggestion, showSuggestions, suggestionsId]);
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
          setSuggestionsOpen(false);
          setActiveSuggestion(-1);
        }}
      >
        <div className="reverse-autocomplete">
          <input
            ref={input}
            role="combobox"
            aria-label={t.reverse}
            aria-autocomplete="list"
            aria-expanded={showSuggestions}
            aria-controls={showSuggestions ? suggestionsId : undefined}
            aria-activedescendant={
              showSuggestions && activeSuggestion >= 0
                ? `${suggestionsId}-${activeSuggestion}`
                : undefined
            }
            placeholder={t.reverseHint}
            value={reverseText}
            onChange={(e) => changeText(e.target.value)}
            onFocus={() => setSuggestionsOpen(true)}
            onBlur={() => {
              setSuggestionsOpen(false);
              setActiveSuggestion(-1);
            }}
            onKeyDown={(e) => {
              if (e.nativeEvent.isComposing) return;
              if (e.key === "Escape") {
                setSuggestionsOpen(false);
                setActiveSuggestion(-1);
              } else if (
                (e.key === "ArrowDown" || e.key === "ArrowUp") &&
                words.length
              ) {
                e.preventDefault();
                setSuggestionsOpen(true);
                setActiveSuggestion((previous) => {
                  if (!showSuggestions || previous < 0)
                    return e.key === "ArrowDown" ? 0 : words.length - 1;
                  return (
                    (previous +
                      (e.key === "ArrowDown" ? 1 : -1) +
                      words.length) %
                    words.length
                  );
                });
              } else if (
                e.key === "Enter" &&
                showSuggestions &&
                activeSuggestion >= 0
              ) {
                e.preventDefault();
                selectSuggestion(words[activeSuggestion]);
              }
            }}
            required
            maxLength={200}
            autoComplete="off"
            spellCheck={false}
          />
          {showSuggestions && (
            <ul
              id={suggestionsId}
              className="reverse-suggestions"
              role="listbox"
              aria-label={
                language === "en"
                  ? "Verb form suggestions"
                  : "Fiil biçimi önerileri"
              }
            >
              {words.map((word, index) => (
                <li
                  key={word}
                  id={`${suggestionsId}-${index}`}
                  role="option"
                  aria-selected={activeSuggestion === index}
                  onPointerDown={(e) => e.preventDefault()}
                  onClick={() => selectSuggestion(word)}
                >
                  {word}
                </li>
              ))}
            </ul>
          )}
        </div>
        <button className="primary">{t.find} ↗</button>
        <button
          type="button"
          onClick={() => {
            setReverseText("");
            setReverseQuery("");
            setReversePage(0);
            setSuggestionsOpen(false);
            setActiveSuggestion(-1);
            onSearch("");
            input.current?.focus();
          }}
        >
          {t.reset}
        </button>
      </form>
      <CharacterBar value={reverseText} onChange={changeText} input={input} />
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
              <ReverseMatch
                key={i}
                match={match}
                language={language}
                onSelect={onSelect}
              />
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
