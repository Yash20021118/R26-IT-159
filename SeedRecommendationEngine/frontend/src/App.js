import React, { useState } from "react";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import RecommendationList from "./components/RecommendationList";
import Loader from "./components/Loader";
import ErrorBanner from "./components/ErrorBanner";
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
  const [values, setValues] = useState(initialState);
  const [prediction, setPrediction] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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
      setError("Unable to fetch recommendations. Check the API and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">Smart Agriculture Decision Support</p>
          <h1>Seed Recommendation Engine</h1>
          <p>
            Enter soil and climate parameters to get ranked crop recommendations
            with confidence scores.
          </p>
        </div>
      </header>

      <main className="content">
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
        <p>Research prototype for crop suitability intelligence.</p>
      </footer>
    </div>
  );
}
