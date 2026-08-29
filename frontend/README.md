# EngiSummary

Engineering Drawing Summary Generator — a small, focused frontend for a single
flow: **Upload PDF → Process → Preview Result → Download PDF**.

## Stack

- React 18 + Vite
- Tailwind CSS
- React Router
- Axios
- Lucide React icons

## Getting started

```bash
npm install
npm run dev
```

The app runs in **mock mode** by default, so the full flow (upload, processing
steps, extracted summary, downloadable PDF) works with no backend connected —
useful for demos and frontend development.

## Connecting a real backend

1. Copy `.env.example` to `.env`.
2. Set `VITE_API_BASE_URL` to your API's base URL.
3. Set `VITE_MOCK_MODE=false`.

The frontend expects three endpoints, already wired in `src/api/client.js`:

| Method | Endpoint            | Purpose                                             |
| ------ | -------------------- | ---------------------------------------------------- |
| POST   | `/api/upload`         | Upload the PDF (`multipart/form-data`), returns `{ id, filename, size }` |
| POST   | `/api/process`        | Start processing for a given `{ id }`                |
| GET    | `/api/result/:id`     | Returns `{ id, pdfUrl, summary: {...} }` — the processed PDF (original drawing + generated summary/BOM table) and the extracted fields |

`summary` fields currently rendered in the title block: `partNumber`,
`drawingTitle`, `material`, `quantity`, `scale`, `revision`,
`toleranceClass`, `surfaceFinish`, `weight`, `drawnBy`, `checkedDate`. Adjust
`src/components/TitleBlock.jsx` to match whatever your backend actually
extracts.

## Project structure

```
src/
  api/client.js            axios + mock API layer
  context/DrawingContext.jsx   shares file & result state across routes
  components/               Logo, Button, UploadDropzone, ProcessingSteps,
                             TitleBlock, PDFPreview, TopNav
  pages/                     HomePage, ProcessingPage, ResultPage
  App.jsx                    routes
```
