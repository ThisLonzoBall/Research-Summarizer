# Research Summarizer – Frontend

React 19 + Vite + Tailwind CSS v4 single-page app for the Research Summarizer API.

## Development

```bash
npm install
npm run dev        # http://localhost:5173
```

The dev server proxies `/api/*` to the FastAPI backend on `http://localhost:8080`
(see `vite.config.js`), so start the backend first with `python app.py` from the repo root.

To call a backend hosted elsewhere, set `VITE_API_URL`:

```bash
VITE_API_URL=https://my-backend.example.com npm run dev
```

## Production build

```bash
npm run build      # outputs dist/
```

When `frontend/dist` exists, FastAPI serves it at `/`, so the Docker image ships the UI and API as one service.

## Structure

```
src/
├── pages/Home.jsx          # tabs (PDF / text), result + loading states
├── components/             # Layout, PdfUpload, TextInput, SummaryCard, LoadingCard, ErrorBanner, PrimaryButton
├── hooks/useSummarize.js   # request state, validation, cancellation
└── services/api.js         # axios client + error formatting
```
