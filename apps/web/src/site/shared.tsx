import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import type { Language } from "../i18n";

export type Text = { en: string; tr: string };
export const text = (en: string, tr: string): Text => ({ en, tr });
export function readLanguage(): Language {
  const query = new URLSearchParams(window.location.search).get("lang");
  if (query === "en" || query === "tr") return query;
  try {
    return localStorage.getItem("lazuri-language") === "tr" ? "tr" : "en";
  } catch {
    return "en";
  }
}
export function useLanguage() {
  const [language, setLanguage] = useState<Language>(readLanguage);
  useEffect(() => {
    document.documentElement.lang = language;
    try {
      localStorage.setItem("lazuri-language", language);
    } catch {
      /* Private browsing may disable storage. */
    }
    const url = new URL(window.location.href);
    url.searchParams.set("lang", language);
    window.history.replaceState(null, "", url);
  }, [language]);
  return [language, setLanguage] as const;
}
export function localLink(path: string, language: Language) {
  const url = new URL(path, window.location.origin);
  url.searchParams.set("lang", language);
  return url.pathname + url.search + url.hash;
}
export const navigation = [
  ["/conjugator", text("Conjugator", "Fiil çekimi")],
  ["/verbs", text("Verbs", "Fiiller")],
  ["/resources/phrase-guide", text("Phrases", "İfadeler")],
  ["/keyboard", text("Keyboard", "Klavye")],
  ["/resources", text("Resources", "Kaynaklar")],
] as const;

export function Header({
  language,
  setLanguage,
}: {
  language: Language;
  setLanguage: (language: Language) => void;
}) {
  const path = window.location.pathname.replace(/\/$/, "") || "/";
  return (
    <>
      <a className="skip-link" href="#main">
        {language === "en" ? "Skip to content" : "İçeriğe geç"}
      </a>
      <header className="topbar site-header">
        <a
          className="wordmark"
          href={localLink("/", language)}
          aria-label="Lazuri home"
        >
          lazuri<span>✳</span>
        </a>
        <nav aria-label={language === "en" ? "Main navigation" : "Ana menü"}>
          {navigation.map(([url, label]) => (
            <a
              key={url}
              href={localLink(url, language)}
              aria-current={path === url ? "page" : undefined}
            >
              {label[language]}
            </a>
          ))}
        </nav>
        <div className="language" aria-label="Language">
          {(["en", "tr"] as const).map((lang) => (
            <button
              key={lang}
              aria-pressed={language === lang}
              onClick={() => setLanguage(lang)}
            >
              {lang.toUpperCase()}
            </button>
          ))}
        </div>
      </header>
    </>
  );
}
export function Footer({
  language,
  children,
}: {
  language: Language;
  children?: ReactNode;
}) {
  return (
    <footer className="site-footer">
      <a className="wordmark" href={localLink("/", language)}>
        lazuri<span>✳</span>
      </a>
      <nav aria-label={language === "en" ? "More links" : "Diğer bağlantılar"}>
        {[
          ["/about", text("About", "Hakkımızda")],
          ["/events", text("Workshops", "Atölyeler")],
          ["/feedback", text("Feedback", "Geri bildirim")],
        ].map(([url, label]) => (
          <a key={url as string} href={localLink(url as string, language)}>
            {(label as Text)[language]}
          </a>
        ))}
        <a href="mailto:info@lazuri.org">
          {language === "en" ? "Contact" : "İletişim"}
        </a>
        <a href="https://buymeacoffee.com/lazuri.org">
          {language === "en" ? "Support us ↗" : "Destek olun ↗"}
        </a>
      </nav>
      {children}
    </footer>
  );
}
export function PageIntro({
  title,
  description,
  eyebrow = "LAZURİ NENA",
}: {
  title: string;
  description?: string;
  eyebrow?: string;
}) {
  return (
    <section className="intro page-intro">
      <p className="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      {description && <p>{description}</p>}
    </section>
  );
}
export function Card({
  href,
  title,
  description,
  index,
}: {
  href: string;
  title: string;
  description: string;
  index?: string;
}) {
  return (
    <a className="resource-card panel" href={href}>
      <span className="card-index">{index ?? "↗"}</span>
      <h2>{title}</h2>
      <p>{description}</p>
      <span className="card-arrow" aria-hidden="true">
        ↗
      </span>
    </a>
  );
}
