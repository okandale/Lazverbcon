import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import VerbTable from './VerbTable';
import {
  translations,
  API_URLS,
  getStoredLanguage,
  setStoredLanguage,
  specialCharacters
} from './constants';

const VerbList = () => {
  const [verbs, setVerbs] = useState([]);
  const [filteredVerbs, setFilteredVerbs] = useState([]);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState(getStoredLanguage());
  const [searchTerm, setSearchTerm] = useState('');
  const searchInputRef = useRef(null);

  useEffect(() => {
    const fetchVerbs = async () => {
      try {
        const response = await fetch(API_URLS.verbs);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setVerbs(data);
        setFilteredVerbs(data);
      } catch (err) {
        console.error('Error fetching verbs:', err);
        setError('Failed to load verbs data.');
      }
    };

    fetchVerbs();
  }, []);

  useEffect(() => {
    const filtered = verbs.filter(verb => 
      verb['Laz Infinitive'].toLowerCase().includes(searchTerm.toLowerCase()) ||
      verb['Turkish Verb'].toLowerCase().includes(searchTerm.toLowerCase()) ||
      verb['English Translation'].toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredVerbs(filtered);
  }, [searchTerm, verbs]);

  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  const insertSpecialCharacter = char => {
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

  if (error) {
    return <div className="text-red-500 text-center">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4 relative">
      {/* Language Toggle Buttons */}
      <div className="absolute top-0 right-0 space-x-2">
        <button
          onClick={toggleLanguage}
          className={`focus:outline-none p-1 rounded ${language === 'en' ? 'bg-blue-100' : ''}`}
          aria-label="Switch to English"
        >
          <img src="/united-kingdom-flag-icon.svg" alt="British flag" className="w-6 h-6" />
        </button>
        <button
          onClick={toggleLanguage}
          className={`focus:outline-none p-1 rounded ${language === 'tr' ? 'bg-red-100' : ''}`}
          aria-label="Türkçe'ye geç"
        >
          <img src="/turkey-flag-icon.svg" alt="Turkish flag" className="w-6 h-6" />
        </button>
      </div>

      <nav className="mb-4">
        <Link to="/" className="text-blue-500 hover:underline">
          &larr; {translations[language].backToConjugator}
        </Link>
      </nav>
      
      <h1 className="text-3xl font-bold mb-6 text-center">
        {translations[language].verbsListTitle}
      </h1>

      {/* Special Characters */}
      <div className="mb-4 flex justify-center space-x-2">
        {specialCharacters.map((char, index) => (
          <button
            key={index}
            className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400"
            onClick={() => insertSpecialCharacter(char)}
          >
            {char}
          </button>
        ))}
      </div>

      {/* Search Bar */}
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

      <VerbTable verbs={filteredVerbs} language={language} />
    </div>
  );
};

export default VerbList;