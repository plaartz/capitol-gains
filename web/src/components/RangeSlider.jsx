import "./styles/TextBox.css";
import "./styles/RangeSlider.css";

export default function RangeSlider({ minPrice, setMinPrice, maxPrice, setMaxPrice }) {

  const handleMinSliderChange = (e) => {
    const newValue = Number(e.target.value);
    if (newValue < maxPrice) {
      setMinPrice(newValue);
    }
  };

  const handleMaxSliderChange = (e) => {
    const newValue = Number(e.target.value);
    if (newValue > minPrice) {
      setMaxPrice(newValue);
    }
  };

  const handleMinPriceChange = (e) => {
    const newValue = e.target.value === "" ? 0 : Number(e.target.value);
    if (newValue < maxPrice) {
      setMinPrice(newValue);
    }
  };

  const handleMaxPriceChange = (e) => {
    const newValue = e.target.value === "" ? 10000 : Number(e.target.value);
    if (newValue > minPrice) {
      setMaxPrice(newValue);
    }
  };

  return (
    <div className="range_container">
      <div className="sliders_control">
        <input
          id="fromSlider"
          type="range"
          min={minPrice}
          max={maxPrice}
          value={minPrice}
          onChange={handleMinSliderChange}
        />
        <input
          id="toSlider"
          type="range"
          min={minPrice}
          max={maxPrice}
          value={maxPrice}
          onChange={handleMaxSliderChange}
        />
      </div>
      <div className="form_control">
        <div className="form_control_container">
          <div className="form_control_container__time">Min</div>
          <input
            className="form_control_container__time__input"
            type="number"
            min="0"
            max={maxPrice}
            value={minPrice}
            onChange={handleMinPriceChange}
            placeholder="0"
          />
        </div>
        <div className="form_control_container">
          <div className="form_control_container__time">Max</div>
          <input
            className="form_control_container__time__input"
            type="number"
            min={minPrice}
            max="10000"
            value={maxPrice}
            onChange={handleMaxPriceChange}
            placeholder="10000"
          />
        </div>
      </div>
    </div>
  );
}

