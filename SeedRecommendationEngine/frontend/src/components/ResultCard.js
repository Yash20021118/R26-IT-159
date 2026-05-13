import React from "react";

export default function ResultCard({ prediction }) {
  if (!prediction) {
    return (
      <div className="card empty">
        <h3>Best Match</h3>
        <p>Enter soil parameters to see the best crop recommendation.</p>
      </div>
    );
  }

  return (
    <div className="card highlight">
      <h3>Best Match</h3>
      <div className="crop-name">{prediction.crop}</div>
      <div className="confidence">{prediction.confidence}% confidence</div>
    </div>
  );
}
