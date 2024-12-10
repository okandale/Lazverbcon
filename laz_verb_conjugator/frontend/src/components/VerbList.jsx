import React, { useState, useRef, useMemo } from 'react';
import { Link } from 'react-router-dom';
import VerbTable from './VerbTable';
import LanguageToggle from './ui/LanguageToggle';
import SpecialCharButton from './ui/SpecialCharButton';
import {
  translations,
  getStoredLanguage,
  setStoredLanguage,
  specialCharacters
} from './constants';
import { 
  verbList, 
  processVerbSearch, 
  formatVerbListForDisplay 
} from './verb-data';

const VerbList = () => {
  const [language, setLanguage] = useState(getStoredLanguage());
  const [searchTerm, setSearchTerm] = useState('');
  const searchInputRef = useRef(null);

  // Memoize the filtered and formatted verbs
  const filteredVerbs = useMemo(() => {
    const filtered = processVerbSearch(searchTerm);
    return formatVerbListForDisplay(filtered);
  }, [searchTerm]);

  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  const handleSpecialCharClick = char => {
    if (searchInputRef.current) {
      const input = searchInputRef.current;
      const start = input.selectionStart;
      const end = input.selectionEnd;
      const text = input.value;
      const before = text.substring(0, start);
      const after = text.substring(end, text.length);
      const newValue = before + char + after;
      input.value = newValue;
      input.selectionStart = input.selectionEnd = start + char.length;
      input.focus();
      setSearchTerm(newValue);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Header with navigation and language toggle */}
      <div className="flex justify-between items-center mb-8 pt-2">
        <Link to="/" className="text-blue-500 hover:underline">
          &larr; {translations[language].backToConjugator}
        </Link>
        <LanguageToggle language={language} onToggle={toggleLanguage} />
      </div>
      
      {/* Title */}
      <h1 className="text-3xl font-bold mb-6 text-center">
        {translations[language].verbsListTitle}
      </h1>

      {/* Special Characters */}
      <div className="flex flex-wrap justify-center gap-2 mb-6">
        {specialCharacters.map((char, index) => (
          <SpecialCharButton
            key={index}
            char={char}
            onClick={handleSpecialCharClick}
          />
        ))}
      </div>

      {/* Search Input */}
      <div className="mb-6">
        <input
          ref={searchInputRef}
          type="text"
          placeholder={translations[language].searchPlaceholder}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Verb Table */}
      <VerbTable 
        verbs={filteredVerbs}
        language={language}
      />

      {/* Verb count */}
      <div className="mt-4 text-center text-sm text-gray-600">
        {filteredVerbs.length} {language === 'en' ? 'verbs' : 'fiil'}
      </div>
    </div>
  );
};

export default VerbList;