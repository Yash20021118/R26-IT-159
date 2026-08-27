const mongoose = require("mongoose");

const supplierSchema = new mongoose.Schema(
  {
    supplierName: {
      type: String,
      required: true,
    },

    seedType: {
      type: String,
      required: true,
    },

    region: {
      type: String,
      required: true,
    },

    price: {
      type: Number,
      required: true,
    },

    rating: {
      type: Number,
      required: true,
      min: 0,
      max: 5,
    },

    distance_km: {
      type: Number,
      required: true,
      min: 0,
    },

    stock: {
      type: Number,
      required: true,
      min: 0,
    },

    deliveryTime_days: {
      type: Number,
      min: 0,
    },

    organicCertified: {
      type: Boolean,
      default: false,
    },

    reviews: {
      type: Number,
      min: 0,
    },
  },
  {
    collection: "suppliers",
  }
);

module.exports = mongoose.model("Supplier", supplierSchema);