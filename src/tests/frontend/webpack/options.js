const path = require("path")

const projectName = process.env.PROJECT_NAME
const siteName = process.env.SITE_NAME
const devServer = {
  client: {
    host: "192.168.1.102",
    port: 8081,
  },
  server: {
    host: "192.168.1.102",
    port: 8080,
  }
}

const _bundlesDirBase = "bundles"
const _bundlesDirPrefixServer = `${_bundlesDirBase}/server`
const _bundlesDirPrefixClient = `${_bundlesDirBase}/client`
const _bundlesDir = {
  client: {
    development: `${_bundlesDirPrefixClient}/development`,
  },
  server: {
    development: `${_bundlesDirPrefixServer}/development`,
  }
}
const bundlesDirPath = {
  client: {
    development: path.resolve(`./${_bundlesDir.client.development}`),
  },
  server: {
    development: path.resolve(`./${_bundlesDir.server.development}`),
  }
}

const publicPath = {
  client: {
    development: `http://${devServer.client.host}:${devServer.client.port}/${
      _bundlesDir.client.development
    }/`,
  },
  server: {
    development: `http://${devServer.server.host}:${devServer.server.port}/${
      _bundlesDir.server.development
    }/`,
  }
}

const _webpackStatsFileNameBase = "webpack-stats.client"
const _webpackStats = {
  client: {
    development: `${_webpackStatsFileNameBase}.development.json`,
  }
}
const webpackStatsPath = {
  client: {
    development: `./${_webpackStats.client.development}`,
  }
}


module.exports = {
  siteName,
  bundlesDirPath,
  devServer,
  publicPath,
  webpackStatsPath
}
