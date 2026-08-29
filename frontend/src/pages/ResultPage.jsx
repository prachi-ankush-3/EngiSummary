import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { CheckCircle2, Download, Eye, RotateCcw } from 'lucide-react'
import TopNav from '../components/TopNav.jsx'
import PDFPreview from '../components/PDFPreview.jsx'
import TitleBlock from '../components/TitleBlock.jsx'
import Button from '../components/Button.jsx'
import { useDrawing } from '../context/DrawingContext.jsx'

export default function ResultPage() {
  const navigate = useNavigate()
  const { file, result, reset } = useDrawing()

  useEffect(() => {
    if (!result) {
      navigate('/', { replace: true })
    }
  }, [result, navigate])

  if (!result) return null

  const handleView = () => {
    window.open(result.pdfUrl, '_blank', 'noopener,noreferrer')
  }

  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = result.pdfUrl
    link.download = file?.name ? `${file.name.replace(/\.pdf$/i, '')}-summary.pdf` : 'drawing-summary.pdf'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const handleUploadAnother = () => {
    reset()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-canvas">
      <TopNav />

      <main className="mx-auto max-w-5xl px-6 pb-20 pt-10">
        <div className="flex items-center gap-2.5 rounded-lg border border-success-border bg-success-bg px-4 py-3">
          <CheckCircle2 className="h-5 w-5 shrink-0 text-success" />
          <p className="text-sm font-medium text-success">Summary Generated Successfully</p>
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-5">
          <section className="lg:col-span-3">
            <p className="mb-2 text-sm font-medium text-ink">Drawing Preview</p>
            <PDFPreview url={result.pdfUrl} title={file?.name} />

            <div className="mt-4 flex flex-wrap gap-3">
              <Button variant="secondary" icon={Eye} onClick={handleView}>
                View PDF
              </Button>
              <Button variant="primary" icon={Download} onClick={handleDownload}>
                Download PDF
              </Button>
              <Button variant="ghost" icon={RotateCcw} onClick={handleUploadAnother}>
                Upload Another
              </Button>
            </div>
          </section>

          <section className="lg:col-span-2">
            <p className="mb-2 text-sm font-medium text-ink">Extracted Information</p>
            <TitleBlock data={result.summary} />
          </section>
        </div>
      </main>
    </div>
  )
}
