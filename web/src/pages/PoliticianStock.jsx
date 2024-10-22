import { useEffect, useState } from "react";

function PoliticianStock() {
  const [data, setData] = useState([]);
  useEffect(() => {
    fetch("/api/core/search", {
      method: "POST",
      body: JSON.stringify({ 
        "pageNo": 1,
        "pageSize": 100 
      }),
    })
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
        setData(res.data);
      });
  });
  return (
    <div style={{ padding: "20px" }}>
      <h2>Politician Stock Transactions</h2>
      <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
        {data.map((transaction, index) => {
          const {
            transaction_amount,
            transaction_date,
            disclosure_date,
            transaction_type,
            full_name,
            politician_type,
            stock_ticker,
          } = transaction;

          return (
            <div
              key={index}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                border: "1px solid black",
                borderRadius: "5px",
                padding: "15px",
                width: "100%",
                boxSizing: "border-box",
              }}
            >
              <div style={{ flex: 1, paddingRight: "15px" }}>
                <h3>{full_name}</h3>
                <p>Transaction Type: {transaction_type}</p>
                <p>Politician Type: {politician_type}</p>
              </div>
              <div style={{ flex: 1, paddingRight: "15px" }}>
                <p>Transaction Date: {transaction_date}</p>
                <p>Disclosure Date: {disclosure_date}</p>
              </div>
              <div style={{ flex: 1 }}>
                <p>Amount: ${transaction_amount}</p>
                <p>Stock Ticker: {stock_ticker}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default PoliticianStock;
