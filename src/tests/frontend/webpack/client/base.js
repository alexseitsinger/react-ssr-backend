const webpack = require("webpack")
const merge = require("webpack-merge")

const configBase = require("../base")

module.exports = merge.smart(configBase, {
  entry: {
    client: "./src/client.js"
  },
  optimization: {
    runtimeChunk: "single",
    splitChunks: {
      cacheGroups: {
        vendors: {
          name: "vendors",
          test: /\/node_modules\//,
          chunks: "all",
        },
      }
    }
  },
  plugins: [
    new webpack.DefinePlugin({
      AGENT_NAME: JSON.stringify("client")
    })
  ]
})
