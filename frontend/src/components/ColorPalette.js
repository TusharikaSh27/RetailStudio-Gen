import React, { useState } from "react";
import "./ColorPalette.css";

export default function ColorPalette({ colors = [], onColorSelect }) {
  const [selectedColor, setSelectedColor] = useState(null);

  const handleSelect = (color) => {
    setSelectedColor(color);
    onColorSelect(color);
  };

  return (
    <div className="palette-container">
      <h3>🎨 Color Palette</h3>

      <div className="swatch-row">
        {colors.map((c, i) => (
          <div
            key={i}
            className={`swatch ${selectedColor === c ? "active" : ""}`}
            style={{ backgroundColor: c }}
            onClick={() => handleSelect(c)}
          />
        ))}
      </div>

      <div className="manual-picker">
        <label>Pick Custom Color</label>
        <input
          type="color"
          onChange={(e) => handleSelect(e.target.value)}
        />
      </div>
    </div>
  );
}
