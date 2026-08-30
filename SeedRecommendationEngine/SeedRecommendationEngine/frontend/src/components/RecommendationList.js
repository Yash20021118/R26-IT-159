import React from "react";

export default function RecommendationList({ recommendations }) {
  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="card empty">
        <h3>Top 3 Recommendations</h3>
        <p>Submit inputs to see ranked recommendations.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3>Top 3 Recommendations</h3>
      <div className="recommendations">
        {recommendations.map((item) => (
          <div key={item.crop} className="recommendation-row">
            <div>
              <span className="crop-label">{item.crop}</span>
              <span className="crop-score">{item.confidence}%</span>
            </div>
            <div className="bar">
              <span style={{ width: `${item.confidence}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
