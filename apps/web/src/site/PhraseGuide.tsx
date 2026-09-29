import { useEffect, useState } from "react";
import type { Language } from "../i18n";
import { Card, localLink, PageIntro } from "./shared";
import { phraseDialects } from "./content";
import { categories, phrases, vocabulary } from "./phrases";
import type { Category } from "./phrases";

function categoryFromURL(): Category {
  const value = new URLSearchParams(window.location.search).get("category");
  return value && Object.hasOwn(categories, value)
    ? (value as Category)
    : "market";
}
export function PhraseGuide({
  language: l,
  dialect,
}: {
  language: Language;
  dialect?: string;
}) {
  const [category, setCategory] = useState<Category>(categoryFromURL);
  const [notice, setNotice] = useState("");
  const region = phraseDialects.find((d) => d.slug === dialect);
  useEffect(() => {
    const update = () => setCategory(categoryFromURL());
    window.addEventListener("popstate", update);
    return () => window.removeEventListener("popstate", update);
  }, []);
  function select(next: Category) {
    setCategory(next);
    setNotice("");
    const url = new URL(window.location.href);
    url.searchParams.set("category", next);
    window.history.pushState(null, "", url);
  }
  async function copy(value: string) {
    try {
      await navigator.clipboard.writeText(value);
      setNotice(l === "en" ? "Phrase copied." : "İfade kopyalandı.");
    } catch {
      setNotice(
        l === "en"
          ? "Select the phrase to copy it manually."
          : "Kopyalamak için ifadeyi seçin.",
      );
    }
  }
  return (
    <>
      <PageIntro
        title={
          region
            ? `${region.name} · ${l === "en" ? "Phrase guide" : "İfade rehberi"}`
            : l === "en"
              ? "Start a conversation."
              : "Sohbete başlayın."
        }
        description={
          l === "en"
            ? "Everyday words for the places you go."
            : "Gittiğiniz yerlerde kullanabileceğiniz günlük ifadeler."
        }
      />
      {!region ? (
        <div className="card-grid">
          {phraseDialects.map((d) => (
            <Card
              key={d.slug}
              index={d.code}
              href={localLink(`/resources/phrase-guide/${d.slug}`, l)}
              title={d.name}
              description={
                d.slug === "hopa"
                  ? l === "en"
                    ? "Market, pharmacy, restaurant and hotel phrases."
                    : "Market, eczane, restoran ve otel ifadeleri."
                  : l === "en"
                    ? "Translations are not available yet."
                    : "Çeviriler henüz mevcut değil."
              }
            />
          ))}
        </div>
      ) : (
        <>
          <a
            className="back-link"
            href={localLink("/resources/phrase-guide", l)}
          >
            ← {l === "en" ? "All dialects" : "Tüm lehçeler"}
          </a>
          {dialect !== "hopa" ? (
            <section className="panel prose">
              <h2>
                {l === "en"
                  ? "These phrases are still to come."
                  : "Bu ifadeler henüz hazır değil."}
              </h2>
              <p>
                {l === "en"
                  ? `We don’t yet have reviewed ${region.name} translations for this guide. You can explore the Hopa guide or contact us to contribute phrases.`
                  : `Bu rehber için gözden geçirilmiş ${region.name} çevirileri henüz yok. Hopa rehberini inceleyebilir veya ifade eklemek için bizimle iletişime geçebilirsiniz.`}
              </p>
              <a href={localLink("/resources/phrase-guide/hopa", l)}>
                {l === "en"
                  ? "Explore Hopa phrases →"
                  : "Hopa ifadelerini inceleyin →"}
              </a>
              <p>
                <a href="mailto:info@lazuri.org">info@lazuri.org</a>
              </p>
            </section>
          ) : (
            <>
              <div
                className="category-nav"
                role="group"
                aria-label={
                  l === "en" ? "Phrase categories" : "İfade kategorileri"
                }
              >
                {(Object.keys(categories) as Category[]).map((c) => (
                  <button
                    key={c}
                    aria-pressed={category === c}
                    onClick={() => select(c)}
                  >
                    {categories[c][l]}
                  </button>
                ))}
              </div>
              <h2 className="content-heading">{categories[category][l]}</h2>
              <div className="phrase-list">
                {phrases[category].map((p, i) => (
                  <article className="panel phrase" key={`${category}-${i}`}>
                    <div className="phrase-meaning">
                      <span className="card-index">
                        {String(i + 1).padStart(2, "0")}
                      </span>
                      <h3>{p[l]}</h3>
                      <p lang={l === "en" ? "tr" : "en"}>
                        {l === "en" ? p.tr : p.en}
                      </p>
                    </div>
                    <div className="phrase-laz">
                      <p lang="lzz">{p.laz}</p>
                      <button
                        aria-label={`${l === "en" ? "Copy" : "Kopyala"}: ${p.laz}`}
                        onClick={() => void copy(p.laz)}
                      >
                        {l === "en" ? "Copy ↗" : "Kopyala ↗"}
                      </button>
                    </div>
                    {p.vocabulary && (
                      <details className="vocabulary">
                        <summary>
                          {l === "en"
                            ? "Words to use in this phrase"
                            : "Bu ifadede kullanabileceğiniz kelimeler"}
                        </summary>
                        <table>
                          <thead>
                            <tr>
                              <th scope="col">
                                {l === "en" ? "English" : "Türkçe"}
                              </th>
                              <th scope="col">Lazuri</th>
                            </tr>
                          </thead>
                          <tbody>
                            {vocabulary.map((v) => (
                              <tr key={v.en}>
                                <td>{v[l]}</td>
                                <td lang="lzz">{v.laz}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </details>
                    )}
                  </article>
                ))}
              </div>
              <p role="status" className="page-note">
                {notice}
              </p>
              <p className="page-note">
                {l === "en"
                  ? "Have a correction or a local variation?"
                  : "Düzeltme veya yerel bir kullanım paylaşmak ister misiniz?"}{" "}
                <a
                  href={localLink(
                    "/feedback?context=" +
                      encodeURIComponent(
                        window.location.pathname + window.location.search,
                      ),
                    l,
                  )}
                >
                  {l === "en" ? "Let us know →" : "Bize yazın →"}
                </a>
              </p>
            </>
          )}
        </>
      )}
    </>
  );
}
