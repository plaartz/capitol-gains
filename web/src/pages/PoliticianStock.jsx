import Table from "src/components/Table";
import { useContext, useEffect, useState } from "react";
import { FilterContext } from "src/contexts/Filters";

function PoliticianStock() {
  return (
    <div style={{ padding: "20px" }}>
      <h2>Politician Stock Transactions</h2>
      <Table />
    </div>
  );
}

export default PoliticianStock;
