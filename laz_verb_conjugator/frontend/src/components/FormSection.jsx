// FormSection.jsx
import React from 'react';
import { SUBJECTS, OBJECTS, TENSES, ASPECTS, translations } from './constants';

const FormSection = ({ 
  language, 
  formData, 
  handleInputChange, 
  handleRegionChange,
  isAspectDisabled,
  isTenseDisabled,
  isObjectDisabled,
  infinitiveInputRef,
  insertSpecialCharacter
}) => {
  return (
    <form onSubmit={e => e.preventDefault()} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
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
            {SUBJECTS.map(subject => (
              <option key={subject.value} value={subject.value}>
                {subject.label[language]}
              </option>
            ))}
          </select>
        </div>

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
            {OBJECTS.map(object => (
              <option key={object.value} value={object.value}>
                {object.label[language]}
              </option>
            ))}
          </select>
        </div>

        {/* Tense and Aspect Selectors */}
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
          >
            {TENSES.map(tense => (
              <option key={tense.value} value={tense.value}>
                {tense.label[language]}
              </option>
            ))}
          </select>
        </div>

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
            {ASPECTS.map(aspect => (
              <option key={aspect.value} value={aspect.value}>
                {aspect.label[language]}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Regions Fieldset */}
      <fieldset className="mb-4 border border-gray-300 rounded p-3">
        <legend className="font-bold">{translations[language].regions}</legend>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(REGION_NAMES).map(([code, name]) => (
            <label key={code} className="block">
              <input
                type="checkbox"
                name="regions"
                value={code}
                checked={formData.regions.includes(code)}
                onChange={handleRegionChange}
                className="mr-2"
              />
              {name}
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
    </form>
  );
};

export default FormSection;