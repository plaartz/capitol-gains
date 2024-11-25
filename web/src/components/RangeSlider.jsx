import { useState } from 'react';
import Slider from 'react-slider';
import styles from "./styles/RangeSlider.module.css";

export default function RangeSlider({ minPrice, setMinPrice, maxPrice, setMaxPrice }) {
  const [values, setValues] = useState([minPrice, maxPrice]);

  const [copiedMaxPrice, _] = useState(maxPrice);

  const handleChange = (newValues) => {
    setValues(newValues);
    setMinPrice(newValues[0]);
    setMaxPrice(newValues[1]);
  };

  return (
    <div className={styles.container}>
      <p>Use the slider to select a price range:</p>
      <Slider
        className={styles.slider}
        value={values}
        onChange={handleChange}
        min={0}
        max={copiedMaxPrice}
        thumbClassName={styles.thumb}
      />
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <div>
          <label htmlFor="minPrice">Min Price:</label>
          <input
            type="number"
            id="minPrice"
            value={values[0]}
            onChange={(e) => handleChange([+e.target.value, values[1]])}
          />
        </div>
        <div>
          <label htmlFor="maxPrice">Max Price:</label>
          <input
            type="number"
            id="maxPrice"
            value={values[1]}
            onChange={(e) => handleChange([values[0], +e.target.value])}
          />
        </div>
      </div>
    </div>
  );
}
