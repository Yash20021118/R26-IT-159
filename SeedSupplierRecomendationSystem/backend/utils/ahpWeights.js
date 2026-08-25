const calculateAHPWeights = (pairwiseMatrix) => {
  const n = pairwiseMatrix.length;

  // Step 1: Calculate column sums
  const columnSums = new Array(n).fill(0);

  for (let j = 0; j < n; j++) {
    for (let i = 0; i < n; i++) {
      columnSums[j] += pairwiseMatrix[i][j];
    }
  }

  // Step 2: Normalize pairwise matrix
  const normalizedMatrix = pairwiseMatrix.map((row) =>
    row.map((value, j) => value / columnSums[j])
  );

  // Step 3: Calculate priority vector
  const weights = normalizedMatrix.map(
    (row) =>
      row.reduce((sum, value) => sum + value, 0) / n
  );

  return weights;
};

module.exports = calculateAHPWeights;