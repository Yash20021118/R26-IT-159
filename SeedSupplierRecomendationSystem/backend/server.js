const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

const supplierRoutes = require("./routes/supplierRoutes");

const app = express();

app.use(cors({
    origin: "http://localhost:5173"
}));

app.use(express.json());

app.get("/", (req, res) => {
    res.send("API Running Successfully");
});

// routes
app.use("/api/suppliers", supplierRoutes);

mongoose.connect(process.env.MONGO_URI)
.then(() => {
    console.log("MongoDB Connected");

    app.listen(5001, () => {
        console.log("Server Running on Port 5001");
    });
})
.catch((error) => {
    console.log(error);
});