import React from 'react';

const VerbTable = ({ verbs }) => {
  return (
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
  );
};

export default VerbTable;