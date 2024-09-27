import { defineConfig } from 'dumi';

const repo = 'MCDRPlugins'

export default defineConfig({
  title: 'Aimerny\'s MCDR Plugins',
  mode: 'site',
  devServer: {
    port: 9091
  },
  base: process.env.NODE_ENV === 'production' ? `/${repo}/`: '/',
  publicPath: process.env.NODE_ENV === 'production' ? `/${repo}/` : '/',
  // more config: https://d.umijs.org/config
});
