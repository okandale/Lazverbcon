import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { translations, getStoredLanguage, setStoredLanguage } from './constants';
import LanguageToggle from './ui/LanguageToggle';
import { Home } from 'lucide-react';

const dialects = [
  { key: 'pazar', nameEn: 'Pazar', nameTr: 'Pazar' },
  { key: 'ardesen', nameEn: 'Ardeşen', nameTr: 'Ardeşen' },
  { key: 'findikli-arhavi', nameEn: 'Fındıklı/Arhavi', nameTr: 'Fındıklı/Arhavi' },
  { key: 'hopa', nameEn: 'Hopa', nameTr: 'Hopa' },
];

const PhraseGuide = () => {
  const [language, setLanguage] = useState(getStoredLanguage());
  const localized = (en, tr) => (language === 'tr' ? tr : en);

  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  return (
    
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white px-4 py-8">
      <div className="max-w-3xl mx-auto">
        {/* Top bar with Home and language toggle */}
        <div className="flex justify-between items-center mb-8 pt-2">
          <Link to="/" className="text-gray-600 hover:text-gray-800">
            <Home size={24} />
          </Link>
          <LanguageToggle language={language} onToggle={toggleLanguage} />
        </div>

        {/* Page title */}
        <h1 className="text-4xl font-extrabold mb-8 text-gray-800 text-center">
          {localized('Phrase Guide', 'İfade Rehberi')}
        </h1>
        <p className="text-lg text-gray-700 mb-6 text-center">
          {localized(
            'Choose a dialect to see phrases specific to that region:',
            'Bölgeye özgü ifadeleri görmek için bir ağız seçin:'
          )}
        </p>
        <ul className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {dialects.map((dialect) => (
            <li key={dialect.key}>
              <Link
                to={`/resources/phrase-guide/${dialect.key}`}
                className="block bg-white rounded-xl shadow-md p-6 text-center text-xl font-semibold text-blue-700 hover:bg-blue-100 transition"
              >
                {localized(dialect.nameEn, dialect.nameTr)}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default PhraseGuide;

