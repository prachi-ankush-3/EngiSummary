import { useCallback, useRef, useState } from 'react'
import { FileText, UploadCloud, X, AlertTriangle } from 'lucide-react'

const MAX_SIZE_MB = 25

function formatBytes(bytes) {
  if (bytes === 0) return '0 KB'
  const kb = bytes / 1024
  if (kb < 1024) return `${kb.toFixed(0)} KB`
  return `${(kb / 1024).toFixed(1)} MB`
}

export default function UploadDropzone({ file, onSelect }) {
  const inputRef = useRef(null)
  const [isDragging, setIsDragging] = useState(false)
  const [error, setError] = useState('')

  const validateAndSet = useCallback(
    (selected) => {
      if (!selected) return
      if (selected.type !== 'application/pdf' && !selected.name.toLowerCase().endsWith('.pdf')) {
        setError('Only PDF files are supported.')
        return
      }
      if (selected.size > MAX_SIZE_MB * 1024 * 1024) {
        setError(`File is larger than ${MAX_SIZE_MB} MB.`)
        return
      }
      setError('')
      onSelect(selected)
    },
    [onSelect]
  )

  const handleDrop = useCallback(
    (event) => {
      event.preventDefault()
      setIsDragging(false)
      const dropped = event.dataTransfer.files?.[0]
      validateAndSet(dropped)
    },
    [validateAndSet]
  )

  if (file) {
    return (
      <div className="flex items-center justify-between rounded-lg border border-border-strong bg-white px-5 py-4 shadow-panel">
        <div className="flex min-w-0 items-center gap-3">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
            <FileText className="h-5 w-5" strokeWidth={2} />
          </span>
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-ink">{file.name}</p>
            <p className="font-mono text-xs text-muted">{formatBytes(file.size)}</p>
          </div>
        </div>
        <button
          type="button"
          onClick={() => onSelect(null)}
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-faint transition-colors hover:bg-black/[0.04] hover:text-ink"
          aria-label="Remove file"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    )
  }

  return (
    <div>
      <div
        onDragOver={(e) => {
          e.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === 'Enter' && inputRef.current?.click()}
        className={`flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed px-6 py-14 text-center transition-colors duration-150 ${
          isDragging
            ? 'border-primary bg-primary/5'
            : 'border-border-strong bg-white hover:border-primary/60 hover:bg-primary/[0.03]'
        }`}
      >
        <span className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
          <UploadCloud className="h-6 w-6" strokeWidth={2} />
        </span>
        <p className="mt-4 text-sm font-medium text-ink">
          Drag and drop your drawing here
        </p>
        <p className="mt-1 text-xs text-muted">PDF up to {MAX_SIZE_MB} MB</p>

        <span
          onClick={(e) => {
            e.stopPropagation()
            inputRef.current?.click()
          }}
          className="mt-5 inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-dark"
        >
          Browse PDF
        </span>

        <input
          ref={inputRef}
          type="file"
          accept=".pdf,application/pdf"
          className="hidden"
          onChange={(e) => validateAndSet(e.target.files?.[0])}
        />
      </div>

      {error && (
        <p className="mt-3 flex items-center gap-1.5 text-sm text-danger">
          <AlertTriangle className="h-4 w-4" />
          {error}
        </p>
      )}
    </div>
  )
}
