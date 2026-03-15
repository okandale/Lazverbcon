import React from 'react';

const ReverseSearchSection = ({
  language,
  reverseQuery,
  setReverseQuery,
  onSubmit,
  isSearching = false,
  inputRef,
}) => {
  const localized = (en, tr) => (language === 'tr' ? tr : en);

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
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="reverseQuery"
          >
            {localized('Enter a verb form:', 'Bir fiil biçimi girin:')}
          </label>
          <input
            ref={inputRef}
            id="reverseQuery"
            type="text"
            value={reverseQuery}
            onChange={(e) => setReverseQuery(e.target.value)}
            placeholder={localized('e.g. t̆axu', 'örn. t̆axu')}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
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
        </div>
      </form>
    </div>
  );
};

export default ReverseSearchSection;