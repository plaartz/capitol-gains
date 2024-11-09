import React from "react";
import "./styles/DatePickerInput.css";

export default function DatePickerInput({ selectedDate, onDateChange, label }) {
  return (
    <div className="datePickerContainer">
      {label && <label>{label}</label>}
      <input
        type="date"
        value={selectedDate || ""}
        onChange={(e) => onDateChange(e.target.value)}
        className="datePickerInput"
      />
    </div>
  );
}

