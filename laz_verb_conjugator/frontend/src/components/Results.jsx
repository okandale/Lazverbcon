import React from 'react';
import { regionNames, subjectOrder, objectOrder } from './constants';

const Results = ({ results, language, translations }) => {
  if (results.error) {
    return <p className="text-red-600">{results.error}</p>;
  }

  if (Object.entries(results.data).length === 0) {
    return <p>No results to display.</p>;
  }

  const sortForms = forms => {
    return forms.sort((a, b) => {
      const [prefixA] = a.split(':');
      const [prefixB] = b.split(':');
      const [subjectA, objectA] = prefixA.trim().split(' ');
      const [subjectB, objectB] = prefixB.trim().split(' ');

      const subjectCompare = subjectOrder.indexOf(subjectA) - subjectOrder.indexOf(subjectB);
      if (subjectCompare !== 0) return subjectCompare;

      return objectOrder.indexOf(objectA) - objectOrder.indexOf(objectB);
    });
  };

  const regionOrder = ['AŞ', 'PZ', 'FA', 'HO'];

  return (
    <div className="bg-white shadow-md rounded px-8 pt-6 pb-8">
      <h2 className="text-2xl font-bold mb-4">{translations[language].results}:</h2>
      {regionOrder
        .map(regionCode => {
          const region = Object.entries(results.data).find(([key]) => key === regionCode);
          if (!region) return null;

          const [regionName, forms] = region;
          return (
            <div key={regionName} className="mb-4">
              <h3 className="text-xl font-semibold text-blue-600">
                {regionNames[regionName] || regionName}
              </h3>
              {Array.isArray(forms) ? (
                sortForms(forms).map((form, index) => (
                  <p key={index} className="ml-4">
                    {form}
                  </p>
                ))
              ) : (
                <p>{forms}</p>
              )}
            </div>
          );
        })
        .filter(Boolean)}
    </div>
  );
};

export default Results;