import type { Language } from "../i18n";
import { Card, localLink, PageIntro } from "./shared";
import { guides } from "./keyboards";

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
          <ol className="guide-steps">
            {guide.steps.map((step) => (
              <li key={step.title.en}>
                <h2>{step.title[l]}</h2>
                <p>{step.body[l]}</p>
                {step.image && (
                  <figure>
                    <img
                      loading="lazy"
                      src={`/images/keyboard/${step.image}`}
                      alt={step.title[l]}
                    />
                    <figcaption>
                      {l === "en"
                        ? "From the original Lazuri guide; menus may look different in newer versions."
                        : "İlk Lazuri rehberinden; yeni sürümlerde menüler farklı görünebilir."}
                    </figcaption>
                  </figure>
                )}
              </li>
            ))}
          </ol>
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
