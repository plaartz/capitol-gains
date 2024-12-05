import { useState, useEffect, useContext } from "react";
import { useSearchParams } from "react-router-dom";
import { FilterContext } from "src/contexts/Filters.js";
import TableRow from "./TableRow";
import styles from "./styles/Table.module.css";
import { search } from "src/utils/api.ts";
import Pagination from "./Pagination";
import PageSize from "./PageSize";

export default function Table() {
  const [isIdle, setIdle] = useState(true);
  const [searchParams, setSearchParams] = useSearchParams();
  const [data, setData] = useState([]);
  const [colOrder, setOrder] = useState([]);
  const [filters, updateFilter] = useContext(FilterContext);
  const [totalPosts, setTotal] = useState(0);
  const [pageSize, setPageSize] = useState(
    Number(searchParams.get("pageSize")) || 100
  );
  const [currPageNo, setPageNo] = useState(
    Number(searchParams.get("pageNo")) || 1
  );
  const [isLoading, setLoading] = useState(true);
  const [orderBy, setOrderBy] = useState("transaction_date");
  const [direction, setDirection] = useState("DESC");

  useEffect(() => {
    const savedFilters = JSON.parse(localStorage.getItem("filters"));
    const fullName = savedFilters?.fullName || "";
    const stock = savedFilters?.stock || "";
    const startDate = savedFilters?.startDate || null;
    const endDate = savedFilters?.endDate || null;
    const minPrice = savedFilters?.minPrice || 0;
    const maxPrice = savedFilters?.maxPrice || 1000000000;
    const purchaseSelected = savedFilters?.purchaseSelected || false;
    const saleSelected = savedFilters?.saleSelected || false;
    const positiveGainSelected = savedFilters?.positiveGainSelected || false;
    const negativeGainSelected = savedFilters?.negativeGainSelected || false;
    const noGainSelected = savedFilters?.noGainSelected || false;
    if (savedFilters) {
      updateFilter("full_name", fullName);
      updateFilter("stock_ticker", stock);
      updateFilter("start_date", startDate);
      updateFilter("end_date", endDate);
      updateFilter("min_price", minPrice);
      updateFilter("max_price", maxPrice);
      updateFilter("is_purchase", purchaseSelected);
      updateFilter("is_sale", saleSelected);
      updateFilter("positive_gain", positiveGainSelected);
      updateFilter("negative_gain", negativeGainSelected);
      updateFilter("no_gain", noGainSelected);    }
  }, [])

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


  function changeOrder(key) {
    setIdle(false);
    if (orderBy == key) {
      setDirection((prev) => (prev == "DESC" ? "ASC" : "DESC"));
    } else {
      setDirection("DESC");
      setOrderBy(key);
    }
    setIdle(true);
  }


  useEffect(() => {
    if (!isLoading & isIdle) {
      fetch(search(currPageNo, pageSize, orderBy, direction), {
        method: "POST",
        body: JSON.stringify(filters),
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
  }, [isLoading, filters, pageSize, currPageNo, orderBy, direction]);

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
                      .map(([key, val]) => (
                        <th
                          onClick={() => {
                            changeOrder(key);
                          }}
                          key={key}
                          className={styles.headerKey}
                        >
                          {val.display}{" "}
                          {orderBy === key
                            ? direction === "DESC"
                              ? "\u2B07"
                              : "\u2B06"
                            : undefined}
                        </th>
                      ))
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
