import React from 'react';

const LanguageToggle = ({ language, onToggle }) => {
  return (
    <div className="flex gap-2">
      <button
        onClick={onToggle}
        className={`flex items-center justify-center p-2 rounded-lg transition-all duration-200
                   ${language === 'en' 
                     ? 'bg-blue-100 ring-2 ring-blue-300' 
                     : 'hover:bg-gray-100'}`}
        aria-label="Switch to English"
      >
        <img 
          src="/united-kingdom-flag-icon.svg" 
          alt="British flag" 
          className="w-7 h-7"
        />
      </button>
      <button
        onClick={onToggle}
        className={`flex items-center justify-center p-2 rounded-lg transition-all duration-200
                   ${language === 'tr' 
                     ? 'bg-red-100 ring-2 ring-red-300' 
                     : 'hover:bg-gray-100'}`}
        aria-label="Türkçe'ye geç"
      >
        <img 
          src="/turkey-flag-icon.svg" 
          alt="Turkish flag" 
          className="w-7 h-7"
        />
      </button>
    </div>
  );
};

export default LanguageToggle;