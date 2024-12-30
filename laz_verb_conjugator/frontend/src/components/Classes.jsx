import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Home } from 'lucide-react';
import { translations, getStoredLanguage, setStoredLanguage } from './constants';
import LanguageToggle from './ui/LanguageToggle';

const Classes = () => {
  const [language, setLanguage] = useState(getStoredLanguage());
  const t = translations[language].classTypes;
  
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
        {translations[language].classesTitle}
      </h1>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">{t.title}</h2>
        
        <div className="space-y-6">
          <div className="border-b pb-4">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              {t.individual.title}
            </h3>
            <div className="text-gray-700 mb-3 bg-blue-50 p-3 rounded whitespace-pre-line">
              {t.individual.schedule}
            </div>
            <p className="text-gray-600 mb-2">
              {t.individual.description}
            </p>
            <ul className="list-disc list-inside text-gray-600 ml-4">
              {t.individual.features.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
          </div>

          <div className="border-b pb-4">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              {t.group.title}
            </h3>
            <div className="text-gray-700 mb-3 bg-blue-50 p-3 rounded whitespace-pre-line">
              {t.group.schedule}
            </div>
            <p className="text-gray-600 mb-2">
              {t.group.description}
            </p>
            <ul className="list-disc list-inside text-gray-600 ml-4">
              {t.group.features.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
          </div>

          <div className="flex justify-center pt-4">
            <a            
              href="https://docs.google.com/forms/d/e/1FAIpQLSeK3GLB2ucNw758KtkRvOXcKsbBhdFUM1aU7TPosO2pFpj2GQ/viewform?usp=header"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xl py-4 px-8 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 shadow-lg"
            >
              {translations[language].signUpbutton}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Classes;