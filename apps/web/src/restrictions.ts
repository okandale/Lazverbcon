import type { Language } from "./i18n";

const turkish: Record<string, string> = {
  dialect_unavailable: "Bu kaydın seçilen lehçede bir kök biçimi yok.",
  potential_required: "Bu fiil yeterlilik biçimiyle kullanılabilir.",
  mood_tense: "Bu kip için zaman alanında şimdiki zamanı seçin.",
  imperative_subject: "Emir kipinde ikinci tekil veya çoğul kişiyi seçin.",
  person_combination: "Bu özne ve nesne birleşimi kullanılamıyor.",
  derivation_class: "Bu fiil sınıfı için seçilen türetim uygulanmamış.",
  derivation_construction:
    "Bildirme kipinde bir zaman veya yeterlilik ile istek kipini seçin.",
  derivation_object:
    "Bu türetimde nesne ve uygulamalı işaretleyici kullanılamaz.",
  derivation_marker: "Bu işaretleyici seçilen türetimde uygulanmamış.",
  optional_preverb_unsupported: "Bu biçimde isteğe bağlı ön ek uygulanmamış.",
  perfect_features:
    "Yakın geçmiş TVE/TVM fiillerinde nesne ve işaretleyici olmadan kullanılabilir.",
  marker_required: "Bu fiil uygulamalı veya ettirgen işaretleyici gerektirir.",
  nominative_object:
    "Bu nominatif biçimde nesne veya işaretleyici kullanılamaz.",
  dative_marker: "Bu datif biçimde ek işaretleyici kullanılamaz.",
  dative_optative_object: "Datif istek ve emir biçimleri nesne almaz.",
  object_forbidden: "Bu fiil nesne alamaz.",
  marker_object: "Uygulamalı veya ettirgen biçim için bir nesne seçin.",
  not_generated: "Bu birleşim yayımlanan veritabanında üretilmemiş.",
};

export function restrictionText(
  code: string | null | undefined,
  fallback: string | null | undefined,
  language: Language,
) {
  return (
    (language === "tr" && code ? turkish[code] : undefined) ??
    fallback ??
    code ??
    ""
  );
}
