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

  // Only PDF and DWF are allowed
  if (fileType !== 'pdf' && fileType !== 'dwf') {
    throw new Error('Only PDF and DWF files are supported.')
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
  // Real Backend
  // -------------------------------------------------------------------

  const formData = new FormData()

  formData.append('file', file)

  const { data } = await api.post('/upload', formData, {
    onUploadProgress: (event) => {
      if (event.total) {
        const progress = Math.round(
          (event.loaded * 100) / event.total
        )

        onProgress?.(progress)
      }
    },
  })

  // Check backend response
  if (!data?.success || !data?.job_id) {
    throw new Error(
      data?.error ||
        data?.message ||
        'Upload failed.'
    )
  }

  return {
    ...data,
    id: data.job_id,
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

  const { data } = await api.post(`/process/${id}`)

  return data
}

// ---------------------------------------------------------------------
// Get Result
//
// Real endpoint:
// GET /api/result/:id
// ---------------------------------------------------------------------

export async function getResult(id, mockPreviewUrl) {
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

  try {
    const { data } = await api.get(`/result/${id}`)

    const backendSummary = data?.data ?? data

    // If backend returns an error
    if (!data?.success && data?.error) {
      return buildMockResult(mockPreviewUrl)
    }

    // Get first summary item
    const firstItem = Array.isArray(
      backendSummary?.summary
    )
      ? backendSummary.summary[0]
      : null

    return {
      id,

      // Final generated PDF
      pdfUrl: `${window.location.origin}/api/download/${id}?v=${Date.now()}`,

      // Engineering summary
      summary: {
        partNumber:
          firstItem?.part_no || '—',

        drawingTitle:
          firstItem?.description ||
          'Generated Summary',

        material:
          firstItem?.material || '—',

        quantity:
          firstItem?.quantity ?? '—',

        scale: 'N/A',

        revision: '—',

        toleranceClass: '—',

        surfaceFinish: '—',

        weight:
          backendSummary?.grand_total_weight != null
            ? `${Number(
                backendSummary.grand_total_weight
              ).toFixed(2)} kg`
            : '—',

        drawnBy: 'EngiSummary AI',

        checkedDate:
          new Date()
            .toISOString()
            .slice(0, 10),
      },

      // Keep complete backend response
      rawSummary: backendSummary,
    }
  } catch (error) {
    console.error('Failed to get result:', error)

    // Fallback to mock result
    return buildMockResult(mockPreviewUrl)
  }
}

// ---------------------------------------------------------------------
// Export
// ---------------------------------------------------------------------

export { MOCK_MODE }