import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import VerbTable from './VerbTable';
import { translations, API_URLS } from './constants';

const VerbList = () => {
  const [verbs, setVerbs] = useState([]);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState('en');

  useEffect(() => {
    const fetchVerbs = async () => {
      try {
        const response = await fetch(API_URLS.verbs);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setVerbs(data);
      } catch (err) {
        console.error('Error fetching verbs:', err);
        setError('Failed to load verbs data.');
      }
    };

    fetchVerbs();
  }, []);

  if (error) {
    return <div className="text-red-500 text-center">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <nav className="mb-4">
        <Link to="/" className="text-blue-500 hover:underline">
          &larr; {translations[language].backToConjugator}
        </Link>
      </nav>
      
      <h1 className="text-3xl font-bold mb-6 text-center">
        {translations[language].verbsListTitle}
      </h1>

      <VerbTable verbs={verbs} />
    </div>
  );
};

export default VerbList;