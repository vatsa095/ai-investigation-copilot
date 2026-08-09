/** @type {import('next').NextConfig} */
const nextConfig = {
  allowedDevOrigins: ["192.168.0.102"],

  async rewrites() {
    return [
      {
        source: "/api/cases/:path*",
        destination: "http://127.0.0.1:8000/cases/:path*",
      },
    ];
  },
};

export default nextConfig;