import { defineConfig } from 'dumi';

const repo = 'MCDRPlugins'

export default defineConfig({
  base: process.env.NODE_ENV === 'production' ? `/${repo}/`: '/',
  publicPath: process.env.NODE_ENV === 'production' ? `/${repo}/` : '/',
  themeConfig: {
    name: 'AMPR',
    lastUpdated: true,
    logo: 'public/icon.svg',

  },
  locales: [
    { id: 'zh-CN', name: '中文' },
    { id: 'en-US', name: 'EN' },
  ],
});
