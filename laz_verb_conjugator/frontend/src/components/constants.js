const BASE_URL = import.meta.env.PROD 
  ? 'https://api.lazuri.org'
  : 'http://127.0.0.1:5000';

export const API_URLS = {
  conjugate: `${BASE_URL}/api/conjugate`,
};

export const specialCharacters = ['ç̌', 't̆', 'ž', 'ǩ', 'ʒ', 'ǯ', 'p̌'];

export const regionNames = {
  'AŞ': 'Ardeşen (Art̆aşeni)',
  'PZ': 'Pazar (Atina)',
  'FA': 'Fındıklı/Arhavi (Viǯe/Arǩabi)',
  'HO': 'Hopa (Xopa)',
  'FI': 'Fındıklı (Viǯe)',
  'AR': 'Arhavi (Arǩabi)',
  'ÇX': 'Çhala (Çxala)',
};

export const subjectOrder = [
  'ma', 'si', 'him', 'himuk', 'himus', 'heya', 'heyas', 'heyak',
  '(h)em', '(h)emus', '(h)emuk', 'şǩu', 'çki', 'çku', 'çkin', 't̆ǩva', 'tkvan',
  'hini', 'hinik', 'hinis', 'tkva', 'hentepe', 'hentepes', 'hentepek',
  'entepe', 'entepes', 'entepek',
];

export const objectOrder = [
  'ma', 'si', 'him', 'himus', 'heya', 'heyas', '(h)em', '(h)emus', 'şǩu', 'çki', 'çku', 'çkin',
  't̆ǩva', 'tkva', 'tkvan', 'hini', 'hinis', 'hentepe', 'hentepes', 'entepe', 'entepes'
];

// Language persistence helper functions
export const getStoredLanguage = () => {
  return localStorage.getItem('preferredLanguage') || 'en';
};

export const setStoredLanguage = (language) => {
  localStorage.setItem('preferredLanguage', language);
};

