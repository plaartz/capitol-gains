import { useState } from "react";
import PropTypes from "prop-types";
import "./styles/TextBox.css";

export default function TextBox({ label, value, onChange, placeholder, className }) {
  const [inputValue, setInputValue] = useState(value);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    onChange(e.target.value);
  };

  return (
    <div className={`textbox-container ${className}`}>
      {label && <label className="textbox-label">{label}</label>}
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder={placeholder}
        className="textbox-input"
      />
    </div>
  );
}

TextBox.propTypes = {
  label: PropTypes.string,
  onChange: PropTypes.func.isRequired,
  placeholder: PropTypes.string,
  className: PropTypes.string,
};