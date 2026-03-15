import React from 'react';

const VerbToolTabs = ({ activeTab, onTabChange, language }) => {
  const localized = (en, tr) => (language === 'tr' ? tr : en);

  const tabs = [
    {
      key: 'conjugator',
      label: localized('Conjugator', 'Fiil Çekimi'),
    },
    {
      key: 'reverse',
      label: localized('Form Lookup', 'Biçim Arama'),
    },
  ];

  return (
    <div className="mb-6 overflow-x-auto border-b border-gray-200 pb-2">
      <div className="flex gap-4 w-max min-w-full">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            type="button"
            onClick={() => onTabChange(tab.key)}
            className={`px-4 py-2 rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.key
                ? 'font-bold text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-blue-500'
            }`}
            aria-selected={activeTab === tab.key}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default VerbToolTabs;