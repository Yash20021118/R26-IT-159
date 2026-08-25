const express = require("express");

const router = express.Router();

const {
  getRankedSuppliers,
} = require("../controllers/supplierController");

// POST ROUTE
router.post("/rank", getRankedSuppliers);

module.exports = router;