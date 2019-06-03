const path = require("path")
const webpack = require("webpack")
const merge = require("webpack-merge")

const options = require("../options")
const developmentBaseConfig = require("../development.base")
const serverBaseConfig = require("./base")

module.exports = merge.smart(developmentBaseConfig, serverBaseConfig, {
  output: {
    path: options.bundlesDirPath.server.development,
    publicPath: options.publicPath.server.development
  }
})


