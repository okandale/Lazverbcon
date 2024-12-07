import React, { useState } from 'react';
import { regionNames, subjectOrder, objectOrder } from './constants';
import { Copy, Check } from 'lucide-react';

const Results = ({ results, language, translations }) => {
  const [copiedId, setCopiedId] = useState(null);

  if (results.error) {
    return (
      <div className="rounded-lg bg-red-50 p-4 border border-red-200">
        <p className="text-red-600 text-sm">{results.error}</p>
      </div>
    );
  }

  if (Object.entries(results.data).length === 0) {
    return null;
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

  const formatConjugation = (form) => {
    const [prefix, conjugation] = form.split(':').map(part => part.trim());
    return { prefix, conjugation };
  };

  const handleCopy = async (text, id) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const regionOrder = ['AŞ', 'PZ', 'FA', 'HO'];

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="border-b border-gray-200 px-6 py-4">
        <h2 className="text-2xl font-semibold text-gray-800">
          {translations[language].results}
        </h2>
      </div>
      
      <div className="divide-y-2 divide-gray-200">
        {regionOrder
          .map(regionCode => {
            const region = Object.entries(results.data).find(([key]) => key === regionCode);
            if (!region) return null;

            const [regionName, forms] = region;
            const regionDisplayName = regionNames[regionName] || regionName;

            return (
              <div key={regionName} className="px-6 py-4">
                <h3 className="text-xl font-semibold text-blue-600 mb-4">
                  {regionDisplayName}
                </h3>
                
                <div className="divide-y divide-gray-200">
                  {Array.isArray(forms) ? (
                    sortForms(forms).map((form, index) => {
                      const { prefix, conjugation } = formatConjugation(form);
                      const formId = `${regionName}-${index}`;
                      
                      return (
                        <div 
                          key={index}
                          className="flex items-center py-3 group"
                        >
                          <div className="w-1/3 font-medium text-gray-500 min-w-fit pr-4">
                            {prefix}
                          </div>
                          <div className="w-2/3 text-gray-900 flex items-center justify-between">
                            <span className="mr-2">{conjugation}</span>
                            <button
                              onClick={() => handleCopy(conjugation, formId)}
                              className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 p-1 hover:text-blue-500 flex-shrink-0"
                              title="Copy to clipboard"
                            >
                              {copiedId === formId ? (
                                <Check className="w-4 h-4 text-green-500" />
                              ) : (
                                <Copy className="w-4 h-4" />
                              )}
                            </button>
                          </div>
                        </div>
                      );
                    })
                  ) : (
                    <div className="text-gray-700">{forms}</div>
                  )}
                </div>
              </div>
            );
          })
          .filter(Boolean)}
      </div>
    </div>
  );
};

export default Results;