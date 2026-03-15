import React from 'react';
import ReverseSearchResultCard from './ReverseSearchResultCard';

const ReverseSearchResults = ({
  language,
  results = [],
  isSearching = false,
  hasSearched = false,
  onOpenInConjugator,
}) => {
  const localized = (en, tr) => (language === 'tr' ? tr : en);

  if (isSearching) {
    return (
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 text-center text-gray-600">
        {localized('Searching...', 'Aranıyor...')}
      </div>
    );
  }

  if (!hasSearched) {
    return (
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 text-center text-gray-500">
        {localized(
          'Search for a form to see possible matches.',
          'Olası eşleşmeleri görmek için bir biçim arayın.'
        )}
      </div>
    );
  }

  if (!results || results.length === 0) {
    return (
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 text-center text-gray-600">
        {localized(
          'No matching forms found.',
          'Eşleşen biçim bulunamadı.'
        )}
      </div>
    );
  }

  return (
    <div className="space-y-4 mb-4">
      {results.map((result, index) => (
        <ReverseSearchResultCard
          key={result.id ?? `${result.infinitive ?? 'result'}-${index}`}
          result={result}
          language={language}
          onOpenInConjugator={onOpenInConjugator}
        />
      ))}
    </div>
  );
};

export default ReverseSearchResults;