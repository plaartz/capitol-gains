import {
  LineChart,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Line,
  ReferenceLine,
  Label,
} from "recharts";

export default function StockGraph({
  ticker,
  data,
  transaction = false,
  transaction_details = {},
}) {
  return (
    <ResponsiveContainer width="100%" height="100%" aspect={2}>
      <LineChart data={data}>
        {transaction ? (
          <>
            <ReferenceLine x={transaction_details.transaction_date} />
          </>
        ) : (
          <></>
        )}
        <XAxis dataKey="date" />
        <YAxis />
        <Line type="linear" dataKey="price" dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
