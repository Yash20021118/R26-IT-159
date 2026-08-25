const Supplier = require("../models/Supplier");
const calculateTOPSIS = require("../utils/rankingAlgorithm");

// AHP-derived weights
// TEMPORARY values for development/testing.
// Final values must come from your AHP expert evaluation.

const ahpWeights = {
  price: 0.30,
  rating: 0.30,
  distance_km: 0.20,
  stock: 0.20,
};

const getRankedSuppliers = async (req, res) => {
  try {
    const {
      seedType,
      region,
      minimumRating,
      maximumDistance,
    } = req.body;

    // -----------------------------------------
    // 1. Rule-based eligibility filtering
    // -----------------------------------------

    const query = {
      seedType,
      region,
    };

    if (minimumRating !== undefined) {
      query.rating = {
        $gte: Number(minimumRating),
      };
    }

    if (maximumDistance !== undefined) {
      query.distance_km = {
        $lte: Number(maximumDistance),
      };
    }

    const suppliers = await Supplier.find(query);

    if (suppliers.length === 0) {
      return res.json([]);
    }

    // -----------------------------------------
    // 2. TOPSIS ranking
    // -----------------------------------------

    const rankedSuppliers = calculateTOPSIS(
      suppliers,
      ahpWeights
    );

    res.json(rankedSuppliers);

  } catch (error) {
    console.error(error);

    res.status(500).json({
      message: error.message,
    });
  }
};

module.exports = {
  getRankedSuppliers,
};