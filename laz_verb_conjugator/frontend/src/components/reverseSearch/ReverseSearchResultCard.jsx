import React, { useState } from 'react';

const ReverseSearchResultCard = ({ result, language, onOpenInConjugator }) => {
  const [expanded, setExpanded] = useState(false);
  const localized = (en, tr) => (language === 'tr' ? tr : en);

  return (
    <div className="bg-white shadow-md rounded px-6 pt-5 pb-5">
      <div className="flex justify-between items-start gap-4">
        <div>
            <p className="text-lg font-bold text-blue-700">
            {result.conjugated_form || '—'}
            </p>
            <p className="text-gray-800 font-medium">
            {result.infinitive || '—'}
            </p>
            <p className="text-sm text-gray-600 mt-1">
            {[
                result.tense,
                result.subject,
                result.object || null,
                result.dialect,
            ].filter(Boolean).join(' • ')}
            </p>
        </div>

        <button
          type="button"
          onClick={() => setExpanded((prev) => !prev)}
          className="text-sm text-blue-600 hover:text-blue-800 font-medium"
        >
          {expanded
            ? localized('Hide details', 'Detayları gizle')
            : localized('Show details', 'Detayları göster')}
        </button>
      </div>

      {expanded && (
        <div className="mt-4 border-t pt-4 text-sm text-gray-700 space-y-2">
          <p>
            <span className="font-semibold">
              {localized('Infinitive:', 'Mastar:')}
            </span>{' '}
            {result.infinitive || '—'}
          </p>
          <p>
            <span className="font-semibold">
              {localized('Tense:', 'Zaman:')}
            </span>{' '}
            {result.tense || '—'}
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
              {localized('Dialect:', 'Ağız/Lehçe:')}
            </span>{' '}
            {result.dialect || '—'}
          </p>
          <p>
            <span className="font-semibold">
              {localized('Match type:', 'Eşleşme türü:')}
            </span>{' '}
            {result.match_type || '—'}
          </p>

          {Array.isArray(result.markers) && result.markers.length > 0 && (
            <p>
              <span className="font-semibold">
                {localized('Markers:', 'Belirteçler:')}
              </span>{' '}
              {result.markers.join(', ')}
            </p>
          )}

          {result.infinitive && (
            <div className="pt-2">
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