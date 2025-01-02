import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
     '/generate_abc': 'http://localhost:8000',
     '/get_midi': 'http://localhost:8000',
    }
  }
})
