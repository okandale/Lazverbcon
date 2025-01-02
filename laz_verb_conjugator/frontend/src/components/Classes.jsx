import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Home, Clock, DollarSign } from 'lucide-react';
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
          {translations[language].classesTitle}
        </h1>
        
        {/* Main Content Card */}
        <div className="bg-white rounded-xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            {t.title}
          </h2>
          
          {/* Cost Information - New Addition */}
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-8 flex items-center">
            <DollarSign className="w-6 h-6 text-blue-500 mr-3 flex-shrink-0" />
            <p className="text-lg font-semibold text-blue-900">
              {t.cost}
            </p>
          </div>

          {/* Teacher Description */}
          <div className="pb-4 mb-8 border-b border-gray-300">
            <p className="text-gray-700 leading-relaxed italic">
              {t.teacherDescription}
            </p>
          </div>
          
          {/* Class Types */}
          <div className="space-y-8">
            
            {/* Individual Classes */}
            <div className="border-b pb-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
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
            
            {/* Group Classes */}
            <div className="border-b pb-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
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
            
            {/* Sign-Up Button */}
            <div className="flex justify-center pt-4">
              <a
                href="https://docs.google.com/forms/d/e/1FAIpQLSeK3GLB2ucNw758KtkRvOXcKsbBhdFUM1aU7TPosO2pFpj2GQ/viewform"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xl py-4 px-8 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 shadow-md"
              >
                {translations[language].signUpbutton}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Classes;