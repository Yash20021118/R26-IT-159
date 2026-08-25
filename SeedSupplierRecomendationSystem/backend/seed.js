const fs = require("fs");
const csv = require("csv-parser");
const mongoose = require("mongoose");

const Supplier = require("./models/Supplier");

mongoose
  .connect("mongodb://127.0.0.1:27017/smartseed")
  .then(() => {
    console.log("MongoDB connected");
  })
  .catch((error) => {
    console.error("MongoDB connection error:", error);
  });

const results = [];

fs.createReadStream("./seedData/suppliers.csv")
  .pipe(csv())
  .on("data", (data) => {
    results.push({
      supplierName: data.supplierName,

      contact_person: data.contact_person,
      address: data.address,
      telephone: data.telephone,

      seedType: data.seedType,
      region: data.region,

      price: Number(data.price),
      rating: Number(data.rating),
      distance_km: Number(data.distance_km),
      stock: Number(data.stock),

      deliveryTime_days: Number(data.deliveryTime_days),

      organicCertified:
        String(data.organicCertified).toLowerCase() === "true",

      reviews: Number(data.reviews),
    });
  })
  .on("end", async () => {
    try {
      // Remove old supplier records
      await Supplier.deleteMany({});

      // Insert new dataset
      await Supplier.insertMany(results);

      console.log(
        `${results.length} suppliers imported successfully.`
      );

      await mongoose.connection.close();
    } catch (error) {
      console.error("Import error:", error);
      await mongoose.connection.close();
      process.exit(1);
    }
  });