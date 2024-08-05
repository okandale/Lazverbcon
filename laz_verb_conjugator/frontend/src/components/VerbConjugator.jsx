import React, { useState, useEffect, useRef } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const VerbConjugator = () => {
  const defaultFormData = {
    infinitive: '',
    subject: 'all',
    obj: '',
    tense: 'present',
    aspect: '',
    applicative: false,
    causative: false,
    optative: false,
    regions: [],
  };

  const [formData, setFormData] = useState(defaultFormData);
  const [results, setResults] = useState({ data: {}, error: '' });
  const [showRegions, setShowRegions] = useState(false);
  const infinitiveInputRef = useRef(null);

  const specialCharacters = ['ç̌', 't̆', 'ž', 'k̆', 'ʒ', 'ʒ̆'];

  const regionNames = {
    'AŞ': 'Ardeşen (Art̆aşeni)',
    'PZ': 'Pazar (Atina)',
    'FA': 'Fındıklı/Arhavi (Viʒ̆e/Ark̆abi)',
    'HO': 'Hopa (Xopa)',
    'FI': 'Fındıklı (Viʒ̆e)',
    'AR': 'Arhavi (Ark̆abi)',
    'ÇX': 'Çhala (Çxala)'
    // Add other region codes and names here
  };

  useEffect(() => {
    updateFormState();
  }, [formData.optative, formData.applicative, formData.causative, formData.tense, formData.aspect]);

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
      }

      if (prevData.tense === 'presentperf') {
        newData.obj = '';
        if (newData.obj !== '') {
          setResults({ data: {}, error: 'Object is not applicable in present perfect tense.' });
        }
      }

      return newData;
    });
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleRegionChange = (e) => {
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
    setResults({ data: {}, error: '' }); // Clear previous results and error
    const params = new URLSearchParams();
    Object.entries(formData).forEach(([key, value]) => {
      if (key === 'regions') {
        if (value.length > 0) { // Ensure regions are only appended if they are not empty
          params.append('region', value.join(','));
        }
      } else if (typeof value === 'boolean') {
        params.append(key, value ? 'true' : 'false');
      } else {
        params.append(key, value);
      }
    });

    console.log(`/conjugate?${params.toString()}`); // Log the request URL for debugging

    try {
      const response = await fetch(`/conjugate?${params.toString()}`);
      
      if (!response.ok) {
        const errorData = await response.json();
        if (errorData.error === 'This verb cannot have an object.') {
          setResults({ data: {}, error: 'This verb cannot have an object.' });
        } else {
          setResults({ data: {}, error: errorData.error || 'This verb does not exist in our database.' });
        }
        return;
      }

      const data = await response.json();
      
      if (Object.keys(data).length === 0) {
        setResults({ data: {}, error: 'No conjugations found for this verb.' });
      } else {
        setResults({ data, error: '' });
      }
    } catch (error) {
      console.error('Error:', error);
      setResults({ data: {}, error: 'An error occurred while conjugating the verb. Please try again later.' });
    }
  };

  const handleReset = () => {
    setFormData(defaultFormData);
    setResults({ data: {}, error: '' });
  };

  const isAspectDisabled = formData.optative || formData.applicative;
  const isTenseDisabled = formData.optative;
  const isObjectDisabled = formData.aspect !== '' || formData.tense === 'presentperf';

  const insertSpecialCharacter = (char) => {
    if (infinitiveInputRef.current) {
      const input = infinitiveInputRef.current;
      const start = input.selectionStart;
      const end = input.selectionEnd;
      const text = input.value;
      const before = text.substring(0, start);
      const after = text.substring(end, text.length);
      input.value = (before + char + after);
      input.selectionStart = input.selectionEnd = start + char.length;
      input.focus();
      setFormData(prevData => ({
        ...prevData,
        infinitive: input.value
      }));
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <ToastContainer position="top-right" autoClose={5000} hideProgressBar={false} newestOnTop={false} closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">Verb Conjugator</h1>
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
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="infinitive">
            Infinitive:
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

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="subject">
              Subject:
            </label>
            <select
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="subject"
              name="subject"
              value={formData.subject}
              onChange={handleInputChange}
              required
            >
              <option value="S1_Singular">I</option>
              <option value="S2_Singular">You (singular)</option>
              <option value="S3_Singular">He/She/It</option>
              <option value="S1_Plural">We</option>
              <option value="S2_Plural">You (plural)</option>
              <option value="S3_Plural">They</option>
              <option value="all">All</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="obj">
              Object:
            </label>
            <select
              className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${isObjectDisabled ? 'text-gray-500 bg-gray-300' : ''}`}
              id="obj"
              name="obj"
              value={formData.obj}
              onChange={handleInputChange}
              disabled={isObjectDisabled}
            >
              <option value="">None</option>
              <option value="O1_Singular">Me</option>
              <option value="O2_Singular">You (singular)</option>
              <option value="O3_Singular">Him/Her/It</option>
              <option value="O1_Plural">Us</option>
              <option value="O2_Plural">You (plural)</option>
              <option value="O3_Singular">Them</option>
              <option value="all">All</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="tense">
              Tense:
            </label>
            <select
              className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${isTenseDisabled ? 'text-gray-500 bg-gray-300' : ''}`}
              id="tense"
              name="tense"
              value={formData.tense}
              onChange={handleInputChange}
              disabled={isTenseDisabled}
              required
            >
              <option value="present">Present</option>
              <option value="past">Past</option>
              <option value="future">Future</option>
              <option value="pastpro">Past Progressive</option>
              <option value="presentperf">Present Perfect</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="aspect">
              Aspect:
            </label>
            <select
              className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${isAspectDisabled ? 'text-gray-500 bg-gray-300' : ''}`}
              id="aspect"
              name="aspect"
              value={formData.aspect}
              onChange={handleInputChange}
              disabled={isAspectDisabled}
            >
              <option value="">None</option>
              <option value="potential">Potential</option>
              <option value="passive">Passive</option>
            </select>
          </div>
        </div>

        <fieldset className="mb-4 border border-gray-300 rounded p-3">
          <legend
            className="font-bold cursor-pointer"
            onClick={() => setShowRegions(!showRegions)}
          >
            Regions
          </legend>
          {showRegions && (
            <div className="grid grid-cols-2 gap-4">
              {[
                { code: 'AŞ', name: 'Ardeşen (AŞ)' },
                { code: 'FA', name: 'Fındıklı-Arhavi (FA)' },
                { code: 'HO', name: 'Hopa (HO)' },
                { code: 'PZ', name: 'Pazar (PZ)' },
              ].map((region) => (
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
          )}
        </fieldset>

        <div className="mb-4 flex items-center">
          <input
            type="checkbox"
            id="applicative"
            name="applicative"
            checked={formData.applicative}
            onChange={handleInputChange}
            className="mr-2"
          />
          <label className="text-gray-700 text-sm font-bold" htmlFor="applicative">
            Applicative
          </label>
        </div>

        <div className="mb-4 flex items-center">
          <input
            type="checkbox"
            id="causative"
            name="causative"
            checked={formData.causative}
            onChange={handleInputChange}
            className="mr-2"
          />
          <label className="text-gray-700 text-sm font-bold" htmlFor="causative">
            Causative
          </label>
        </div>

        <div className="mb-4 flex items-center">
          <input
            type="checkbox"
            id="optative"
            name="optative"
            checked={formData.optative}
            onChange={handleInputChange}
            className="mr-2"
          />
          <label className="text-gray-700 text-sm font-bold" htmlFor="optative">
            Optative
          </label>
        </div>

        <div className="flex justify-between">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
          >
            Conjugate
          </button>
          <button
            type="button"
            className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            onClick={handleReset}
          >
            Reset
          </button>
        </div>
      </form>

      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8">
        <h2 className="text-2xl font-bold mb-4">Results:</h2>
        {results.error ? (
          <p className="text-red-600">{results.error}</p>
        ) : (
          Object.entries(results.data).length > 0 ? (
            Object.entries(results.data).map(([region, forms]) => (
              <div key={region} className="mb-4">
                <h3 className="text-xl font-semibold text-blue-600">{regionNames[region] || region}</h3>
                {forms.map((form, index) => (
                  <p key={index} className="ml-4">{form}</p>
                ))}
              </div>
            ))
          ) : (
            <p>No results to display.</p>
          )
        )}
      </div>
    </div>
  );
};

export default VerbConjugator;
