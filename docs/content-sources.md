# Public website content

Migrated on 2026-09-29. UI content lives in `apps/web/src/site/`; it is versioned
with the app and has no database dependency. Normal anchor navigation uses
language query parameters so direct links and server refreshes work. The Python
server serves only the known public routes as successful application pages.

## Sources and deliberate changes

| Content | Source | Migration choice |
| --- | --- | --- |
| Home, about, resources and acknowledgements | Old frontend components and live lazuri.org | Rewrote copy for the shared layout; preserved useful external destinations and corrected the Institute link. |
| Events | Live https://lazuri.org/events | Kept the current no-events state. Did not publish the repo's older class schedule/pricing/signup link as current. |
| Hopa phrases | https://lazuri.org/resources/phrase-guide/hopa | All 24 phrases across Market (6), Pharmacy (5), Restaurant (7), Hotel (6), plus all 12 Market vocabulary entries. Preserved Laz spelling, capitalization, punctuation and variants verbatim. Fixed English “loafs” and Turkish “receçetesiz” and sentence capitalization. Added Turkish vocabulary labels. |
| Other phrase dialects | Live phrase-guide index and dialect pages | Original pages showed placeholders, including the wrong Pazar title on other dialect routes. Correct titles and honest unavailable states now replace these. Reviewed translations remain in the backlog. |
| Keyboard illustrations | `laz_verb_conjugator/frontend/public/images/keyboard/` | Copied 12 relevant local illustrations into the new public assets. Labelled them as original-version examples. Did not download third-party media. |
| Keyboard instructions | Original six guide components and official Keyman docs below | Rewrote shorter English/Turkish steps, linked official help, removed dead video links and unnecessary keyboard-removal walkthroughs. OS shortcut behavior is no longer stated as universal. |
| Feedback | Original form fields and public `info@lazuri.org` contact | Email draft + copy workflow. No embedded Google script or JSONP; no claim of server delivery. The user reviews and sends the message in their own email app. |

No external forms, email messages or feedback were submitted while migrating.
No admin session or production data was accessed.

## Keyboard references

- [Laz keyboard](https://keyman.com/keyboards/laz): supported desktop/mobile
  platforms and the install destination.
- [Windows installation](https://help.keyman.com/products/windows/current-version/start/download-and-install-keyboard).
- [macOS help](https://help.keyman.com/products/mac/).
- [Android setup](https://help.keyman.com/products/android/current-version/start/)
  and [system keyboard setup](https://help.keyman.com/products/android/current-version/start/enabling-system-keyboard).
- [iPhone/iPad setup](https://help.keyman.com/products/iphone-and-ipad/current-version/start/).
- [Keyboard-specific help](https://help.keyman.com/keyboard/laz), linked from the
  official keyboard listing. Its content could not be fetched during this audit;
  layout details still use the original local guide. Windows/macOS/Android/iOS
  installations were not exercised on physical devices.

## External link verification limits

The Laz Institute, its dictionary, the Minecraft GitHub project and the official
Keyman listing/help pages were reachable during research. The research browser
could not confirm Lazca.xyz, Panglot or Buy Me a Coffee; their original links are
retained, not represented as fully verified. The Minecraft video and app-store
destinations are carried from the original guides; no downloads or installs ran.
Recheck external destinations before a public launch.

## Editing content

- `Pages.tsx`: home, events and about copy.
- `content.ts`: external resources and phrase dialect names.
- `keyboards.ts`: bilingual keyboard steps and help links.
- `phrases.ts`: Hopa phrases and vocabulary, with source date. New dialect data
  must be keyed separately and reviewed; do not reuse Hopa forms under another label.
- `shared.tsx`: navigation, shared footer and language preference handling.
- `Site.tsx` and Python `website.py`: update both when adding a public URL; the
  route tests should verify direct loading as well as in-app navigation.

Remaining linguistic/content questions and optional integrations are tracked in
[the migration checklist](migration-backlog.md).
