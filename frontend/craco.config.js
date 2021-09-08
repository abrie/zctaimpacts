const path = require("path");
const babelInclude = require("@dealmore/craco-plugin-babel-include");

module.exports = {
  style: {
    postcss: {
      plugins: [require("tailwindcss"), require("autoprefixer")],
    },
  },
  plugins: [
    {
      plugin: babelInclude,
      options: {
        include: [
          path.resolve("src"),
          path.resolve("../node_modules/@react-leaflet"),
          path.resolve("../node_modules/react-leaflet"),
        ],
      },
    },
  ],
};
