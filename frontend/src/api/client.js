import axios from 'axios'

// --- Configuration -----------------------------------------------------
// Point VITE_API_BASE_URL at your backend and set VITE_MOCK_MODE=false
// (in a .env file) once the real endpoints below are ready to use.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const MOCK_MODE = import.meta.env.VITE_MOCK_MODE !== 'false'

const api = axios.create({ baseURL: API_BASE_URL })

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

// --- Mock data -----------------------------------------------------------
// Stands in for a real drawing-analysis backend during demos and frontend
// development. Replace by wiring the axios calls below to your API.
function buildMockSummary() {
  return {
    partNumber: 'ENG-4471-B',
    drawingTitle: 'Bracket Mounting Assembly',
    material: 'Aluminium 6061-T6',
    quantity: 12,
    scale: '1:5',
    revision: 'C',
    toleranceClass: 'ISO 2768-m',
    surfaceFinish: 'Ra 3.2',
    weight: '0.86 kg',
    drawnBy: 'EngiSummary AI',
    checkedDate: new Date().toISOString().slice(0, 10),
  }
}

/**
 * Uploads the PDF.
 * Real endpoint: POST /api/upload (multipart/form-data)
 */
export async function uploadPdf(file, onProgress) {
  if (MOCK_MODE) {
    await wait(900)
    onProgress?.(100)
    return { id: `drw-${Date.now()}`, filename: file.name, size: file.size }
  }

  const formData = new FormData()
  formData.append('file', file)

  const { data } = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (event) => {
      if (event.total) onProgress?.(Math.round((event.loaded * 100) / event.total))
    },
  })
  return data
}

/**
 * Kicks off drawing analysis for a previously uploaded file.
 * Real endpoint: POST /api/process
 */
export async function processDrawing(id) {
  if (MOCK_MODE) {
    await wait(1500)
    return { id, status: 'completed' }
  }

  const { data } = await api.post('/process', { id })
  return data
}

/**
 * Retrieves the generated summary and the resulting PDF.
 * Real endpoint: GET /api/result/:id
 * Expected shape: { id, pdfUrl, summary: {...} }
 */
export async function getResult(id, mockPreviewUrl) {
  if (MOCK_MODE) {
    await wait(700)
    return {
      id,
      pdfUrl: mockPreviewUrl,
      summary: buildMockSummary(),
    }
  }

  const { data } = await api.get(`/result/${id}`)
  return data
}

export { MOCK_MODE }
