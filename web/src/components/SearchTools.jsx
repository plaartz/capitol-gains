import { useState, useEffect, useContext } from "react";
import {FilterContext} from "src/contexts/Filters";
import TextBox from "./TextBox";
import DatePickerInput from "./DatePickerInput";
import RangeSlider from "./RangeSlider";
import styles from "./styles/SearchBar.module.css";

export default function SearchTools() {
  const [isLoading, setLoading] = useState(true)
  const [fullName, setFullName] = useState("");
  const [stock, setStock] = useState("");
  const [advancedFiltersSelected, setAdvancedFiltersSelected] = useState(false);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(1000000000);
  const [purchaseSelected, setPurchaseSelected] = useState(false);
  const [saleSelected, setSaleSelected] = useState(false);
  const [positiveGainSelected, setPositiveGainSelected] = useState(false);
  const [negativeGainSelected, setNegativeGainSelected] = useState(false);
  const [noGainSelected, setNoGainSelected] = useState(false);
  const [_, updateFilter] = useContext(FilterContext);

  // Load saved filters from localStorage when the component mounts
  useEffect(() => {
    const savedFilters = JSON.parse(localStorage.getItem("filters"));

    if (savedFilters) {
      setFullName(savedFilters.fullName || "");
      setStock(savedFilters.stock || "");
      setStartDate(savedFilters.startDate || null);
      setEndDate(savedFilters.endDate || null);
      setMinPrice(savedFilters.minPrice || 0);
      setMaxPrice(savedFilters.maxPrice || 1000000000);
      setPurchaseSelected(savedFilters.purchaseSelected || false);
      setSaleSelected(savedFilters.saleSelected || false);
      setPositiveGainSelected(savedFilters.positiveGainSelected || false);
      setNegativeGainSelected(savedFilters.negativeGainSelected || false);
      setNoGainSelected(savedFilters.noGainSelected || false);
      setAdvancedFiltersSelected(savedFilters.advancedFiltersSelected || false);
    }
    setLoading(false);
  }, []);

  const handleSearch = () => {
    const filters = {
      fullName,
      stock,
      startDate,
      endDate,
      minPrice,
      maxPrice,
      purchaseSelected,
      saleSelected,
      positiveGainSelected,
      negativeGainSelected,
      noGainSelected,
      advancedFiltersSelected,
    };

    // Save filters to localStorage
    localStorage.setItem("filters", JSON.stringify(filters));

    // Update Filter Context
    updateFilter("full_name", fullName);
    updateFilter("stock_ticker", stock);
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

  if (isLoading) {
    return <div>Loading filters</div>
  }
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
          onClick={() => setAdvancedFiltersSelected((prevState) => !prevState)}
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
                onChange={() => setPurchaseSelected((prevState) => !prevState)}
                className={styles.checkbox}
              />
              Purchase
            </label>
            <label>
              <input
                type="checkbox"
                checked={saleSelected}
                onChange={() => setSaleSelected((prevState) => !prevState)}
                className={styles.checkbox}
              />
              Sale
            </label>
            <label>
              <input
                type="checkbox"
                checked={positiveGainSelected}
                onChange={() => setPositiveGainSelected((prevState) => !prevState)}
                className={styles.checkbox}
              />
              Positive Gain
            </label>
            <label>
              <input
                type="checkbox"
                checked={negativeGainSelected}
                onChange={() => setNegativeGainSelected((prevState) => !prevState)}
                className={styles.checkbox}
              />
              Negative Gain
            </label>
            <label>
              <input
                type="checkbox"
                checked={noGainSelected}
                onChange={() => setNoGainSelected((prevState) => !prevState)}
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
