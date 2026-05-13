const API_BASE =
  process.env.REACT_APP_API_BASE || "http://localhost:8000";

export async function fetchPrediction(payload) {
  const response = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Prediction request failed.");
  }

  return response.json();
}

export async function fetchRecommendations(payload) {
  const response = await fetch(`${API_BASE}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Recommendation request failed.");
  }

  return response.json();
}
