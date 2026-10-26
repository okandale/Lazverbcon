import type { Language } from "../i18n";
import { Card, localLink, PageIntro } from "./shared";
import { guides } from "./keyboards";
import type { Guide } from "./keyboards";

function Steps({
  steps,
  language,
}: {
  steps: Guide["steps"];
  language: Language;
}) {
  return (
    <ol className="guide-steps">
      {steps.map((step) => (
        <li key={step.title.en}>
          <h2>{step.title[language]}</h2>
          <p>{step.body[language]}</p>
          {step.image && (
            <figure>
              <img
                loading="lazy"
                src={`/images/keyboard/${step.image}`}
                alt={step.title[language]}
              />
            </figure>
          )}
        </li>
      ))}
    </ol>
  );
}

export function Keyboard({
  language: l,
  platform,
}: {
  language: Language;
  platform?: string;
}) {
  const guide = platform ? guides[platform] : undefined;
  if (!guide)
    return (
      <>
        <PageIntro
          title={
            l === "en" ? "Make room for every letter." : "Her harfe yer açın."
          }
          description={
            l === "en"
              ? "Install a Laz keyboard, then learn your way around it."
              : "Lazca klavye kurun ve kullanmayı öğrenin."
          }
        />
        <h2 className="content-heading">
          {l === "en" ? "Set up your keyboard" : "Klavyenizi kurun"}
        </h2>
        <div className="card-grid">
          {["windows", "mac", "android", "iphone"].map((slug, i) => (
            <Card
              key={slug}
              index={`0${i + 1}`}
              href={localLink(`/keyboard/${slug}`, l)}
              title={guides[slug].title[l]}
              description={guides[slug].intro[l]}
            />
          ))}
        </div>
        <h2 className="content-heading">
          {l === "en" ? "Learn the layout" : "Klavye düzenini öğrenin"}
        </h2>
        <div className="card-grid">
          {["computer", "phone"].map((slug) => (
            <Card
              key={slug}
              href={localLink(`/keyboard/${slug}`, l)}
              title={guides[slug].title[l]}
              description={guides[slug].intro[l]}
            />
          ))}
        </div>
      </>
    );
  return (
    <>
      <PageIntro title={guide.title[l]} description={guide.intro[l]} />
      <a className="back-link" href={localLink("/keyboard", l)}>
        ← {l === "en" ? "All keyboard guides" : "Tüm klavye rehberleri"}
      </a>
      <div className="guide-layout">
        <article className="panel prose">
          <p className="page-note">
            {l === "en"
              ? "Screenshots are from the original Lazuri guides. Menu names may differ in newer versions."
              : "Görseller ilk Lazuri rehberlerindendir. Yeni sürümlerde menü adları değişebilir."}
          </p>
          <Steps steps={guide.steps} language={l} />
          {guide.optional?.map((section) => (
            <details key={section.title.en}>
              <summary>{section.title[l]}</summary>
              <Steps steps={section.steps} language={l} />
            </details>
          ))}
        </article>
        <aside className="panel guide-links">
          <h2>{l === "en" ? "Downloads & help" : "İndirme ve yardım"}</h2>
          {guide.links.map((link) => (
            <a key={link.href} href={link.href}>
              {link.label[l]} ↗
            </a>
          ))}
          <a href={localLink(`/keyboard/${guide.next}`, l)}>
            {guides[guide.next].title[l]} →
          </a>
          <p>
            {l === "en"
              ? "These links open the keyboard provider’s site."
              : "Bu bağlantılar klavye sağlayıcısının sitesini açar."}
          </p>
        </aside>
      </div>
    </>
  );
}
