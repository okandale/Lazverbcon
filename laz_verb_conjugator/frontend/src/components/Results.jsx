import React, { useState, useMemo } from 'react';
import { regionNames } from './constants';
import { Copy, Check } from 'lucide-react';

const Results = ({ results, language, translations }) => {
  const [copiedId, setCopiedId] = useState(null);

  const data = results?.data && typeof results.data === 'object' ? results.data : {};
  const error = results?.error || '';

  // Keep your preferred display order
  const regionOrder = ['AŞ', 'PZ', 'FA', 'HO'];

  // Include all possible group types you want rendered
  const groupOrder = ['Dative', 'Ergative', 'Nominative'];

  const hasAnyForms = useMemo(() => {
    return regionOrder.some((regionCode) => {
      const regionData = data?.[regionCode];
      if (!regionData || typeof regionData !== 'object') return false;

      return groupOrder.some((groupType) => {
        const forms = regionData[groupType];
        return Array.isArray(forms) && forms.length > 0;
      });
    });
  }, [data]);

  const handleCopy = async (text, id) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  if (error) {
    return (
      <div className="rounded-lg bg-red-50 p-4 border border-red-200">
        <p className="text-red-600 text-sm">{error}</p>
      </div>
    );
  }

  // Nothing to show
  if (!hasAnyForms) return null;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="border-b border-gray-200 px-6 py-4">
        <h2 className="text-2xl font-semibold text-gray-800">
          {translations[language].results}
        </h2>
      </div>

      <div className="divide-y divide-gray-200">
        {regionOrder
          .filter((regionCode) => data?.[regionCode])
          .map((regionCode) => {
            const regionData = data[regionCode];
            const regionDisplayName = regionNames?.[regionCode] || regionCode;

            return (
              <div key={regionCode} className="px-6 py-4">
                <h3 className="text-xl font-semibold text-blue-600 mb-4">
                  {regionDisplayName}
                </h3>

                <div className="space-y-8">
                  {groupOrder.map((groupType) => {
                    const formsRaw = regionData?.[groupType];
                    const forms = Array.isArray(formsRaw) ? formsRaw : [];

                    if (forms.length === 0) return null;

                    return (
                      <div key={groupType} className="space-y-4">
                        <h4 className="font-medium text-gray-700 border-b border-gray-200 pb-2">
                          {groupType}
                        </h4>

                        <div className="space-y-2">
                          {forms.map((form, index) => {
                            const formId = `${regionCode}-${groupType}-${index}`;

                            const subject = (form?.subject ?? '').trim();
                            const obj = (form?.object ?? '').trim();
                            const label = obj ? `${subject} ${obj}` : subject;

                            const conj = form?.conjugation ?? '';

                            return (
                              <div
                                key={formId}
                                className="flex items-center py-1 group"
                              >
                                <div className="w-1/3 font-medium text-gray-500">
                                  {label}
                                </div>

                                <div className="w-2/3 flex items-center justify-between">
                                  <span className="text-gray-900">{conj}</span>

                                  <button
                                    type="button"
                                    onClick={() => handleCopy(conj, formId)}
                                    className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 p-1 hover:text-blue-500"
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
                          })}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default Results;