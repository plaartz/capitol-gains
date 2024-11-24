import { useState, useEffect, useContext } from "react";
import {FilterContext} from "src/contexts/Filters";
import TextBox from "./TextBox";
import DatePickerInput from "./DatePickerInput";
import RangeSlider from "./RangeSlider";
import "./styles/SearchBar.css";

export default function SearchTools() {
  const [fullName, setFullName] = useState("");
  const [stock, setStock] = useState("");
  const [advancedFiltersSelected, setAdvancedFiltersSelected] = useState(false);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(10000);
  const [purchaseSelected, setPurchaseSelceted] = useState(false);
  const [saleSelected, setSaleSelected] = useState(false);
  const [positiveGainSelected, setPositiveGainSelected] = useState(false);
  const [negativeGainSelected, setNegativeGainSelected] = useState(false);
  const [noGainSelected, setNoGainSelected] = useState(false);
  const [_, setFilters] = useContext(FilterContext);

  useEffect(() => {
    fetch(`/api/core/search`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({})
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch maximum price");
        }
        return response.json();
      })
      .then((result) => {
        console.log(result);
        if (result && result.data && Array.isArray(result.data)) {
          const maxStockPrice = Math.max(
            ...result.data.map((item) => item.transaction_amount)
          );
          console.log("Maximum stock price:", maxStockPrice);
          setMaxPrice(maxStockPrice);
        } else {
          console.error("No valid 'data' array found in the response");
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const handleSearch = () => {
    setFilters({
      full_name: fullName,
      stock: stock,
      start_date: startDate,
      end_date: endDate,
      min_price: minPrice,
      max_price: maxPrice,
      is_purchase: purchaseSelected,
      is_sale: saleSelected,
      positive_gain: positiveGainSelected,
      negative_gain: negativeGainSelected
    });
  };

  return (
    <div>
      <div className="searchBar">
        <div className="basicSearch">
          <TextBox
            label="Full Name"
            placeholder="Enter Full Name..."
            value={fullName}
            onChange={setFullName}
            className="searchInput"
          />
          <TextBox
            label="Company Ticker"
            placeholder="Enter Company Ticker..."
            value={stock}
            onChange={setStock}
            className="searchInput"
          />
          <button onClick={handleSearch} className="searchButton">
            Search
          </button>
        </div>
      </div>
      <div className="advancedOptionsToggle">
        <span
          onClick={() => setAdvancedFiltersSelected(!advancedFiltersSelected)}
          style={{ color: "red", cursor: "pointer" }}
        >
          {advancedFiltersSelected ? "Hide Advanced Options" : "Show Advanced Options"}
        </span>
      </div>
      {advancedFiltersSelected && (
        <div>
          <div className="advancedOptions">
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
                style={{ marginRight: "5px" }}
              />
              Purchase
            </label>
            <label>
              <input
                type="checkbox"
                checked={saleSelected}
                onChange={() => setSaleSelected(!saleSelected)}
                style={{ marginRight: "5px" }}
              />
              Sale
            </label>
            <label>
              <input
                type="checkbox"
                checked={positiveGainSelected}
                onChange={() => setPositiveGainSelected(!positiveGainSelected)}
                style={{ marginRight: "5px" }}
              />
              Positive Gain
            </label>
            <label>
              <input
                type="checkbox"
                checked={negativeGainSelected}
                onChange={() => setNegativeGainSelected(!negativeGainSelected)}
                style={{ marginRight: "5px" }}
              />
              Negative Gain
            </label>
            <label>
              <input
                type="checkbox"
                checked={noGainSelected}
                onChange={() => setNoGainSelected(!noGainSelected)}
                style={{ marginRight: "5px" }}
              />
              No Gain
            </label>
          </div>
          <div className="advancedOptions">
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
