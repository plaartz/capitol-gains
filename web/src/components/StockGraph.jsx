import { useState, useEffect } from "react";

import {
  LineChart,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Line,
  ReferenceLine
} from "recharts";

export default function StockGraph({
  data,
  transaction = false,
  transaction_details = {},
}) {
  const [min, setMin] = useState(0)
  const [max, setMax] = useState(Infinity)

  useEffect(()=>{
    const sortedData = data?.toSorted((a, b)=>a["price"] - b["price"])

    let minPrice = sortedData.at(0)?.price ?? 10
    setMin(minPrice - 10)
    setMax((sortedData.at(-1)?.price ?? Infinity) + 10)
  },[data])

  if (!data.length) {
    return <div>Loading...</div>;
  }
  
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
        <XAxis dataKey="date" angle={10} tick={false} />
        <YAxis domain={[min, max]} />
        <Line type="linear" dataKey="price" dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
