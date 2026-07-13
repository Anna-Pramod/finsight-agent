import type { NextConfig } from "next";

// Static export for GitHub Pages. The backend is NOT hosted here; the app calls
// the deployed Cloud Run API via NEXT_PUBLIC_API_BASE_URL.
// GITHUB_PAGES=true (set by the Pages workflow) enables the project-site basePath.
const onPages = process.env.GITHUB_PAGES === "true";

const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true }, // required for static export
  trailingSlash: true,
  ...(onPages ? { basePath: "/finsight-agent", assetPrefix: "/finsight-agent/" } : {}),
};

export default nextConfig;
