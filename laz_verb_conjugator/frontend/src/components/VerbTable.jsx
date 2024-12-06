import React from 'react';

const VerbTable = ({ verbs, language }) => {
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
            <tr key={index} className="hover:bg-gray-100">
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