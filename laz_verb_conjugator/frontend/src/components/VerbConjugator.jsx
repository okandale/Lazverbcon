import React, { useState, useEffect, useRef } from 'react';
import { ToastContainer } from 'react-toastify';
import { Link, useLocation } from 'react-router-dom';
import 'react-toastify/dist/ReactToastify.css';
import { Home } from 'lucide-react';
import VerbToolTabs from './shared/VerbToolTabs';
import Results from './conjugator/Results';
import FeedbackForm from './FeedbackForm';
import FormSection from './conjugator/FormSection';
import LanguageToggle from './ui/LanguageToggle';
import SpecialCharacterBar from './shared/SpecialCharacterBar';
import ReverseSearchSection from './reverseSearch/ReverseSearchSection';
import ReverseSearchResults from './reverseSearch/ReverseSearchResults';
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
  return DIALECT_KEYS.some((k) => Object.prototype.hasOwnProperty.call(obj, k));
}

function normalizeConjugationPayload(payload) {
  if (!payload) {
    return { data: {}, meta: null, error: 'Empty response from server.' };
  }

  if (payload && typeof payload === 'object' && 'error' in payload) {
    return {
      data: {},
      meta: payload.meta ?? null,
      error: payload.error || 'Error fetching conjugations.',
    };
  }



  const meta = payload.meta ?? payload.result?.meta ?? null;
  let dataCandidate = null;

  if (looksLikeDialectPayload(payload.result)) {
    dataCandidate = payload.result;
  } else if (looksLikeDialectPayload(payload)) {
    dataCandidate = payload;
  } else if (looksLikeDialectPayload(payload.result?.result)) {
    dataCandidate = payload.result.result;
  } else if (
    payload.result &&
    typeof payload.result === 'object' &&
    'error' in payload.result
  ) {
    return {
      data: {},
      meta,
      error: payload.result.error || 'Error fetching conjugations.',
    };
  }

  if (!dataCandidate || typeof dataCandidate !== 'object') {
    return { data: {}, meta, error: 'Unexpected response format from server.' };
  }

  if ('meta' in dataCandidate) {
    const { meta: _ignore, ...rest } = dataCandidate;
    dataCandidate = rest;
  }

  if (!looksLikeDialectPayload(dataCandidate) || Object.keys(dataCandidate).length === 0) {
    return { data: {}, meta, error: 'No conjugations found for this verb.' };
  }

  return { data: dataCandidate, meta, error: '' };
}

