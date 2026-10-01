import React from "react";
import type { Match } from "../../api/client";
import { dialectNames, labels, names } from "../../i18n";
import type { Language } from "../../i18n";

export function ReverseMatch({
  match,
  language,
  onSelect,
}: {
  match: Match;
  language: Language;
  onSelect: (match: Match) => void;
}) {
  const t = labels[language];
  const n = names[language];
  const dialects = [...new Set(match.variants.map((v) => v.features.dialect))];
  const prefixLabel = (features: Match["features"]) =>
    features.optional_prefix && features.optional_prefix !== "none"
      ? features.optional_prefix
      : features.optional_preverb
        ? t.optional
        : language === "en"
          ? "No optional preverb"
          : "İsteğe bağlı ön fiil yok";
  const mixedPreverbs =
    new Set(match.variants.map((v) => prefixLabel(v.features))).size > 1;
  return (
    <article className="match">
      <div>
        <h3>{match.form.spelling}</h3>
        <p>
          {match.entry.infinitive} ·{" "}
          {language === "en" ? match.entry.english : match.entry.turkish}
        </p>
        <small>
          {dialects.map((d) => dialectNames[d]).join(" · ")} ·{" "}
          {n[match.features.tense]} · {n[match.features.mood]} ·{" "}
          {n[match.features.subject]}
          {match.features.object && ` → ${n[match.features.object]}`}
          {` · ${n[match.entry.verb_class]}`}
          {match.features.derivation !== "none" &&
            ` · ${n[match.features.derivation]}`}
          {match.features.applicative && ` · ${t.applicative}`}
          {match.features.causative !== "none" &&
            ` · ${t.causative}: ${n[match.features.causative]}`}
          {!mixedPreverbs &&
            (match.features.optional_preverb ||
              (match.features.optional_prefix &&
                match.features.optional_prefix !== "none")) &&
            ` · ${prefixLabel(match.features)}`}
        </small>
        <details className="analysis-details">
          <summary>
            {language === "en"
              ? "Dialects and options"
              : "Lehçeler ve seçenekler"}
          </summary>
          {mixedPreverbs && (
            <p>
              {language === "en"
                ? "Several prefix settings give this spelling."
                : "Birden fazla ön ek seçeneği bu biçimi verir."}
            </p>
          )}
          <ul>
            {match.variants.map((variant, index) => (
              <li key={index}>
                <span>
                  {dialectNames[variant.features.dialect]} ·{" "}
                  {prefixLabel(variant.features)}
                </span>
                <button
                  type="button"
                  aria-label={`${t.open}: ${dialectNames[variant.features.dialect]} · ${prefixLabel(variant.features)}`}
                  onClick={() =>
                    onSelect({ ...match, ...variant, variants: [variant] })
                  }
                >
                  {t.open} →
                </button>
              </li>
            ))}
          </ul>
        </details>
      </div>
      <button type="button" onClick={() => onSelect(match)}>
        {t.open} →
      </button>
    </article>
  );
}
