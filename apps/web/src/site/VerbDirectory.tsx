import { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import type { Language } from "../i18n";
import { api, defaults, requireData } from "../api/client";
import { CharacterBar } from "../features/CharacterBar";
import { localLink, PageIntro } from "./shared";

export function VerbDirectory({ language: l }: { language: Language }) {
  const [search, setSearch] = useState(() =>
    (new URLSearchParams(window.location.search).get("q") ?? "").slice(0, 200),
  );
  const [query, setQuery] = useState(search);
  const [page, setPage] = useState(0);
  const input = useRef<HTMLInputElement>(null);
  useEffect(() => {
    const timer = setTimeout(() => {
      setQuery(search);
      setPage(0);
      const url = new URL(window.location.href);
      if (search) url.searchParams.set("q", search);
      else url.searchParams.delete("q");
      window.history.replaceState(null, "", url);
    }, 200);
    return () => clearTimeout(timer);
  }, [search]);
  const verbs = useQuery({
    queryKey: ["directory", query, page],
    queryFn: async ({ signal }) =>
      requireData(
        await api.GET("/api/v1/verbs", {
          params: { query: { q: query, limit: 30, offset: page * 30 } },
          signal,
        }),
      ),
  });
  return (
    <>
      <PageIntro
        title={l === "en" ? "A lexicon to explore." : "Keşfedilecek fiiller."}
        description={
          l === "en"
            ? "Find a verb in Laz, Turkish or English, then explore its forms."
            : "Lazca, Türkçe veya İngilizce bir fiil arayın ve çekimlerini inceleyin."
        }
      />
      <section className="panel directory">
        <label className="field">
          <span>{l === "en" ? "Search verbs" : "Fiil ara"}</span>
          <input
            ref={input}
            value={search}
            maxLength={200}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Lazuri · Türkçe · English"
          />
        </label>
        <CharacterBar value={search} onChange={setSearch} input={input} />
        {verbs.isPending && (
          <p role="status">{l === "en" ? "Loading…" : "Yükleniyor…"}</p>
        )}
        {verbs.error && <p role="alert">{verbs.error.message}</p>}
        {verbs.data && (
          <>
            <p className="page-note" role="status">
              {verbs.data.total} {l === "en" ? "entries" : "kayıt"}
            </p>
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th scope="col">Lazuri</th>
                    <th scope="col">Türkçe</th>
                    <th scope="col">English</th>
                    <th scope="col">{l === "en" ? "Class" : "Sınıf"}</th>
                  </tr>
                </thead>
                <tbody>
                  {verbs.data.entries.map((entry) => (
                    <tr key={entry.id}>
                      <td>
                        <a
                          lang="lzz"
                          href={localLink(
                            "/conjugator?selection=" +
                              encodeURIComponent(
                                JSON.stringify({
                                  ...defaults,
                                  entry_id: entry.id,
                                }),
                              ),
                            l,
                          )}
                        >
                          {entry.infinitive} ↗
                        </a>
                      </td>
                      <td lang="tr">{entry.turkish}</td>
                      <td lang="en">{entry.english}</td>
                      <td>
                        <abbr
                          title={
                            {
                              TVE: "Ergative",
                              TVM: "Nominative",
                              IVD: "Dative",
                            }[entry.verb_class]
                          }
                        >
                          {entry.verb_class}
                        </abbr>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {verbs.data.total === 0 && (
              <p>
                {l === "en" ? "No matching verbs." : "Eşleşen fiil bulunamadı."}
              </p>
            )}
          </>
        )}
        <div className="pagination">
          <button
            disabled={page === 0 || verbs.isFetching}
            onClick={() => setPage((p) => p - 1)}
          >
            ← {l === "en" ? "Previous" : "Önceki"}
          </button>
          <span>{page + 1}</span>
          <button
            disabled={
              !verbs.data ||
              (page + 1) * 30 >= verbs.data.total ||
              verbs.isFetching
            }
            onClick={() => setPage((p) => p + 1)}
          >
            {l === "en" ? "Next" : "Sonraki"} →
          </button>
        </div>
      </section>
    </>
  );
}
