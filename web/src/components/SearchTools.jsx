import React, { useState, useEffect, useContext } from "react";
import {FilterContext} from "src/contexts/Filters";
import TextBox from "./TextBox";
import DatePickerInput from "./DatePickerInput";
import RangeSlider from "./RangeSlider";
import "./styles/SearchBar.css";

export default function SearchTools() {
  const [fullName, setFullName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [middleInitial, setMiddleInitial] = useState("");
  const [lastName, setLastName] = useState("");
  const [stock, setStock ] = useState("");
  const [advancedFiltersSelected, setAdvancedFiltersSelected] = useState(false);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(10000);
  const [purchaseSelected, setPurchaseSelceted] = useState(false);
  const [saleSelected, setSaleSelected] = useState(false);
  const [filters, _] = useContext(FilterContext)

  useEffect(() => {
    const nameComponents = fullName.split(" ");
    if (nameComponents.length == 1) {
      setFirstName(nameComponents[0]);
    } else if (nameComponents.length == 2) {
      setFirstName(nameComponents[0]);
      setLastName(nameComponents[1])
    } else {
      setFirstName(nameComponents[0]);
      setMiddleInitial(nameComponents[1]);
      setLastName(nameComponents[2]);
    }
  }, [fullName])

  const handleSearch = () => {
    fetch("http://api:8000/api/core/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        'first_name': firstName,
        'middle_inital': middleInitial,
        'last_name': lastName,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Search results:", data);
      })
      .catch((error) => {
        console.error("Error fetching search results:", error);
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
