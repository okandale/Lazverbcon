import { useState } from "react";
import type { Language } from "../i18n";
import { PageIntro } from "./shared";

export function Feedback({ language: l }: { language: Language }) {
  const [incorrect, setIncorrect] = useState("");
  const [correction, setCorrection] = useState("");
  const [explanation, setExplanation] = useState("");
  const [ready, setReady] = useState(false);
  const [notice, setNotice] = useState("");
  const context = (
    new URLSearchParams(window.location.search).get("context") ?? ""
  ).slice(0, 3000);
  const body = `Lazuri feedback\n\nForm / text: ${incorrect}\nSuggested correction: ${correction}\nDialect / explanation: ${explanation}${context ? `\n\nPage / selection: ${context}` : ""}`;
  return (
    <>
      <PageIntro
        title={l === "en" ? "Help us get it right." : "Birlikte düzeltelim."}
        description={
          l === "en"
            ? "Report a form, suggest a translation or share a local variation."
            : "Bir çekimi bildirin, çeviri önerin veya yerel bir kullanım paylaşın."
        }
      />
      <section className="panel prose feedback">
        <p>
          {l === "en"
            ? "Prepare a message for info@lazuri.org. You’ll review and send it from your own email app, or copy it to an email."
            : "info@lazuri.org için bir mesaj hazırlayın. Mesajı kendi e-posta uygulamanızda inceleyip gönderebilir veya bir e-postaya kopyalayabilirsiniz."}
        </p>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            setReady(true);
            setNotice("");
          }}
          onChange={() => setReady(false)}
        >
          <label className="field">
            <span>
              {l === "en"
                ? "Form or text to review"
                : "İncelenecek çekim veya metin"}
            </span>
            <input
              required
              maxLength={200}
              value={incorrect}
              onChange={(e) => setIncorrect(e.target.value)}
            />
          </label>
          <label className="field">
            <span>
              {l === "en" ? "Suggested correction" : "Düzeltme önerisi"}
            </span>
            <input
              maxLength={200}
              value={correction}
              onChange={(e) => setCorrection(e.target.value)}
            />
          </label>
          <label className="field">
            <span>
              {l === "en"
                ? "Dialect, example or explanation"
                : "Lehçe, örnek veya açıklama"}
            </span>
            <textarea
              rows={5}
              required
              maxLength={2000}
              value={explanation}
              onChange={(e) => setExplanation(e.target.value)}
            />
          </label>
          {context && (
            <details>
              <summary>
                {l === "en"
                  ? "Included page and selection"
                  : "Eklenen sayfa ve seçim"}
              </summary>
              <p className="feedback-context">{context}</p>
            </details>
          )}
          <button className="primary" type="submit">
            {l === "en" ? "Prepare email →" : "E-postayı hazırla →"}
          </button>
        </form>
        {ready && (
          <div className="email-draft">
            <h2>
              {l === "en"
                ? "Your message is ready to send."
                : "Mesajınız gönderilmeye hazır."}
            </h2>
            <p>
              {l === "en"
                ? "Nothing has been sent yet."
                : "Henüz hiçbir şey gönderilmedi."}
            </p>
            <pre>{body}</pre>
            <div className="actions">
              <a
                className="primary"
                href={`mailto:info@lazuri.org?subject=${encodeURIComponent("Lazuri feedback")}&body=${encodeURIComponent(body)}`}
              >
                {l === "en" ? "Open email app ↗" : "E-posta uygulamasını aç ↗"}
              </a>
              <button
                type="button"
                className="text-button"
                onClick={async () => {
                  try {
                    await navigator.clipboard.writeText(body);
                    setNotice(
                      l === "en" ? "Message copied." : "Mesaj kopyalandı.",
                    );
                  } catch {
                    setNotice(
                      l === "en"
                        ? "Select and copy the message above."
                        : "Yukarıdaki mesajı seçip kopyalayın.",
                    );
                  }
                }}
              >
                {l === "en" ? "Copy message" : "Mesajı kopyala"}
              </button>
            </div>
          </div>
        )}
        <p role="status">{notice}</p>
      </section>
    </>
  );
}
