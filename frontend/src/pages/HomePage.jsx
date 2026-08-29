import { useNavigate } from 'react-router-dom'
import { ArrowRight, ClipboardList, ScanSearch, Table2 } from 'lucide-react'
import TopNav from '../components/TopNav.jsx'
import UploadDropzone from '../components/UploadDropzone.jsx'
import Button from '../components/Button.jsx'
import { useDrawing } from '../context/DrawingContext.jsx'

const HIGHLIGHTS = [
  {
    icon: ScanSearch,
    title: 'Reads the drawing',
    description: 'Extracts title block fields, notes and dimensions automatically.',
  },
  {
    icon: Table2,
    title: 'Builds the Summary',
    description: 'Compiles a clean summary table.',
  },
  {
    icon: ClipboardList,
    title: 'Adds it to the PDF',
    description: 'Returns your original drawing with the table appended.',
  },
]

export default function HomePage() {
  const navigate = useNavigate()
  const { file, selectFile } = useDrawing()

  const handleProcess = () => {
    if (!file) return
    navigate('/processing')
  }

  return (
    <div className="min-h-screen bg-blueprint">
      <TopNav />

      <main className="mx-auto max-w-3xl px-6 pb-20 pt-16 sm:pt-20">
        <div className="text-center">
          <span className="inline-flex items-center rounded-full border border-border-strong bg-white px-3 py-1 font-mono text-[11px] uppercase tracking-wider text-muted">
            PDF In → Summarized PDF Out
          </span>
          <h1 className="mt-5 text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            Engineering Drawings to Structured Summaries.
          </h1>
          <p className="mx-auto mt-3 max-w-xl text-base text-muted">
            Upload an engineering drawing PDF. EngiSummary reads it and hands back the same
            drawing with a summary table added.
          </p>
        </div>

        <div className="mt-10">
          <UploadDropzone file={file} onSelect={selectFile} />
        </div>

        <div className="mt-6 flex justify-center">
          <Button
            variant="primary"
            icon={ArrowRight}
            iconPosition="right"
            disabled={!file}
            onClick={handleProcess}
            className="px-6 py-3 text-base"
          >
            Process Drawing
          </Button>
        </div>

        <div className="mt-16 grid gap-4 sm:grid-cols-3">
          {HIGHLIGHTS.map(({ icon: Icon, title, description }) => (
            <div
              key={title}
              className="rounded-lg border border-border bg-white/70 p-4 text-left"
            >
              <span className="flex h-9 w-9 items-center justify-center rounded-md bg-primary/10 text-primary">
                <Icon className="h-[18px] w-[18px]" strokeWidth={2} />
              </span>
              <p className="mt-3 text-sm font-medium text-ink">{title}</p>
              <p className="mt-1 text-xs text-muted">{description}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
