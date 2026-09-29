import React, { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api, requireData } from "../../api/client";
import { labels } from "../../i18n";
import type { Language } from "../../i18n";
import { CharacterBar } from "../CharacterBar";

export function Lexicon({
  language,
  selectedId,
  onSelect,
}: {
  language: Language;
  selectedId: string;
  onSelect: (id: string) => void;
}) {
  const t = labels[language];
  const [search, setSearch] = useState("");
  const [debounced, setDebounced] = useState("");
  const [page, setPage] = useState(0);
  const input = useRef<HTMLInputElement>(null);
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebounced(search);
      setPage(0);
    }, 200);
    return () => clearTimeout(timer);
  }, [search]);
  const verbs = useQuery({
    queryKey: ["verbs", debounced, page],
    queryFn: async ({ signal }) =>
      requireData(
        await api.GET("/api/v1/verbs", {
          params: { query: { q: debounced, limit: 18, offset: page * 18 } },
          signal,
        }),
      ),
  });
  return (
    <aside className="lexicon panel">
      <div className="section-title">
        <h2>{t.search}</h2>
        <span>{verbs.data?.total ?? "—"}</span>
      </div>
      <div className="searchbox">
        <span aria-hidden="true">⌕</span>
        <input
          ref={input}
          aria-label={t.search}
          placeholder={t.searchHint}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>
      <CharacterBar value={search} onChange={setSearch} input={input} />
      <div className="entry-list" aria-label={t.entries}>
        {verbs.isPending && <p className="muted">{t.loading}</p>}
        {verbs.error && <p role="alert">{verbs.error.message}</p>}
        {verbs.data?.entries.map((entry) => (
          <button
            key={entry.id}
            className={`entry ${selectedId === entry.id ? "selected" : ""}`}
            onClick={() => onSelect(entry.id)}
          >
            <span>
              <strong>{entry.infinitive}</strong>
              <small>{language === "en" ? entry.english : entry.turkish}</small>
            </span>
            <span className="class-code">{entry.verb_class}</span>
          </button>
        ))}
        {verbs.data?.total === 0 && <p>{t.noMatches}</p>}
      </div>
      <div className="pagination">
        <button disabled={page === 0} onClick={() => setPage(page - 1)}>
          ← {t.previous}
        </button>
        <span>{page + 1}</span>
        <button
          disabled={!verbs.data || (page + 1) * 18 >= verbs.data.total}
          onClick={() => setPage(page + 1)}
        >
          {t.next} →
        </button>
      </div>
      <p className="aside-note">{t.same}</p>
    </aside>
  );
}
