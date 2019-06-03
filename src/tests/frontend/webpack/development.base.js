const webpack = require("webpack")

module.exports = {
  mode: "development",
  watch: true,
  watchOptions: {
    poll: true,
    ignored: /node_modules/,
  },
  plugins: [
    new webpack.DefinePlugin({
      ENVIRONMENT_NAME: JSON.stringify("development")
    })
  ],
}
