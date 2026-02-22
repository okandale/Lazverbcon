import React, { useState, useEffect } from 'react';
import { ToastContainer } from 'react-toastify';
import { Link, useLocation } from 'react-router-dom';
import 'react-toastify/dist/ReactToastify.css';
import { Home } from 'lucide-react';

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

const DIALECT_KEYS = ['FA', 'PZ', 'HO', 'AŞ'];

function looksLikeDialectPayload(obj) {
  if (!obj || typeof obj !== 'object') return false;
  // Must contain at least one dialect key
  return DIALECT_KEYS.some((k) => Object.prototype.hasOwnProperty.call(obj, k));
}

function normalizeConjugationPayload(payload) {
  // Accept shapes:
  // A) { meta, result }                          <-- current backend (HAR)
  // B) { result: { ...dialects..., meta } }      <-- older messy backend
  // C) { ...dialects... }                        <-- very old backend
  // D) { result: { result: ...dialects... } }    <-- double-wrapped
  // Also accept error shapes:
  // { error: "..." } or { result: { error: "..." } }

  // If payload is null/undefined
  if (!payload) {
    return { data: {}, meta: null, error: 'Empty response from server.' };
  }

  // If server returns an explicit top-level error
  if (payload && typeof payload === 'object' && 'error' in payload) {
    return {
      data: {},
      meta: payload.meta ?? null,
      error: payload.error || 'Error fetching conjugations.',
    };
  }

  const meta = payload.meta ?? payload.result?.meta ?? null;

  // Candidate for "dialect object"
  let dataCandidate = null;

  // New/current: { meta, result: {FA, ...} }
  if (looksLikeDialectPayload(payload.result)) {
    dataCandidate = payload.result;
  }
  // Old: dialects at top-level
  else if (looksLikeDialectPayload(payload)) {
    dataCandidate = payload;
  }
  // Double-wrapped: { result: { result: {FA,...} } }
  else if (looksLikeDialectPayload(payload.result?.result)) {
    dataCandidate = payload.result.result;
  }
  // Sometimes: { result: {...} } where {...} isn't dialects but might be error
  else if (payload.result && typeof payload.result === 'object' && 'error' in payload.result) {
    return {
      data: {},
      meta,
      error: payload.result.error || 'Error fetching conjugations.',
    };
  }

  if (!dataCandidate || typeof dataCandidate !== 'object') {
    return { data: {}, meta, error: 'Unexpected response format from server.' };
  }

  // Strip meta if it got mixed into dialect keys object
  if ('meta' in dataCandidate) {
    // eslint-disable-next-line no-unused-vars
    const { meta: _ignore, ...rest } = dataCandidate;
    dataCandidate = rest;
  }

  // If no dialect keys after stripping
  if (!looksLikeDialectPayload(dataCandidate) || Object.keys(dataCandidate).length === 0) {
    return { data: {}, meta, error: 'No conjugations found for this verb.' };
  }

  return { data: dataCandidate, meta, error: '' };
}

const VerbConjugator = () => {
  const location = useLocation();
  const [language, setLanguage] = useState(getStoredLanguage());
  const [formData, setFormData] = useState(defaultFormData);

  // results.data = dialect object (FA/PZ/HO/AŞ)
  // results.meta = backend debug/meta
  // results.error = user-facing error
  const [results, setResults] = useState({ data: {}, meta: null, error: '' });

  const [isFeedbackVisible, setFeedbackVisible] = useState(false);

  // Handle incoming verb from navigation
  useEffect(() => {
    if (location.state?.infinitive) {
      setFormData((prev) => ({
        ...prev,
        infinitive: location.state.infinitive,
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
    setResults({ data: {}, meta: null, error: '' });

    const params = new URLSearchParams();
    Object.entries(formData).forEach(([key, value]) => {
      if (key === 'regions') {
        if (Array.isArray(value) && value.length > 0) {
          params.append('region', value.join(','));
        }
      } else if (typeof value === 'boolean') {
        params.append(key, value ? 'true' : 'false');
      } else if (value !== '' && value !== null && value !== undefined) {
        params.append(key, String(value));
      }
    });

    try {
      if (!API_URLS?.conjugate) {
        throw new Error("API_URLS.conjugate is missing/undefined");
      }

      const url = `${API_URLS.conjugate}?${params.toString()}`;
      console.log("Fetch URL:", url);

      const response = await fetch(url);

      const text = await response.text(); // always read as text first

      let payload = null;
      try {
        payload = JSON.parse(text);
      } catch {
        // not JSON
        if (!response.ok) {
          throw new Error(`HTTP ${response.status} non-JSON: ${text.slice(0, 300)}`);
        }
        throw new Error(`Backend returned non-JSON: ${text.slice(0, 300)}`);
      }

      // non-2xx
      if (!response.ok) {
        const msg = payload?.error || payload?.result?.error || `HTTP ${response.status}`;
        setResults({ data: {}, meta: payload?.meta ?? null, error: msg });
        return;
      }

      // normalize: expect {meta, result} but accept older shapes
      const meta = payload?.meta ?? payload?.result?.meta ?? null;
      let data =
        payload?.result?.FA ||
        payload?.result?.PZ ||
        payload?.result?.HO ||
        payload?.result?.["AŞ"]
          ? payload.result
          : (payload?.result?.result ?? payload?.result ?? payload);

      if (data && typeof data === 'object' && 'meta' in data) {
        const { meta: _ignore, ...rest } = data;
        data = rest;
      }

      if (!data || typeof data !== 'object' || Object.keys(data).length === 0) {
        setResults({ data: {}, meta, error: 'No conjugations found for this verb.' });
        return;
      }

      setResults({ data, meta, error: '' });
    } catch (err) {
      console.error("handleSubmit crashed:", err);
      setResults({
        data: {},
        meta: null,
        error: `Frontend error: ${err?.message ?? String(err)}`
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <div className="max-w-2xl mx-auto p-4">
        {/* Header section with language toggle */}
        <div className="flex justify-between items-center mb-8 pt-2">
          <Link to="/" className="text-gray-600 hover:text-gray-800">
            <Home size={24} />
          </Link>
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

        <Results results={results} language={language} translations={translations} />

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

        <div className="text-center mt-6">
          <p className="text-gray-700 text-sm italic">
            {translations[language].thankYouNote.prefix}
            <a
              href={translations[language].thankYouNote.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              {translations[language].thankYouNote.linkText}
            </a>
            {translations[language].thankYouNote.suffix}
          </p>
        </div>

        <FeedbackForm
          isVisible={isFeedbackVisible}
          onClose={() => setFeedbackVisible(false)}
          language={language}
          translations={translations}
        />
      </div>
    </div>
  );
};

export default VerbConjugator;