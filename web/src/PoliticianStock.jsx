import React from 'react';

// JSON data provided
const jsonData = {
  "data": [
    {
      "transaction_amount": "2000",
      "transaction_date": "2024-10-01",
      "disclosure_date": "2024-10-02",
      "transaction_type": "Purchase",
      "full_name": "Chris L. Anderson",
      "politician_type": "House",
      "politician_house": "D",
      "stock_ticker": "AAPL",
      "stock_price": 226.21,
      "percent_gain": 0.0,
      "stock_description": "Provides consumer electronics, software, and services."
    },
    {
      "transaction_amount": "5000",
      "transaction_date": "2024-09-15",
      "disclosure_date": "2024-09-16",
      "transaction_type": "Sale",
      "full_name": "Susan M. Walker",
      "politician_type": "Senate",
      "politician_house": "R",
      "stock_ticker": "TSLA",
      "stock_price": 759.12,
      "percent_gain": 15.3,
      "stock_description": "Electric vehicle and clean energy company."
    },
    {
      "transaction_amount": "1500",
      "transaction_date": "2024-08-22",
      "disclosure_date": "2024-08-23",
      "transaction_type": "Purchase",
      "full_name": "John B. Doe",
      "politician_type": "House",
      "politician_house": "I",
      "stock_ticker": "AMZN",
      "stock_price": 3345.55,
      "percent_gain": 0.0,
      "stock_description": "Online retail and cloud computing company."
    }
  ],
  "size": 3
};

function PoliticianStock() {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Politician Stock Transactions</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        {jsonData.data.map((transaction, index) => {
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
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                border: '1px solid black',
                borderRadius: '5px',
                padding: '15px',
                width: '100%',
                boxSizing: 'border-box',
              }}
            >
              <div style={{ flex: 1, paddingRight: '15px' }}>
                <h3>{full_name}</h3>
                <p>Transaction Type: {transaction_type}</p>
                <p>Politician Type: {politician_type}</p>
              </div>
              <div style={{ flex: 1, paddingRight: '15px' }}>
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
