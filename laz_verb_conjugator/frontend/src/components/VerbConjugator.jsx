import React, { useState, useEffect } from 'react';

const VerbConjugator = () => {
  const [formData, setFormData] = useState({
    infinitive: '',
    subject: 'S1_Singular',
    obj: '',
    tense: 'present',
    aspect: '',
    applicative: false,
    causative: false,
    optative: false,
    regions: [],
  });
  const [results, setResults] = useState({});
  const [showRegions, setShowRegions] = useState(false);

  useEffect(() => {
    updateFormState();
  }, [formData.optative, formData.applicative, formData.causative, formData.tense, formData.aspect]);

  const updateFormState = () => {
    setFormData(prevData => ({
      ...prevData,
      aspect: (prevData.optative || prevData.applicative || prevData.causative) ? '' : prevData.aspect,
      tense: prevData.optative ? 'present' : prevData.tense,
      obj: prevData.aspect !== '' ? '' : prevData.obj,
    }));
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
    const params = new URLSearchParams();
    Object.entries(formData).forEach(([key, value]) => {
      if (key === 'regions') {
        params.append('region', value.join(','));
      } else if (typeof value === 'boolean') {
        params.append(key, value ? 'true' : 'false');
      } else {
        params.append(key, value);
      }
    });

    try {
      const response = await fetch(`/conjugate?${params.toString()}`);
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">Verb Conjugator</h1>
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
            required
          />
        </div>
        
        {/* Add similar input fields for subject, obj, tense, aspect */}
        
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Regions:
          </label>
          <div className="bg-gray-100 p-2 rounded">
            <button
              type="button"
              className="text-blue-500 hover:text-blue-700"
              onClick={() => setShowRegions(!showRegions)}
            >
              {showRegions ? 'Hide Regions' : 'Show Regions'}
            </button>
            {showRegions && (
              <div className="mt-2">
                {['AŞ', 'FA', 'HO', 'PZ'].map((region) => (
                  <label key={region} className="block">
                    <input
                      type="checkbox"
                      name="regions"
                      value={region}
                      checked={formData.regions.includes(region)}
                      onChange={handleRegionChange}
                      className="mr-2"
                    />
                    {region}
                  </label>
                ))}
              </div>
            )}
          </div>
        </div>
        
        {/* Add checkboxes for applicative, causative, optative */}
        
        <div className="flex items-center justify-between">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
          >
            Conjugate
          </button>
        </div>
      </form>

      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8">
        <h2 className="text-2xl font-bold mb-4">Results:</h2>
        {Object.entries(results).map(([region, forms]) => (
          <div key={region} className="mb-4">
            <h3 className="text-xl font-semibold text-blue-600">{region}</h3>
            {forms.map((form, index) => (
              <p key={index} className="ml-4">{form}</p>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default VerbConjugator;