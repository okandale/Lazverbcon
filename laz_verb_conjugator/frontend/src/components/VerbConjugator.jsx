import React, { useState, useEffect, useRef } from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const API_URL = "https://laz-verb-conjugator-backend.onrender.com/api/conjugate";

const VerbConjugator = () => {
  const [language, setLanguage] = useState('en');
  const defaultFormData = {
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

  const [formData, setFormData] = useState(defaultFormData);
  const [results, setResults] = useState({ data: {}, error: '' });
  const [isLoading, setIsLoading] = useState(false); // Loading state
  const infinitiveInputRef = useRef(null);
  const [isFeedbackVisible, setFeedbackVisible] = useState(false);
  const [feedbackData, setFeedbackData] = useState({
    incorrectWord: '',
    correction: '',
    explanation: '',
  });

  const specialCharacters = ['ç̌', 't̆', 'ž', 'k̆', 'ʒ', 'ʒ̆', 'p̌'];

  const regionNames = {
    'AŞ': 'Ardeşen (Art̆aşeni)',
    'PZ': 'Pazar (Atina)',
    'FA': 'Fındıklı/Arhavi (Viʒ̆e/Ark̆abi)',
    'HO': 'Hopa (Xopa)',
    'FI': 'Fındıklı (Viʒ̆e)',
    'AR': 'Arhavi (Ark̆abi)',
    'ÇX': 'Çhala (Çxala)',
  };

  const subjectOrder = [
    'ma', 'si', 'him', 'himuk', 'himus', 'heya', 'heyas', 'heyak',
    'em/hem', 'emus/hemus', 'emuk/hemuk', 'şk̆u', 'çki', 'çku', 'çkin', 't̆k̆va','tkvan',
    'hini', 'hinik', 'hinis', 'tkva', 'hentepe', 'hentepes', 'hentepek',
    'entepe', 'entepes', 'entepek',
  ];
  const objectOrder = [
    'ma', 'si', 'him', 'heya', 'em/hem', 'şk̆u', 'çki', 'çku', 'çkin',
    't̆k̆va', 'tkva', 'tkvan', 'hini', 'hentepe', 'entepe',
  ];

  const translations = {
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
      betaMessage: 'Please submit your feedback using the',
      feedbackLinkText: 'feedback form',
      feedbackTitle: 'Submit Feedback',
      feedbackLabels: {
        incorrectWord: 'Incorrect Word(s)',
        correction: 'Correction',
        explanation: 'Explanation',
        cancel: 'Cancel',
        submit: 'Submit',
      },
      loadingMessage: 'Loading, please wait... (this may take up to 3 minutes)',
    },
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
      betaMessage: 'Lütfen geri bildirim formunu kullanarak görüşlerinizi iletin',
      feedbackLinkText: 'geri bildirim formu',
      feedbackTitle: 'Geri Bildirim Gönder',
      feedbackLabels: {
        incorrectWord: 'Yanlış Kelime(ler)',
        correction: 'Doğrusu',
        explanation: 'Açıklama',
        cancel: 'İptal',
        submit: 'Gönder',
      },
      loadingMessage: 'Yükleniyor, lütfen bekleyin... (bu işlem 3 dakika kadar sürebilir)',
    },
  };

  const firstInputRef = useRef(null);

  useEffect(() => {
    if (isFeedbackVisible && firstInputRef.current) {
      firstInputRef.current.focus();
    }
  }, [isFeedbackVisible]);

  const toggleLanguage = () => {
    setLanguage(prevLang => (prevLang === 'en' ? 'tr' : 'en'));
  };

  useEffect(() => {
    updateFormState();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    formData.optative,
    formData.applicative,
    formData.causative,
    formData.tense,
    formData.aspect,
    formData.imperative,
    formData.neg_imperative,
  ]);

  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        setFeedbackVisible(false);
      }
    };
  
    if (isFeedbackVisible) {
      document.addEventListener('keydown', handleEscape);
    } else {
      document.removeEventListener('keydown', handleEscape);
    }
  
    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isFeedbackVisible]);

  const updateFormState = () => {
    setFormData(prevData => {
      const newData = { ...prevData };

      if (prevData.optative) {
        newData.aspect = '';
        newData.tense = 'present';
        if (newData.aspect !== '' || newData.tense !== 'present') {
          setResults({ data: {}, error: 'Aspect and tense are not applicable when optative is selected.' });
        }
      }

      if (prevData.aspect !== '') {
        newData.obj = '';
        if (newData.obj !== '') {
          setResults({ data: {}, error: 'Object is not applicable when an aspect is selected.' });
        }
      } else if (prevData.tense === 'presentperf') {
        newData.obj = '';
        if (newData.obj !== '') {
          setResults({ data: {}, error: 'Object is not applicable in present perfect tense.' });
        }
      } else {
        newData.obj = prevData.obj;
      }

      if (prevData.imperative || prevData.neg_imperative) {
        newData.tense = 'present';
      }

      return newData;
    });
  };


  const handleFeedbackChange = (e) => {
    const { name, value } = e.target;
    setFeedbackData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Handle feedback form submission
  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    const scriptURL = 'https://script.google.com/macros/s/AKfycbwMoxTnwlccunb20qeYxt--0-GqHiGiLpTcKx0KVHMJwEi2uFCsNPv5mtQyw_QKbcwZ/exec'; // Your script URL
  
    try {
      const formData = new URLSearchParams();
      formData.append('incorrectWord', feedbackData.incorrectWord);
      formData.append('correction', feedbackData.correction);
      formData.append('explanation', feedbackData.explanation);
  
      await fetch(scriptURL, {
        method: 'POST',
        body: formData,
      });
  
      // Reset the form and close it
      setFeedbackData({
        incorrectWord: '',
        correction: '',
        explanation: '',
      });
      setFeedbackVisible(false);
  
      alert('Thank you for your feedback!');
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('There was an error submitting your feedback. Please try again later.');
    }
  };
  const handleInputChange = e => {
    const { name, value, type, checked } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleRegionChange = e => {
    const { value, checked } = e.target;
    setFormData(prevData => ({
      ...prevData,
      regions: checked
        ? [...prevData.regions, value]
        : prevData.regions.filter(region => region !== value),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResults({ data: {}, error: '' });
    setIsLoading(true); // Start loading

    const params = new URLSearchParams();
    Object.entries(formData).forEach(([key, value]) => {
      if (key === 'regions') {
        if (value.length > 0) {
          params.append('region', value.join(','));
        }
      } else if (typeof value === 'boolean') {
        params.append(key, value ? 'true' : 'false');
      } else if (value !== '') { // Exclude empty strings
        params.append(key, value);
      }
    });

    try {
      const response = await fetch(`${API_URL}?${params.toString()}`);
      const data = await response.json();

      if (!response.ok) {
        setResults({ data: {}, error: data.error || 'Error fetching conjugations.' });
        return;
      }

      if (Object.keys(data).length === 0) {
        setResults({ data: {}, error: 'No conjugations found for this verb.' });
      } else {
        setResults({ data, error: '' });
      }
    } catch (error) {
      setResults({
        data: {},
        error: 'An error occurred while fetching conjugation. Please try again.',
      });
    } finally {
      setIsLoading(false); // End loading
    }
  };
  const LoadingScreen = ({ message }) => (
    <div className="fixed inset-0 bg-white bg-opacity-80 flex flex-col items-center justify-center z-50">
      <svg className="animate-spin h-10 w-10 text-blue-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
      </svg>
      <p className="text-center text-lg">{message}</p>
    </div>
  );

  const handleReset = () => {
    setFormData(defaultFormData);
    setResults({ data: {}, error: '' });
  };

  const isAspectDisabled = formData.optative || formData.applicative || formData.obj;
  const isTenseDisabled = formData.optative || formData.imperative || formData.neg_imperative;
  const isObjectDisabled = formData.aspect !== '' || formData.tense === 'presentperf';

  const insertSpecialCharacter = char => {
    if (infinitiveInputRef.current) {
      const input = infinitiveInputRef.current;
      const start = input.selectionStart;
      const end = input.selectionEnd;
      const text = input.value;
      const before = text.substring(0, start);
      const after = text.substring(end, text.length);
      input.value = before + char + after;
      input.selectionStart = input.selectionEnd = start + char.length;
      input.focus();
      setFormData(prevData => ({
        ...prevData,
        infinitive: input.value,
      }));
    }
  };

  const sortForms = forms => {
    return forms.sort((a, b) => {
      const [prefixA] = a.split(':');
      const [prefixB] = b.split(':');
      const [subjectA, objectA] = prefixA.trim().split(' ');
      const [subjectB, objectB] = prefixB.trim().split(' ');

      const subjectCompare = subjectOrder.indexOf(subjectA) - subjectOrder.indexOf(subjectB);
      if (subjectCompare !== 0) return subjectCompare;

      return objectOrder.indexOf(objectA) - objectOrder.indexOf(objectB);
    });
  };

  const renderResults = () => {
    if (results.error) {
      return <p className="text-red-600">{results.error}</p>;
    }

    if (Object.entries(results.data).length === 0) {
      return <p>No results to display.</p>;
    }

    const regionOrder = ['AŞ', 'PZ', 'FA', 'HO'];

    return regionOrder
      .map(regionCode => {
        const region = Object.entries(results.data).find(([key]) => key === regionCode);
        if (!region) return null;

        const [regionName, forms] = region;
        return (
          <div key={regionName} className="mb-4">
            <h3 className="text-xl font-semibold text-blue-600">
              {regionNames[regionName] || regionName}
            </h3>
            {Array.isArray(forms) ? (
              sortForms(forms).map((form, index) => (
                <p key={index} className="ml-4">
                  {form}
                </p>
              ))
            ) : (
              <p>{forms}</p>
            )}
          </div>
        );
      })
      .filter(Boolean);
  };

  return (
    <div className="max-w-2xl mx-auto p-4 relative">
    {isLoading && (
      <LoadingScreen message={translations[language].loadingMessage} />
    )}

      {/* Language Toggle Buttons */}      
      <div className="absolute top-0 right-0 space-x-2">
        <button
          onClick={toggleLanguage}
          className={`focus:outline-none p-1 rounded ${language === 'en' ? 'bg-blue-100' : ''}`}
          aria-label="Switch to English"
        >
          <img src="/united-kingdom-flag-icon.svg" alt="British flag" className="w-6 h-6" />
        </button>
        <button
          onClick={toggleLanguage}
          className={`focus:outline-none p-1 rounded ${language === 'tr' ? 'bg-red-100' : ''}`}
          aria-label="Türkçe'ye geç"
        >
          <img src="/turkey-flag-icon.svg" alt="Turkish flag" className="w-6 h-6" />
        </button>
      </div>

      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
        <a 
          href="https://laz-verb-conjugator.onrender.com/" 
          target="_blank" 
          rel="noopener noreferrer" 
          className="hover:underline"
        >
          {translations[language].title}
        </a>
      </h1>
      <div className="mb-4 flex justify-center space-x-2">
        {specialCharacters.map((char, index) => (
          <button
            key={index}
            className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400"
            onClick={() => insertSpecialCharacter(char)}
          >
            {char}
          </button>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        {/* Infinitive Input */}
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="infinitive"
          >
            {translations[language].infinitive}:
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="infinitive"
            type="text"
            name="infinitive"
            value={formData.infinitive}
            onChange={handleInputChange}
            ref={infinitiveInputRef}
            required
          />
        </div>

        {/* Subject and Object Selectors */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          {/* Subject Selector */}
          <div>
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="subject"
            >
              {translations[language].subject}:
            </label>
            <select
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="subject"
              name="subject"
              value={formData.subject}
              onChange={handleInputChange}
              required
            >
              <option value="S1_Singular">{language === 'en' ? 'I' : 'Ben'}</option>
              <option value="S2_Singular">{language === 'en' ? 'You (singular)' : 'Sen'}</option>
              <option value="S3_Singular">{language === 'en' ? 'He/She/It' : 'O'}</option>
              <option value="S1_Plural">{language === 'en' ? 'We' : 'Biz'}</option>
              <option value="S2_Plural">{language === 'en' ? 'You (plural)' : 'Siz'}</option>
              <option value="S3_Plural">{language === 'en' ? 'They' : 'Onlar'}</option>
              <option value="all">{language === 'en' ? 'All' : 'Hepsi'}</option>
            </select>
          </div>

          {/* Object Selector */}
          <div>
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="obj"
            >
              {translations[language].object}:
            </label>
            <select
              className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
                isObjectDisabled ? 'text-gray-500 bg-gray-300' : ''
              }`}
              id="obj"
              name="obj"
              value={formData.obj}
              onChange={handleInputChange}
              disabled={isObjectDisabled}
            >
              <option value="">{language === 'en' ? 'None' : 'Yok'}</option>
              <option value="O1_Singular">{language === 'en' ? 'Me' : 'Beni'}</option>
              <option value="O2_Singular">{language === 'en' ? 'You (singular)' : 'Seni'}</option>
              <option value="O3_Singular">{language === 'en' ? 'Him/Her/It' : 'Onu'}</option>
              <option value="O1_Plural">{language === 'en' ? 'Us' : 'Bizi'}</option>
              <option value="O2_Plural">{language === 'en' ? 'You (plural)' : 'Sizi'}</option>
              <option value="O3_Plural">{language === 'en' ? 'Them' : 'Onları'}</option>
              <option value="all">{language === 'en' ? 'All' : 'Hepsi'}</option>
            </select>
          </div>

          {/* Tense Selector */}
          <div>
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="tense"
            >
              {translations[language].tense}:
            </label>
            <select
              className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
                isTenseDisabled ? 'text-gray-500 bg-gray-300' : ''
              }`}
              id="tense"
              name="tense"
              value={formData.tense}
              onChange={handleInputChange}
              disabled={isTenseDisabled}
              required
            >
              <option value="present">{language === 'en' ? 'Present' : 'Şimdiki Zaman'}</option>
              <option value="past">{language === 'en' ? 'Past' : 'Geçmiş Zaman'}</option>
              <option value="future">{language === 'en' ? 'Future' : 'Gelecek Zaman'}</option>
              <option value="pastpro">{language === 'en' ? 'Past Progressive' : 'Geçmişte Devam Eden'}</option>
              <option value="presentperf">{language === 'en' ? 'Present Perfect' : 'Yakın Geçmiş'}</option>
            </select>
          </div>

          {/* Aspect Selector */}
          <div>
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="aspect"
            >
              {translations[language].aspect}:
            </label>
            <select
              className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
                isAspectDisabled ? 'text-gray-500 bg-gray-300' : ''
              }`}
              id="aspect"
              name="aspect"
              value={formData.aspect}
              onChange={handleInputChange}
              disabled={isAspectDisabled}
            >
              <option value="">{language === 'en' ? 'None' : 'Yok'}</option>
              <option value="potential">{language === 'en' ? 'Potential' : 'Yeterlilik'}</option>
              <option value="passive">{language === 'en' ? 'Passive' : 'Edilgen'}</option>
            </select>
          </div>
        </div>

        {/* Regions Fieldset */}
        <fieldset className="mb-4 border border-gray-300 rounded p-3">
          <legend className="font-bold">
            {translations[language].regions}
          </legend>
          <div className="grid grid-cols-2 gap-4">
            {[
              { code: 'AŞ', name: 'Ardeşen (AŞ)' },
              { code: 'FA', name: 'Fındıklı-Arhavi (FA)' },
              { code: 'HO', name: 'Hopa (HO)' },
              { code: 'PZ', name: 'Pazar (PZ)' },
            ].map(region => (
              <label key={region.code} className="block">
                <input
                  type="checkbox"
                  name="regions"
                  value={region.code}
                  checked={formData.regions.includes(region.code)}
                  onChange={handleRegionChange}
                  className="mr-2"
                />
                {region.name}
              </label>
            ))}
          </div>
        </fieldset>

        {/* Checkbox Options */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          {/* Applicative */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="applicative"
              name="applicative"
              checked={formData.applicative}
              onChange={handleInputChange}
              className="mr-2"
            />
            <label className="text-gray-700 text-sm font-bold" htmlFor="applicative">
              {translations[language].applicative}
            </label>
          </div>

          {/* Imperative */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="imperative"
              name="imperative"
              checked={formData.imperative}
              onChange={handleInputChange}
              className="mr-2"
              disabled={formData.neg_imperative}
            />
            <label className="text-gray-700 text-sm font-bold" htmlFor="imperative">
              {translations[language].imperative}
            </label>
          </div>

          {/* Causative */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="causative"
              name="causative"
              checked={formData.causative}
              onChange={handleInputChange}
              className="mr-2"
            />
            <label className="text-gray-700 text-sm font-bold" htmlFor="causative">
              {translations[language].causative}
            </label>
          </div>

          {/* Negative Imperative */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="neg_imperative"
              name="neg_imperative"
              checked={formData.neg_imperative}
              onChange={handleInputChange}
              className="mr-2"
              disabled={formData.imperative}
            />
            <label className="text-gray-700 text-sm font-bold" htmlFor="neg_imperative">
              {translations[language].negImperative}
            </label>
          </div>

          {/* Optative */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="optative"
              name="optative"
              checked={formData.optative}
              onChange={handleInputChange}
              className="mr-2"
            />
            <label className="text-gray-700 text-sm font-bold" htmlFor="optative">
              {translations[language].optative}
            </label>
          </div>
        </div>

        {/* Submit and Reset Buttons */}
        <div className="flex justify-between">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
          >
            {translations[language].conjugate}
          </button>
          <button
            type="button"
            className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            onClick={handleReset}
          >
            {translations[language].reset}
          </button>
        </div>
      </form>

      {/* Results Section */}
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8">
        <h2 className="text-2xl font-bold mb-4">{translations[language].results}:</h2>
        {renderResults()}
      </div>
      
      {/* Updated Bottom Message with Feedback Link */}
      <div className="text-center mt-6">
        <p className="text-gray-700 text-sm">
          {translations[language].betaMessage}{' '}
          <button
            onClick={() => setFeedbackVisible(true)}
            className="text-blue-500 hover:underline"
          >
            {translations[language].feedbackLinkText}
          </button>
          .
        </p>
      </div>

      {/* Feedback Modal */}
      {isFeedbackVisible && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
          onClick={() => setFeedbackVisible(false)}
        >
          <div
            className="bg-white rounded-lg overflow-hidden shadow-xl max-w-md w-full mx-2"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="px-6 py-4">
              <h3 className="text-xl font-bold mb-4">
                {translations[language].feedbackTitle}
              </h3>
              <form onSubmit={handleFeedbackSubmit}>
                <div className="mb-3">
                  <label className="block text-gray-700 font-bold mb-1" htmlFor="incorrectWord">
                    {translations[language].feedbackLabels.incorrectWord}
                  </label>
                  <input
                    type="text"
                    name="incorrectWord"
                    value={feedbackData.incorrectWord}
                    onChange={handleFeedbackChange}
                    className="w-full border rounded px-2 py-1"
                    required
                    ref={firstInputRef}
                  />
                </div>
                <div className="mb-3">
                  <label className="block text-gray-700 font-bold mb-1" htmlFor="correction">
                    {translations[language].feedbackLabels.correction}
                  </label>
                  <input
                    type="text"
                    name="correction"
                    value={feedbackData.correction}
                    onChange={handleFeedbackChange}
                    className="w-full border rounded px-2 py-1"
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="block text-gray-700 font-bold mb-1" htmlFor="explanation">
                    {translations[language].feedbackLabels.explanation}
                  </label>
                  <textarea
                    name="explanation"
                    value={feedbackData.explanation}
                    onChange={handleFeedbackChange}
                    className="w-full border rounded px-2 py-1"
                    rows="4"
                  ></textarea>
                </div>
                <div className="flex justify-end space-x-2">
                  <button
                    type="button"
                    onClick={() => setFeedbackVisible(false)}
                    className="px-4 py-2 bg-gray-300 rounded"
                  >
                    {translations[language].feedbackLabels.cancel}
                  </button>
                  <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">
                    {translations[language].feedbackLabels.submit}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VerbConjugator;
