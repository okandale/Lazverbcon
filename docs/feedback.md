# Feedback delivery

The feedback page uses the original Google Apps Script deployment, with the same
`incorrectWord`, `correction` and `explanation` fields. Its endpoint is defined in
`apps/web/src/site/feedbackDelivery.ts` and matches `FeedbackForm.jsx` in the
[archived source](legacy-archive.md).
Page/conjugation context is appended to `explanation`; no server changes are
required. The destination behind that script is managed outside this repository.

The user approved retaining this integration on 2026-10-01. It works independently
of FastAPI and can remain in a future static website.

## Behaviour

- The original JSONP request runs in a hidden iframe with `sandbox="allow-scripts"`.
  It has no access to the app's origin, storage or DOM. The parent accepts a reply
  only from that frame with the request's unique token.
- Only the endpoint's `result: "success"` acknowledgement clears the form.
- Network errors, invalid replies and a 20-second timeout retain the text and
  expose an email/copy fallback to the existing `info@lazuri.org` address.
- The form prevents concurrent submissions. It never retries automatically:
  a lost acknowledgement can mean the original submission already arrived.
- Leaving the page removes the frame and listeners. This does not undo a
  submission that already reached the service.
- Incorrect text and its correction are required, as in the old form. Explanation
  is optional. Both English and Turkish interfaces are supported.

JSONP still sends feedback in a URL and depends on Google's deployment remaining
available. Replacing that protocol would require changing the receiving script;
this migration preserves the existing service contract. A future Content Security
Policy must permit the isolated frame's bootstrap and the Google script/redirect.

## Verification

Local tests cover the exact destination/payload, context, success, rejected and
missing callbacks, network failure, timeout, unexpected window messages, cleanup,
duplicate submission, retry, email fallback and Turkish confirmation. Tests use
local responses and do not submit feedback to production.

On 2026-10-01 the owner confirmed that feedback worked after testing the migrated
integration. Live delivery is therefore marked verified in the migration checklist.
This confirmation is owner-reported; the automated tests use local responses and
do not send production feedback. No receiving-script change was required.
