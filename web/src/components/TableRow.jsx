import { useEffect } from "react";
import styles from "./styles/Table.module.css";

export default function TableRow({ rowData, colOrder = {}, idx = 0 }) {
  useEffect(() => {
    console.log(rowData, idx);
  }, [rowData, idx]);

  return (
    <tr className={styles.tableRow} style={{}}>
      {Object.entries(rowData)
        .filter(([key, _]) => key in colOrder)
        .sort(([key_a, _a], [key_b, _b]) => {
          // console.log(colOrder[key_a],colOrder[key_b])
          return colOrder[key_a].col - colOrder[key_b].col;
        })
        .map(([key, col]) => {
            const style = {}
            if (key == 'percent_gain') {
                style['color'] = col >= 0 ? 'green' : 'red'
            }
            if (key == 'transaction_amount') {
                return <td id={styles[key] ?? ""} style={style} key={key}>
                    ${col.replace("-","-$")}
                </td>;
            }
          return <td id={styles[key] ?? ""} style={style} key={key}>{col ?? "--"}</td>;
        })}
    </tr>
  );
}