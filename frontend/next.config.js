/** @type {import('next').Config} */
const nextConfig = {
  images: {
    domains: [
      'localhost',
      '127.0.0.1',
      // AWS S3 도메인 추가 예정
    ],
    formats: ['image/webp', 'image/avif'],
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080/api/v1',
  },
}

module.exports = nextConfig
