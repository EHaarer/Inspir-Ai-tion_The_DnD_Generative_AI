/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        API_URL: process.env.API_URL || 'http://localhost:8000',
        DB_NAME: process.env.DB_NAME || 'iat',
    },
};

export default nextConfig;
