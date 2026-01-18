import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable standalone output for optimized production builds
  output: 'standalone',

  // Environment variables available at build time
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://999maryam-hackathon-todo-app.hf.space',
  },

  // Image optimization domains (if using external images)
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.hf.space',
      },
    ],
  },
};

export default nextConfig;
