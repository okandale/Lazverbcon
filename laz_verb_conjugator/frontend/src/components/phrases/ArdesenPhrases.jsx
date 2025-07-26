import React, { useState } from 'react';

export default function ArdesenPhrases() {
  const [activeTab, setActiveTab] = useState('market');

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Pazar Phrase Guide</h1>
      
      <div className="flex gap-4 mb-6">
        <button onClick={() => setActiveTab('market')} className={activeTab === 'market' ? 'font-bold' : ''}>Market</button>
        <button onClick={() => setActiveTab('pharmacy')} className={activeTab === 'pharmacy' ? 'font-bold' : ''}>Pharmacy</button>
        <button onClick={() => setActiveTab('restaurant')} className={activeTab === 'restaurant' ? 'font-bold' : ''}>Restaurant</button>
      </div>

      {activeTab === 'market' && (
        <div>
          <h2 className="text-xl font-semibold mb-2">At the Market</h2>
          <p>🗣️ How much is this? → ...</p>
        </div>
      )}

      {activeTab === 'pharmacy' && (
        <div>
          <h2 className="text-xl font-semibold mb-2">At the Pharmacy</h2>
          <p>🗣️ I need medicine for a headache → ...</p>
        </div>
      )}

      {activeTab === 'restaurant' && (
        <div>
          <h2 className="text-xl font-semibold mb-2">At the Restaurant</h2>
          <p>🗣️ I’m vegetarian → ...</p>
        </div>
      )}
    </div>
  );
}
