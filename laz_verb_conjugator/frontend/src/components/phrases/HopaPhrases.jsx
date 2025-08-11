import { useState } from 'react';
import { Link } from 'react-router-dom';
import { getStoredLanguage, setStoredLanguage } from '../constants';
import LanguageToggle from '../ui/LanguageToggle';
import { Home } from 'lucide-react';
import { ChevronDown, ChevronUp } from 'lucide-react';

export default function HopaPhrases() {
  const [activeTab, setActiveTab] = useState('market');
  const [language, setLanguage] = useState(() => getStoredLanguage() || 'en');
  const [showTables, setShowTables] = useState({});

  const localized = (en, tr) => (language === 'tr' ? tr : en);

  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  const toggleTable = (phraseIndex) => {
    setShowTables(prev => ({
      ...prev,
      [`${activeTab}-${phraseIndex}`]: !prev[`${activeTab}-${phraseIndex}`]
    }));
  };

  const tabLabels = {
    market: { en: 'Market', tr: 'Market' },
    pharmacy: { en: 'Pharmacy', tr: 'Eczane' },
    restaurant: { en: 'Restaurant', tr: 'Restoran' },
    hotel: { en: 'Hotel', tr: 'Otel' }
  };

  const marketItems = [
    { english: 'Apple(s)', turkish: 'Elma', hopa: 'Uşkuri' },
    { english: 'Bread', turkish: 'Ekmek', hopa: 'Ǩovali' },
    { english: 'Water', turkish: 'su', hopa: 'Ǯǩari'},
    { english: 'Cheese', turkish: 'Peynir', hopa: 'Qvali'},
    { english: 'Egg(s)', turkish: 'Yumurta', hopa: 'Markvali'},
    { english: 'Milk', turkish: 'Süt', hopa: 'Bja'},
    { english: 'Chicken', turkish: 'Tavuk', hopa: 'Kotume'},
    { english: 'Fish', turkish: 'Balık', hopa: 'Çxomi'},
    { english: 'Anchovy', turkish: 'Hamsi', hopa: 'Kapça'},
    { english: 'Cucumber', turkish: 'Salatalık', hopa: 'Şuǩa'},
    { english: 'Tomato(es)', turkish: 'Domates', hopa: 'Ǩaǩa'},
    { english: 'Onion(s)', turkish: 'Soğan', hopa: 'Ǩromi'}
  ];

  const phraseCategories = {
    market: {
      title: localized('At the Market', 'Markette'),
      phrases: [
        { 
          english: 'How much is this?', 
          turkish: 'Bu ne kadar?', 
          hopa: 'İya naǩo lira ren?' 
        },
        { 
          english: 'Do you have ___?', 
          turkish: '____ var mı?', 
          hopa: '___ giğun-i?',
          table: marketItems
        }
      ]
    },
    pharmacy: {
      title: localized('At the Pharmacy', 'Eczanede'),
      phrases: [
        { 
          english: 'I need medicine for a headache', 
          turkish: 'Baş ağrısı için ilaç lazım', 
          hopa: 'Ti na maǯǩunen şeni ç̌ami domaç̌irs' 
        },
        {
          english: 'My stomach hurts',
          turkish: 'Karnım ağrıyor',
          hopa: 'Korba maǯǩunen'
        }
      ]
    },
    restaurant: {
      title: localized('At the Restaurant', 'Restoranda'),
      phrases: [
        { 
          english: 'I\'m vegetarian', 
          turkish: 'Ben vejetaryenim', 
          hopa: 'Ma vejetaryeni vore' 
        }
      ]
    },
    hotel: {
      title: localized('At the hotel', 'Otelde'),
      phrases: [
        { 
          english: 'Do you have any rooms available?', 
          turkish: 'Boş odanız var mı?', 
          hopa: 'Oda giğun-i?' 
        },
        {
          english: 'I have a reservation',
          turkish: 'Rezervasyonum var',
          hopa: 'Rezervasyoni komiğun'
        }
      ]
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white px-4 py-8">
      <div className="max-w-3xl mx-auto">
        {/* Top bar */}
        <div className="flex justify-between items-center mb-8 pt-2">
          <Link to="/" className="text-gray-600 hover:text-gray-800 transition-colors">
            <Home size={24} />
          </Link>
          <LanguageToggle language={language} onToggle={toggleLanguage} />
        </div>

        <div className="p-6 bg-white rounded-xl shadow-md">
          <h1 className="text-2xl font-bold mb-6 text-blue-800">
            {localized('Hopa Phrase Guide', 'Hopa İfade Rehberi')}
          </h1>
          
          {/* Tabs */}
          <div className="overflow-x-auto mb-8 border-b border-gray-200 pb-2">
            <div className="flex gap-4 w-max min-w-full">
              {Object.keys(tabLabels).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-2 rounded-t-lg transition-colors whitespace-nowrap ${
                    activeTab === tab
                      ? 'font-bold text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-600 hover:text-blue-500'
                  }`}
                >
                  {localized(tabLabels[tab].en, tabLabels[tab].tr)}
                </button>
              ))}
            </div>
          </div>

          {/* Phrases Section */}
          <div>
            <h2 className="text-xl font-semibold mb-4 text-gray-800">
              {phraseCategories[activeTab].title}
            </h2>
            
            <div className="space-y-4">
              {phraseCategories[activeTab].phrases.map((phrase, index) => {
                const tableKey = `${activeTab}-${index}`;
                const isTableVisible = showTables[tableKey];
                
                return (
                  <div 
                    key={index}
                    className="p-4 bg-gray-50 rounded-lg hover:bg-blue-50 transition-colors"
                  >
                    <div className="flex items-start mb-2">
                      <span className="text-2xl mr-3">🗣️</span>
                      <div>
                        <p className="font-medium text-gray-700">
                          {language === 'en' ? phrase.english : phrase.turkish}
                        </p>
                        <p className="text-sm text-gray-500 mt-1">
                          {language === 'en' ? `Turkish: ${phrase.turkish}` : `English: ${phrase.english}`}
                        </p>
                      </div>
                    </div>
                    <div className="pl-10">
                      <p className="font-sans font-bold text-blue-700 bg-blue-100 px-3 py-1 rounded inline-block">
                        {phrase.hopa}
                      </p>
                    </div>

                    {/* Collapsible Table */}
                    {phrase.table && (
                      <div className="mt-3 pl-10">
                        <button
                          onClick={() => toggleTable(index)}
                          className="flex items-center gap-1 text-blue-600 hover:text-blue-800 text-sm font-medium"
                        >
                          {isTableVisible
                            ? localized('Hide word list', 'Kelime listesini gizle')
                            : localized('Show word list', 'Kelime listesini göster')}
                          {isTableVisible ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                        </button>

                        {isTableVisible && (
                          <div className="mt-3 overflow-hidden rounded-lg border border-gray-300 shadow-sm">
                            <table className="w-full border-collapse">
                              <thead className="bg-blue-100">
                                <tr>
                                  <th className="p-2 text-left text-gray-700 font-semibold">
                                    {language === 'en' ? 'English' : 'Türkçe'}
                                  </th>
                                  <th className="p-2 text-left text-gray-700 font-semibold">Laz</th>
                                </tr>
                              </thead>
                              <tbody>
                                {phrase.table.map((item, idx) => (
                                  <tr
                                    key={idx}
                                    className={`${
                                      idx % 2 === 0 ? 'bg-white' : 'bg-blue-50'
                                    } hover:bg-blue-100 transition-colors`}
                                  >
                                    <td className="p-2">{language === 'en' ? item.english : item.turkish}</td>
                                    <td className="p-2 font-bold text-blue-800">{item.hopa}</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}