import { useState, useEffect } from "react";
import TableRow from "./TableRow";
import styles from "./styles/Table.module.css";

export default function Table() {
  const [data, setData] = useState([]);
  const [colOrder, setOrder] = useState([]);

  useEffect(() => {
    fetch("/api/core/search", {
      method: "POST",
      body: JSON.stringify({
        pageNo: 1,
        pageSize: 100,
      }),
    })
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
        setData(res.data);
        setOrder();
        const keys = {
          full_name: { col: 0, display: "Politician" },
          transaction_date: { col: 1, display: "Date" },
          stock_ticker: { col: 2, display: "Ticker" },
          transaction_type: { col: 3, display: "Transaction" },
          transaction_amount: { col: 4, display: "Amount" },
          percent_gain: { col: 5, display: "Gain" },
        };
        setOrder(keys);

        console.log(res.data[0]);
      });
  }, []);

  return (
    <div className={styles.table}>
      {data ? (
        <>
          <table style={{ width: "100%", tableLayout: "fixed" }}>
            <thead className={styles.tableHead}>
              <tr className={styles.tableRow}>
                {data ? (
                  Object.entries(colOrder)
                    .sort((a, b) => a.col - b.col)
                    .map(([key, val]) => <th key={key}>{val.display}</th>)
                ) : (
                  <></>
                )}
              </tr>
            </thead>
            {data.map((row, idx) => (
              <TableRow rowData={row} colOrder={colOrder} idx={idx} key={idx}/>
            ))}
          </table>
          <section className={styles.paginationFooter}>
            <div>Pagination</div>
            <div>Page size</div>
          </section>
        </>
      ) : (
        <></>
      )}
    </div>
  );
}
