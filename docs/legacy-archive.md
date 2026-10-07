# Original application recovery

The original application was removed from the active branch on 1 October 2026.
It remains in Git history at:

`b2f0f8b57e51702da215dc48dc7b78587c139c2d`

[Browse the original application](https://github.com/okandale/Lazverbcon/tree/b2f0f8b57e51702da215dc48dc7b78587c139c2d/laz_verb_conjugator).

Inspect a file without changing your checkout:

```bash
git show b2f0f8b57e51702da215dc48dc7b78587c139c2d:laz_verb_conjugator/frontend/src/components/FeedbackForm.jsx
```

The old Flask app, duplicate frontend/conjugator implementations, notebooks,
obsolete SQL export and one-time import scripts are preserved there. Their old
environments and directory layout are required to run them.

The active tree retains only useful evidence: frozen rules, expected-output
fixtures, source mappings, copied public assets and unfinished translation prompts.
Uploaded dumps and working databases remain Git ignored.

For current instructions use [the project guides](README.md). Detailed migration
reports are in [history](history/README.md).
