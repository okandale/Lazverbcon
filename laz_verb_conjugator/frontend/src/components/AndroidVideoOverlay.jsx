import React from 'react';

const AndroidVideoOverlay = ({ videoUrl, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="relative w-full max-w-4xl">
        <button 
          onClick={onClose}
          className="absolute -top-10 right-0 text-white text-2xl hover:text-gray-300"
          aria-label="Close video"
        >
          &times;
        </button>
        <div className="aspect-w-16 aspect-h-9">
          {videoUrl ? (
            <iframe 
              src={videoUrl}
              className="w-full h-full"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              title="Android için Lazca Klavye Kurulum Rehberi"
            ></iframe>
          ) : (
            <div className="bg-gray-800 text-white p-8 text-center rounded-lg">
              <p>Video yükleniyor...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AndroidVideoOverlay;