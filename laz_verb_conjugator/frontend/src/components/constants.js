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
    conjugate: 'Çek',
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
    conjugatorCard: {
      title: 'Fiil Çekimleyici',
      description: 'Lazca fiilleri tüm zaman ve kiplerde çekimleyin'
    },
    classesCard: {
      title: 'Lazca Dersleri',
      description: 'Deneyimli eğitmenlerle canlı çevrimiçi Lazca dersleri'
    },
    verbListCard: {
      title: 'Fiil Listesi',
      description: 'Kapsamlı Lazca fiil listesine göz atın'
    },
    patronCard: {
      title: 'Patreon\'da Destekleyin',
      description: 'Daha fazla Lazca öğrenme kaynağı oluşturmamıza yardımcı olun'
    },
    aboutTitle: 'Hakkımızda',
    aboutContent: {
      intro: 'Lazca Öğrenme Merkezi, Lazca öğrenmek isteyenlere yardımcı olmak için oluşturuldu. Araçlarımız, Lazcadaki karmaşık fiil çekim sistemini anlamanıza ve pratik yapmanıza olanak sağlar.',
      growth: 'Basit bir fiil çekim aracı olarak başlayan projemiz, Lazca öğrenenler için kapsamlı bir kaynağa dönüştü.',
      mission: 'Misyonumuz',
      missionText: 'Amacımız, kaliteli araçlar ve kaynaklar sunarak Lazca öğrenmeyi daha erişilebilir ve keyifli hale getirmektir.'
    },
    classesTitle: 'Lazca Dersler',
    classTypes: {
      title: 'Mevcut Ders Türleri',
      individual: {
        title: 'Birebir Dersler',
        description: 'Öğrenme stilinize ve hedeflerinize göre özelleştirilmiş eğitim',
        features: [
          'Esnek programlama',
          'Özelleştirilmiş müfredat',
          'Özel ihtiyaçlarınıza odaklanma'
        ]
      },
      group: {
        title: 'Grup Dersleri',
        description: 'İnteraktif bir ortamda başkalarıyla birlikte öğrenin',
        features: [
          'Küçük grup boyutları (4-6 öğrenci)',
          'Düzenli programlanmış oturumlar',
          'Akranlarla konuşma pratiği'
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
    conjugatorCard: {
      title: 'Verb Conjugator',
      description: 'Practice conjugating Laz verbs in all tenses and moods'
    },
    classesCard: {
      title: 'Laz Classes',
      description: 'Join live online Laz language classes with experienced tutors'
    },
    verbListCard: {
      title: 'Verb List',
      description: 'Browse our comprehensive list of Laz verbs'
    },
    patronCard: {
      title: 'Support on Patreon',
      description: 'Help us create more Laz language learning resources'
    },
    aboutTitle: 'About Us',
    aboutContent: {
      intro: 'The Laz Language Learning Center was created to help people learn Laz. Our tools make it easier to understand and practice the complex verb conjugation system in Laz.',
      growth: 'What started as a simple conjugation tool has grown into a comprehensive resource for Laz language learners.',
      mission: 'Our Mission',
      missionText: 'We aim to make Laz language learning more accessible and enjoyable by providing high-quality tools and resources.'
    },
    classesTitle: 'Laz Classes',
    classTypes: {
      title: 'Available Class Types',
      individual: {
        title: 'One-on-One Lessons',
        description: 'Personalized instruction tailored to your learning style and goals',
        features: [
          'Flexible scheduling',
          'Customized curriculum',
          'Focus on your specific needs'
        ]
      },
      group: {
        title: 'Group Classes',
        description: 'Learn with others in an interactive environment',
        features: [
          'Small group sizes (4-6 students)',
          'Regular scheduled sessions',
          'Practice speaking with peers'
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
