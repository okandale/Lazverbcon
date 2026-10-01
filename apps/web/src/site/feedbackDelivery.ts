// Keep the original destination and field names: its Apps Script is managed separately.
export const FEEDBACK_ENDPOINT =
  "https://script.google.com/macros/s/AKfycbxocjHtMbmcehees6xRUs43RLaqTwFiLjp9IXbsswXZj52QcL-owsk4xDG4kkOQksbP/exec";
export const FEEDBACK_TIMEOUT_MS = 20_000;

export type FeedbackData = {
  incorrectWord: string;
  correction: string;
  explanation: string;
};

export function sendFeedback(
  data: FeedbackData,
  signal: AbortSignal,
): Promise<void> {
  return new Promise((resolve, reject) => {
    if (signal.aborted) {
      reject(new DOMException("Cancelled", "AbortError"));
      return;
    }
    // getRandomValues also works on HTTP LAN previews; randomUUID requires HTTPS.
    const token = Array.from(
      crypto.getRandomValues(new Uint8Array(16)),
      (byte) => byte.toString(16).padStart(2, "0"),
    ).join("");
    const callback = "callback" + token;
    const url = new URL(FEEDBACK_ENDPOINT);
    url.searchParams.set("callback", callback);
    url.searchParams.set("data", JSON.stringify(data));
    const frame = document.createElement("iframe");
    frame.hidden = true;
    frame.title = "Feedback delivery";
    // JSONP executes remote JavaScript. Keep it outside the app's origin and DOM.
    frame.setAttribute("sandbox", "allow-scripts");
    frame.referrerPolicy = "no-referrer";
    let finished = false;
    const finish = (error?: Error) => {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      window.removeEventListener("message", receive);
      signal.removeEventListener("abort", abort);
      frame.remove();
      if (error) reject(error);
      else resolve();
    };
    const abort = () => finish(new DOMException("Cancelled", "AbortError"));
    const receive = (event: MessageEvent) => {
      if (event.source !== frame.contentWindow || event.data?.token !== token)
        return;
      finish(
        event.data.result === "success"
          ? undefined
          : new Error("Delivery unconfirmed"),
      );
    };
    const timer = window.setTimeout(
      () => finish(new Error("Delivery timed out")),
      FEEDBACK_TIMEOUT_MS,
    );
    window.addEventListener("message", receive);
    signal.addEventListener("abort", abort, { once: true });
    // Escape '<' even inside a JS string so user text cannot close the script tag.
    const config = JSON.stringify({
      token,
      callback,
      url: url.href,
      origin: location.origin,
    }).replaceAll("<", "\\u003c");
    frame.srcdoc = `<!doctype html><meta name="referrer" content="no-referrer"><script>
      const config = ${config};
      let replied = false;
      function reply(result) {
        if (replied) return;
        replied = true;
        parent.postMessage({token: config.token, result}, config.origin);
      }
      window[config.callback] = response => reply(response?.result === 'success' ? 'success' : 'error');
      const script = document.createElement('script');
      script.src = config.url;
      script.referrerPolicy = 'no-referrer';
      script.onerror = () => reply('error');
      script.onload = () => { if (!replied) reply('error'); };
      document.head.appendChild(script);
    </script>`;
    try {
      document.body.appendChild(frame);
    } catch (error) {
      finish(
        error instanceof Error ? error : new Error("Delivery unavailable"),
      );
    }
  });
}
