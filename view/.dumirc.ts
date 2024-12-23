import { defineConfig } from 'dumi';

const repo = 'MCDRPlugins'

export default defineConfig({
  base: process.env.NODE_ENV === 'production' ? `/${repo}/`: '/',
  publicPath: process.env.NODE_ENV === 'production' ? `/${repo}/` : '/',
  themeConfig: {
    name: 'AMPR',
    lastUpdated: true,
    logo: 'https://aimerny.github.io/MCDRPlugins/icon.svg',
    prefersColor: { default: 'auto' },
    footer: 'Copyright © 2024 | Powered by <a href="https://github.com/Aimerny">Aimerny</a><br/>Thanks for dumi',
    socialLinks: {
      github: 'https://github.com/Aimerny/MCDRPlugins',
    }
  },
  locales: [
    { id: 'zh-CN', name: '中文' },
    // { id: 'en-US', name: 'EN' },
  ],
  alias: {
    "plugins": "../src/",
    "root":"../",
  }
});
