# Historical migration evidence

These reports preserve source rows, linguistic decisions and comparison results.
Their deployment commands, counts and workflows describe earlier versions.
Use [current guides](../README.md) for development, editing and publication.

| Record                                                   | Purpose                                                         |
| -------------------------------------------------------- | --------------------------------------------------------------- |
| [Database comparison](database-comparison-2026-10-01.md) | Initial discrepancies against the supplied dump                 |
| [Rule corrections](rule-corrections-2026-10-01.md)       | First corrections and their scope                               |
| [Maintainer parity](maintainer-parity.md)                | Completed spelling/frame reconciliation and later pronoun notes |
| [Migration audit](migration-audit.md)                    | Detailed completed pages, source audit and original checklist   |
| [Retired API inventory](legacy-api.md)                   | Old endpoint contracts deliberately retired                     |

The author-facing [behaviour review](../conjugation-behaviour-review.md) and its
[details](../conjugation-behaviour-details.md) remain at their shared URLs.
The frozen executable test reference remains in `migration/`.

The obsolete admin implementation plan and former deployment docs can be read
from the commit before cleanup:

```bash
git show 6cb80f5:docs/admin-app-plan.md
git show 6cb80f5:Dockerfile
```

See [original application recovery](../legacy-archive.md) for the older source.
