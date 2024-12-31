import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Home, Clock } from 'lucide-react';
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
            <h3 className="text-xl font-bold text-gray-800 mb-2">
              {t.individual.title}
            </h3>
            <div className="flex items-center gap-2 mb-3">
              <Clock className="w-5 h-5 text-gray-500 flex-shrink-0" />
              <div className="bg-gray-100 p-3 rounded text-gray-700 w-full whitespace-pre-line font-medium">
                {t.individual.schedule}
              </div>
            </div>
            <p className="text-gray-600 mb-2">
              {t.individual.description}
            </p>
            <ul className="list-disc list-inside text-gray-600 ml-4 space-y-1">
              {t.individual.features.map((feature, index) => (
                <li key={index} className="font-medium">{feature}</li>
              ))}
            </ul>
          </div>

          <div className="border-b pb-4">
            <h3 className="text-xl font-bold text-gray-800 mb-2">
              {t.group.title}
            </h3>
            <div className="flex items-center gap-2 mb-3">
              <Clock className="w-5 h-5 text-gray-500 flex-shrink-0" />
              <div className="bg-gray-100 p-3 rounded text-gray-700 w-full whitespace-pre-line font-medium">
                {t.group.schedule}
              </div>
            </div>
            <p className="text-gray-600 mb-2">
              {t.group.description}
            </p>
            <ul className="list-disc list-inside text-gray-600 ml-4 space-y-1">
              {t.group.features.map((feature, index) => (
                <li key={index} className="font-medium">{feature}</li>
              ))}
            </ul>
          </div>

          <div className="flex justify-center pt-4">
            <a            
              href="https://docs.google.com/forms/d/e/1FAIpQLSeK3GLB2ucNw758KtkRvOXcKsbBhdFUM1aU7TPosO2pFpj2GQ/viewform"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xl py-4 px-8 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 shadow-lg"
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