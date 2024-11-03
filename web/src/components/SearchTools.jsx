import { useState, useContext } from "react";
import { FilterContext } from "src/contexts/Filters.js";
import styles from "./styles/SearchTools.module.css";
import { searchStocks } from "src/utils/api.ts";

export default function SearchTools() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [results, setResults] = useState([]);
  const [filters, _] = useContext(FilterContext);

  const handleSearch = async () => {
    const res = await fetch(searchStocks(firstName, lastName), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filters }),
    });
    const data = await res.json();
    setResults(data.stocks || []);
  };

  return (
    <div className={styles.searchContainer}>
      <div className={styles.inputGroup}>
        <input
          type="text"
          placeholder="First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          className={styles.inputField}
        />
        <input
          type="text"
          placeholder="Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          className={styles.inputField}
        />
        <button onClick={handleSearch} className={styles.searchButton}>
          Search
        </button>
      </div>
      <section className={styles.resultsTable}>
        {results.length > 0 ? (
          <table style={{ width: "100%", tableLayout: "fixed" }}>
            <thead className={styles.tableHead}>
              <tr>
                <th>Stock Ticker</th>
                <th>Company Name</th>
                <th>Transaction Date</th>
              </tr>
            </thead>
            <tbody>
              {results.map((stock, idx) => (
                <tr key={idx} className={styles.tableRow}>
                  <td>{stock.ticker}</td>
                  <td>{stock.companyName}</td>
                  <td>{stock.transactionDate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No results found.</p>
        )}
      </section>
    </div>
  );
}
