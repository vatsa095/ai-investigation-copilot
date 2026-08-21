/** @type {import('next').NextConfig} */

const nextConfig = {
  allowedDevOrigins: ["192.168.0.102"],

  async rewrites() {
    return [
      {
        source: "/api/cases/:path*",
        destination: "https://ai-investigation-copilot.onrender.com/cases/:path*",
      },
    ];
  },
};

export default nextConfig;