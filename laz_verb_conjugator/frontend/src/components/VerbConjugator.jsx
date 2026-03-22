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

const FEEDBACK_TEXT = {
  en: {
    betaMessage:
      'The website is still in beta. Some forms may be grammatically correct but not commonly used, so we encourage you to check with elders in your community.',
    feedbackLinkText: 'feedback form',
    emailText: 'You can report any errors via the',
    emailSuffix: 'or email me at',
  },
  tr: {
    betaMessage:
      'Web sitesi hâlâ beta aşamasındadır. Bazı biçimler doğru olsa da yaygın kullanılmayabilir; bu yüzden topluluğunuzdaki büyüklerle teyit etmeniz önerilir.',
    feedbackLinkText: 'geri bildirim formu',
    emailText: 'Karşılaştığınız hataları',
    emailSuffix: 'üzerinden bildirebilir ya da bana şu adresten e-posta gönderebilirsiniz:',
  },
};

const CREDIT_TEXT = {
  en: {
    prefix: 'Special thanks to the ',
    lazInstituteText: 'Laz Institute',
    middle: ' and ',
    panglotText: 'Panglot',
    suffix: ' for their support.',
  },
  tr: {
    prefix: 'Destekleri için ',
    lazInstituteText: 'Laz Enstitüsü',
    middle: ' ve ',
    panglotText: 'Panglot',
    suffix: '’a özel teşekkürler.',
  },
};

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

  const [reverseQuery, setReverseQuery] = useState('');
  const [isReverseSearching, setIsReverseSearching] = useState(false);
  const [reverseResults, setReverseResults] = useState([]);
  const [reverseMeta, setReverseMeta] = useState({
    query: '',
    matchType: 'none',
  });
  const [hasReverseSearched, setHasReverseSearched] = useState(false);
  const [reverseSuggestions, setReverseSuggestions] = useState([]);
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightedSuggestionIndex, setHighlightedSuggestionIndex] = useState(-1);

  const infinitiveInputRef = useRef(null);
  const reverseSearchInputRef = useRef(null);
  const skipNextSuggestionFetch = useRef(false);
  const suppressSuggestionsRef = useRef(false);
  const reverseLookupAbortRef = useRef(null);

  useEffect(() => {
    if (location.state?.infinitive) {
      setFormData((prev) => ({
        ...prev,
        infinitive: location.state.infinitive,
      }));
      window.history.replaceState({}, document.title);
    }
  }, [location.state]);

  useEffect(() => {
    if (skipNextSuggestionFetch.current) {
      skipNextSuggestionFetch.current = false;
      return;
    }

    const query = reverseQuery.trim();

    if (!query) {
      setReverseSuggestions([]);
      setShowSuggestions(false);
      setHighlightedSuggestionIndex(-1);
      return;
    }

    const controller = new AbortController();

    const timeout = setTimeout(async () => {
      try {
        setIsLoadingSuggestions(true);

        const response = await fetch(
          `${API_URLS.reverse}/suggestions?q=${encodeURIComponent(query)}`,
          { signal: controller.signal }
        );

        const payload = await response.json();
        const suggestions = Array.isArray(payload?.suggestions) ? payload.suggestions : [];

        setReverseSuggestions(suggestions);

        if (!suppressSuggestionsRef.current) {
          setShowSuggestions(suggestions.length > 0);
        }

        setHighlightedSuggestionIndex(-1);
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Suggestion fetch failed:', err);
          setReverseSuggestions([]);
          setShowSuggestions(false);
        }
      } finally {
        setIsLoadingSuggestions(false);
      }
    }, 200);

    return () => {
      clearTimeout(timeout);
      controller.abort();
    };
  }, [reverseQuery]);

  const toggleLanguage = () => {
    const newLanguage = language === 'en' ? 'tr' : 'en';
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  const handleReverseSearchSubmit = async (e) => {
    e.preventDefault();

    suppressSuggestionsRef.current = true;
    setShowSuggestions(false);
    setHighlightedSuggestionIndex(-1);

    const spelling = reverseQuery.trim();

    if (!spelling) {
      setReverseResults([]);
      setReverseMeta({
        query: '',
        matchType: 'none',
      });
      setHasReverseSearched(false);
      setIsReverseSearching(false);
      return;
    }

    if (reverseLookupAbortRef.current) {
      reverseLookupAbortRef.current.abort();
    }

    const controller = new AbortController();
    reverseLookupAbortRef.current = controller;

    setIsReverseSearching(true);
    setHasReverseSearched(true);
    setReverseMeta({
      query: '',
      matchType: 'none',
    });

    try {
      if (!API_URLS?.reverse) {
        throw new Error('API_URLS.reverse is missing/undefined');
      }

      const url = `${API_URLS.reverse}?spelling=${encodeURIComponent(spelling)}`;
      console.log('Reverse fetch URL:', url);

      const response = await fetch(url, { signal: controller.signal });
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
      setReverseMeta({
        query: payload?.query || spelling,
        matchType:
          payload?.match_type ||
          (matches.length ? matches[0]?.match_type || 'exact' : 'none'),
      });
    } catch (err) {
      if (err.name === 'AbortError') {
        return;
      }

      console.error('handleReverseSearchSubmit crashed:', err);
      setReverseResults([]);
      setReverseMeta({
        query: spelling,
        matchType: 'none',
      });
    } finally {
      if (reverseLookupAbortRef.current === controller) {
        reverseLookupAbortRef.current = null;
      }
      setIsReverseSearching(false);
    }
  };

  const handleReverseReset = () => {
    if (reverseLookupAbortRef.current) {
      reverseLookupAbortRef.current.abort();
      reverseLookupAbortRef.current = null;
    }

    suppressSuggestionsRef.current = false;
    skipNextSuggestionFetch.current = true;

    setReverseQuery('');
    setReverseResults([]);
    setReverseMeta({
      query: '',
      matchType: 'none',
    });
    setHasReverseSearched(false);
    setIsReverseSearching(false);
    setReverseSuggestions([]);
    setIsLoadingSuggestions(false);
    setShowSuggestions(false);
    setHighlightedSuggestionIndex(-1);

    requestAnimationFrame(() => {
      reverseSearchInputRef.current?.focus();
    });
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
              onReset={handleReverseReset}
              isSearching={isReverseSearching}
              inputRef={reverseSearchInputRef}
              suggestions={reverseSuggestions}
              isLoadingSuggestions={isLoadingSuggestions}
              showSuggestions={showSuggestions}
              setShowSuggestions={setShowSuggestions}
              highlightedSuggestionIndex={highlightedSuggestionIndex}
              setHighlightedSuggestionIndex={setHighlightedSuggestionIndex}
              skipNextSuggestionFetch={skipNextSuggestionFetch}
              suppressSuggestionsRef={suppressSuggestionsRef}
            />

            <ReverseSearchResults
              language={language}
              results={reverseResults}
              isSearching={isReverseSearching}
              hasSearched={hasReverseSearched}
              meta={reverseMeta}
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
            {FEEDBACK_TEXT[language].betaMessage}{' '}
            {FEEDBACK_TEXT[language].emailText}{' '}
            <button
              onClick={() => setFeedbackVisible(true)}
              className="text-blue-500 hover:underline"
              type="button"
            >
              {FEEDBACK_TEXT[language].feedbackLinkText}
            </button>{' '}
            {FEEDBACK_TEXT[language].emailSuffix}{' '}
            <a
              href="mailto:info@lazuri.org"
              className="text-blue-500 hover:underline"
            >
              info@lazuri.org
            </a>
            .
          </p>
        </div>

        <div className="text-center mt-6">
          <p className="text-gray-700 text-sm italic">
            {CREDIT_TEXT[language].prefix}
            <a
              href="https://lazuri.org/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              {CREDIT_TEXT[language].lazInstituteText}
            </a>
            {CREDIT_TEXT[language].middle}
            <a
              href="https://panglot.app/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              {CREDIT_TEXT[language].panglotText}
            </a>
            {CREDIT_TEXT[language].suffix}
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