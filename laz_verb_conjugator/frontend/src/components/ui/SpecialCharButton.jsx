import React from 'react';

const SpecialCharButton = ({ char, onClick }) => {
  return (
    <button
      type="button"
      className="w-12 h-12 flex items-center justify-center text-lg bg-white rounded-lg shadow-sm border border-gray-200 
                 hover:bg-gray-50 hover:border-gray-300 transition-all duration-200 
                 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                 active:bg-gray-100"
      onClick={() => onClick(char)}
    >
      {char}
    </button>
  );
};

export default SpecialCharButton;