import { useRef, useState } from "react";
import { LineChart, ResponsiveContainer, XAxis, YAxis, Line } from 'recharts'

export default function StockGraph({ticker, data}) {
    return (
      <ResponsiveContainer width="100%" height="100%" aspect={2}>
        <LineChart data={data}>

          <XAxis dataKey="date" />
          <YAxis />
          <Line type="linear" dataKey="price" dot={false}/>
        </LineChart>
      </ResponsiveContainer>
    );

}