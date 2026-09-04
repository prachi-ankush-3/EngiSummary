import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AlertTriangle } from 'lucide-react'

import TopNav from '../components/TopNav.jsx'
import ProcessingSteps from '../components/ProcessingSteps.jsx'
import Button from '../components/Button.jsx'

import { useDrawing } from '../context/DrawingContext.jsx'
import {
  uploadPdf,
  processDrawing,
  getResult,
  buildMockResult,
  MOCK_MODE,
} from '../api/client.js'

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export default function ProcessingPage() {
  const navigate = useNavigate()

  const {
    file,
    previewUrl,
    setDrawingId,
    setResult,
  } = useDrawing()

  const [stepIndex, setStepIndex] = useState(0)
  const [error, setError] = useState('')

  const hasStarted = useRef(false)

  useEffect(() => {
    if (!file) {
      navigate('/', { replace: true })
      return
    }

    if (hasStarted.current) return

    hasStarted.current = true

    const run = async () => {
      try {
        // ---------------------------------------------------------
        // STEP 1 — Uploading
        // ---------------------------------------------------------

        setStepIndex(0)

        const uploaded = await uploadPdf(file)

        const jobId = uploaded.job_id || uploaded.id

        if (!jobId) {
          throw new Error('Upload failed. No drawing ID was returned.')
        }

        setDrawingId(jobId)

        // Keep Uploading visible briefly
        await wait(800)

        // ---------------------------------------------------------
        // STEP 2 — Analyzing
        // ---------------------------------------------------------

        setStepIndex(1)

        await wait(1500)

        // ---------------------------------------------------------
        // STEP 3 — Generating Summary
        // ---------------------------------------------------------

        setStepIndex(2)

        if (MOCK_MODE) {
          // Demo mode
          await wait(2000)
        } else {
          // Real backend processing
          await processDrawing(jobId)
        }

        // ---------------------------------------------------------
        // STEP 4 — Completed
        // ---------------------------------------------------------

        setStepIndex(3)

        await wait(1000)

        // ---------------------------------------------------------
        // Get final result
        // ---------------------------------------------------------

        const resultData = await getResult(
          jobId,
          previewUrl
        )

        setResult(resultData)

        // Give user time to see "Completed"
        await wait(1200)

        // Go to result page
        navigate('/result')
      } catch (err) {
        console.error('Processing error:', err)

        // ---------------------------------------------------------
        // If real backend fails
        // ---------------------------------------------------------

        if (MOCK_MODE) {
          const fallbackResult = buildMockResult(previewUrl)

          setStepIndex(3)
          setResult(fallbackResult)

          await wait(1200)

          navigate('/result')
          return
        }

        // Show actual error instead of silently jumping to result
        setError(
          err?.message ||
            'Something went wrong while processing the drawing.'
        )
      }
    }

    run()

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [file])

  return (
    <div className="min-h-screen bg-blueprint">
      <TopNav />

      <main className="mx-auto flex max-w-md flex-col items-center px-6 pb-20 pt-16 sm:pt-24">
        <div className="w-full rounded-lg border border-border-strong bg-white p-8 shadow-panel">
          {error ? (
            <div className="text-center">
              <span className="mx-auto flex h-11 w-11 items-center justify-center rounded-full bg-danger-bg text-danger">
                <AlertTriangle className="h-5 w-5" />
              </span>

              <p className="mt-4 text-sm font-medium text-ink">
                Processing failed
              </p>

              <p className="mt-1 text-sm text-muted">
                {error}
              </p>

              <Button
                variant="primary"
                className="mt-6 w-full"
                onClick={() => navigate('/')}
              >
                Back to Upload
              </Button>
            </div>
          ) : (
            <>
              <p className="text-sm font-medium text-ink">
                Processing your drawing
              </p>

              <p className="mt-1 truncate font-mono text-xs text-muted">
                {file?.name}
              </p>

              <div className="mt-8">
                <ProcessingSteps
                  currentIndex={stepIndex}
                />
              </div>
            </>
          )}
        </div>

        {!error && (
          <p className="mt-6 text-center text-xs text-faint">
            This usually takes a few seconds. Please keep this tab open.
          </p>
        )}
      </main>
    </div>
  )
}