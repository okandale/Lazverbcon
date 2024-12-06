import React, { useRef } from 'react';
import { translations, specialCharacters } from './constants';
import { useFormValidation } from './useFormValidation';

const FormSection = ({
  language,
  formData,
  setFormData,
  setResults,
  onSubmit
}) => {
  const infinitiveInputRef = useRef(null);

  // Use the form validation hook
  useFormValidation(formData, setFormData, setResults);

  // Calculate disabled states
  const isAspectDisabled = formData.optative || formData.applicative || formData.obj;
  const isTenseDisabled = formData.optative || formData.imperative || formData.neg_imperative;
  const isObjectDisabled = formData.aspect !== '' || formData.tense === 'presentperf';

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

  const handleReset = () => {
    setFormData({
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
    });
    setResults({ data: {}, error: '' });
  };

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
    <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      {/* Special Characters */}
      <div className="mb-4 flex justify-center space-x-2">
        {specialCharacters.map((char, index) => (
          <button
            key={index}
            type="button"
            className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400"
            onClick={() => insertSpecialCharacter(char)}
          >
            {char}
          </button>
        ))}
      </div>

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
              isObjectDisabled ? 'bg-gray-200' : ''
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
              isTenseDisabled ? 'bg-gray-200' : ''
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
              isAspectDisabled ? 'bg-gray-200' : ''
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
        {[
          { name: 'applicative', label: translations[language].applicative },
          { name: 'imperative', label: translations[language].imperative, disabled: formData.neg_imperative },
          { name: 'causative', label: translations[language].causative },
          { name: 'neg_imperative', label: translations[language].negImperative, disabled: formData.imperative },
          { name: 'optative', label: translations[language].optative }
        ].map(({ name, label, disabled }) => (
          <div key={name} className="flex items-center">
            <input
              type="checkbox"
              id={name}
              name={name}
              checked={formData[name]}
              onChange={handleInputChange}
              disabled={disabled}
              className="mr-2"
            />
            <label className="text-gray-700 text-sm font-bold" htmlFor={name}>
              {label}
            </label>
          </div>
        ))}
      </div>

      {/* Submit and Reset Buttons */}
      <div className="flex justify-between">
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
          onClick={onSubmit}
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
    </div>
  );
};

export default FormSection;