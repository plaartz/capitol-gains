import { useState, useEffect, useContext } from "react";
import {FilterContext} from "src/contexts/Filters";
import "src/styles/SearchBar.css";

export default function SearchTools() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [middleInitial, setMiddleInitial] = useState("");
  const [stock, setStock ] = useState("");
  const [filters, _] = useContext(FilterContext)

  const handleSearch = () => {
    if (!query) return;

    fetch("/api/stocks/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ firstName }),
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
    <div className="searchBar">
      <input
        type="text"
        placeholder="Enter search term..."
        value={firstName}
        onChange={(e) => setFirstName(e.target.value)}
        className="searchInput"
      />
      <button onClick={handleSearch} className="searchButton">
        Search
      </button>
    </div>
  );
}
