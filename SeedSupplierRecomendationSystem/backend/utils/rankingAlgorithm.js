const calculateTOPSIS = (suppliers, weights) => {
  if (!suppliers || suppliers.length === 0) {
    return [];
  }

  const criteria = [
    {
      key: "price",
      type: "cost",
    },
    {
      key: "rating",
      type: "benefit",
    },
    {
      key: "distance_km",
      type: "cost",
    },
    {
      key: "stock",
      type: "benefit",
    },
  ];

  // 1. Construct decision matrix

  const matrix = suppliers.map((supplier) =>
    criteria.map((criterion) => {
      const value = Number(supplier[criterion.key]);

      if (!Number.isFinite(value)) {
        throw new Error(
          `Invalid ${criterion.key} value for supplier ${supplier.supplierName}`,
        );
      }

      return value;
    }),
  );

  // 2. Vector normalization
  // rij = xij / sqrt(sum(xij^2))


  const normalizedMatrix = matrix.map(() => new Array(criteria.length).fill(0));

  for (let j = 0; j < criteria.length; j++) {
    const denominator = Math.sqrt(
      matrix.reduce((sum, row) => {
        return sum + Math.pow(row[j], 2);
      }, 0),
    );

    for (let i = 0; i < matrix.length; i++) {
      normalizedMatrix[i][j] =
        denominator === 0 ? 0 : matrix[i][j] / denominator;
    }
  }

  
  // 3. Weighted normalized matrix
  //
  // vij = rij * wj
  

  const weightedMatrix = normalizedMatrix.map((row) =>
    row.map((value, j) => {
      const criterionKey = criteria[j].key;
      return value * weights[criterionKey];
    }),
  );

  // 4. Positive and Negative Ideal Solutions

  const positiveIdeal = [];
  const negativeIdeal = [];

  for (let j = 0; j < criteria.length; j++) {
    const values = weightedMatrix.map((row) => row[j]);

    if (criteria[j].type === "benefit") {
      positiveIdeal[j] = Math.max(...values);
      negativeIdeal[j] = Math.min(...values);
    } else {
      // Cost criterion: lower value is better
      positiveIdeal[j] = Math.min(...values);
      negativeIdeal[j] = Math.max(...values);
    }
  }

  // 5. Calculate distances and TOPSIS score

  const results = suppliers.map((supplier, i) => {
    const positiveDistance = Math.sqrt(
      weightedMatrix[i].reduce((sum, value, j) => {
        return sum + Math.pow(value - positiveIdeal[j], 2);
      }, 0),
    );

    const negativeDistance = Math.sqrt(
      weightedMatrix[i].reduce((sum, value, j) => {
        return sum + Math.pow(value - negativeIdeal[j], 2);
      }, 0),
    );

    // Ci = Si- / (Si+ + Si-)

    const topsisScore =
      positiveDistance + negativeDistance === 0
        ? 0
        : negativeDistance / (positiveDistance + negativeDistance);

    return {
      ...supplier.toObject(),

      score: Number(topsisScore.toFixed(4)),
    };
  });

  // 6. Rank suppliers

  return results
    .sort((a, b) => b.score - a.score)
    .map((supplier, index) => ({
      ...supplier,
      rank: index + 1,
    }));
};

module.exports = calculateTOPSIS;
