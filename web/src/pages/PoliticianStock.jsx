import { useEffect, useState } from "react";
import Table from "src/components/Table";

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
  },[]);
  return (
    <div style={{ padding: "20px" }}>
      <h2>Politician Stock Transactions</h2>
      <Table />
    </div>
  );
}

export default PoliticianStock;
