import React, { useState } from 'react';

const DropdownMenu = ({ options }) => {
  const [selectedOption, setSelectedOption] = useState(options[0]);

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
  };

  return (
    <div className="dropdown">
      <div className="dropdown__selected-option">{selectedOption}</div>
      <ul className="dropdown__options">
        {options.map((option) => (
          <li key={option} onClick={() => handleOptionSelect(option)}>
            {option}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DropdownMenu;


