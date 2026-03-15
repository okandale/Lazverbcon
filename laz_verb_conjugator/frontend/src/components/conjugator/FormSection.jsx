import React, { useRef } from 'react';
import { translations, specialCharacters } from '../constants';
import { useFormValidation } from '../useFormValidation';
import SpecialCharButton from '../ui/SpecialCharButton';

const FormSection = ({
  language,
  formData,
  setFormData,
  setResults,
  onSubmit
}) => {
  const infinitiveInputRef = useRef(null);
  const t = translations[language] || translations.en || translations.tr;

  useFormValidation(formData, setFormData, setResults);

  const isAspectDisabled = formData.optative || formData.applicative || formData.obj;
  const isTenseDisabled = formData.optative || formData.imperative || formData.neg_imperative;
  const isObjectDisabled = formData.aspect !== '' || formData.tense === 'present_perfect';

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;

    setFormData((prevData) => {
      if (type === 'checkbox' && checked) {
        if (name === 'causative') {
          return { ...prevData, causative: true, simple_causative: false };
        }
        if (name === 'simple_causative') {
          return { ...prevData, simple_causative: true, causative: false };
        }
      }

      return {
        ...prevData,
        [name]: type === 'checkbox' ? checked : value,
      };
    });
  };

  const handleRegionChange = (e) => {
    const { value, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      regions: checked
        ? [...prevData.regions, value]
        : prevData.regions.filter((region) => region !== value),
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
      simple_causative: false,
      optative: false,
      imperative: false,
      neg_imperative: false,
      regions: [],
    });
    setResults({ data: {}, meta: null, error: '' });
  };

  const handleSpecialCharClick = (char) => {
    if (infinitiveInputRef.current) {
      const input = infinitiveInputRef.current;
      const start = input.selectionStart;
      const end = input.selectionEnd;
      const text = input.value;
      const before = text.substring(0, start);
      const after = text.substring(end);

      input.value = before + char + after;
      input.selectionStart = input.selectionEnd = start + char.length;
      input.focus();

      setFormData((prevData) => ({
        ...prevData,
        infinitive: input.value,
      }));
    }
  };

  return (
    <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <div className="grid grid-cols-4 sm:flex sm:flex-wrap justify-center gap-2 mb-6">
        {specialCharacters.map((char, index) => (
          <SpecialCharButton
            key={index}
            char={char}
            onClick={handleSpecialCharClick}
          />
        ))}
      </div>

      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="infinitive">
          {t.infinitive}:
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
            {t.subject}:
          </label>
          <select
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-white"
            id="subject"
            name="subject"
            value={formData.subject}
            onChange={handleInputChange}
            required
          >
            <option value="S1SG">{language === 'en' ? 'I' : 'Ben'}</option>
            <option value="S2SG">{language === 'en' ? 'You (singular)' : 'Sen'}</option>
            <option value="S3SG">{language === 'en' ? 'He/She/It' : 'O'}</option>
            <option value="S1PL">{language === 'en' ? 'We' : 'Biz'}</option>
            <option value="S2PL">{language === 'en' ? 'You (plural)' : 'Siz'}</option>
            <option value="S3PL">{language === 'en' ? 'They' : 'Onlar'}</option>
            <option value="all">{language === 'en' ? 'All' : 'Hepsi'}</option>
          </select>
        </div>

        <div>
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="obj">
            {t.object}:
          </label>
          <select
            className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
              isObjectDisabled ? 'bg-gray-200 opacity-60' : 'bg-white'
            }`}
            id="obj"
            name="obj"
            value={formData.obj}
            onChange={handleInputChange}
            disabled={isObjectDisabled}
          >
            <option value="">{language === 'en' ? 'None' : 'Yok'}</option>
            <option value="O1SG">{language === 'en' ? 'Me' : 'Beni'}</option>
            <option value="O2SG">{language === 'en' ? 'You (singular)' : 'Seni'}</option>
            <option value="O3SG">{language === 'en' ? 'Him/Her/It' : 'Onu'}</option>
            <option value="O1PL">{language === 'en' ? 'Us' : 'Bizi'}</option>
            <option value="O2PL">{language === 'en' ? 'You (plural)' : 'Sizi'}</option>
            <option value="O3PL">{language === 'en' ? 'Them' : 'Onları'}</option>
            <option value="all">{language === 'en' ? 'All' : 'Hepsi'}</option>
          </select>
        </div>

        <div>
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="tense">
            {t.tense}:
          </label>
          <select
            className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
              isTenseDisabled ? 'bg-gray-200 opacity-60' : 'bg-white'
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
            <option value="past_progressive">{language === 'en' ? 'Past Progressive' : 'Geçmişte Devam Eden'}</option>
            <option value="present_perfect">{language === 'en' ? 'Present Perfect' : 'Yakın Geçmiş'}</option>
          </select>
        </div>

        <div>
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="aspect">
            {t.aspect}:
          </label>
          <select
            className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
              isAspectDisabled ? 'bg-gray-200 opacity-60' : 'bg-white'
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

      <fieldset className="mb-4 border border-gray-300 rounded p-3">
        <legend className="font-bold">{t.regions}</legend>
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
      </fieldset>

      <div className="grid grid-cols-2 gap-4 mb-8">
        {[
          { name: 'applicative', label: t.applicative },
          { name: 'imperative', label: t.imperative, disabled: formData.neg_imperative },
          { name: 'simple_causative', label: t.simple_causative },
          { name: 'causative', label: t.causative },
          { name: 'neg_imperative', label: t.negImperative, disabled: formData.imperative },
          { name: 'optative', label: t.optative }
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

      <div className="flex justify-between gap-4">
        <button
          className="flex-1 min-w-32 bg-blue-500 hover:bg-blue-600 active:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-150 ease-in-out shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed"
          type="submit"
          onClick={onSubmit}
        >
          <span className="block w-full text-center">
            {t.conjugate}
          </span>
        </button>
        <button
          type="button"
          className="flex-1 min-w-32 bg-gray-500 hover:bg-gray-600 active:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-150 ease-in-out shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50"
          onClick={handleReset}
        >
          <span className="block w-full text-center">
            {t.reset}
          </span>
        </button>
      </div>
    </div>
  );
};

export default FormSection;