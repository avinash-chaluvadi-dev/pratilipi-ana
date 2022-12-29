import React, { useState, useEffect } from 'react';
import Select, { components } from 'react-select';
import selectIcon from 'static/images/selectIcon.png';

const DropdownIndicator = (props) => {
  return (
    <components.DropdownIndicator {...props}>
      <img src={selectIcon} alt="" width="20px" height="20px" />
    </components.DropdownIndicator>
  );
};

const Placeholder = (props) => {
  return <components.Placeholder {...props} />;
};

function DropDown(props) {
  const { listUserData, handleChangeDropDown, placeHolderText, selectedVal } = props;
  const [selectedOption, setSelectedOption] = useState(selectedVal);

  useEffect(() => {
    setSelectedOption(selectedVal);
  }, [selectedVal]);

  const handleChange = (selectedOption) => {
    handleChangeDropDown(selectedOption);
    setSelectedOption(selectedOption);
  };

  return (
    <Select
      components={{ Placeholder, DropdownIndicator, IndicatorSeparator: () => null }}
      onChange={handleChange}
      placeholder={placeHolderText ? placeHolderText : 'Select Options'}
      menuPlacement="bottom"
      styles={{
        control: (provided) => ({
          ...provided,
          border: 'solid 1px #949494',
          borderRadius: '8px',
          paddingTop: '0',
          paddingBottom: '0',
          boxShadow: 'none',
          cursor: 'pointer',
          '&:hover': {
            border: '1px solid #D8D8D8',
          },
        }),
        placeholder: (base) => ({
          ...base,
          fontSize: '14px',
          fontWeight: 'bold',
          color: '#286ce2',
          textAlign: 'left',
        }),
        menuList: (provided, state) => ({
          ...provided,
          textAlign: 'left',
          fontSize: '14px',
          fontWeight: 'bold',
        }),
        singleValue: (provided, state) => ({
          ...provided,
          textAlign: 'left',
          fontSize: '14px',
          fontWeight: 'bold',
          color: '#286ce2!important',
        }),
      }}
      options={listUserData}
      value={selectedOption}
    />
  );
}

export default DropDown;
