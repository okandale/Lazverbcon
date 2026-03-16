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

  const formatDerivation = (derivation) => {
    if (!derivation) return null;

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

  const previewParts = [
    formatTense(result.tense),
    subjectObjectPreview,
    formatDerivation(result.derivation),
    result.dialect,
  ].filter(Boolean);

  const markerLabels = [
    result.is_applicative ? localized('Applicative', 'Uygulama') : null,
    result.is_causative ? localized('Causative', 'Ettirgen') : null,
    result.is_double_causative ? localized('Double causative', 'Çift Ettirgen') : null,
  ].filter(Boolean);

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
                {localized('Dialect:', 'Ağız:')}
              </span>{' '}
              {result.dialect || '—'}
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
              {result.object || localized('None', 'Yok')}
            </p>

            <p>
              <span className="font-semibold">
                {localized('Mood:', 'Kip:')}
              </span>{' '}
              {result.mood || '—'}
            </p>

            <p>
              <span className="font-semibold">
                {localized('Derivation:', 'Türetim:')}
              </span>{' '}
              {result.derivation ? formatDerivation(result.derivation) : '—'}
            </p>

            <p className="md:col-span-2">
              <span className="font-semibold">
                {localized('Markers:', 'Belirteçler:')}
              </span>{' '}
              {markerLabels.length > 0
                ? markerLabels.join(', ')
                : localized('None', 'Yok')}
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