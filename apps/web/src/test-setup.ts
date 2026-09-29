// Node's Fetch Request rejects jsdom's AbortSignal from another realm.
// These UI tests mock transport; omit that signal only in the test Request.
const NodeRequest = globalThis.Request;
globalThis.Request = class extends NodeRequest {
  constructor(input: RequestInfo | URL, init?: RequestInit) {
    super(input, { ...init, signal: undefined });
  }
};
