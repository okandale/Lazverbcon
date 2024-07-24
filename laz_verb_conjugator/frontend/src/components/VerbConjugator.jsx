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
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="obj"
              name="obj"
              value={formData.obj}
              onChange={handleInputChange}
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
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="tense"
              name="tense"
              value={formData.tense}
              onChange={handleInputChange}
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
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="aspect"
              name="aspect"
              value={formData.aspect}
              onChange={handleInputChange}
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

        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Conjugate
        </button>
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
