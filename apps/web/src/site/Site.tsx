import { useEffect } from "react";
import { App } from "../App";
import { About, Events, Home, NotFound, Resources } from "./Pages";
import { Header, Footer, useLanguage } from "./shared";
import { Keyboard } from "./Keyboard";
import { guides } from "./keyboards";
import { phraseDialects } from "./content";
import { PhraseGuide } from "./PhraseGuide";
import { VerbDirectory } from "./VerbDirectory";
import { Feedback } from "./Feedback";

export function Site() {
  const path = window.location.pathname.replace(/\/+$/, "") || "/";
  const query = new URLSearchParams(window.location.search);
  // Preserve links shared before the learning-center home was restored.
  if (
    path === "/conjugator" ||
    (path === "/" && (query.has("selection") || query.has("reverse")))
  )
    return <App />;
  return <Content path={path} />;
}
function Content({ path }: { path: string }) {
  const [language, setLanguage] = useLanguage();
  let page;
  let title = language === "en" ? "Page not found" : "Sayfa bulunamadı";
  if (path === "/") {
    page = <Home language={language} />;
    title = language === "en" ? "Learn Laz" : "Lazca öğrenin";
  } else if (path === "/verbs" || path === "/v2/verbs") {
    page = <VerbDirectory language={language} />;
    title = language === "en" ? "Verbs" : "Fiiller";
  } else if (/^\/v2\/verb\/[^/]+\/[^/]+$/.test(path)) {
    page = <NotFound language={language} legacy />;
    title = language === "en" ? "Find a verb" : "Fiil ara";
  } else if (path === "/resources") {
    page = <Resources language={language} />;
    title = language === "en" ? "Resources" : "Kaynaklar";
  } else if (path === "/about") {
    page = <About language={language} />;
    title = language === "en" ? "About" : "Hakkımızda";
  } else if (path === "/events") {
    page = <Events language={language} />;
    title = language === "en" ? "Workshops" : "Atölyeler";
  } else if (path === "/feedback") {
    page = <Feedback language={language} />;
    title = language === "en" ? "Feedback" : "Geri bildirim";
  } else if (
    path === "/keyboard" ||
    (path.startsWith("/keyboard/") && Object.hasOwn(guides, path.slice(10)))
  ) {
    const slug = path.slice(10);
    page = <Keyboard language={language} platform={slug} />;
    title =
      guides[slug]?.title[language] ??
      (language === "en" ? "Keyboard" : "Klavye");
  } else if (
    path === "/resources/phrase-guide" ||
    phraseDialects.some((d) => path === `/resources/phrase-guide/${d.slug}`)
  ) {
    const slug = path.split("/")[3];
    page = <PhraseGuide language={language} dialect={slug} />;
    title = `${phraseDialects.find((d) => d.slug === slug)?.name ?? ""} ${language === "en" ? "Phrase guide" : "İfade rehberi"}`;
  } else page = <NotFound language={language} />;
  useEffect(() => {
    document.title = `${title.trim()} · Lazuri`;
  }, [title]);
  return (
    <>
      <Header language={language} setLanguage={setLanguage} />
      <main id="main" className="content-page">
        {page}
      </main>
      <Footer language={language} />
    </>
  );
}
