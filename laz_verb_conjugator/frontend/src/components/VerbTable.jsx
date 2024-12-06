import React from 'react';
import { useNavigate } from 'react-router-dom';

const VerbTable = ({ verbs, language }) => {
  const navigate = useNavigate();

  const columnTitles = {
    en: {
      laz: 'Laz Infinitive',
      turkish: 'Turkish Verb',
      english: 'English',
    },
    tr: {
      laz: 'Lazuri',
      turkish: 'Türkçe',
      english: 'İngilizce',
    }
  };

  const handleVerbClick = (verb) => {
    navigate('/', { 
      state: { 
        infinitive: verb['Laz Infinitive']
      }
    });
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b">{columnTitles[language].laz}</th>
            <th className="py-2 px-4 border-b">{columnTitles[language].turkish}</th>
            <th className="py-2 px-4 border-b">{columnTitles[language].english}</th>
          </tr>
        </thead>
        <tbody>
          {verbs.map((verb, index) => (
            <tr 
              key={index} 
              onClick={() => handleVerbClick(verb)}
              className="hover:bg-blue-50 cursor-pointer transition-colors duration-150"
            >
              <td className="border px-4 py-2">{verb['Laz Infinitive']}</td>
              <td className="border px-4 py-2">{verb['Turkish Verb']}</td>
              <td className="border px-4 py-2">{verb['English Translation']}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VerbTable;