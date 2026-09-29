import type { Language } from "../i18n";
import { Card, localLink, PageIntro, text } from "./shared";
import { resources } from "./content";

export function Home({ language: l }: { language: Language }) {
  const cards = [
    [
      "/conjugator",
      text("Conjugator", "Fiil çekimi"),
      text(
        "Conjugate Laz verbs and compare forms across dialects.",
        "Lazca fiilleri çekimleyin ve lehçelere göre karşılaştırın.",
      ),
    ],
    [
      "/resources/phrase-guide",
      text("Phrase guide", "İfade rehberi"),
      text(
        "Everyday phrases with Laz, Turkish and English translations.",
        "Lazca, Türkçe ve İngilizce karşılıklarıyla günlük ifadeler.",
      ),
    ],
    [
      "/keyboard",
      text("Keyboard", "Klavye"),
      text(
        "Set up a Laz keyboard on your phone or computer.",
        "Telefonunuza veya bilgisayarınıza Lazca klavye kurun.",
      ),
    ],
    [
      "/resources",
      text("Resources", "Kaynaklar"),
      text(
        "Laz dictionaries, learning materials and community projects.",
        "Lazca sözlükler, öğrenme kaynakları ve topluluk projeleri.",
      ),
    ],
    [
      "/events",
      text("Workshops", "Atölyeler"),
      text(
        "Information about classes and upcoming events.",
        "Dersler ve yaklaşan etkinlikler hakkında bilgi.",
      ),
    ],
    [
      "/verbs",
      text("Verb list", "Fiil listesi"),
      text(
        "Search verbs by their Laz, Turkish or English meaning.",
        "Fiilleri Lazca, Türkçe veya İngilizce karşılıklarıyla arayın.",
      ),
    ],
  ] as const;
  return (
    <>
      <PageIntro
        title={l === "en" ? "Learn Laz." : "Lazca öğrenin."}
        description={
          l === "en"
            ? "Tools and resources for learning and using Laz."
            : "Lazca öğrenmek ve kullanmak için araçlar ve kaynaklar."
        }
      />
      <div className="card-grid home-cards">
        {cards.map(([href, title, description], i) => (
          <Card
            key={href}
            href={localLink(href, l)}
            title={title[l]}
            description={description[l]}
            index={`0${i + 1}`}
          />
        ))}
      </div>
      <section className="support-strip">
        <h2>{l === "en" ? "Support Lazuri" : "Lazuri’ye destek olun"}</h2>
        <p>
          {l === "en"
            ? "Your support helps us create more resources for people learning Laz."
            : "Desteğiniz, Lazca öğrenenler için yeni kaynaklar hazırlamamıza yardımcı olur."}
        </p>
        <a className="primary" href="https://buymeacoffee.com/lazuri.org">
          {l === "en" ? "Support the project ↗" : "Projeyi destekleyin ↗"}
        </a>
      </section>
    </>
  );
}
export function Resources({ language: l }: { language: Language }) {
  return (
    <>
      <PageIntro
        title={l === "en" ? "Keep exploring." : "Keşfetmeye devam edin."}
        description={
          l === "en"
            ? "Useful places to read, listen and learn."
            : "Okumak, dinlemek ve öğrenmek için kaynaklar."
        }
      />
      <div className="card-grid">
        <Card
          href={localLink("/resources/phrase-guide", l)}
          title={l === "en" ? "Phrase guide" : "İfade rehberi"}
          description={
            l === "en"
              ? "Everyday phrases by dialect, including the guides linked from local QR codes."
              : "Bölgedeki QR kodlarından da ulaşabileceğiniz, lehçelere göre günlük ifadeler."
          }
        />
        {resources.map((r) => (
          <Card
            key={r.href}
            href={r.href}
            title={r.title[l]}
            description={r.description[l]}
          />
        ))}
      </div>
      <p className="page-note">
        {l === "en"
          ? "Have a resource to suggest?"
          : "Kaynak önermek ister misiniz?"}{" "}
        <a href="mailto:info@lazuri.org">info@lazuri.org</a>
      </p>
    </>
  );
}
export function Events({ language: l }: { language: Language }) {
  return (
    <>
      <PageIntro
        title={l === "en" ? "Learn together." : "Birlikte öğrenin."}
        description={
          l === "en" ? "Classes & workshops" : "Dersler ve atölyeler"
        }
      />
      <section className="panel prose empty-event">
        <span className="eyebrow">
          {l === "en" ? "WHAT’S NEXT" : "YAKINDA"}
        </span>
        <h2>
          {l === "en"
            ? "No events are scheduled right now."
            : "Şu anda planlanmış bir etkinlik yok."}
        </h2>
        <p>
          {l === "en"
            ? "Interested in hosting a workshop or joining a future group? Get in touch."
            : "Atölye düzenlemek veya gelecekteki bir gruba katılmak mı istiyorsunuz? Bizimle iletişime geçin."}
        </p>
        <a href="mailto:info@lazuri.org">info@lazuri.org ↗</a>
      </section>
    </>
  );
}
export function About({ language: l }: { language: Language }) {
  return (
    <>
      <PageIntro
        title={l === "en" ? "One verb. Many voices." : "Bir fiil. Birçok ses."}
        description={l === "en" ? "About Lazuri" : "Lazuri hakkında"}
      />
      <article className="panel prose">
        <h2>
          {l === "en" ? "A place to learn Laz" : "Lazca öğrenmek için bir yer"}
        </h2>
        <p>
          {l === "en"
            ? "Lazuri began as a verb conjugator. It brings together language tools, keyboard guides and learning resources to help more people use Laz in everyday life."
            : "Lazuri bir fiil çekim aracı olarak başladı. Lazcayı günlük hayatta daha çok kullanabilmek için dil araçlarını, klavye rehberlerini ve öğrenme kaynaklarını bir araya getiriyor."}
        </p>
        <h2>{l === "en" ? "Room for every dialect" : "Her lehçeye yer var"}</h2>
        <p>
          {l === "en"
            ? "Explore the forms available for Pazar, Ardeşen, Fındıklı–Arhavi and Hopa. Usage varies between communities; conversations with speakers remain an essential part of learning."
            : "Pazar, Ardeşen, Fındıklı–Arhavi ve Hopa için mevcut çekimleri inceleyin. Kullanım topluluklara göre değişebilir; Lazca konuşanlarla sohbet etmek öğrenmenin önemli bir parçasıdır."}
        </p>
        <h2>
          {l === "en"
            ? "Help improve the tools"
            : "Araçları geliştirmemize yardım edin"}
        </h2>
        <p>
          {l === "en"
            ? "If a form or translation needs a correction, share the word, dialect and an example of how it is used."
            : "Bir çekim veya çeviri düzeltilmeli ise kelimeyi, lehçeyi ve bir kullanım örneğini paylaşın."}
        </p>
        <a href={localLink("/feedback", l)}>
          {l === "en" ? "Send feedback →" : "Geri bildirim →"}
        </a>
        <h2>{l === "en" ? "With thanks" : "Teşekkürler"}</h2>
        <p>
          {l === "en" ? "Thank you to the " : "Destekleri için "}
          <a href="https://www.lazenstitu.com/">
            {l === "en" ? "Laz Institute" : "Laz Enstitüsü"}
          </a>
          {l === "en" ? " and " : " ve "}
          <a href="https://panglot.app/">Panglot</a>
          {l === "en"
            ? " for their support, and to everyone who contributes words, corrections and time."
            : "’a; kelimeler, düzeltmeler ve zamanlarıyla katkıda bulunan herkese teşekkür ederiz."}
        </p>
      </article>
    </>
  );
}
export function NotFound({
  language: l,
  legacy = false,
}: {
  language: Language;
  legacy?: boolean;
}) {
  return (
    <>
      <PageIntro
        title={
          l === "en"
            ? legacy
              ? "Find your verb again."
              : "This page isn’t here."
            : legacy
              ? "Fiilinizi yeniden bulun."
              : "Bu sayfa bulunamadı."
        }
        description={
          legacy
            ? l === "en"
              ? "This older verb link cannot be matched reliably. Search by the verb’s spelling to open its current entry."
              : "Bu eski fiil bağlantısı güvenilir biçimde eşleştirilemiyor. Güncel kaydı açmak için fiilin yazılışını arayın."
            : "404"
        }
      />
      <a className="primary" href={localLink(legacy ? "/verbs" : "/", l)}>
        {l === "en"
          ? legacy
            ? "Search the verbs →"
            : "Go home →"
          : legacy
            ? "Fiil ara →"
            : "Ana sayfa →"}
      </a>
    </>
  );
}
