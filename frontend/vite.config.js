import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const backendUrl = 'http://localhost:8000';

export default defineConfig({
  plugins: [react()],

  server: {
    proxy: {
      '/graphql': {
        target: backendUrl,
        changeOrigin: true,
      },
      '/csrf_cookie': {
        target: backendUrl,
        changeOrigin: true,
      },
    },
  },
});
