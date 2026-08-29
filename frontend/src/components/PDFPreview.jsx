import { FileWarning } from 'lucide-react'

export default function PDFPreview({ url, title = 'Drawing preview' }) {
  if (!url) {
    return (
      <div className="flex h-full min-h-[420px] flex-col items-center justify-center gap-2 rounded-lg border border-border-strong bg-canvas text-faint">
        <FileWarning className="h-6 w-6" />
        <p className="text-sm">No preview available</p>
      </div>
    )
  }

  return (
    <div className="h-full min-h-[420px] overflow-hidden rounded-lg border border-border-strong bg-canvas">
      <iframe src={url} title={title} className="h-full w-full" style={{ minHeight: 420 }} />
    </div>
  )
}
