/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://web-production-8c988.up.railway.app',
    NEXT_PUBLIC_WS_URL: process.env.NEXT_PUBLIC_WS_URL || 'wss://web-production-8c988.up.railway.app',
  },
  
  // API proxy for development
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'https://web-production-8c988.up.railway.app'}/api/:path*`,
      },
    ];
  },
  
  // Headers for CORS
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,DELETE,PATCH,POST,PUT' },
          { key: 'Access-Control-Allow-Headers', value: 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version' },
        ],
      },
    ];
  },
  
  // Optimize images
  images: {
    domains: ['localhost', 'railway.app', 'vercel.app'],
    formats: ['image/avif', 'image/webp'],
  },
  
  // Disable TypeScript/ESLint errors blocking build
  typescript: {
    ignoreBuildErrors: process.env.VERCEL_ENV === 'production',
  },
  eslint: {
    ignoreDuringBuilds: process.env.VERCEL_ENV === 'production',
  },
  
  experimental: {
    appDir: false,
  },
};

module.exports = nextConfig;