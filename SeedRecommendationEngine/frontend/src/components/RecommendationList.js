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
      <h3>Top Suitability Recommendations</h3>
      <div className="recommendations">
        {recommendations.map((item) => (
          <div key={item.crop} className="recommendation-row" style={{ marginBottom: "16px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span className="crop-label" style={{ textTransform: "capitalize", fontWeight: "bold" }}>{item.crop}</span>
              <span className="crop-score">{item.confidence}% Suitable</span>
            </div>
            <div className="bar" style={{ marginTop: "6px", marginBottom: "8px" }}>
              <span style={{ width: `${item.confidence}%` }} />
            </div>
            <div style={{ textAlign: "right" }}>
              <a
                href={`http://localhost:5000/guidance/${encodeURIComponent(item.crop)}?confidence=${item.confidence}`}
                target="_blank"
                rel="noreferrer"
                style={{
                  fontSize: "12px",
                  color: "#1a7a4a",
                  fontWeight: "600",
                  textDecoration: "none"
                }}
              >
                📖 View After Care Guidance &rarr;
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

