import React from "react";

const fields = [
  { name: "N", label: "Nitrogen (N)" },
  { name: "P", label: "Phosphorus (P)" },
  { name: "K", label: "Potassium (K)" },
  { name: "temperature", label: "Temperature (C)" },
  { name: "humidity", label: "Humidity (%)" },
  { name: "ph", label: "Soil pH" },
  { name: "rainfall", label: "Rainfall (mm)" },
];

export default function InputForm({ values, onChange, onSubmit, disabled }) {
  return (
    <form className="panel" onSubmit={onSubmit}>
      <h2>Soil and Climate Inputs</h2>
      <div className="grid">
        {fields.map((field) => (
          <label key={field.name} className="field">
            <span>{field.label}</span>
            <input
              type="number"
              name={field.name}
              value={values[field.name]}
              onChange={onChange}
              step="any"
              required
            />
          </label>
        ))}
      </div>
      <button type="submit" disabled={disabled}>
        {disabled ? "Analyzing..." : "Recommend Seeds"}
      </button>
    </form>
  );
}
