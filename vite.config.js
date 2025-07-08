// Minimal Vite config for Lovable compatibility
// This project uses Django templates only
export default {
  server: {
    host: "::",
    port: 8080,
  },
  build: {
    outDir: 'dist',
    emptyOutDir: false
  }
}