export const translations = {
  tr: {
    // Original translations
    title: 'Lazca Fiil Çekimleyici',
    infinitive: 'Mastar',
    subject: 'Özne',
    object: 'Nesne',
    tense: 'Zaman',
    aspect: 'Görünüş',
    regions: 'Bölgeler',
    applicative: 'Uygulamalı',
    imperative: 'Emir Kipi',
    causative: 'Ettirgen',
    negImperative: 'Olumsuz Emir',
    optative: 'İstek Kipi',
    conjugate: 'Çekimle',
    reset: 'Sıfırla',
    results: 'Sonuçlar',
    betaMessage: 'Bazı çekimler dilbilgisel olarak doğru olabilir ancak yaygın olarak kullanılmaz. Emin değilseniz, köyünüz için doğru çekimi öğrenmek adına büyüklerinize danışın. Hata görürseniz lütfen buradan görüşlerinizi iletin:',
    thankYouNote: {
      prefix: 'Bu projeye destek veren ',
      linkText: 'Laz Enstitüsü',
      suffix: ' için özel teşekkürler.',
      url: 'https://www.lazenstitu.com/'
    },
    feedbackLinkText: 'geri bildirim formu',
    feedbackTitle: 'Geri Bildirim Gönder',
    feedbackLabels: {
      incorrectWord: 'Yanlış Kelime(ler)',
      correction: 'Doğrusu',
      explanation: 'Açıklama',
      cancel: 'İptal',
      submit: 'Gönder',
    },
    verbListMessage: 'Mevcut fiillerin listesi için',
    verbListLinkText: 'buraya tıklayın',
    feedbackLoadingMessage: 'Geri bildirim gönderiliyor, lütfen bekleyin...',
    feedbackDisclaimer: 'Google Chrome kullanan telefon kullanıcıları formu göndermekte zorluk yaşayabilir; lütfen başka bir tarayıcı kullanın veya Gizli Modu kullanın.',
    searchPlaceholder: 'Fiil ara...',
    backToConjugator: 'Fiil Çekicisine Geri Dön',
    verbsListTitle: 'Mevcut Fiiller',

    // New translations for home and additional pages
    homeTitle: 'Lazca Öğrenme Merkezi',
    homeSubtitle: 'İnteraktif araçlar ve kaynaklarla Lazca öğrenin',
    navigation: {
      home: 'Ana Sayfa',
      conjugator: 'Fiil Çekimi',
      classes: 'Dersler',
      about: 'Hakkında',
      verbs: 'Fiiller'
    },
    info: 'Herhangi bir sorunuz veya talebiniz için lütfen info@lazuri.org adresine e-posta gönderin.',
    conjugatorCard: {
      title: 'Fiil Çekimleyici',
      description: 'Lazca fiilleri çoğu zaman ve kiplerde çekimleyin'
    },
    classesCard: {
      title: 'Lazca Atölyeler',
      description: 'Diğer öğrencilerle birlikte canlı çevrimiçi Lazca gruplarına katılın.'
    },
    keyboardCard: {
      title: 'Lazca Klavye',
      description: 'Lazca karakterleri nasıl yazacağınızı öğrenin'
    },
    verbListCard: {
      title: 'Fiil Listesi',
      description: 'Kapsamlı Lazca fiil listesine göz atın'
    },
    patronCard: {
      title: 'Bizi Destekleyin',
      description: 'Daha fazla Lazca öğrenme kaynağı oluşturmamıza yardımcı olun'
    },
    aboutTitle: 'Hakkımızda',
    aboutContent: {
      intro: 'Lazca Öğrenme Merkezi, Lazca öğrenmek isteyenlere yardımcı olmak için oluşturuldu. Araçlarımız, Lazcadaki karmaşık fiil çekim sistemini anlamanıza ve pratik yapmanıza olanak sağlar.',
      growth: 'Basit bir fiil çekim aracı olarak başlayan projemiz, Lazca öğrenenler için kapsamlı bir kaynağa dönüştü.',
      mission: 'Misyonumuz',
      missionText: 'Amacımız, kaliteli araçlar ve kaynaklar sunarak Lazca öğrenmeyi daha erişilebilir ve keyifli hale getirmektir.'
    },
    signUpbutton: 'Kayıt Ol',
    classesTitle: 'Lazca Atölyeler',
    classTypes: {
      title: 'Mevcut Atölyeler',
      teacherDescription: 'Modern Diller alanında Londra Üniversitesi Goldsmiths\'tan aldığım öğretmenlik diplomasıyla, Laz Enstitüsü\'nde onların öğrenci merkezli ve anlamlı ders metodolojilerini uyguladım. Yaklaşımım, miras öğrenenlere tehdit altındaki bir dili öğretmek için kültürel farkındalığı entegre eder ve mutlak başlangıç seviyesindeki öğrencilere bile etkili destek sağlar. Öğrenciler, oyunlu yöntemlerle dilbilgisi ve kelime dağarcığına tanıtılır ve öğrenme süreci boyunca aktif olarak katılmaları teşvik edilir. Herhangi bir sorunuz veya talebiniz için lütfen info@lazuri.org adresine e-posta gönderin.',
      cost: 'Tüm atölyeler ücretsizdir.',
      individual: {
        title: 'Başlangıç Seviye',
        schedule: '30 Ocak\'tan itibaren - Her hafta Çarşamba 20:00 - 21:00 saatleri arasında 12 hafta boyunca',
        description: 'Bu seviyede öğrenciler, temel selamlaşmalar, soru sorma, kendini tanıtma, ve sayılar gibi basit konularla iletişim kurmayı öğrenir. Yönelme, iyelik ve ergatif fiil yapıları ile temel dilbilgisi becerilerini geliştirmeleri amaçlanmaktadır. Dil bilgisi çok sınırlı olan öğrenciler için idealdir. Bu atölyede şunları öğreneceksiniz: ',
        features: [
          'Yönelme (datif) fiilleri',
          'iyelik (-şi)',
          'ergatif fiiller',
          'çoğul biçimleri',
          'temel sıfatlar',
          'Sayılar',
          'vücut bölümleri',
          'aile terimleri',
          'iyelik ekli basit cümleler'
        ]
      },
      group: {
        title: 'Üst Başlangıç Seviye',
        schedule: '2 Şubat\'tan itibaren - Her hafta Pazar 17:00 - 18:00 saatleri arasında 12 hafta boyunca',
        description: 'Bu seviyede öğrencilerin, geçmiş zaman, emir kipi ve şart-cümleleri kullanarak daha akıcı konuşmalar yapmaları, kıyafetler, yiyecekler, doğum günü ve coğrafya gibi konularda kendilerini ifade etmeleri hedeflenmektedir. Şehirde yön sorma ve hava durumu gibi günlük konularda daha rahat iletişim kurmaları beklenir. Bu atölyede şunları öğreneceksiniz:',
        features: [
          'Geçmiş zaman',
          'Çoğul (tekrarlama)',
          'Emir kipi',
          'Şart-sonuç cümleleri',
          'Ergatif fiillerin gelecek zamanı',
          'Kıyafetler',
          'Meyveler',
          'Doğum günü terimleri',
          'Coğrafya',
          'Hava durumu',
          'Şehirdeki binalar'
        ]
      }
    }
  },
  en: {
    // Original translations
    title: 'Laz Verb Conjugator',
    infinitive: 'Infinitive',
    subject: 'Subject',
    object: 'Object',
    tense: 'Tense',
    aspect: 'Aspect',
    regions: 'Regions',
    applicative: 'Applicative',
    imperative: 'Imperative',
    causative: 'Causative',
    negImperative: 'Negative Imperative',
    optative: 'Optative',
    conjugate: 'Conjugate',
    reset: 'Reset',
    results: 'Results',
    betaMessage: 'Some conjugations may be grammatically correct but are not commonly used. If you are unsure, please consult your elders to obtain the correct conjugation for your community. If you spot a mistake, please submit your feedback using the',
    thankYouNote: {
      prefix: 'Special thanks to the ',
      linkText: 'Laz Institute',
      suffix: ' for their support of this project.',
      url: 'https://www.lazenstitu.com/'
    },
    feedbackLinkText: 'feedback form',
    feedbackTitle: 'Submit Feedback',
    feedbackLabels: {
      incorrectWord: 'Incorrect Word(s)',
      correction: 'Correction',
      explanation: 'Explanation',
      cancel: 'Cancel',
      submit: 'Submit',
    },
    verbListMessage: 'See here for a',
    verbListLinkText: 'list of available verbs',
    feedbackLoadingMessage: 'Submitting...',
    feedbackDisclaimer: 'Phone users using Google Chrome may experience difficulties submitting the form; please use a different browser or use Incognito Mode.',
    searchPlaceholder: 'Search verbs...',
    backToConjugator: 'Back to Conjugator',
    verbsListTitle: 'Available Verbs',

    // New translations for home and additional pages
    homeTitle: 'Laz Language Learning Center',
    homeSubtitle: 'Learn Laz with interactive tools and resources',
    navigation: {
      home: 'Home',
      conjugator: 'Conjugator',
      classes: 'Classes',
      about: 'About',
      verbs: 'Verbs'
    },
    info: 'For any questions or inquiries, please email info@lazuri.org.',
    conjugatorCard: {
      title: 'Verb Conjugator',
      description: 'Practice conjugating Laz verbs in most tenses and moods.'
    },
    classesCard: {
      title: 'Laz Workshops',
      description: 'Join live online Laz language groups with other students.'
    },
    keyboardCard: {
      title: 'Laz Keyboard',
      description: 'Learn how to type Laz characters'
    },
    verbListCard: {
      title: 'Verb List',
      description: 'Browse our comprehensive list of Laz verbs.'
    },
    patronCard: {
      title: 'Support Us',
      description: 'Help us create more Laz language learning resources.'
    },
    aboutTitle: 'About Us',
    aboutContent: {
      intro: 'The Laz Language Learning Center was created to help people learn Laz. Our tools make it easier to understand and practice the complex verb conjugation system in Laz.',
      growth: 'What started as a simple conjugation tool has grown into a comprehensive resource for Laz language learners.',
      mission: 'Our Mission',
      missionText: 'We aim to make Laz language learning more accessible and enjoyable by providing high-quality tools and resources.'
    },
    signUpbutton: 'Sign Up',
    classesTitle: 'Laz Workshops',
    classTypes: {
      title: 'Available Workshops',
      teacherDescription: 'With a teaching degree in Modern Languages from Goldsmiths, University of London, I have applied their student-centered, meaningful lesson methodologies at the Laz Institute. My approach integrates cultural awareness to teach an endangered language to heritage learners, effectively supporting even absolute beginners. Students are introduced to grammar and vocabulary through playful methods and are encouraged to engage actively throughout the learning process. For any questions or inquiries, please email info@lazuri.org.',
      cost: 'All workshops are free of charge.',
      individual: {
        title: 'Beginner Groups',
        schedule: 'Starting January 30th - Weekly classes from 4:00 PM to 5:00 PM (UTC+3, Istanbul Time) for 12 weeks',
        description: 'At this level, students learn to communicate on simple topics such as basic greetings, asking questions, introducing themselves, and numbers. The aim is to develop basic grammar skills with structures like dative, possessive, and ergative verb forms. Ideal for students who have very limited knowledge of the language. In this workshop, you will learn:',
        features: [
          'Dative verbs',
          'Possessive (-şi)',
          'Ergative verbs',
          'Plural forms',
          'Basic adjectives',
          'Numbers',
          'Body parts',
          'Family terms',
          'Simple sentences with possessive suffixes'
          
        ]
      },
      group: {
        title: 'Upper Beginner Groups',
        description: 'At this level, students are expected to hold more fluent conversations using past tense, imperative mood, and conditional sentences. The goal is to express themselves on topics such as clothes, food, birthdays, and geography. They are also expected to communicate more comfortably on daily topics like asking for directions in the city and the weather.',
        schedule: 'Starting February 2nd Sunday from 5:00 PM - 6:00 PM, for 12 weeks.',
        features: [
          'Past tense',
          'Plural (repetition)',
          'Imperative mood',
          'Conditional-result sentences',
          'Future tense of ergative verbs',
          'Clothes',
          'Fruits',
          'Birthday terms',
          'Geography',
          'Weather',
          'Buildings in the city'
        ]
      }
    }
  }
};

export const defaultFormData = {
  infinitive: '',
  subject: 'all',
  obj: '',
  tense: 'present',
  aspect: '',
  applicative: false,
  causative: false,
  optative: false,
  imperative: false,
  neg_imperative: false,
  regions: [],
};
