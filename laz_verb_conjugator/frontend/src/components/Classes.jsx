import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Home, Clock, Video, DollarSign } from 'lucide-react';
import { getStoredLanguage, setStoredLanguage } from './constants';
import LanguageToggle from './ui/LanguageToggle';

const Classes = () => {
  const [language, setLanguage] = useState(getStoredLanguage() || 'en');
  const [showWorkshops, setShowWorkshops] = useState(false); // Global toggle for all workshops

  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  const localized = (en, tr) => (language === 'tr' ? tr : en);

  const workshops = [
    {
      id: 1,
      show: false, // Individual workshop visibility
      title: { en: 'Beginner Level', tr: 'Başlangıç Seviye' },
      schedule: { en: 'Starting Jan 29 - Wednesdays 20:00-21:00, 12 weeks', tr: '29 Ocak\'tan itibaren - Her hafta Çarşamba 20:00 - 21:00, 12 hafta' },
      platform: 'Zoom',
      description: {
        en: 'Students learn simple topics such as basic greetings, asking questions, introducing themselves, and numbers. Aimed at developing basic grammar skills including dative, possessive, and ergative forms. Ideal for students with very limited language knowledge.',
        tr: 'Bu seviyede öğrenciler, temel selamlaşmalar, soru sorma, kendini tanıtma ve sayılar gibi basit konularla iletişim kurmayı öğrenir. Yönelme, iyelik ve ergatif fiil yapıları ile temel dilbilgisi becerilerini geliştirmeleri amaçlanmaktadır. Dil bilgisi çok sınırlı olan öğrenciler için idealdir.'
      },
      points: [
        { en: 'Dative verbs', tr: 'Yönelme (datif) fiilleri' },
        { en: 'Possessive (-şi)', tr: 'iyelik (-şi)' },
        { en: 'Ergative verbs', tr: 'Ergatif fiiller' },
        { en: 'Plural forms', tr: 'Çoğul biçimleri' },
        { en: 'Basic adjectives', tr: 'Temel sıfatlar' },
        { en: 'Numbers', tr: 'Sayılar' },
        { en: 'Body parts', tr: 'Vücut bölümleri' },
        { en: 'Family terms', tr: 'Aile terimleri' },
        { en: 'Simple sentences with possessive', tr: 'İyelik ekli basit cümleler' }
      ]
    },
    {
      id: 2,
      show: false, // Individual workshop visibility
      title: { en: 'Upper Beginner Level', tr: 'Üst Başlangıç Seviye' },
      schedule: { en: 'Starting Feb 2 - Sundays 17:00-18:00, 12 weeks', tr: '2 Şubat\'tan itibaren - Her hafta Pazar 17:00 - 18:00, 12 hafta' },
      platform: 'Zoom',
      description: {
        en: 'Students aim to speak more fluently using past tense, imperative, and conditional sentences, expressing themselves on clothes, food, birthdays, and geography. Expected to communicate comfortably on daily topics like asking directions or weather.',
        tr: 'Bu seviyede öğrencilerin, geçmiş zaman, emir kipi ve şart-cümleleri kullanarak daha akıcı konuşmalar yapmaları, kıyafetler, yiyecekler, doğum günü ve coğrafya gibi konularda kendilerini ifade etmeleri hedeflenmektedir. Şehirde yön sorma ve hava durumu gibi günlük konularda daha rahat iletişim kurmaları beklenir.'
      },
      points: [
        { en: 'Past tense', tr: 'Geçmiş zaman' },
        { en: 'Plural repetition', tr: 'Çoğul (tekrarlama)' },
        { en: 'Imperative', tr: 'Emir kipi' },
        { en: 'Conditional sentences', tr: 'Şart-sonuç cümleleri' },
        { en: 'Future tense of ergative verbs', tr: 'Ergatif fiillerin gelecek zamanı' },
        { en: 'Clothes', tr: 'Kıyafetler' },
        { en: 'Fruits', tr: 'Meyveler' },
        { en: 'Birthday terms', tr: 'Doğum günü terimleri' },
        { en: 'Geography', tr: 'Coğrafya' },
        { en: 'Weather', tr: 'Hava durumu' },
        { en: 'Buildings in the city', tr: 'Şehirdeki binalar' }
      ]
    },
    {
      id: 3,
      show: true, // Individual workshop visibility
      title: { en: 'Beginner Workshops offered by the Laz Institute', tr: 'Laz Enstitüsü tarafından Başlangıç Atölyeleri' },
      schedule: { en: '5-week and 10-week workshops; registration forms will go live shortly', tr: '5 ve 10 haftalık atölyeler; kayıt formları yakında açılacak' },
      platform: { en: 'Zoom', tr: 'Zoom' },
      description: {
        en: 'The 5-week workshop is more introductory, focusing on basic phrases for everyday communication. The 10-week workshop covers simple topics such as greetings, questions, introducing yourself, numbers, and basic grammar structures like dative and ergative. Ideal for absolute beginners. Please email info@lazuri.org for questions.',
        tr: '5 haftalık atölye, günlük iletişim için temel ifadelere odaklanan daha giriş niteliğindedir. 10 haftalık atölye, temel selamlaşmalar, soru sorma, kendini tanıtma, sayılar ve yönelme ve ergatif gibi temel dilbilgisi yapıları gibi basit konuları kapsar. Mutlak başlangıç seviyesindeki öğrenciler için idealdir. Daha fazla bilgi için **[info@lazuri.org](mailto:info@lazuri.org)** adresine e-posta gönderin!'
      },
      points: [
        { en: '5-week introductory workshop: basic phrases', tr: '5 haftalık giriş atölyesi: temel ifadeler' },
        { en: '10-week workshop: simple topics & grammar', tr: '10 haftalık atölye: basit konular ve dilbilgisi' },
        { en: 'Focus on everyday communication', tr: 'Günlük iletişime odaklanır' },
        { en: 'Suitable for absolute beginners', tr: 'Yeni başlayanlar için uygundur' }
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Top bar */}
        <div className="flex justify-between items-center mb-8 pt-2">
          <Link to="/" className="text-gray-600 hover:text-gray-800 transition duration-300">
            <Home size={24} />
          </Link>
          <LanguageToggle language={language} onToggle={toggleLanguage} />
        </div>

        <h1 className="text-4xl font-extrabold mb-8 text-center text-gray-800 tracking-tight">
          {localized('Classes & Workshops', 'Dersler ve Atölyeler')}
        </h1>

        {/* Conditional Rendering */}
        {showWorkshops ? (
          <>
            {/* Render Workshops dynamically (only those with show: true) */}
            {workshops
              .filter(workshop => workshop.show)
              .map(workshop => (
                <div key={workshop.id} className="bg-white rounded-xl shadow-xl p-8 mb-8">
                  <h2 className="text-2xl font-bold text-gray-800 mb-6">
                    {localized(workshop.title.en, workshop.title.tr)}
                  </h2>

                  {/* Cost Information - Now inside each workshop card */}
                  <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6 flex items-center">
                    <DollarSign className="w-6 h-6 text-blue-500 mr-3 flex-shrink-0" />
                    <p className="text-lg font-semibold text-blue-900">
                      {localized('Free of charge', 'Ücretsiz')}
                    </p>
                  </div>

                  <div className="space-y-2 mb-3">
                    <div className="flex items-center gap-2">
                      <Clock className="w-5 h-5 text-gray-500 flex-shrink-0" />
                      <div className="bg-gray-100 p-3 rounded text-gray-700 w-full whitespace-pre-line font-medium">
                        {localized(workshop.schedule.en, workshop.schedule.tr)}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Video className="w-5 h-5 text-gray-500 flex-shrink-0" />
                      <div className="bg-gray-100 p-3 rounded text-gray-700 w-full font-medium">
                        {typeof workshop.platform === 'string' ? workshop.platform : localized(workshop.platform.en, workshop.platform.tr)}
                      </div>
                    </div>
                  </div>

                  <p className="text-gray-600 mb-2">
                    {localized(workshop.description.en, workshop.description.tr)}
                  </p>

                  <ul className="list-disc list-inside text-gray-600 ml-4 space-y-1">
                    {workshop.points.map((point, index) => (
                      <li key={index} className="font-medium">{localized(point.en, point.tr)}</li>
                    ))}
                  </ul>

                  <div className="flex justify-center pt-4">
                    <a
                      href="https://docs.google.com/forms/d/e/1FAIpQLSeK3GLB2ucNw758KtkRvOXcKsbBhdFUM1aU7TPosO2pFpj2GQ/viewform"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xl py-4 px-8 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 shadow-md"
                    >
                      {localized('Sign Up', 'Kayıt Ol')}
                    </a>
                  </div>
                </div>
              ))}
          </>
        ) : (
          // No Events Message (Bilingual)
          <div className="bg-white rounded-xl shadow-xl p-8 mb-8 text-center">
            <p className="text-gray-700 text-lg">
              {language === 'en' 
                ? 'No current events scheduled. If you are interested in hosting an event, please reach out to ' 
                : 'Şu anda planlanmış bir etkinlik bulunmamaktadır. Eğer bir etkinlik düzenlemek isterseniz, lütfen '}
              <a href="mailto:info@lazuri.org" className="text-blue-600 hover:text-blue-800">
                info@lazuri.org
              </a>
              {language === 'en' ? '.' : ' adresine e-posta gönderin.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Classes;