const VerbConjugator = () => {
  const location = useLocation();
  const [language, setLanguage] = useState(getStoredLanguage());
  const [formData, setFormData] = useState(defaultFormData);
  const [results, setResults] = useState({ data: {}, meta: null, error: '' });
  const [isFeedbackVisible, setFeedbackVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('conjugator');
  const infinitiveInputRef = useRef(null);
  const reverseSearchInputRef = useRef(null);
  const [reverseQuery, setReverseQuery] = useState('');
  const [isReverseSearching, setIsReverseSearching] = useState(false);
  const [reverseResults, setReverseResults] = useState([]);
  const [hasReverseSearched, setHasReverseSearched] = useState(false);
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


  const handleReverseSearchSubmit = async (e) => {
    e.preventDefault();
    setIsReverseSearching(true);
    setHasReverseSearched(true);
    setReverseResults([]);

    try {
      const spelling = reverseQuery.trim();

      if (!spelling) {
        setReverseResults([]);
        return;
      }
      if (!API_URLS?.reverse) {
        throw new Error('API_URLS.reverse is missing/undefined');
      }

      const url = `${API_URLS.reverse}?spelling=${encodeURIComponent(spelling)}`;
      console.log('Reverse fetch URL:', url);

      const response = await fetch(url);
      const text = await response.text();

      let payload = null;
      try {
        payload = JSON.parse(text);
      } catch {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status} non-JSON: ${text.slice(0, 300)}`);
        }
        throw new Error(`Backend returned non-JSON: ${text.slice(0, 300)}`);
      }

      if (!response.ok) {
        throw new Error(payload?.error || `HTTP ${response.status}`);
      }

      const matches = Array.isArray(payload?.matches) ? payload.matches : [];
      setReverseResults(matches);
    } catch (err) {
      console.error('handleReverseSearchSubmit crashed:', err);
      setReverseResults([]);
    } finally {
      setIsReverseSearching(false);
    }
  };
  const handleSpecialCharClick = (char) => {
    if (activeTab === 'reverse') {
      const input = reverseSearchInputRef.current;
      if (!input) return;

      const start = input.selectionStart ?? input.value.length;
      const end = input.selectionEnd ?? input.value.length;
      const text = input.value ?? '';
      const newValue = text.slice(0, start) + char + text.slice(end);

      setReverseQuery(newValue);

      requestAnimationFrame(() => {
        input.focus();
        input.setSelectionRange(start + char.length, start + char.length);
      });

      return;
    }

    const input = infinitiveInputRef.current;
    if (!input) return;

    const start = input.selectionStart ?? input.value.length;
    const end = input.selectionEnd ?? input.value.length;
    const text = input.value ?? '';
    const newValue = text.slice(0, start) + char + text.slice(end);

    setFormData((prev) => ({
      ...prev,
      infinitive: newValue,
    }));

    requestAnimationFrame(() => {
      input.focus();
      input.setSelectionRange(start + char.length, start + char.length);
    });
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
        throw new Error('API_URLS.conjugate is missing/undefined');
      }

      const url = `${API_URLS.conjugate}?${params.toString()}`;
      console.log('Fetch URL:', url);

      const response = await fetch(url);
      const text = await response.text();

      let payload = null;
      try {
        payload = JSON.parse(text);
      } catch {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status} non-JSON: ${text.slice(0, 300)}`);
        }
        throw new Error(`Backend returned non-JSON: ${text.slice(0, 300)}`);
      }

      if (!response.ok) {
        const msg = payload?.error || payload?.result?.error || `HTTP ${response.status}`;
        setResults({ data: {}, meta: payload?.meta ?? null, error: msg });
        return;
      }

      const normalized = normalizeConjugationPayload(payload);
      setResults(normalized);
    } catch (err) {
      console.error('handleSubmit crashed:', err);
      setResults({
        data: {},
        meta: null,
        error: `Frontend error: ${err?.message ?? String(err)}`,
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <div className="max-w-2xl mx-auto p-4">
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
        <VerbToolTabs
          activeTab={activeTab}
          onTabChange={setActiveTab}
          language={language}
        />
        <SpecialCharacterBar onCharClick={handleSpecialCharClick} />

        {activeTab === 'conjugator' ? (
          <>
            <form onSubmit={handleSubmit}>
              <FormSection
                language={language}
                formData={formData}
                setFormData={setFormData}
                setResults={setResults}
                infinitiveInputRef={infinitiveInputRef}
              />
            </form>

            <Results
              results={results}
              language={language}
              translations={translations}
              selectedObject={formData.obj}
            />
          </>
        ) : (
          <>
            <ReverseSearchSection
              language={language}
              reverseQuery={reverseQuery}
              setReverseQuery={setReverseQuery}
              onSubmit={handleReverseSearchSubmit}
              isSearching={isReverseSearching}
              inputRef={reverseSearchInputRef}
            />

            <ReverseSearchResults
              language={language}
              results={reverseResults}
              isSearching={isReverseSearching}
              hasSearched={hasReverseSearched}
              onOpenInConjugator={(result) => {
                const mood = result.mood || 'indicative';
                const derivation = result.derivation || 'none';

                setActiveTab('conjugator');
                setFormData((prev) => ({
                  ...prev,
                  infinitive: result.infinitive || prev.infinitive,
                  tense: result.tense || prev.tense,
                  subject: result.subject_code || prev.subject,
                  obj: result.object_code || '',

                  aspect:
                    derivation === 'passive' || derivation === 'potential'
                      ? derivation
                      : '',

                  optative: mood === 'optative',
                  imperative: mood === 'imperative',
                  neg_imperative: mood === 'neg_imperative',

                  applicative: !!result.is_applicative,
                  simple_causative: !!result.is_causative,
                  causative: !!result.is_double_causative,
                }));

                setResults({ data: {}, meta: null, error: '' });
              }}
            />
          </>
        )}

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