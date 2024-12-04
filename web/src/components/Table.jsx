import { useState, useEffect, useContext } from "react";
import { useSearchParams } from "react-router-dom";
import { FilterContext } from "src/contexts/Filters.js";
import TableRow from "./TableRow";
import styles from "./styles/Table.module.css";
import { search } from "src/utils/api.ts";
import Pagination from "./Pagination";
import PageSize from "./PageSize";

export default function Table() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [data, setData] = useState([]);
  const [colOrder, setOrder] = useState([]);
  const [filters, _] = useContext(FilterContext);
  const [totalPosts, setTotal] = useState();
  const [pageSize, setPageSize] = useState(
    Number(searchParams.get("pageSize")) || 100
  );
  const [currPageNo, setPageNo] = useState(
    Number(searchParams.get("pageNo")) || 1
  );
  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    if (searchParams.size > 0) {
      setPageNo((prev) => parseInt(searchParams.get("pageNo") ?? prev));
      setPageSize((prev) => parseInt(searchParams.get("pageSize") ?? prev));
    }

    setLoading(false);
  }, [location.search]);

  useEffect(() => {
    if (!isLoading) {
      if (
        searchParams.has("pageSize") ||
        searchParams.get("pageSize") != pageSize
      ) {
        setSearchParams((params) => {
          params.set("pageSize", pageSize);
          return params;
        });
      }
    }
  }, [pageSize]);

  useEffect(() => {
    if (!isLoading) {
      if (
        searchParams.has("pageNo") ||
        searchParams.get("pageNo") != currPageNo
      ) {
        setSearchParams((params) => {
          params.set("pageNo", currPageNo);
          return params;
        });
      }
    }
  }, [currPageNo]);

  useEffect(() => {
    if (!isLoading) {
      fetch(search(currPageNo, pageSize), {
        method: "POST",
        body: JSON.stringify({}),
      })
        .then((res) => res.json())
        .then((res) => {
          setData(res.data);
          setTotal(res.size);
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
    }
  }, [isLoading, filters, pageSize, currPageNo]);

  const paginate = (pageNumber) => {
    if (pageNumber === 0) {
      setPageNo(currPageNo - 1);
    } else if (pageNumber === -1) {
      setPageNo(currPageNo + 1);
    } else {
      setPageNo(pageNumber);
    }
  };

  const pageSizer = (pageSizeSelected) => {
    setPageSize(pageSizeSelected);
    setPageNo(1);
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }
  return (
    <div style={{ width: "80%", margin: "0 auto" }}>
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
            <div className={styles.paginating}>
              <Pagination
                totalPosts={totalPosts}
                pageSize={pageSize}
                currPageNo={currPageNo}
                paginate={paginate}
              />
            </div>
            <div className={styles.pageSizeSelect}>
              <PageSize pageSizer={pageSizer} />
            </div>
          </section>
        </>
      ) : (
        <></>
      )}
    </div>
  );
}
