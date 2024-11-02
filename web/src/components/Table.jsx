import { useState, useEffect, useContext } from "react";
import {FilterContext} from 'src/contexts/Filters.js'
import TableRow from "./TableRow";
import styles from "./styles/Table.module.css";
import { search } from "src/utils/api.ts";

export default function Table() {
  const [data, setData] = useState([]);
  const [colOrder, setOrder] = useState([]);
  const [filters, _] = useContext(FilterContext);

  useEffect(() => {
    fetch(search(1,100), {
      method: "POST",
      body: JSON.stringify({}),
    })
      .then((res) => res.json())
      .then((res) => {
        setData(res.data);
        const keys = {
          full_name: { col: 0, display: "Politician" },
          transaction_date: { col: 1, display: "Date" },
          stock_ticker: { col: 2, display: "Ticker" },
          transaction_type: { col: 3, display: "Transaction" },
          transaction_amount: { col: 4, display: "Amount" },
          percent_gain: { col: 5, display: "Gain" },
        };
        setOrder(keys);
      });
  }, [filters]);

  return (
    <div style={{width:'80%', margin: '0 auto'}}>
      {data ? (
        <>
          <section className={styles.table}>
            <table style={{ width: "100%", tableLayout: "fixed" }}>
              <thead className={styles.tableHead}>
                <tr className={styles.tableRow}>
                  {data ? (
                    Object.entries(colOrder)
                      .sort((a, b) => a[1].col - b[1].col)
                      .map(([key, val]) => <th key={key}>{val.display}</th>)
                  ) : (
                    <></>
                  )}
                </tr>
              </thead>
              <tbody>
                {data.map((row, idx) => (
                  <TableRow
                    rowData={row}
                    colOrder={colOrder}
                    idx={idx}
                    key={idx}
                  />
                ))}
              </tbody>
            </table>
          </section>
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
