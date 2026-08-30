import React, { useState, useEffect } from "react";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import RecommendationList from "./components/RecommendationList";
import Loader from "./components/Loader";
import ErrorBanner from "./components/ErrorBanner";
import AgriSLMChatPage from "./components/AgriSLMChatPage";
import { fetchPrediction, fetchRecommendations } from "./api";

const initialState = {
  N: 90,
  P: 42,
  K: 43,
  temperature: 21,
  humidity: 82,
  ph: 6.5,
  rainfall: 202,
};

export default function App() {
  const [currentPage, setCurrentPage] = useState(() => {
    return window.location.hash === "#/agri-slm" ? "agri-slm" : "recommendation";
  });

  const [values, setValues] = useState(initialState);
  const [prediction, setPrediction] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Sync state with URL hash
  useEffect(() => {
    const handleHashChange = () => {
      if (window.location.hash === "#/agri-slm") {
        setCurrentPage("agri-slm");
      } else {
        setCurrentPage("recommendation");
      }
    };
    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  const navigateTo = (page) => {
    setCurrentPage(page);
    window.location.hash = page === "agri-slm" ? "#/agri-slm" : "#/";
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setValues((prev) => ({ ...prev, [name]: Number(value) }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const [predictionData, recommendationData] = await Promise.all([
        fetchPrediction(values),
        fetchRecommendations(values),
      ]);
      setPrediction(predictionData);
      setRecommendations(recommendationData.recommendations || []);
    } catch (err) {
      setError("Unable to fetch recommendations. Check if the backend API is running at http://localhost:8001.");
    } finally {
      setLoading(false);
    }
  };

  // If on the dedicated Agri-SLM Chatbot page, render full-screen workspace
  if (currentPage === "agri-slm") {
    return <AgriSLMChatPage onNavigateHome={() => navigateTo("recommendation")} />;
  }

  return (
    <div className="app">
      {/* Top Navbar */}
      <nav className="app-navbar">
        <div className="nav-brand">
          <span className="nav-logo">🌾</span>
          <div className="nav-title-group">
            <span className="nav-title">Smart Agriculture Decision Support System</span>
            <span className="nav-subtitle">Sri Lanka Agro-Ecological Intelligence</span>
          </div>
        </div>

        <div className="nav-links">
          <button
            className={`nav-tab-link ${currentPage === "recommendation" ? "active" : ""}`}
            onClick={() => navigateTo("recommendation")}
          >
            <span>🌾 Seed Recommendation Engine</span>
          </button>
          <button
            className={`nav-tab-link ${currentPage === "agri-slm" ? "active" : ""}`}
            onClick={() => navigateTo("agri-slm")}
          >
            <span>🤖 Agri-SLM Research Assistant</span>
            <span className="nav-pill">Trilingual AI</span>
          </button>
        </div>
      </nav>

      {/* Hero Header */}
      <header className="hero">
        <div>
          <p className="eyebrow">Sri Lanka Smart Agriculture Decision Support</p>
          <h1>Seed Recommendation & Agronomic AI Engine</h1>
          <p>
            An end-to-end intelligent agricultural intelligence suite combining ML soil classification,
            ranked seed recommendations, and an offline trilingual Small Language Model (SLM) conversational suite.
          </p>
        </div>
      </header>

      {/* Feature Spotlight Card for Dedicated Agri-SLM Workspace */}
      <section className="spotlight-wrapper">
        <div className="agri-slm-spotlight-card">
          <div className="spotlight-text">
            <div className="spotlight-badge-row">
              <span className="spotlight-badge">🌾 RESEARCH COMPONENT SPOTLIGHT</span>
              <span className="spotlight-privacy-tag">🔒 100% Offline & Private (No API Keys)</span>
            </div>
            <h2>Trilingual Agri-SLM Conversational Research Assistant</h2>
            <p>
              A localized agricultural small language model trained to assist farmers and agronomists across
              Sri Lanka's 25 districts and 46 agro-ecological zones. Supports laboratory soil test report ingestion (PDF/CSV),
              nutrient deficiency remediation, and seasonal Maha/Yala crop planning in Sinhala (සිංහල), English, and Tamil (தமிழ்).
            </p>
            <div className="spotlight-pills">
              <span className="pill-item">🇱🇰 25 Districts & AERs</span>
              <span className="pill-item">📄 PDF/CSV Soil Lab Reports</span>
              <span className="pill-item">🎯 99.5% Accuracy Model</span>
              <span className="pill-item">⚡ Sub-10ms Inference</span>
            </div>
          </div>
          <div className="spotlight-action">
            <button className="launch-agri-slm-btn" onClick={() => navigateTo("agri-slm")}>
              Launch Agri-SLM Workspace →
            </button>
          </div>
        </div>
      </section>

      {/* Main Content Area: Seed Recommendation Engine */}
      <main className="content">
        <div className="section-title-bar">
          <h3>Soil & Climatic Parameter Input</h3>
          <p>Input field measurements to evaluate crop suitability ranking using the trained Random Forest classifier.</p>
        </div>

        <InputForm
          values={values}
          onChange={handleChange}
          onSubmit={handleSubmit}
          disabled={loading}
        />

        <section className="results">
          {loading && <Loader />}
          {!loading && (
            <>
              <ResultCard prediction={prediction} />
              <RecommendationList recommendations={recommendations} />
            </>
          )}
        </section>

        <ErrorBanner message={error} />
      </main>

      <footer>
        <p>
          Final Year Research Prototype: Multimodal Soil Classification, Agronomic Reasoning & Custom Trilingual SLM.
        </p>
      </footer>
    </div>
  );
}
