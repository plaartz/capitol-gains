import { useState, useContext } from "react";
import {FilterContext} from "src/contexts/Filters";
import TextBox from "./TextBox";
import DatePickerInput from "./DatePickerInput";
import RangeSlider from "./RangeSlider";
import styles from "./styles/SearchBar.module.css";

export default function SearchTools() {
  const [fullName, setFullName] = useState("");
  const [stock, setStock] = useState("");
  const [advancedFiltersSelected, setAdvancedFiltersSelected] = useState(false);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(1000000000);
  const [purchaseSelected, setPurchaseSelceted] = useState(false);
  const [saleSelected, setSaleSelected] = useState(false);
  const [positiveGainSelected, setPositiveGainSelected] = useState(false);
  const [negativeGainSelected, setNegativeGainSelected] = useState(false);
  const [noGainSelected, setNoGainSelected] = useState(false);
  const [_, updateFilter] = useContext(FilterContext);

  const handleSearch = () => {
    updateFilter("full_name", fullName);
    updateFilter("company", stock);
    updateFilter("start_date", startDate);
    updateFilter("end_date", endDate);
    updateFilter("min_price", minPrice);
    updateFilter("max_price", maxPrice);
    updateFilter("is_purchase", purchaseSelected);
    updateFilter("is_sale", saleSelected);
    updateFilter("positive_gain", positiveGainSelected);
    updateFilter("negative_gain", negativeGainSelected);
    updateFilter("no_gain", noGainSelected);
  };

  return (
    <div>
      <div className={styles.searchBar}>
        <div className={styles.basicSearch}>
          <TextBox
            label="Full Name"
            placeholder="Enter Full Name..."
            value={fullName}
            onChange={setFullName}
            className={styles.searchInput}
          />
          <TextBox
            label="Company Ticker"
            placeholder="Enter Company Ticker..."
            value={stock}
            onChange={setStock}
            className={styles.searchInput}
          />
          <button onClick={handleSearch} className={styles.searchButton}>
            Search
          </button>
        </div>
      </div>
      <div className={styles.advancedOptionsToggle}>
        <span
          onClick={() => setAdvancedFiltersSelected(!advancedFiltersSelected)}
          style={{ color: "red", cursor: "pointer" }}
        >
          {advancedFiltersSelected ? "Hide Advanced Options ▲" : "Show Advanced Options ▼"}
        </span>
      </div>
      {advancedFiltersSelected && (
        <div>
          <div className={styles.advancedOptions}>
            <DatePickerInput
              label="Start Date"
              selectedDate={startDate}
              onDateChange={setStartDate}
            />
            <DatePickerInput
              label="End Date"
              selectedDate={endDate}
              onDateChange={setEndDate}
            />
            <label>
              <input
                type="checkbox"
                checked={purchaseSelected}
                onChange={() => setPurchaseSelceted(!purchaseSelected)}
                className={styles.checkbox}
              />
              Purchase
            </label>
            <label>
              <input
                type="checkbox"
                checked={saleSelected}
                onChange={() => setSaleSelected(!saleSelected)}
                className={styles.checkbox}
              />
              Sale
            </label>
            <label>
              <input
                type="checkbox"
                checked={positiveGainSelected}
                onChange={() => setPositiveGainSelected(!positiveGainSelected)}
                className={styles.checkbox}
              />
              Positive Gain
            </label>
            <label>
              <input
                type="checkbox"
                checked={negativeGainSelected}
                onChange={() => setNegativeGainSelected(!negativeGainSelected)}
                className={styles.checkbox}
              />
              Negative Gain
            </label>
            <label>
              <input
                type="checkbox"
                checked={noGainSelected}
                onChange={() => setNoGainSelected(!noGainSelected)}
                className={styles.checkbox}
              />
              No Gain
            </label>
          </div>
          <div className={styles.advancedOptions}>
            <RangeSlider 
              minPrice={minPrice}
              setMinPrice={setMinPrice}
              maxPrice={maxPrice} 
              setMaxPrice={setMaxPrice}
            />
          </div>
        </div>
      )}
    </div>
  );
}
