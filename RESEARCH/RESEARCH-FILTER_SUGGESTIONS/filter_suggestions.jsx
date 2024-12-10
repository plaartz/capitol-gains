/**
 *  the following code is created using ChatGPT and has not been tested with the implementation of our project, so it does not
 * necessarily fit the style guide, but this would be a starting point for attempting to implement filter suggestions using a
 * websocket and added debouncing. 
*/
import React, { useState, useEffect, useRef } from "react";
import debounce from "lodash.debounce";

const WebSocketDropdownWithDebounce = () => {
  const [searchValue, setSearchValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const wsRef = useRef(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const ws = new WebSocket("ws://your-websocket-server-url");
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket connection established");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "suggestions") {
        setSuggestions(data.suggestions);
        setIsDropdownOpen(true);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      ws.close(); // Clean up the WebSocket connection on component unmount
    };
  }, []);

  // Debounced WebSocket message sender
  const sendSearchQuery = debounce((query) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: "search", query }));
    }
  }, 300); // Adjust debounce delay as needed

  const handleInputChange = (e) => {
    const input = e.target.value;
    setSearchValue(input);

    if (input) {
      sendSearchQuery(input);
    } else {
      setIsDropdownOpen(false);
      setSuggestions([]);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setSearchValue(suggestion);
    setIsDropdownOpen(false);
    setSuggestions([]);
  };

  

  return (
    <div style={{ width: "300px", margin: "0 auto", position: "relative" }}>
      <input
        type="text"
        value={searchValue}
        onChange={handleInputChange}
        placeholder="Search..."
        style={{ width: "100%", padding: "8px", boxSizing: "border-box" }}
      />
      {isDropdownOpen && suggestions.length > 0 && (
        <ul
          style={{
            listStyleType: "none",
            margin: 0,
            padding: 0,
            position: "absolute",
            width: "100%",
            backgroundColor: "#fff",
            border: "1px solid #ccc",
            maxHeight: "150px",
            overflowY: "auto",
            zIndex: 1,
          }}
        >
          {suggestions.map((suggestion, index) => (
            <li
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              style={{
                padding: "8px",
                cursor: "pointer",
                borderBottom: "1px solid #eee",
              }}
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default WebSocketDropdownWithDebounce;