const API_BASE =
  process.env.REACT_APP_API_BASE || "http://127.0.0.1:8000";

export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE}/health`, { method: "GET" });
    if (!response.ok) return false;
    const data = await response.json();
    return data.status === "ok";
  } catch (err) {
    return false;
  }
}

export async function fetchChatStatus() {
  const response = await fetch(`${API_BASE}/chat/status`, { method: "GET" });
  if (!response.ok) {
    throw new Error("Unable to reach Agri-SLM status endpoint.");
  }
  return response.json();
}

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

export async function sendChatMessage(message, language = "auto", sessionId = null) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      language,
      session_id: sessionId,
    }),
  });

  if (!response.ok) {
    throw new Error("Chat request failed. Please ensure the backend is running at " + API_BASE);
  }

  return response.json();
}

export async function uploadChatFile(file, message = "", language = "auto", sessionId = null) {
  const formData = new FormData();
  formData.append("file", file);
  if (message) formData.append("message", message);
  if (language) formData.append("language", language);
  if (sessionId) formData.append("session_id", sessionId);

  const response = await fetch(`${API_BASE}/chat/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("File upload failed. Please ensure the backend is running at " + API_BASE);
  }

  return response.json();
}
