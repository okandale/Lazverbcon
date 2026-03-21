import React, { useEffect, useRef } from 'react';

const ReverseSearchSection = ({
  language,
  reverseQuery,
  setReverseQuery,
  onSubmit,
  onReset,
  isSearching = false,
  inputRef,
  suggestions = [],
  isLoadingSuggestions = false,
  showSuggestions = false,
  setShowSuggestions,
  highlightedSuggestionIndex = -1,
  setHighlightedSuggestionIndex,
  skipNextSuggestionFetch,
}) => {
  const localized = (en, tr) => (language === 'tr' ? tr : en);
  const containerRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [setShowSuggestions]);

  const handleSelectSuggestion = (item) => {
    skipNextSuggestionFetch.current = true;
    setReverseQuery(item.spelling);
    setShowSuggestions(false);
    setHighlightedSuggestionIndex(-1);
  };

  const handleInputChange = (e) => {
    setReverseQuery(e.target.value);
    setShowSuggestions(true);
    setHighlightedSuggestionIndex(-1);
  };

  const handleInputFocus = () => {
    if (suggestions.length > 0) {
      setShowSuggestions(true);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      if (showSuggestions && suggestions.length > 0 && highlightedSuggestionIndex >= 0) {
        e.preventDefault();
        handleSelectSuggestion(suggestions[highlightedSuggestionIndex]);
        return;
      }

      setShowSuggestions(false);
      setHighlightedSuggestionIndex(-1);
      return;
    }

    if (!showSuggestions || suggestions.length === 0) {
      return;
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setHighlightedSuggestionIndex((prev) =>
        prev < suggestions.length - 1 ? prev + 1 : 0
      );
      return;
    }

    if (e.key === 'ArrowUp') {
      e.preventDefault();
      setHighlightedSuggestionIndex((prev) =>
        prev > 0 ? prev - 1 : suggestions.length - 1
      );
      return;
    }

    if (e.key === 'Escape') {
      setShowSuggestions(false);
      setHighlightedSuggestionIndex(-1);
    }
  };

  return (
    <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <div className="mb-4">
        <h2 className="text-xl font-bold text-gray-800 mb-2">
          {localized('Form Lookup', 'Biçim Arama')}
        </h2>
        <p className="text-sm text-gray-600">
          {localized(
            'Search for a conjugated Laz verb form to find possible infinitives and grammatical analyses.',
            'Çekimli bir Lazca fiil biçimini arayarak olası mastarları ve dilbilgisel çözümlemeleri bulun.'
          )}
        </p>
      </div>

      <form onSubmit={onSubmit}>
        <div className="mb-4 relative" ref={containerRef}>
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="reverseQuery"
          >
            {localized('Enter a verb form:', 'Bir fiil biçimi girin:')}
          </label>

          <div className="relative">
            <input
              ref={inputRef}
              id="reverseQuery"
              type="text"
              value={reverseQuery}
              onChange={handleInputChange}
              onFocus={handleInputFocus}
              onKeyDown={handleKeyDown}
              placeholder={localized('e.g. t̆axu', 'örn. t̆axu')}
              className="shadow appearance-none border rounded w-full py-2 px-3 pr-10 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
              autoComplete="off"
            />

            {isLoadingSuggestions && reverseQuery.trim() && (
              <div className="absolute inset-y-0 right-3 flex items-center text-xs text-gray-400">
                {localized('...', '...')}
              </div>
            )}
          </div>

          {showSuggestions && suggestions.length > 0 && (
            <ul className="absolute z-20 mt-1 w-full overflow-y-auto max-h-60 rounded-lg border border-gray-200 bg-white shadow-lg">
              {suggestions.map((item, index) => (
                <li
                  key={`${item.spelling}-${index}`}
                  onMouseDown={() => handleSelectSuggestion(item)}
                  className={`px-3 py-2 cursor-pointer text-sm ${
                    index === highlightedSuggestionIndex
                      ? 'bg-blue-50 text-blue-700'
                      : 'hover:bg-gray-50 text-gray-700'
                  }`}
                >
                  <div className="font-medium">{item.spelling}</div>

                  {(item.infinitive || item.dialect) && (
                    <div className="text-xs text-gray-500">
                      {[item.infinitive, item.dialect].filter(Boolean).join(' • ')}
                    </div>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="flex justify-between gap-4">
          <button
            type="submit"
            disabled={isSearching}
            className="flex-1 min-w-32 bg-blue-500 hover:bg-blue-600 active:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-150 ease-in-out shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="block w-full text-center">
              {isSearching
                ? localized('Searching...', 'Aranıyor...')
                : localized('Search', 'Ara')}
            </span>
          </button>

          <button
            type="button"
            onClick={onReset}
            className="flex-1 min-w-32 bg-gray-500 hover:bg-gray-600 active:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-150 ease-in-out shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50"
          >
            <span className="block w-full text-center">
              {localized('Reset', 'Sıfırla')}
            </span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default ReverseSearchSection;