import { parseSelection } from "../api/selection";
import { dialectNames, labels, names } from "../i18n";
import type { Language } from "../i18n";

/** Show a readable selection, never raw JSON or a caller-provided external link. */
export function feedbackContext(raw: string, language: Language) {
  if (!raw || raw.length > 3000) return null;
  try {
    const url = new URL(raw, window.location.origin);
    if (url.origin !== window.location.origin || url.pathname !== "/conjugator")
      return null;
    const t = labels[language],
      n = names[language];
    const details: [string, string][] = [
      [
        language === "en" ? "Page" : "Sayfa",
        language === "en" ? "Conjugator" : "Fiil çekimi",
      ],
    ];
    const encoded = url.searchParams.get("selection");
    const reverse = url.searchParams.get("reverse");
    let link = "/conjugator";
    if (encoded) {
      const input = JSON.parse(encoded);
      const selected = parseSelection(encoded);
      if (!input || input.entry_id !== selected.entry_id) return null;
      details.push(
        [
          language === "en" ? "Verb" : "Fiil",
          url.searchParams.get("verb")?.slice(0, 200) || selected.entry_id,
        ],
        [t.tense, n[selected.tense ?? "present"]],
        [t.mood, n[selected.mood ?? "indicative"]],
        [t.derivation, n[selected.derivation ?? "none"]],
        [
          t.subject,
          selected.subject === "all" ? t.all : n[selected.subject ?? "1sg"],
        ],
        [
          t.object,
          selected.object === "all"
            ? t.all
            : selected.object
              ? n[selected.object]
              : t.none,
        ],
        [
          t.dialects,
          (selected.dialects ?? []).map((d) => dialectNames[d]).join(" · "),
        ],
        [
          t.markers,
          [
            selected.applicative ? t.applicative : null,
            selected.causative !== "none" ? n[selected.causative!] : null,
          ]
            .filter(Boolean)
            .join(" · ") || t.none,
        ],
        [
          t.optional,
          selected.optional_preverb
            ? language === "en"
              ? "Previous setting"
              : "Önceki seçenek"
            : selected.optional_prefix === "none"
              ? t.none
              : (selected.optional_prefix ?? t.none),
        ],
      );
      link += "?selection=" + encodeURIComponent(JSON.stringify(selected));
    } else if (reverse) {
      details.push([t.reverse, reverse.slice(0, 200)]);
      link += "?reverse=" + encodeURIComponent(reverse.slice(0, 200));
    } else if (url.searchParams.get("view") === "verbs") {
      details[0][1] = language === "en" ? "Verb list" : "Fiil listesi";
      link += "?view=verbs";
    }
    return {
      details,
      link,
      text: details.map(([label, value]) => `${label}: ${value}`).join("\n"),
    };
  } catch {
    return null;
  }
}
