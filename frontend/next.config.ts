import type { NextConfig } from "next";

// Static export for GitHub Pages. The backend is NOT hosted here; the app calls
// the deployed Cloud Run API via NEXT_PUBLIC_API_BASE_URL.
const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true }, // required for static export
  trailingSlash: true,
  // For a GitHub Pages PROJECT site served at /finsight-agent, uncomment these
  // before building for deployment (Issue #16):
  // basePath: "/finsight-agent",
  // assetPrefix: "/finsight-agent/",
};

export default nextConfig;
