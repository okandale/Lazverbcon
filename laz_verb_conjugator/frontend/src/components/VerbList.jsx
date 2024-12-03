import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const API_URL = "/api/verbs";

const VerbList = () => {
  const [verbs, setVerbs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const translations = {
    en: {
      backToConjugator: 'Back to Conjugator',
      verbsListTitle: 'Available Verbs',
      loading: 'Loading verbs...',
    },
    tr: {
      backToConjugator: 'Fiil Çekicisine Geri Dön',
      verbsListTitle: 'Mevcut Fiiller',
      loading: 'Fiiller yükleniyor...',
    },
  };

  useEffect(() => {
    fetch(API_URL)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        setVerbs(data);
        setIsLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching verbs:', err);
        setError('Failed to load verbs data.');
        setIsLoading(false);
      });
  }, []);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-xl">{translations.en.loading} / {translations.tr.loading}</div>
      </div>
    );
  }

  if (error) {
    return <div className="text-red-500 text-center">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <nav className="mb-4">
        <Link to="/conjugator" className="text-blue-500 hover:underline">
          &larr; {translations.en.backToConjugator} / {translations.tr.backToConjugator}
        </Link>
      </nav>

      <h1 className="text-3xl font-bold mb-6 text-center">
        {translations.en.verbsListTitle} / {translations.tr.verbsListTitle}
      </h1>

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
    </div>
  );
};

export default VerbList;