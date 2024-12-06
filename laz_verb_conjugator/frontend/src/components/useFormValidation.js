// hooks/useFormValidation.js
import { useEffect } from 'react';

export const useFormValidation = (formData, setFormData, setResults) => {
  useEffect(() => {
    const newData = { ...formData };
    let error = '';

    if (formData.optative) {
      newData.aspect = '';
      newData.tense = 'present';
      if (newData.aspect !== '' || newData.tense !== 'present') {
        error = 'Aspect and tense are not applicable when optative is selected.';
      }
    }

    if (formData.aspect !== '' || formData.tense === 'presentperf') {
      newData.obj = '';
      if (newData.obj !== '') {
        error = formData.aspect !== '' ? 
          'Object is not applicable when an aspect is selected.' :
          'Object is not applicable in present perfect tense.';
      }
    }

    if (formData.imperative || formData.neg_imperative) {
      newData.tense = 'present';
    }

    setFormData(newData);
    if (error) setResults({ data: {}, error });
  }, [
    formData.optative,
    formData.applicative,
    formData.causative,
    formData.tense,
    formData.aspect,
    formData.imperative,
    formData.neg_imperative,
    setFormData,
    setResults
  ]);
};