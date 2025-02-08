import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Home } from 'lucide-react';
import { translations, getStoredLanguage, setStoredLanguage } from './constants';
import LanguageToggle from './ui/LanguageToggle';

const Resources = () => {
  const [language, setLanguage] = useState(getStoredLanguage());
  const t = translations[language].resourceContent;

  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* Top Bar (Home link + Language Toggle) */}
        <div className="flex justify-between items-center mb-8 pt-2">
          <Link 
            to="/" 
            className="text-gray-600 hover:text-gray-800 transition duration-300"
          >
            <Home size={24} />
          </Link>
          <LanguageToggle language={language} onToggle={toggleLanguage} />
        </div>

        {/* Page Title */}
        <h1 className="text-4xl font-extrabold mb-8 text-center text-gray-800 tracking-tight">
          {translations[language].resourceCard.title}
        </h1>

        {/* Resources Section */}
        <div className="bg-white rounded-xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            {t.dictionariesTitle}
          </h2>

          {/* Laz Institute's Dictionary */}
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              {t.lazInstituteDictionary.title}
            </h3>
            <p className="text-gray-600 mb-4">
              {t.lazInstituteDictionary.description}
            </p>
            <a
              href="https://www.lazcasozluk.org/#/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800"
            >
              {t.lazInstituteDictionary.linkText}
            </a>
          </div>

          {/* Lazca.xyz Dictionary */}
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              {t.lazcaXyzDictionary.title}
            </h3>
            <p className="text-gray-600 mb-4">
              {t.lazcaXyzDictionary.description}
            </p>
            <a
              href="https://lazca.xyz/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800"
            >
              {t.lazcaXyzDictionary.linkText}
            </a>
          </div>

          {/* General Information Section */}
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            {t.generalInformationTitle}
          </h2>

          {/* The Laz Institute */}
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              {t.lazInstitute.title}
            </h3>
            <p className="text-gray-600 mb-4">
              {t.lazInstitute.description}
            </p>
            <a
              href="https://www.lazenstitu.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800"
            >
              {t.lazInstitute.linkText}
            </a>
          </div>
        </div>

        {/* Call to Action */}
        <div className="bg-white rounded-xl shadow-xl p-8 text-center">
          <p className="text-gray-700 text-lg">
            {t.callToAction}{' '}
            <a href="mailto:info@lazuri.org" className="text-blue-600 hover:text-blue-800">
              info@lazuri.org
            </a>
            .
          </p>
        </div>
      </div>
    </div>
  );
};

export default Resources;