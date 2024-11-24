import { useState } from 'react';
import Slider from 'react-slider';
import "./styles/RangeSlider.css";

export default function RangeSlider({ minPrice, setMinPrice, maxPrice, setMaxPrice }) {
  const [values, setValues] = useState([minPrice, maxPrice]);

  const [copiedMaxPrice, _] = useState(maxPrice);

  const handleChange = (newValues) => {
    setValues(newValues);
    setMinPrice(newValues[0]);
    setMaxPrice(newValues[1]);
  };

  const getTrackStyle = () => {
    const minPercent = (values[0] / minPrice) * 100
    const maxPercent = (values[1] / maxPrice) * 100;

    return {
      background: `linear-gradient(to right, crimson ${minPercent}%, crimson ${maxPercent}%, #ccc ${maxPercent}%, #ccc 100%)`,
    };
  };

  return (
    <div className="container">
      <p>Use the slider to select a price range:</p>
      <Slider
        className="slider"
        value={values}
        onChange={handleChange}
        min={0}
        max={copiedMaxPrice}
        renderTrack={(props, state) => (
          <div {...props} className="rc-slider-track" style={getTrackStyle()} />
        )}
        renderThumb={(props, state) => (
          <div {...props} className="thumb" />
        )}
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
