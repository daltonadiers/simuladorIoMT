import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate', // Registra automaticamente o Service Worker
      manifest: {
        name: 'Meu App PWA',        // Nome do app
        short_name: 'App',           // Nome curto do app
        description: 'Descrição do meu app', // Descrição
        theme_color: '#ffffff',     // Cor do tema
        background_color: '#ffffff', // Cor de fundo da tela inicial
        display: 'standalone',      // Exibe o app em modo standalone
        start_url: '/',             // URL de início
        icons: [
          {
            src: '/icon-192x192.png', // Caminho do ícone de 192x192px
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/icon-512x512.png', // Caminho do ícone de 512x512px
            sizes: '512x512',
            type: 'image/png',
          },
        ],
      },
    }),
  ],
  server: {
    port: 80,
    host: true,
    https: false,
  },
})
