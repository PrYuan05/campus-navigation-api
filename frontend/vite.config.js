import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://34.180.115.60:31080',
        changeOrigin: true,
      },
      '/dgrv4': {
        target: 'http://34.180.115.60:31080',
        changeOrigin: true,
      }
    }
  }
})
