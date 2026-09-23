import axios from 'axios'

// ---------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------

// Point VITE_API_BASE_URL at your backend and set
// VITE_MOCK_MODE=false in your .env file
// when the real backend is ready.

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const MOCK_MODE = import.meta.env.VITE_MOCK_MODE === 'true'

const api = axios.create({
  baseURL: API_BASE_URL,
})

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

// ---------------------------------------------------------------------
// Helper Functions
// ---------------------------------------------------------------------

function getFileType(fileName) {
  const extension = fileName.split('.').pop()?.toLowerCase()

  if (extension === 'pdf') return 'pdf'
  if (extension === 'dwf') return 'dwf'
  return 'unknown'
}

// ---------------------------------------------------------------------
// Mock Data
// ---------------------------------------------------------------------

export function buildMockSummary() {
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

export function buildMockResult(mockPreviewUrl) {
  return {
    id: `mock-${Date.now()}`,
    pdfUrl: mockPreviewUrl || '',

    summary: buildMockSummary(),

    rawSummary: {
      job_id: `mock-${Date.now()}`,
      summary: [],
      grand_total_weight: 0.86,
      processing_status: 'completed',
    },
  }
}

// ---------------------------------------------------------------------
// Upload Drawing
// Supports PDF + DWF
//
// Function name intentionally kept as uploadPdf()
// so existing ProcessingPage.jsx code does not need to change.
//
// Real endpoint:
// POST /api/upload
// ---------------------------------------------------------------------

export async function uploadPdf(file, onProgress) {
  if (!file) {
    throw new Error('No drawing file selected.')
  }

  // Get file type from extension
  const fileType = getFileType(file.name)

  if (!['pdf', 'dwf'].includes(fileType)) {
    throw new Error('Only PDF and DWF files are supported by the backend.')
  }

  // -------------------------------------------------------------------
  // Mock Mode
  // -------------------------------------------------------------------

  if (MOCK_MODE) {
    await wait(900)

    onProgress?.(100)

    return {
      id: `drw-${Date.now()}`,
      filename: file.name,
      size: file.size,
      fileType,
    }
  }

  // -------------------------------------------------------------------
  // The integrated backend processes the file during upload.
  // -------------------------------------------------------------------

  const formData = new FormData()

  formData.append('file', file)

  const { data } = await api.post('/upload', formData, {
    responseType: 'blob',
    onUploadProgress: (event) => {
      if (event.total) {
        const progress = Math.round(
          (event.loaded * 100) / event.total
        )

        onProgress?.(progress)
      }
    },
  })

  return {
    id: `${file.name}-${Date.now()}`,
    pdfUrl: URL.createObjectURL(data),
    filename: file.name,
    size: file.size,
    fileType,
  }
}

// ---------------------------------------------------------------------
// Process Drawing
//
// Real endpoint:
// POST /api/process/:id
// ---------------------------------------------------------------------

export async function processDrawing(id) {
  if (!id) {
    throw new Error('Drawing ID is missing.')
  }

  // -------------------------------------------------------------------
  // Mock Mode
  // -------------------------------------------------------------------

  if (MOCK_MODE) {
    await wait(1500)

    return {
      id,
      status: 'completed',
    }
  }

  // -------------------------------------------------------------------
  // Real Backend
  // -------------------------------------------------------------------

  return { id, status: 'completed' }
}

// ---------------------------------------------------------------------
// Get Result
//
// Real endpoint:
// GET /api/result/:id
// ---------------------------------------------------------------------

export async function getResult(id, mockPreviewUrl, generatedPdfUrl) {
  if (!id) {
    throw new Error('Drawing ID is missing.')
  }

  // -------------------------------------------------------------------
  // Mock Mode
  // -------------------------------------------------------------------

  if (MOCK_MODE) {
    await wait(700)

    return buildMockResult(mockPreviewUrl)
  }

  // -------------------------------------------------------------------
  // Real Backend
  // -------------------------------------------------------------------

  return {
    id,
    pdfUrl: generatedPdfUrl || mockPreviewUrl || '',
    summary: {
      partNumber: 'See generated PDF',
      drawingTitle: 'Generated Summary',
      material: 'See generated PDF',
      quantity: 'See generated PDF',
      scale: 'N/A',
      revision: '—',
      toleranceClass: '—',
      surfaceFinish: '—',
      weight: 'See generated PDF',
      drawnBy: 'BOM Drawing Summary Backend',
      checkedDate: new Date().toISOString().slice(0, 10),
    },
    rawSummary: null,
  }
}

// ---------------------------------------------------------------------
// Send generated PDF via email
//
// Real endpoint:
// POST /api/send-pdf/:id
// Body: { email }
//
// NOTE: this must respect MOCK_MODE like every other call in this file.
// Previously this function always hit the real backend even while the rest
// of the app (upload/process/result) was running on mock data. Since mock
// IDs (e.g. "drw-...", "mock-...") never exist as real jobs on the backend,
// every "Send Email" click failed with a 404 "Job not found" error — this
// was the root cause of email sending appearing broken in the default
// (mock) configuration. Set VITE_MOCK_MODE=false once the real backend and
// its SMTP settings are configured, so this hits the real /send-pdf route.
// ---------------------------------------------------------------------

export async function sendPdfEmail(id, email) {
  if (!id) {
    throw new Error('Drawing ID is missing.')
  }

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    throw new Error('Please enter a valid email address.')
  }

  // -------------------------------------------------------------------
  // Mock Mode
  // -------------------------------------------------------------------

  if (MOCK_MODE) {
    await wait(700)

    return {
      success: true,
      message: 'Email sent (mock mode — no real email was sent).',
    }
  }

  // -------------------------------------------------------------------
  // Real Backend
  // -------------------------------------------------------------------

  const { data } = await api.post(`/send-pdf/${id}`, { email })

  return data
}

// ---------------------------------------------------------------------
// Export
// ---------------------------------------------------------------------

export { MOCK_MODE }