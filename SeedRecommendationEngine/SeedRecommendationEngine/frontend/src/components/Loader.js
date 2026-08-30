import React from "react";

export default function Loader() {
  return (
    <div className="loader">
      <span className="dot" />
      <span className="dot" />
      <span className="dot" />
      <p>Generating recommendations...</p>
    </div>
  );
}
