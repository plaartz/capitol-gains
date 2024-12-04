import { useState, useEffect } from "react";
import Slider from "react-slider";
import styles from "./styles/RangeSlider.module.css";

export default function RangeSlider({ minPrice, setMinPrice, maxPrice, setMaxPrice }) {
  const maxDisplayValue = 1000000000;
  const middleStart = 10000; // Start of emphasized range
  const middleEnd = 1000000; // End of emphasized range

   // Load saved slider values from localStorage, or default to initial state
   const loadSavedValues = () => {
    const savedMinPrice = localStorage.getItem("minPrice");
    const savedMaxPrice = localStorage.getItem("maxPrice");
    const savedSliderValue = localStorage.getItem("sliderValue");

    return {
      minPrice: savedMinPrice ? parseInt(savedMinPrice) : 0,
      maxPrice: savedMaxPrice ? parseInt(savedMaxPrice) : 1000000000,
      sliderValue: savedSliderValue
        ? JSON.parse(savedSliderValue)
        : [0, 1], // Default slider value
    };
  };

  // Initialize the state with the saved values
  const { minPrice: savedMinPrice, maxPrice: savedMaxPrice, sliderValue: savedSliderValue } = loadSavedValues();

  const [sliderValue, setSliderValue] = useState(savedSliderValue);

  // Map slider value (0 to 1) to the actual price range
  const mapToPrice = (value) => {
    if (value < 0.1) {
      // Start range (0-10%)
      return (value / 0.1) * middleStart;
    } else if (value < 0.9) {
      // Middle range (10%-90%)
      const scaledValue = (value - 0.1) / 0.8; // Normalize to [0, 1]
      return middleStart * Math.pow(middleEnd / middleStart, scaledValue); // Logarithmic interpolation
    } else {
      // End range (90%-100%)
      const scaledValue = (value - 0.9) / 0.1; // Normalize to [0, 1]
      return middleEnd + scaledValue * (maxDisplayValue - middleEnd);
    }
  };

  // Map price back to the slider value (0 to 1)
  const mapToSliderValue = (price) => {
    if (price < middleStart) {
      // Start range (0-10%)
      return (price / middleStart) * 0.1;
    } else if (price < middleEnd) {
      // Middle range (10%-90%)
      const logRatio = Math.log10(price / middleStart) / Math.log10(middleEnd / middleStart);
      return 0.1 + logRatio * 0.8; // Scale back to [0.1, 0.9]
    } else {
      // End range (90%-100%)
      return 0.9 + ((price - middleEnd) / (maxDisplayValue - middleEnd)) * 0.1;
    }
  };

  const handleSliderChange = (values) => {
    const newMinPrice = Math.round(mapToPrice(values[0]));
    const newMaxPrice = Math.round(mapToPrice(values[1]));
    setSliderValue(values); // Update internal state
    setMinPrice(newMinPrice); // Update displayed min price
    setMaxPrice(newMaxPrice); // Update displayed max price

    localStorage.setItem("minPrice", newMinPrice);
    localStorage.setItem("maxPrice", newMaxPrice);
    localStorage.setItem("sliderValue", JSON.stringify(values));
  };

  useEffect(() => {
    setMinPrice(savedMinPrice);
    setMaxPrice(savedMaxPrice);
  }, [savedMinPrice, savedMaxPrice, setMinPrice, setMaxPrice]);

  return (
    <div className={styles.container}>
      <p>Use the slider to select a price range:</p>
      <Slider
        className={styles.slider}
        value={sliderValue}
        onChange={handleSliderChange}
        min={0}
        max={1}
        step={0.001} // Small steps for smooth sliding
        thumbClassName={styles.thumb}
      />
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div>
          <label htmlFor="minPrice">Min Price:</label>
          <input
            type="number"
            id="minPrice"
            value={minPrice}
            onChange={(e) => {
              const newValue = Math.min(maxPrice, +e.target.value);
              const newSliderValue = mapToSliderValue(newValue);
              setSliderValue([newSliderValue, sliderValue[1]]);
              setMinPrice(newValue);
            }}
          />
        </div>
        <div>
          <label htmlFor="maxPrice">Max Price:</label>
          <input
            type="number"
            id="maxPrice"
            value={maxPrice}
            onChange={(e) => {
              const newValue = Math.max(minPrice, +e.target.value);
              const newSliderValue = mapToSliderValue(newValue);
              setSliderValue([sliderValue[0], newSliderValue]);
              setMaxPrice(newValue);
            }}
          />
        </div>
      </div>
    </div>
  );
}
