import React, { useState, useEffect, useRef } from 'react';
import { ToastContainer } from 'react-toastify';
import { Link } from 'react-router-dom';
import 'react-toastify/dist/ReactToastify.css';

import Results from './Results';
import FeedbackForm from './FeedbackForm';
import {
  API_URL,
  specialCharacters,
  translations,
  defaultFormData
} from './constants';

const VerbConjugator = () => {
  const [language, setLanguage] = useState('en');
  const [formData, setFormData] = useState(defaultFormData);
  const [results, setResults] = useState({ data: {}, error: '' });
  const [isFeedbackVisible, setFeedbackVisible] = useState(false);
  const infinitiveInputRef = useRef(null);

  useEffect(() => {
    updateFormState();
  }, [
    formData.optative,
    formData.applicative,
    formData.causative,
    formData.tense,
    formData.aspect,
    formData.imperative,
    formData.neg_imperative,
  ]);

  const toggleLanguage = () => {
    setLanguage(prevLang => (prevLang === 'en' ? 'tr' : 'en'));
  };

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

    const params = new URLSearchParams();
    Object.entries(formData).forEach(([key, value]) => {
      if (key === 'regions') {
        if (value.length > 0) {
          params.append('region', value.join(','));
        }
      } else if (typeof value === 'boolean') {
        params.append(key, value ? 'true' : 'false');
      } else if (value !== '') {
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
    }
  };
  
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

  return (
    <div className="max-w-2xl mx-auto p-4 relative">
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

      <ToastContainer />
      
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

      <div className="text-center mb-4">
        <p className="text-gray-700 text-sm">
          {translations[language].verbListMessage}{' '}
          <Link to="/verbs" className="text-blue-500 hover:underline">
            {translations[language].verbListLinkText}
          </Link>
          .
        </p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        {/* Infinitive Input */}
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="infinitive">
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
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="subject">
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
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="obj">
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
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="tense">
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
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="aspect">
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
          <legend className="font-bold">{translations[language].regions}</legend>
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
      <Results 
        results={results}
        language={language}
        translations={translations}
      />
      
      {/* Bottom Message with Feedback Link */}
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

      {/* Feedback Form */}
      <FeedbackForm
        isVisible={isFeedbackVisible}
        onClose={() => setFeedbackVisible(false)}
        language={language}
        translations={translations}
      />
    </div>
  );
};

export default VerbConjugator;