import React, { useState } from 'react';

const ReverseSearchResultCard = ({ result, language, onOpenInConjugator }) => {
  const [expanded, setExpanded] = useState(false);
  const localized = (en, tr) => (language === 'tr' ? tr : en);

  const matchLabel =
    result.match_type === 'normalized_strict' || result.match_type === 'normalized_broad'
      ? localized('Alternate spelling match', 'Alternatif yazım eşleşmesi')
      : result.match_type === 'fuzzy'
      ? localized('Similar spelling match', 'Benzer yazım eşleşmesi')
      : null;

  const formatTense = (tense) => {
    const tenseLabels = {
      present: localized('Present', 'Şimdiki Zaman'),
      past: localized('Past', 'Geçmiş Zaman'),
      future: localized('Future', 'Gelecek Zaman'),
      past_progressive: localized('Past Progressive', 'Geçmişte Devam Eden'),
      present_perfect: localized('Present Perfect', 'Yakın Geçmiş'),
    };

    return tenseLabels[tense] || tense || '—';
  };

  const formatMood = (mood) => {
    if (!mood) return '—';

    const moodLabels = {
      indicative: localized('Indicative', 'Bildirme kipi'),
      imperative: localized('Imperative', 'Emir kipi'),
      negative_imperative: localized('Negative imperative', 'Olumsuz emir kipi'),
      optative: localized('Optative', 'İstek kipi'),
    };

    return moodLabels[mood] || mood;
  };

  const formatDerivation = (derivation) => {
    if (!derivation || derivation === 'none') return null;

    const derivationLabels = {
      passive: localized('Passive', 'Edilgen'),
      potential: localized('Potential', 'Yeterlilik'),
    };

    return derivationLabels[derivation] || derivation;
  };

  const normalizeObjectCode = (code) => {
    if (code === 'O3SG' || code === 'O3PL') return 'O3';
    return code || null;
  };

  const formatPersonCode = (code, type = 'subject') => {
    if (!code) return null;

    const normalizedCode =
      type === 'object' ? normalizeObjectCode(code) : code;

    const labels = {
      en: {
        S1SG: 'I',
        S2SG: 'you',
        S3SG: 's/he',
        S1PL: 'we',
        S2PL: 'you (plural)',
        S3PL: 'they',

        O1SG: 'I',
        O2SG: 'you',
        O3SG: 's/he',
        O1PL: 'we',
        O2PL: 'you (plural)',
        O3PL: 'they',
        O3: 'she/he/they',
      },
      tr: {
        S1SG: 'ben',
        S2SG: 'sen',
        S3SG: 'o',
        S1PL: 'biz',
        S2PL: 'siz',
        S3PL: 'onlar',

        O1SG: 'ben',
        O2SG: 'sen',
        O3SG: 'o',
        O1PL: 'biz',
        O2PL: 'siz',
        O3PL: 'onlar',
        O3: 'o/onlar',
      },
    };

    return labels[language]?.[normalizedCode] || normalizedCode;
  };

  const formatVerbGroup = () => {
    const frame = result.frame || '';

    const frameLabels = {
      Dative: localized('Dative', 'Yönelme fiili'),
      Ergative: localized('Ergative', 'Ergatif fiili'),
      Nominative: localized('Nominative', 'Nominatif fiili'),
    };

    if (frameLabels[frame]) {
      return frameLabels[frame];
    }

    if (language === 'tr') {
      return result.verb_group_turkish || result.verb_group_code || '—';
    }
    return result.verb_group_english || result.verb_group_code || '—';
  };

  const meaning =
    language === 'tr'
      ? result.meaning_turkish || result.meaning_english
      : result.meaning_english || result.meaning_turkish;

  const displaySubject = formatPersonCode(result.subject_code, 'subject');
  const displayObject = formatPersonCode(result.object_code, 'object');
  const displayVerbGroup = formatVerbGroup();

  const subjectObjectPreview =
    displaySubject && displayObject
      ? `${displaySubject} → ${displayObject}`
      : displaySubject || displayObject || null;

  const regionLabel =
    Array.isArray(result.regions) && result.regions.length > 0
      ? result.regions.join(', ')
      : result.dialect || null;

  const previewParts = [
    formatTense(result.tense),
    subjectObjectPreview,
    formatDerivation(result.derivation),
    regionLabel,
  ].filter(Boolean);

  const markerLabels = [
    result.is_applicative ? localized('Applicative', 'Uygulama') : null,
    result.is_causative ? localized('Causative', 'Oldurgan') : null,
    result.is_double_causative ? localized('Double causative', 'Ettirgen') : null,
  ].filter(Boolean);

  const valueChipClass = (isActive) =>
    isActive
      ? 'inline-flex items-center rounded-full bg-blue-50 text-blue-700 px-3 py-1 text-sm font-semibold'
      : 'inline-flex items-center rounded-full bg-gray-100 text-gray-500 px-3 py-1 text-sm font-medium';

  const hasSubject = !!displaySubject;
  const hasObject = !!displayObject;
  const isNonDefaultMood = !!result.mood && result.mood !== 'indicative';
  const derivationLabel = formatDerivation(result.derivation);
  const hasDerivation = !!derivationLabel;
  const hasMarkers = markerLabels.length > 0;
  const hasVerbGroup = !!displayVerbGroup && displayVerbGroup !== '—';

  return (
    <div className="bg-white shadow-md rounded px-6 pt-5 pb-5">
      <div className="flex justify-between items-start gap-4">
        <div className="min-w-0 flex-1">
          <p className="text-lg font-bold text-blue-700 break-words">
            {result.conjugated_form || '—'}
          </p>

          {matchLabel && (
            <div className="mt-1">
              <span className="inline-flex items-center rounded-full bg-amber-50 text-amber-700 px-2.5 py-0.5 text-xs font-medium">
                {matchLabel}
              </span>
            </div>
          )}

          <p className="text-gray-800 font-medium break-words">
            {result.infinitive || '—'}
            {meaning && (
              <span className="text-gray-500 italic font-normal">
                {' — '}
                {meaning}
              </span>
            )}
          </p>

          <p className="text-sm text-gray-600 mt-2 break-words">
            {previewParts.join(' • ')}
          </p>
        </div>

        <button
          type="button"
          onClick={() => setExpanded((prev) => !prev)}
          className="text-sm text-blue-600 hover:text-blue-800 font-medium shrink-0"
        >
          {expanded
            ? localized('Hide details', 'Detayları gizle')
            : localized('Show details', 'Detayları göster')}
        </button>
      </div>

      {expanded && (
        <div className="mt-4 border-t pt-4">
          <div className="grid grid-cols-2 gap-x-4 gap-y-3 text-sm text-gray-700">
            <p className="col-span-2">
              <span className="font-semibold">
                {localized('Infinitive:', 'Mastar:')}
              </span>{' '}
              {result.infinitive || '—'}
            </p>

            <p>
              <span className="font-semibold">
                {localized('Tense:', 'Zaman:')}
              </span>{' '}
              {formatTense(result.tense)}
            </p>

            <p>
              <span className="font-semibold">
                {localized('Regions:', 'Bölgeler:')}
              </span>{' '}
              {Array.isArray(result.regions) && result.regions.length > 0
                ? result.regions.join(', ')
                : result.dialect || '—'}
            </p>

            <p>
              <span className="font-semibold">
                {localized('Subject:', 'Özne:')}
              </span>{' '}
              <span className={valueChipClass(hasSubject)}>
                {displaySubject || localized('None', 'Yok')}
              </span>
            </p>

            <p>
              <span className="font-semibold">
                {localized('Object:', 'Nesne:')}
              </span>{' '}
              <span className={valueChipClass(hasObject)}>
                {displayObject || localized('None', 'Yok')}
              </span>
            </p>

            <p>
              <span className="font-semibold">
                {localized('Mood:', 'Kip:')}
              </span>{' '}
              <span className={valueChipClass(isNonDefaultMood)}>
                {formatMood(result.mood)}
              </span>
            </p>

            <p>
              <span className="font-semibold">
                {localized('Verb group:', 'Fiil grubu:')}
              </span>{' '}
              <span className={valueChipClass(hasVerbGroup)}>
                {displayVerbGroup}
              </span>
            </p>

            <p>
              <span className="font-semibold">
                {localized('Derivation:', 'Türetim:')}
              </span>{' '}
              <span className={valueChipClass(hasDerivation)}>
                {derivationLabel || localized('None', 'Yok')}
              </span>
            </p>

            <p>
              <span className="font-semibold">
                {localized('Markers:', 'Belirteç:')}
              </span>{' '}
              <span className={valueChipClass(hasMarkers)}>
                {hasMarkers
                  ? markerLabels.join(', ')
                  : localized('None', 'Yok')}
              </span>
            </p>
          </div>

          {result.infinitive && (
            <div className="pt-4">
              <button
                type="button"
                onClick={() => onOpenInConjugator?.(result)}
                className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg transition-colors"
              >
                {localized('Open in Conjugator', 'Çekim Aracında Aç')}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ReverseSearchResultCard;