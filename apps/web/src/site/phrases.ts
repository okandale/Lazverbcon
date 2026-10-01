// Transcribed from https://lazuri.org/resources/phrase-guide/hopa on 2026-09-29.
// Laz spelling is preserved. Only obvious English/Turkish typos were corrected.
import { text } from "./shared";
export const categories = {
  market: text("At the market", "Markette"),
  pharmacy: text("At the pharmacy", "Eczanede"),
  restaurant: text("At the restaurant", "Restoranda"),
  hotel: text("At the hotel", "Otelde"),
};
export type Category = keyof typeof categories;
export type Phrase = {
  en: string;
  tr: string;
  laz: string | null;
  vocabulary?: boolean;
};
export const phrases: Record<Category, Phrase[]> = {
  market: [
    { en: "How much is this?", tr: "Bu ne kadar?", laz: "İya muǩos ren?" },
    {
      en: "Do you have ___?",
      tr: "____ var mı?",
      laz: "___ giğun-i?",
      vocabulary: true,
    },
    {
      en: "I would like a kilo of apples",
      tr: "Bir kilo elma istiyorum",
      laz: "Ar kilo uşkiri minon?",
    },
    { en: "I am just looking", tr: "Sadece bakıyorum", laz: "xvala viǯǩer" },
    {
      en: "I would like to buy two loaves of bread",
      tr: "İki ekmek almak istiyorum",
      laz: "Jur kuvali yeç̌opinu minon",
    },
    { en: "Thank you!", tr: "Teşekkür ederim!", laz: "Gogixta/Sağolasen!" },
  ],
  pharmacy: [
    {
      en: "I need medicine for a headache",
      tr: "Baş ağrısı için ilaç lazım",
      laz: "Tiş ǯǩuni şeni ç̌ami minon",
    },
    { en: "My stomach hurts", tr: "Karnım ağrıyor", laz: "Korba mǯǩups" },
    {
      en: "I need something for a cough",
      tr: "Öksürük için bir şey lazım",
      laz: "Oxvalu şeni ç̌ami minon",
    },
    { en: "I have a fever", tr: "Ateşim var", laz: "Daçxiri madven" },
    {
      en: "Can I get this without a prescription?",
      tr: "Bunu reçetesiz alabilir miyim?",
      laz: "İya ureçeteli yemaç̌opinen-i?",
    },
  ],
  restaurant: [
    {
      en: "I’m vegetarian",
      tr: "Ben vejetaryenim",
      laz: "Ma vejetaryeni vore",
    },
    {
      en: "I am allergic to _____",
      tr: "___ye alerjim var",
      laz: "___ alerji miğun/maǯqens",
    },
    {
      en: "Can I have the menu please?",
      tr: "Menü alabilir miyim?",
      laz: "Menu momçat̆iǩon iqven-i??",
    },
    {
      en: "What do you recommend?",
      tr: "Ne tavsiye edersiniz?",
      laz: "Mu tavsiye moğodap?",
    },
    {
      en: "I would like this dish",
      tr: "Bu yemeği istiyorum",
      laz: "Aya gyari minon",
    },
    { en: "Please, no salt", tr: "Lütfen tuzsuz", laz: "Umcumeli (r)t̆as" },
    {
      en: "Can we have the bill, please?",
      tr: "Hesabı alabilir miyiz?",
      laz: "Xesabi komomiği(t)",
    },
  ],
  hotel: [
    {
      en: "Do you have any rooms available?",
      tr: "Boş odanız var mı?",
      laz: "Oda giğunan-i?",
    },
    {
      en: "I have a reservation",
      tr: "Rezervasyonum var",
      laz: "Rezervasyoni komiğun",
    },
    {
      en: "How much is a room per night?",
      tr: "Oda gecelik ne kadar?",
      laz: "Oda ar seris muǩo liras didginen?",
    },
    {
      en: "Is breakfast included?",
      tr: "Kahvaltı dahil mi?",
      laz: "Gyaobaşi/Ç̌umaneri gyari niçen-i?",
    },
    {
      en: "Can I see the room first?",
      tr: "Önce odayı görebilir miyim?",
      laz: "Oda ǯoxleşen mažiren-i?",
    },
    {
      en: "Can I check out late?",
      tr: "Geç çıkış yapabilir miyim?",
      laz: "Yano gamumalen-i?",
    },
  ],
};
export const vocabulary = [
  { en: "Apple(s)", tr: "Elma", laz: "Uşkiri" },
  { en: "Bread", tr: "Ekmek", laz: "Kuvali" },
  { en: "Water", tr: "Su", laz: "Ǯǩari" },
  { en: "Cheese", tr: "Peynir", laz: "Qvali" },
  { en: "Egg(s)", tr: "Yumurta", laz: "Makvali" },
  { en: "Milk", tr: "Süt", laz: "Mja" },
  { en: "Chicken", tr: "Tavuk", laz: "Kotume" },
  { en: "Fish", tr: "Balık", laz: "Çxomi" },
  { en: "Anchovy", tr: "Hamsi", laz: "Kapşiya" },
  { en: "Cucumber", tr: "Salatalık", laz: "Şuǩa" },
  { en: "Tomato(es)", tr: "Domates", laz: "Domatisi/Ǩaǩa" },
  { en: "Onion(s)", tr: "Soğan", laz: "Ǩromi" },
];

// Live Pazar, Ardeşen and Fındıklı–Arhavi guides checked on 2026-10-01.
// Each had these three English prompts and literal "..." translations, with no hotel tab.
// Keep independent data per dialect so authors can fill each guide separately.
function unfinishedGuide(): Partial<Record<Category, Phrase[]>> {
  return {
    market: [{ en: "How much is this?", tr: "Bu ne kadar?", laz: null }],
    pharmacy: [
      {
        en: "I need medicine for a headache",
        tr: "Baş ağrısı için ilaç lazım",
        laz: null,
      },
    ],
    restaurant: [{ en: "I’m vegetarian", tr: "Ben vejetaryenim", laz: null }],
  };
}
export const draftGuides: Record<
  string,
  Partial<Record<Category, Phrase[]>>
> = {
  pazar: unfinishedGuide(),
  ardesen: unfinishedGuide(),
  "findikli-arhavi": unfinishedGuide(),
};
