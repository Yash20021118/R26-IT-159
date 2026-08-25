const mongoose = require("mongoose")
require("dotenv").config()

const Supplier = require("./models/Supplier")

mongoose.connect(process.env.MONGO_URI)

const suppliers = [

  {
    name: "Agro Lanka",
    region: "Colombo",
    seedType: "Rice Seed",
    price: 2500,
    rating: 4.8,
    distance: 5,
    stock: 120
  },

  {
    name: "Green Harvest",
    region: "Galle",
    seedType: "Rice Seed",
    price: 2200,
    rating: 4.2,
    distance: 150f,
    stock: 90
  },

  {
    name: "Seed Master",
    region: "Kandy",
    seedType: "Corn Seed",
    price: 3100,
    rating: 4.9,
    distance: 7,
    stock: 150
  },

  {
    name: "Farm Hub",
    region: "Galle",
    seedType: "Tomato Seed",
    price: 1800,
    rating: 4.5,
    distance: 10,
    stock: 75
  },

  {
    name: "Lanka Agro Center",
    region: "Colombo",
    seedType: "Rice Seed",
    price: 2600,
    rating: 4.6,
    distance: 4,
    stock: 140
  },

  {
    name: "Nature Seed Suppliers",
    region: "Kandy",
    seedType: "Corn Seed",
    price: 2800,
    rating: 4.3,
    distance: 8,
    stock: 110
  },

  {
    name: "Smart Farm Solutions",
    region: "Galle",
    seedType: "Tomato Seed",
    price: 2100,
    rating: 4.7,
    distance: 6,
    stock: 95
  },

  {
    name: "Harvest House",
    region: "Colombo",
    seedType: "Rice Seed",
    price: 2400,
    rating: 4.4,
    distance: 9,
    stock: 130
  },

  {
    name: "Future Agro",
    region: "Kandy",
    seedType: "Corn Seed",
    price: 2950,
    rating: 4.8,
    distance: 3,
    stock: 160
  },

  {
    name: "Fresh Grow",
    region: "Galle",
    seedType: "Tomato Seed",
    price: 1750,
    rating: 4.1,
    distance: 15,
    stock: 70
  }

]

const seedDB = async () => {

  await Supplier.deleteMany()

  await Supplier.insertMany(suppliers)

  console.log("Sample Suppliers Inserted")

  mongoose.connection.close()
}

seedDB()