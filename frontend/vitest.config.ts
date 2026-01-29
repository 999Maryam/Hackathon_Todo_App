import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { join } from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    css: true,
    alias: {
      // Mirror the Next.js path aliases from tsconfig.json
      '@/app': join(__dirname, './src/app'),
      '@/components': join(__dirname, './src/components'),
      '@/hooks': join(__dirname, './src/hooks'),
      '@/lib': join(__dirname, './src/lib'),
      '@/public': join(__dirname, './public'),
      '@': join(__dirname, './src'),
    },
  },
});