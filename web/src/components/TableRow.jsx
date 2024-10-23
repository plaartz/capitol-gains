import { useEffect } from "react";
import styles from "./styles/Table.module.css";

export default function TableRow({ rowData, colOrder = {}, idx = 0 }) {
  useEffect(() => {
    console.log(rowData);
  }, []);

  return (
    <tr className={styles.tableRow} style={{}}>
      {Object.entries(rowData)
        .filter(([key, col]) => key in colOrder)
        .sort(([key_a, val_a], [key_b, val_b]) => {
          // console.log(colOrder[key_a],colOrder[key_b])
          return colOrder[key_a].col - colOrder[key_b].col;
        })
        .map(([key, col]) => {
            const style = {}
            if (key == 'percent_gain') {
                style['color'] = col >= 0 ? 'green' : 'red'
            }
          return <td id={styles[key] ?? ""} style={style}>{col ?? "--"}</td>;
        })}
    </tr>
  );
}
