import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Home } from 'lucide-react';
import LanguageToggle from './ui/LanguageToggle';
import { translations, getStoredLanguage, setStoredLanguage } from './constants';

const HomePage = () => {
  const [language, setLanguage] = useState(getStoredLanguage());
  const t = translations[language];
  
  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="flex justify-end items-center mb-8 pt-2">
        <LanguageToggle language={language} onToggle={toggleLanguage} />
      </div>

      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          {t.homeTitle}
        </h1>
        <p className="text-xl text-gray-600">
          {t.homeSubtitle}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
        <Link 
          to="/conjugator" 
          className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-3">
            {t.conjugatorCard.title}
          </h2>
          <p className="text-gray-600">
            {t.conjugatorCard.description}
          </p>
        </Link>

        <Link 
          to="/classes" 
          className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-3">
            {t.classesCard.title}
          </h2>
          <p className="text-gray-600">
            {t.classesCard.description}
          </p>
        </Link>

        <Link 
          to="/verbs" 
          className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-3">
            {t.verbListCard.title}
          </h2>
          <p className="text-gray-600">
            {t.verbListCard.description}
          </p>
        </Link>

        <a 
          href="https://www.patreon.com/" 
          target="_blank" 
          rel="noopener noreferrer"
          className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-3">
            {t.patronCard.title}
          </h2>
          <p className="text-gray-600">
            {t.patronCard.description}
          </p>
        </a>
      </div>
    </div>
  );
};

export default HomePage;