import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Home } from 'lucide-react';
import { translations, getStoredLanguage, setStoredLanguage } from './constants';
import LanguageToggle from './ui/LanguageToggle';

const Keyboard = () => {
  const [language, setLanguage] = useState(getStoredLanguage());
  const t = translations[language].keyboardContent;

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
          {translations[language].keyboardCard.title}
        </h1>

        {/* Main Content */}
        <div className="bg-white rounded-xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            {t.howToDownload}
          </h2>
          
          <ul className="space-y-4 mb-8">
            <li>
              <Link to="/keyboard/windows" className="text-blue-600 hover:text-blue-800">
                {t.platforms.windows}
              </Link>
            </li>
            <li>
              <Link to="/keyboard/mac" className="text-blue-600 hover:text-blue-800">
                {t.platforms.mac}
              </Link>
            </li>
            <li>
              <Link to="/keyboard/android" className="text-blue-600 hover:text-blue-800">
                {t.platforms.android}
              </Link>
            </li>
            <li>
              <Link to="/keyboard/iphone" className="text-blue-600 hover:text-blue-800">
                {t.platforms.iphone}
              </Link>
            </li>
          </ul>

          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            {t.howToUse}
          </h2>
          
          <ul className="space-y-4">
            <li>
              <Link to="/keyboard/computer" className="text-blue-600 hover:text-blue-800">
                {t.platforms.computer}
              </Link>
            </li>
            <li>
              <Link to="/keyboard/phone" className="text-blue-600 hover:text-blue-800">
                {t.platforms.phone}
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Keyboard;