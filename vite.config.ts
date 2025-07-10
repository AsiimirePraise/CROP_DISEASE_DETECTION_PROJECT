// TypeScript version for Lovable compatibility
// This project uses Django templates only
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    host: "::",
    port: 8080,
  },
  build: {
    outDir: 'dist',
    emptyOutDir: false
  }
})