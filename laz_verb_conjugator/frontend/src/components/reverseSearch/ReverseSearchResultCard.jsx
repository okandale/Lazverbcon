import React, { useState } from 'react';

const ReverseSearchResultCard = ({ result, language, onOpenInConjugator }) => {
  const [expanded, setExpanded] = useState(false);
  const localized = (en, tr) => (language === 'tr' ? tr : en);

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

  const meaning =
    language === 'tr'
      ? result.meaning_turkish || result.meaning_english
      : result.meaning_english || result.meaning_turkish;

  const subjectObjectPreview =
    result.subject && result.object
      ? `${result.subject} → ${result.object}`
      : result.subject || result.object || null;

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
    result.is_causative ? localized('Causative', 'Ettirgen') : null,
    result.is_double_causative ? localized('Double causative', 'Çift Ettirgen') : null,
  ].filter(Boolean);

  const valueChipClass = (isActive) =>
    isActive
      ? 'inline-flex items-center rounded-full bg-blue-50 text-blue-700 px-2.5 py-0.5 text-xs font-semibold'
      : 'inline-flex items-center rounded-full bg-gray-100 text-gray-500 px-2.5 py-0.5 text-xs font-medium';

  const hasObject = !!result.object;
  const isNonDefaultMood = !!result.mood && result.mood !== 'indicative';
  const derivationLabel = formatDerivation(result.derivation);
  const hasDerivation = !!derivationLabel;
  const hasMarkers = markerLabels.length > 0;

  return (
    <div className="bg-white shadow-md rounded px-6 pt-5 pb-5">
      <div className="flex justify-between items-start gap-4">
        <div className="min-w-0 flex-1">
          <p className="text-lg font-bold text-blue-700 break-words">
            {result.conjugated_form || '—'}
          </p>

          <p className="text-gray-800 font-medium break-words">
            {result.infinitive || '—'}
            {meaning && (
              <span className="text-gray-500 italic font-normal">
                {' — '}{meaning}
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
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-3 text-sm text-gray-700">
            <p className="md:col-span-2">
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
              {result.subject || '—'}
            </p>

            <p>
              <span className="font-semibold">
                {localized('Object:', 'Nesne:')}
              </span>{' '}
              <span className={valueChipClass(hasObject)}>
                {result.object || localized('None', 'Yok')}
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
                {localized('Derivation:', 'Türetim:')}
              </span>{' '}
              <span className={valueChipClass(hasDerivation)}>
                {derivationLabel || localized('None', 'Yok')}
              </span>
            </p>

            <p className="md:col-span-2">
              <span className="font-semibold">
                {localized('Markers:', 'Belirteçler:')}
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