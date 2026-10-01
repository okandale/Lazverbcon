import { afterEach, expect, it, vi } from "vitest";
import {
  FEEDBACK_ENDPOINT,
  FEEDBACK_TIMEOUT_MS,
  sendFeedback,
} from "./feedbackDelivery";

const data = {
  incorrectWord: "doviba",
  correction: "test",
  explanation: "</script><script>test & ç̌</script>",
};
afterEach(() => {
  vi.useRealTimers();
});

function request() {
  const controller = new AbortController();
  const promise = sendFeedback(data, controller.signal);
  const frame = document.querySelector<HTMLIFrameElement>(
    'iframe[title="Feedback delivery"]',
  )!;
  const config = JSON.parse(frame.srcdoc.match(/const config = (.*);/)![1]) as {
    token: string;
    callback: string;
    url: string;
  };
  const response = (
    result: string,
    source: Window | null = frame.contentWindow,
    token = config.token,
  ) => {
    window.dispatchEvent(
      new MessageEvent("message", { source, data: { token, result } }),
    );
  };
  return { controller, promise, frame, config, response };
}

it("uses the original endpoint and fields, isolated from the app, and cleans up on acknowledgement", async () => {
  const { promise, frame, config, response } = request();
  const url = new URL(config.url);
  expect(url.origin + url.pathname).toBe(FEEDBACK_ENDPOINT);
  expect(JSON.parse(url.searchParams.get("data")!)).toEqual(data);
  expect(url.searchParams.get("callback")).toBe(config.callback);
  expect(frame.getAttribute("sandbox")).toBe("allow-scripts");
  expect(frame.srcdoc.match(/<\/script>/g)).toHaveLength(1);
  response("success", window); // An unrelated window must not confirm delivery.
  response("success", frame.contentWindow, "wrong-token");
  expect(frame.isConnected).toBe(true);
  response("success");
  await promise;
  expect(frame.isConnected).toBe(false);
});

it.each(["error", "unexpected"])(
  "rejects %s responses without claiming delivery",
  async (result) => {
    const { promise, frame, response } = request();
    const rejected = expect(promise).rejects.toThrow("Delivery unconfirmed");
    response(result);
    await rejected;
    expect(frame.isConnected).toBe(false);
  },
);

it("times out, removes the frame and ignores a late reply", async () => {
  vi.useFakeTimers();
  const { promise, frame, response } = request();
  const rejected = expect(promise).rejects.toThrow("Delivery timed out");
  await vi.advanceTimersByTimeAsync(FEEDBACK_TIMEOUT_MS);
  await rejected;
  expect(frame.isConnected).toBe(false);
  response("success");
  expect(vi.getTimerCount()).toBe(0);
});

it("cancels an in-flight request and creates no frame for an already cancelled request", async () => {
  const { promise, frame, controller } = request();
  const rejected = expect(promise).rejects.toMatchObject({
    name: "AbortError",
  });
  controller.abort();
  await rejected;
  expect(frame.isConnected).toBe(false);
  await expect(sendFeedback(data, controller.signal)).rejects.toMatchObject({
    name: "AbortError",
  });
  expect(
    document.querySelector('iframe[title="Feedback delivery"]'),
  ).toBeNull();
});

it.each(["success", "rejection", "network", "missing-callback"])(
  "runs the iframe callback protocol: %s",
  async (scenario) => {
    const { promise, frame, config } = request();
    const outcome =
      scenario === "success"
        ? expect(promise).resolves.toBeUndefined()
        : expect(promise).rejects.toThrow();
    const callbacks: Record<string, (value: unknown) => void> = {};
    let script: HTMLScriptElement | undefined;
    // Execute the frame wrapper with a local script loader; never contact production.
    const source = new DOMParser()
      .parseFromString(frame.srcdoc, "text/html")
      .querySelector("script")!.textContent!;
    const frameWindow = frame.contentWindow;
    new Function("window", "document", "parent", source)(
      callbacks,
      {
        createElement: () => document.createElement("script"),
        head: {
          appendChild: (element: HTMLScriptElement) => {
            script = element;
          },
        },
      },
      {
        postMessage: (message: unknown, origin: string) => {
          expect(origin).toBe(location.origin);
          window.dispatchEvent(
            new MessageEvent("message", { source: frameWindow, data: message }),
          );
        },
      },
    );
    expect(script!.src).toBe(config.url);
    if (scenario === "network") script!.dispatchEvent(new Event("error"));
    else if (scenario === "missing-callback")
      script!.dispatchEvent(new Event("load"));
    else
      callbacks[config.callback](
        scenario === "success" ? { result: "success" } : null,
      );
    await outcome;
    expect(frame.isConnected).toBe(false);
  },
);
