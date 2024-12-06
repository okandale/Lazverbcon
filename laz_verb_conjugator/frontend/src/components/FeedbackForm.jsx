import React, { useEffect, useRef, useState } from 'react';

const FeedbackForm = ({ isVisible, onClose, language, translations }) => {
  const [feedbackData, setFeedbackData] = useState({
    incorrectWord: '',
    correction: '',
    explanation: '',
  });

  const firstInputRef = useRef(null);

  useEffect(() => {
    if (isVisible && firstInputRef.current) {
      firstInputRef.current.focus();
    }
  }, [isVisible]);

  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isVisible) {
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isVisible, onClose]);

  const handleFeedbackChange = (e) => {
    const { name, value } = e.target;
    setFeedbackData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    const scriptURL = 'https://script.google.com/macros/s/AKfycbxocjHtMbmcehees6xRUs43RLaqTwFiLjp9IXbsswXZj52QcL-owsk4xDG4kkOQksbP/exec';
    
    try {
      const callbackName = 'callback' + Date.now();
      
      window[callbackName] = function(response) {
        if (response.result === 'success') {
          setFeedbackData({
            incorrectWord: '',
            correction: '',
            explanation: '',
          });
          onClose();
          alert('Thank you for your feedback!');
        } else {
          alert('An error occurred: ' + response.error);
        }
        
        delete window[callbackName];
        document.body.removeChild(script);
      };
      
      const queryString = `callback=${callbackName}&data=${encodeURIComponent(JSON.stringify(feedbackData))}`;
      const script = document.createElement('script');
      script.src = `${scriptURL}?${queryString}`;
      
      document.body.appendChild(script);
    } catch (error) {
      alert('An error occurred while submitting feedback. Please try again later.');
    }
  };

  if (!isVisible) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-lg overflow-hidden shadow-xl max-w-md w-full mx-2"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-6 py-4">
          <h3 className="text-xl font-bold mb-4">
            {translations[language].feedbackTitle}
          </h3>
          <form onSubmit={handleFeedbackSubmit}>
            <div className="mb-3">
              <label className="block text-gray-700 font-bold mb-1" htmlFor="incorrectWord">
                {translations[language].feedbackLabels.incorrectWord}
              </label>
              <input
                type="text"
                name="incorrectWord"
                value={feedbackData.incorrectWord}
                onChange={handleFeedbackChange}
                className="w-full border rounded px-2 py-1"
                required
                ref={firstInputRef}
              />
            </div>
            <div className="mb-3">
              <label className="block text-gray-700 font-bold mb-1" htmlFor="correction">
                {translations[language].feedbackLabels.correction}
              </label>
              <input
                type="text"
                name="correction"
                value={feedbackData.correction}
                onChange={handleFeedbackChange}
                className="w-full border rounded px-2 py-1"
                required
              />
            </div>
            <div className="mb-3">
              <label className="block text-gray-700 font-bold mb-1" htmlFor="explanation">
                {translations[language].feedbackLabels.explanation}
              </label>
              <textarea
                name="explanation"
                value={feedbackData.explanation}
                onChange={handleFeedbackChange}
                className="w-full border rounded px-2 py-1"
                rows="4"
              ></textarea>
            </div>
            <p className="text-sm text-gray-600 mb-3">
              {translations[language].feedbackDisclaimer}
            </p>
            <div className="flex justify-end space-x-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 bg-gray-300 rounded"
              >
                {translations[language].feedbackLabels.cancel}
              </button>
              <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">
                {translations[language].feedbackLabels.submit}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default FeedbackForm;