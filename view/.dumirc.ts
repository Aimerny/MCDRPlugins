import { defineConfig } from 'dumi';

export default defineConfig({
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
