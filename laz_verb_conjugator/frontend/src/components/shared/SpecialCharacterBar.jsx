import React from 'react';
import SpecialCharButton from '../ui/SpecialCharButton';
import { specialCharacters } from '../constants';

const SpecialCharacterBar = ({ onCharClick, className = '' }) => {
  return (
    <div className={`flex flex-wrap justify-center gap-2 mb-6 ${className}`}>
      {specialCharacters.map((char, index) => (
        <SpecialCharButton
          key={index}
          char={char}
          onClick={onCharClick}
        />
      ))}
    </div>
  );
};

export default SpecialCharacterBar;