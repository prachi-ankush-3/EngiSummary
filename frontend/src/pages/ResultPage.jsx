import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { CheckCircle2, Download, Eye, Mail, RotateCcw } from 'lucide-react'
import TopNav from '../components/TopNav.jsx'
import PDFPreview from '../components/PDFPreview.jsx'
import TitleBlock from '../components/TitleBlock.jsx'
import Button from '../components/Button.jsx'
import { useDrawing } from '../context/DrawingContext.jsx'
import { sendPdfEmail } from '../api/client.js'

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export default function ResultPage() {
  const navigate = useNavigate()
  const { file, result, reset } = useDrawing()
  const [showEmailForm, setShowEmailForm] = useState(false)
  const [email, setEmail] = useState('')
  const [emailStatus, setEmailStatus] = useState(null)
  const [emailMessage, setEmailMessage] = useState('')
  const [sending, setSending] = useState(false)

  useEffect(() => {
    if (!result) {
      navigate('/', { replace: true })
    }
  }, [result, navigate])

  if (!result) return null

  const handleView = () => {
    if (result.pdfUrl) {
      window.open(result.pdfUrl, '_blank', 'noopener,noreferrer')
    }
  }

  const handleDownload = () => {
    if (!result.pdfUrl) return

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

  const handleSendEmail = async () => {
    const trimmed = email.trim()

    if (!EMAIL_PATTERN.test(trimmed)) {
      setEmailStatus('error')
      setEmailMessage('Please enter a valid email address.')
      return
    }

    setSending(true)
    setEmailStatus(null)
    setEmailMessage('')

    try {
      const data = await sendPdfEmail(result.id, trimmed)

      if (data?.success) {
        setEmailStatus('success')
        setEmailMessage(data.message || 'PDF sent successfully to your email.')
      } else {
        setEmailStatus('error')
        setEmailMessage(data?.error || 'Failed to send PDF. Please try again.')
      }
    } catch (error) {
      setEmailStatus('error')
      const backendMessage =
        error?.response?.data?.error || error?.response?.data?.detail
      setEmailMessage(
        backendMessage || error?.message || 'Failed to send PDF. Please try again.'
      )
    } finally {
      setSending(false)
    }
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
              <Button
                variant="secondary"
                icon={Mail}
                onClick={() => setShowEmailForm((open) => !open)}
              >
                Send PDF via Email
              </Button>
              <Button variant="ghost" icon={RotateCcw} onClick={handleUploadAnother}>
                Upload Another
              </Button>
            </div>

            {showEmailForm && (
              <div className="mt-4 rounded-lg border border-border bg-white p-4">
                <label htmlFor="pdf-email" className="mb-1.5 block text-sm font-medium text-ink">
                  Email address
                </label>
                <div className="flex flex-wrap gap-3">
                  <input
                    id="pdf-email"
                    type="email"
                    value={email}
                    onChange={(event) => {
                      setEmail(event.target.value)
                      setEmailStatus(null)
                      setEmailMessage('')
                    }}
                    placeholder="name@example.com"
                    className="min-w-[16rem] flex-1 rounded-md border border-border-strong bg-white px-3 py-2.5 text-sm text-ink outline-none focus:border-primary"
                    disabled={sending}
                  />
                  <Button variant="primary" onClick={handleSendEmail} disabled={sending}>
                    {sending ? 'Sending…' : 'Send Email'}
                  </Button>
                </div>
                {emailMessage && (
                  <p
                    className={`mt-2 text-sm font-medium ${
                      emailStatus === 'success' ? 'text-success' : 'text-red-600'
                    }`}
                  >
                    {emailMessage}
                  </p>
                )}
              </div>
            )}
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
