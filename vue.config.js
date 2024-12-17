const webpack = require('webpack');

module.exports = {
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false), // false로 설정
      }),
    ],
  },
};
