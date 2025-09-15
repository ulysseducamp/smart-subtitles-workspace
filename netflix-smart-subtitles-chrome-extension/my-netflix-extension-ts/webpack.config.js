/*
 * Netflix Subtitle Downloader
 * Copyright (C) 2025 Based on Subadub by Russel Simmons
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');
const Dotenv = require('dotenv-webpack');

module.exports = {
  entry: {
    popup: './src/popup/popup.ts',
    'content-script': './src/content-script.ts',
    'page-script': './src/page-script.ts'
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
    clean: true
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/
      }
    ]
  },
  resolve: {
    extensions: ['.ts', '.js']
  },
  plugins: [
    new Dotenv({
      path: './.env',
      safe: true,
      allowEmptyValues: true,
      systemvars: true,
      silent: true,
      defaults: false
    }),
    new CopyPlugin({
      patterns: [
        { from: 'src/popup/popup.html', to: 'popup.html' },
        { from: 'src/popup/popup.css', to: 'popup.css' },
        { from: 'manifest.json', to: 'manifest.json' }
      ]
    })
  ],
  optimization: {
    splitChunks: false
  }
};
