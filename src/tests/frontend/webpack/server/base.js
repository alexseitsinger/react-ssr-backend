const webpack = require("webpack")
const merge = require("webpack-merge")
const nodeExternals = require("webpack-node-externals")

const baseConfig = require("../base")

module.exports = merge.smart(baseConfig, {
  target: "node",
  entry: {
    server: "./src/server.js"
  },
  output: {
    libraryTarget: "commonjs2"
  },
  externals: [nodeExternals()],
  plugins: [
    new webpack.DefinePlugin({
      AGENT_NAME: JSON.stringify("server")
    })
  ]
})
