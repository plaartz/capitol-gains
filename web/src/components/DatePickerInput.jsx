import styles from "./styles/DatePickerInput.module.css";

export default function DatePickerInput({ selectedDate, onDateChange, label }) {
  return (
    <div className={styles.datePickerContainer}>
      {label && <label>{label}</label>}
      <input
        type="date"
        value={selectedDate || ""}
        onChange={(e) => onDateChange(e.target.value)}
        className={styles.datePickerInput}
      />
    </div>
  );
}

