const path = require("path")
const webpack = require("webpack")
const merge = require("webpack-merge")
const BundleTracker = require("webpack-bundle-tracker")

const options = require("../options")
const developmentBaseConfig = require("../development.base")
const clientBaseConfig = require("./base")

module.exports = merge.smart(developmentBaseConfig, clientBaseConfig, {
  output: {
    path: options.bundlesDirPath.client.development,
    publicPath: options.publicPath.client.development,
  },
  plugins: [
    new webpack.SourceMapDevToolPlugin({
      filename: "[name].js.map",
    }),
    new webpack.HotModuleReplacementPlugin(),
    new BundleTracker({
      filename: options.webpackStatsPath.client.development
    })
  ],
  devServer: {
    host: options.devServer.client.host,
    port: options.devServer.client.port,
    historyApiFallback: true,
    // Serve staticfiles from django, not express. (default: /)
    publicPath: options.publicPath.client.development,
    // Disable serving static content from webpack. (we use Django)
    contentBase: false,
    watchOptions: {
      poll: true,
      ignored: /node_modules/,
    },
    watchContentBase: false,
    serveIndex: false,
    // Enable HMR (default: false)
    //hot: true,
    hotOnly: true,
    overlay: {
      warnings: true,
      errors: true
    },
    // Allow inline HMR for react. (default: false)
    inline: true,
    headers: {
      "Access-Control-Allow-Origin": "*"
    }
  }
})
