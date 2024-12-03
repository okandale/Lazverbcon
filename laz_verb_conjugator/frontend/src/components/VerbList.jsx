import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import { Link } from 'react-router-dom';

const VerbList = () => {
  const [verbs, setVerbs] = useState([]);
  const [error, setError] = useState(null);

  const translations = {
    en: {
      backToConjugator: 'Back to Conjugator',
      verbsListTitle: 'Available Verbs',
    },
    tr: {
      backToConjugator: 'Fiil Çekicisine Geri Dön',
      verbsListTitle: 'Mevcut Fiiller',
    },
  };

  useEffect(() => {
    fetch(
      'https://raw.githubusercontent.com/okandale/Lazverbcon/main/laz_verb_conjugator/notebooks/data/Test%20Verb%20Present%20tense.csv'
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      .then((csvText) => {
        Papa.parse(csvText, {
          header: true, // Assumes the CSV has headers
          skipEmptyLines: true,
          complete: (results) => {
            setVerbs(results.data);
          },
          error: (err) => {
            console.error('Error parsing CSV:', err);
            setError('Failed to parse CSV data.');
          },
        });
      })
      .catch((err) => {
        console.error('Error fetching CSV file:', err);
        setError('Failed to load verbs data.');
      });
  }, []);

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Navigation Link to Conjugator */}
      <nav className="mb-4">
        <Link to="/conjugator" className="text-blue-500 hover:underline">
          &larr; {translations.en.backToConjugator} / {translations.tr.backToConjugator}
        </Link>
      </nav>

      {/* Title */}
      <h1 className="text-3xl font-bold mb-6 text-center">
        {translations.en.verbsListTitle} / {translations.tr.verbsListTitle}
      </h1>

      {/* Verbs Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b">Lazuri / Laz Infinitive</th>
              <th className="py-2 px-4 border-b">Türkçe / Turkish Verb</th>
              <th className="py-2 px-4 border-b">English / İngilizce</th>
            </tr>
          </thead>
          <tbody>
            {verbs.map((verb, index) => (
              <tr key={index} className="hover:bg-gray-100">
                <td className="border px-4 py-2">{verb['Laz Infinitive']}</td>
                <td className="border px-4 py-2">{verb['Turkish Verb']}</td>
                <td className="border px-4 py-2">{verb['English Translation']}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Optional: Pagination or Lazy Loading for Large Lists */}
    </div>
  );
};

export default VerbList;
