import { useState } from "react";
import styles from "./styles/SearchBar.css";

export default function SearchBar() {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    if (!query) return;

    fetch("/api/stocks/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
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
    <div className={styles.searchBar}>
      <input
        type="text"
        placeholder="Enter search term..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className={styles.searchInput}
      />
      <button onClick={handleSearch} className={styles.searchButton}>
        Search
      </button>
    </div>
  );
}
