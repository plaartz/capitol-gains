import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import styles from "./styles/Transaction.module.css";
import StockGraph from "../components/StockGraph";

export default function Transaction() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [tradeData, setData] = useState({});
  const [priceData, setPriceData] = useState([]);

  useEffect(() => {
    fetch(`/api/core/search?id=${id}`,{method:"POST",body:JSON.stringify({})})
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else throw new Error("bad request");
      })
      .then((res) => {
        setData(res.data[0]);
      })
      .catch((_) => {
        navigate("/404");
      });
    fetch(`/api/core/get-transaction-price-details?id=${id}`)
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else throw new Error("bad request");
      }).then((res) => {
        setPriceData(res.prices);
      }).catch((_) => {
        console.log("error fetching prices");
      });
  }, [id]);

  if (!tradeData) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.container}>
      <section className={""}>
        <Link to="/transactions" className={styles.backLink}>
          {"<-"}
          Back to All Trades
        </Link>
      </section>
      <section>
        <section>
          <h1 className={styles.title}>
            {tradeData.full_name} bought ${tradeData.stock_ticker} on{" "}
            {tradeData.transaction_date}
          </h1>
        </section>
        <section className={styles.grid}>
          <section className={styles.card}>
            <div className={styles.cardHeader}>
              <h2 className={styles.cardTitle}>Trade Details</h2>
            </div>
            <div className={styles.cardContent}>
              <dl className={styles.detailsList}>
                <div className={styles.detailItem}>
                  <dt className={styles.detailLabel}>Transaction</dt>
                  <dd className={styles.detailValue}>
                    {tradeData.transaction_type}
                  </dd>
                </div>

                <div className={styles.detailItem}>
                  <dt className={styles.detailLabel}>Amount</dt>
                  <dd className={styles.detailValue}>
                    {tradeData.transaction_amount}
                  </dd>
                </div>

                <div className={styles.detailItem}>
                  <dt className={styles.detailLabel}>Stock</dt>
                  <dd className={styles.detailValue}>
                    <div>{tradeData.stock_ticker}</div>
                    <div className={styles.smallText}>stock details...</div>
                  </dd>
                </div>

                <div className={styles.detailItem}>
                  <dt className={styles.detailLabel}>Politician</dt>
                  <dd className={styles.detailValue}>
                    <div>{tradeData.full_name}</div>
                    <div className={styles.smallText}>
                      politician details...
                    </div>
                  </dd>
                </div>

                <div className={styles.detailItem}>
                  <dt className={styles.detailLabel}>Traded</dt>
                  <dd className={styles.detailValue}>
                    {tradeData.transaction_date}
                  </dd>
                </div>

                <div className={styles.detailItem}>
                  <dt className={styles.detailLabel}>Disclosed</dt>
                  <dd className={styles.detailValue}>
                    {tradeData.disclosure_date}
                  </dd>
                </div>
              </dl>
            </div>
          </section>

          <section className={styles.card}>
            <div className={styles.cardHeader}>
              <h2 className={styles.cardTitle}>
                ${tradeData.stock_ticker} Stock Chart
              </h2>
            </div>
            <section className={styles.cardContent}>
              <section className={styles.chartPlaceHolder}>
                <StockGraph data={priceData} transaction={true} transaction_details={tradeData}/>
              </section>

              <section className={styles.metricsGrid}>
                <div className={styles.metricCard}>
                  <div className={styles.metricLabel}>Percent gain</div>
                  <div
                    className={styles.metricValue}
                    style={{
                      color: tradeData.percent_gain >= 0 ? "green" : "red",
                    }}
                  >
                    {tradeData.percent_gain}
                  </div>
                </div>

                <div className={styles.metricCard}>
                  <div className={styles.metricLabel}>
                    {tradeData.stock_ticker} Price change since trade
                  </div>
                  <div
                    className={styles.metricValue}
                    style={{
                      color: tradeData.percent_gain >= 0 ? "green" : "red",
                    }}
                  >
                    0
                  </div>
                </div>
              </section>
            </section>
          </section>
        </section>
      </section>
    </div>
  );
}
