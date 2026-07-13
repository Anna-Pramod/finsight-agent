# Deployment

How FinSight Agent is deployed: a static frontend on **GitHub Pages** and a single
**Cloud Run** service for the backend (the persona data layer runs in-process — no Go
sidecar needed).

## 1. Backend → Google Cloud Run

Prereqs: `gcloud` CLI authenticated (`gcloud auth login`), billing enabled, and a
Gemini API key.

```sh
gcloud config set project <YOUR_PROJECT_ID>
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# Build & deploy straight from source (Cloud Build uses backend/Dockerfile;
# the image clones the upstream fi-mcp-dev persona data at build time).
gcloud run deploy finsight-backend \
  --source backend \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_API_KEY=<YOUR_GEMINI_KEY>,GEMINI_MODEL=gemini-3.1-flash-lite,FI_MCP_MODE=local,APP_ENV=production,CORS_ALLOW_ORIGINS=https://<YOUR_GH_USERNAME>.github.io"
```

Note the service URL it prints (e.g. `https://finsight-backend-xxxxx.a.run.app`), then:

```sh
curl https://<SERVICE_URL>/health   # {"status":"ok",...}
```

For production-grade secret handling, put the key in Secret Manager and use
`--set-secrets GOOGLE_API_KEY=finsight-gemini-key:latest` instead of `--set-env-vars`.

### Model quota note

The free Gemini tier is heavily rate-limited and model availability varies by key age
(observed: `gemini-3.5-flash` = 20 requests/day; `gemini-2.5-flash`/`gemini-2.0-flash`
return 404 "no longer available to new users" on new keys even though the models-list
API includes them; `gemini-3.1-flash-lite` works with a much higher quota). Verify a
model with a real generateContent call, not the models list. The backend retries
transient 429/503s with backoff and returns a clean HTTP 503 when exhausted. For a
public demo, enable billing on the key or use Vertex AI (`GOOGLE_GENAI_USE_VERTEXAI=TRUE`).

## 2. Frontend → GitHub Pages

One-time repo setup:

1. **Settings → Pages → Source: GitHub Actions.**
2. **Settings → Secrets and variables → Actions → Variables:** add
   `API_BASE_URL = https://<SERVICE_URL>` (the Cloud Run URL, no trailing slash).

Then push to `main` (or run the `frontend-pages` workflow manually). The workflow
builds the static export with `basePath=/finsight-agent` and publishes it. The site
lands at `https://<YOUR_GH_USERNAME>.github.io/finsight-agent/`.

Finally, make sure the backend's `CORS_ALLOW_ORIGINS` includes
`https://<YOUR_GH_USERNAME>.github.io` (origin only — no path).

## 3. The MCP layer in the hosted demo

The hosted backend runs with `FI_MCP_MODE=local`: the six `fetch_*` tools are served
in-process from the same `test_data_dir/` JSON files the upstream Go server returns
(cloned into the image at build time). Same data shape, same personas, one service.
Set `FI_MCP_MODE=http` + `FI_MCP_BASE_URL` to point at a live `fi-mcp-dev` server
instead (local development with Go, or a separately hosted MCP service).

## 4. CI

- `backend-tests.yml` — pytest on every backend change.
- `frontend-pages.yml` — build + deploy the static site on every frontend change.
