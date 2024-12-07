import React, { useState, useEffect } from 'react';
import { ToastContainer } from 'react-toastify';
import { Link, useLocation } from 'react-router-dom';
import 'react-toastify/dist/ReactToastify.css';

import Results from './Results';
import FeedbackForm from './FeedbackForm';
import FormSection from './FormSection';
import LanguageToggle from './ui/LanguageToggle';
import {
  API_URLS,
  translations,
  defaultFormData,
  getStoredLanguage,
  setStoredLanguage,
} from './constants';

const VerbConjugator = () => {
  const location = useLocation();
  const [language, setLanguage] = useState(getStoredLanguage());
  const [formData, setFormData] = useState(defaultFormData);
  const [results, setResults] = useState({ data: {}, error: '' });
  const [isFeedbackVisible, setFeedbackVisible] = useState(false);

  // Handle incoming verb from navigation
  useEffect(() => {
    if (location.state?.infinitive) {
      setFormData(prev => ({
        ...prev,
        infinitive: location.state.infinitive
      }));
      window.history.replaceState({}, document.title);
    }
  }, [location.state]);

  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
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
      const response = await fetch(`${API_URLS.conjugate}?${params.toString()}`);
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

  return (
    <div className="max-w-2xl mx-auto p-4">
      {/* Header section with language toggle */}
      <div className="flex justify-end mb-8 pt-2">
        <LanguageToggle language={language} onToggle={toggleLanguage} />
      </div>

      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
        style={{
          top: '1rem',
          right: '1rem',
        }}
      />
      
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
        {translations[language].title}
      </h1>

      <div className="text-center mb-4">
        <p className="text-gray-700 text-sm">
          {translations[language].verbListMessage}{' '}
          <Link to="/verbs" className="text-blue-500 hover:underline">
            {translations[language].verbListLinkText}
          </Link>
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <FormSection
          language={language}
          formData={formData}
          setFormData={setFormData}
          setResults={setResults}
          onSubmit={handleSubmit}
        />
      </form>

      <Results 
        results={results}
        language={language}
        translations={translations}
      />
      
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