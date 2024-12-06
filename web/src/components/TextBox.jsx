import { useState } from "react";
import PropTypes from "prop-types";
import styles from "./styles/TextBox.module.css";

export default function TextBox({ label, value, onChange, placeholder, className }) {
  const [inputValue, setInputValue] = useState(value);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    onChange(e.target.value);
  };

  return (
    <div className={`container ${className}`}>
      {label && <label className={styles.label}>{label}</label>}
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder={placeholder}
        className={styles.input}
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