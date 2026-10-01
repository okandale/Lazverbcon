import { useEffect, useRef, useState } from "react";
import type { Language } from "../i18n";
import { PageIntro } from "./shared";
import { sendFeedback } from "./feedbackDelivery";

export function Feedback({ language: l }: { language: Language }) {
  const [incorrect, setIncorrect] = useState("");
  const [correction, setCorrection] = useState("");
  const [explanation, setExplanation] = useState("");
  const [ready, setReady] = useState(false);
  const [notice, setNotice] = useState("");
  const [delivery, setDelivery] = useState<
    "idle" | "sending" | "success" | "error"
  >("idle");
  const pending = useRef<AbortController | null>(null);
  useEffect(() => () => pending.current?.abort(), []);
  const context = (
    new URLSearchParams(window.location.search).get("context") ?? ""
  ).slice(0, 3000);
  const body = `Lazuri feedback\n\nForm / text: ${incorrect}\nSuggested correction: ${correction}\nDialect / explanation: ${explanation}${context ? `\n\nPage / selection: ${context}` : ""}`;
  return (
    <>
      <PageIntro
        title={l === "en" ? "Feedback" : "Geri bildirim"}
        description={
          l === "en"
            ? "Report a form, suggest a translation or share a local variation."
            : "Bir çekimi bildirin, çeviri önerin veya yerel bir kullanım paylaşın."
        }
      />
      <section className="panel prose feedback">
        <p>
          {l === "en"
            ? "Send a correction to the Lazuri team. You can also prepare an email to info@lazuri.org."
            : "Lazuri ekibine bir düzeltme gönderin. İsterseniz info@lazuri.org adresine e-posta da hazırlayabilirsiniz."}
        </p>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            if (pending.current) return;
            const controller = new AbortController();
            pending.current = controller;
            setDelivery("sending");
            setReady(false);
            setNotice("");
            try {
              await sendFeedback(
                {
                  incorrectWord: incorrect,
                  correction,
                  explanation:
                    explanation +
                    (context ? `\n\nPage / selection: ${context}` : ""),
                },
                controller.signal,
              );
              if (controller.signal.aborted) return;
              setDelivery("success");
              setIncorrect("");
              setCorrection("");
              setExplanation("");
            } catch {
              if (!controller.signal.aborted) {
                setDelivery("error");
                setReady(true);
              }
            } finally {
              pending.current = null;
            }
          }}
          onChange={() => {
            setReady(false);
            if (delivery === "success") setDelivery("idle");
            setNotice("");
          }}
          aria-busy={delivery === "sending"}
        >
          <label className="field">
            <span>
              {l === "en"
                ? "Form or text to review"
                : "İncelenecek çekim veya metin"}
            </span>
            <input
              required
              disabled={delivery === "sending"}
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
              required
              disabled={delivery === "sending"}
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
              disabled={delivery === "sending"}
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
          <div className="actions">
            <button
              className="primary"
              type="submit"
              disabled={delivery === "sending"}
            >
              {delivery === "sending"
                ? l === "en"
                  ? "Sending…"
                  : "Gönderiliyor…"
                : l === "en"
                  ? "Send feedback"
                  : "Geri bildirim gönder"}
            </button>
            <button
              className="text-button"
              type="button"
              disabled={delivery === "sending"}
              onClick={() => {
                setReady(true);
                setNotice("");
              }}
            >
              {l === "en" ? "Prepare email instead" : "E-posta hazırla"}
            </button>
          </div>
        </form>
        <p role={delivery === "error" ? "alert" : "status"}>
          {delivery === "success" &&
            (l === "en"
              ? "Feedback sent. Thank you."
              : "Geri bildiriminiz gönderildi. Teşekkürler.")}
          {delivery === "error" &&
            (l === "en"
              ? "We couldn’t confirm delivery. Your text is still here. It may have arrived; retrying or emailing could send a duplicate."
              : "Teslimatı doğrulayamadık. Metniniz burada duruyor. Mesaj ulaşmış olabilir; yeniden göndermek veya e-posta göndermek yinelenen bir mesaj oluşturabilir.")}
        </p>
        {ready && (
          <div className="email-draft">
            <h2>
              {l === "en"
                ? "Your message is ready to send."
                : "Mesajınız gönderilmeye hazır."}
            </h2>
            {delivery !== "error" && (
              <p>
                {l === "en"
                  ? "Nothing has been sent yet."
                  : "Henüz hiçbir şey gönderilmedi."}
              </p>
            )}
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
