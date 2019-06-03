const path = require("path")
const webpack = require("webpack")

const FRONTEND_DIR = path.dirname(__dirname)

module.exports = {
  devtool: false,
  output: {
    filename: "[name].js",
    chunkFilename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/, 
        use: "babel-loader", 
        exclude: /node_modules/
      },
    ]
  },
  resolve: {
    modules: [
      path.resolve(FRONTEND_DIR, "src"),
      "node_modules"
    ],
    extensions: [".js", ".jsx", ".json", ".css"]
  },
}
