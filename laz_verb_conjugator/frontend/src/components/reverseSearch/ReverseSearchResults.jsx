import React, { useMemo } from 'react';
import ReverseSearchResultCard from './ReverseSearchResultCard';

const ReverseSearchResults = ({
  language,
  results = [],
  isSearching = false,
  hasSearched = false,
  meta = { query: '', matchType: 'none' },
  onOpenInConjugator,
}) => {
  const localized = (en, tr) => (language === 'tr' ? tr : en);

  const collapsedResults = useMemo(() => {
    if (!Array.isArray(results) || results.length === 0) {
      return [];
    }

    const grouped = new Map();

    for (const result of results) {
      const key = JSON.stringify([
        result.conjugated_form || '',
        result.infinitive || '',
        result.meaning_english || '',
        result.meaning_turkish || '',
        result.tense || '',
        result.mood || '',
        result.frame || '',
        result.subject || '',
        result.object || '',
        result.subject_code || '',
        result.object_code || '',
        result.derivation || '',
        !!result.is_applicative,
        !!result.is_causative,
        !!result.is_double_causative,
        result.optional_prefix || '',
      ]);

      if (!grouped.has(key)) {
        grouped.set(key, {
          ...result,
          regions: result.dialect ? [result.dialect] : [],
        });
        continue;
      }

      const existing = grouped.get(key);

      if (result.dialect && !existing.regions.includes(result.dialect)) {
        existing.regions.push(result.dialect);
      }
    }

    return Array.from(grouped.values()).map((result) => ({
      ...result,
      regions: [...result.regions].sort((a, b) => a.localeCompare(b)),
    }));
  }, [results]);

  const matchNotice =
    meta?.matchType === 'normalized'
      ? localized(
          `No exact match found for “${meta?.query}”. Showing alternate spelling matches.`,
          `“${meta?.query}” için tam eşleşme bulunamadı. Alternatif yazım eşleşmeleri gösteriliyor.`
        )
      : null;

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

  if (!collapsedResults.length) {
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
      {matchNotice && (
        <div className="bg-amber-50 border border-amber-200 text-amber-800 rounded px-4 py-3 text-sm">
          {matchNotice}
        </div>
      )}

      {collapsedResults.map((result, index) => (
        <ReverseSearchResultCard
          key={`${result.infinitive ?? 'result'}-${result.tense ?? 'tense'}-${result.subject_code ?? 'subject'}-${result.object_code ?? 'object'}-${index}`}
          result={result}
          language={language}
          onOpenInConjugator={onOpenInConjugator}
        />
      ))}
    </div>
  );
};

export default ReverseSearchResults;