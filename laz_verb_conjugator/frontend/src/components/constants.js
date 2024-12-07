export const API_URL = "/api/conjugate";

export const specialCharacters = ['ç̌', 't̆', 'ž', 'k̆', 'ʒ', 'ʒ̆', 'p̌'];

export const regionNames = {
  'AŞ': 'Ardeşen (Art̆aşeni)',
  'PZ': 'Pazar (Atina)',
  'FA': 'Fındıklı/Arhavi (Viʒ̆e/Ark̆abi)',
  'HO': 'Hopa (Xopa)',
  'FI': 'Fındıklı (Viʒ̆e)',
  'AR': 'Arhavi (Ark̆abi)',
  'ÇX': 'Çhala (Çxala)',
};

export const subjectOrder = [
  'ma', 'si', 'him', 'himuk', 'himus', 'heya', 'heyas', 'heyak',
  '(h)em', '(h)emus', '(h)emuk', 'şk̆u', 'çki', 'çku', 'çkin', 't̆k̆va', 'tkvan',
  'hini', 'hinik', 'hinis', 'tkva', 'hentepe', 'hentepes', 'hentepek',
  'entepe', 'entepes', 'entepek',
];

export const objectOrder = [
  'ma', 'si', 'him', 'himus', 'heya', 'heyas', '(h)em', '(h)emus', 'şk̆u', 'çki', 'çku', 'çkin',
  't̆k̆va', 'tkva', 'tkvan', 'hini', 'hinis', 'hentepe', 'hentepes', 'entepe', 'entepes'
];

export const API_URLS = {
  conjugate: "/api/conjugate",
  verbs: "/api/verbs"
};

// Language persistence helper functions
export const getStoredLanguage = () => {
  return localStorage.getItem('preferredLanguage') || 'en';
};

export const setStoredLanguage = (language) => {
  localStorage.setItem('preferredLanguage', language);
};

export const translations = {
  tr: {
    title: 'Fiil Çekimi',
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
    betaMessage: 'Hata görürseniz lütfen buradan görüşlerinizi iletin:',
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
    // Search placeholder
    searchPlaceholder: 'Fiil ara...',
    // Verb List translations
    backToConjugator: 'Fiil Çekicisine Geri Dön',
    verbsListTitle: 'Mevcut Fiiller',
  },
  // English translations
  en: {
    title: 'Verb Conjugator',
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
    betaMessage: 'If you spot a mistake, please submit your feedback using the',
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
  },
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