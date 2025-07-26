import { useState } from 'react';
import { Link } from 'react-router-dom';
import { getStoredLanguage, setStoredLanguage } from '../constants';
import LanguageToggle from '../ui/LanguageToggle';
import { Home } from 'lucide-react';

export default function HopaPhrases() {
  const [activeTab, setActiveTab] = useState('market');
  const [language, setLanguage] = useState('en');
  
  const localized = (en, tr) => (language === 'tr' ? tr : en);

  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
  };
  const tabLabels = {
    market: { en: 'Market', tr: 'Market' },
    pharmacy: { en: 'Pharmacy', tr: 'Eczane' },
    restaurant: { en: 'Restaurant', tr: 'Restoran' },
    hotel: { en: 'Hotel', tr: 'Otel' }
  };

  // Phrase data organized by category
  const phraseCategories = {
    market: {
      title: localized('At the Market', 'Markette'),
      phrases: [
        { 
          english: 'How much is this?', 
          turkish: 'Bu ne kadar?', 
          hopa: 'İya naǩo lira ren?' 
        },
        // Add more phrases here
      ]
    },
    pharmacy: {
      title: localized('At the Pharmacy', 'Eczanede'),
      phrases: [
        { 
          english: 'I need medicine for a headache', 
          turkish: 'Baş ağrısı için ilaç lazım', 
          hopa: 'Ham ǯǩuna şeni ç̌ami domaç̌irs' 
        },
        {
          english: 'My stomach hurts',
          turkish: 'Karnım ağrıyor',
          hopa: 'Korba maǯǩunen'
        },        // Add more phrases here
      ]
    },
    restaurant: {
      title: localized('At the Restaurant', 'Restoranda'),
      phrases: [
        { 
          english: 'I\'m vegetarian', 
          turkish: 'Ben vejetaryenim', 
          hopa: 'Ma vejetaryeni vore' 
        },
        // Add more phrases here
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
        // Add more phrases here
      ]
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white px-4 py-8">
      <div className="max-w-3xl mx-auto">
        {/* Top bar with Home and language toggle */}
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
              {['market', 'pharmacy', 'restaurant', 'hotel'].map((tab) => (
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
              {phraseCategories[activeTab].phrases.map((phrase, index) => (
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
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}