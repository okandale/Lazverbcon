import React, { useState } from 'react';
import { translations, getStoredLanguage, setStoredLanguage } from './constants';

const About = () => {
  const [language, setLanguage] = useState(getStoredLanguage());
  const t = translations[language].aboutContent;
  
  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };
  
  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="flex justify-between items-center mb-8 pt-2">
        <Link to="/" className="text-gray-600 hover:text-gray-800">
          <Home size={24} />
        </Link>
        <LanguageToggle language={language} onToggle={toggleLanguage} />
      </div>
      <h1 className="text-3xl font-bold mb-8 text-center text-gray-800">
        {translations[language].aboutTitle}
      </h1>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="prose max-w-none">
          <p className="text-gray-600 mb-4">
            {t.intro}
          </p>
          
          <p className="text-gray-600 mb-4">
            {t.growth}
          </p>
          
          <h2 className="text-2xl font-bold text-gray-800 my-4">
            {t.mission}
          </h2>
          <p className="text-gray-600 mb-4">
            {t.missionText}
          </p>
        </div>
      </div>
    </div>
  );
};

export default About;