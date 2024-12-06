import Table from "src/components/Table";
import SearchTools from "src/components/SearchTools"

function PoliticianStock() {
  return (
    <div style={{ padding: "20px" }}>
      <h2>Politician Stock Transactions</h2>
      <SearchTools />
      <Table />
    </div>
  );
}

export default PoliticianStock;
