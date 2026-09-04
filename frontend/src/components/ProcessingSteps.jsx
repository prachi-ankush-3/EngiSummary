import { Check, Loader2 } from 'lucide-react'

export const PROCESS_STEPS = [
  { key: 'uploading', label: 'Uploading', description: 'Sending your drawing to EngiSummary' },
  { key: 'analyzing', label: 'Analyzing', description: 'Reading title block, views and annotations' },
  { key: 'generating', label: 'Generating Summary', description: 'Building the summary table' },
  { key: 'completed', label: 'Completed', description: 'Your PDF is ready' },
]

export default function ProcessingSteps({ currentIndex }) {
  return (
    <ol className="space-y-0">
      {PROCESS_STEPS.map((step, index) => {
        const isDone = index < currentIndex
        const isActive = index === currentIndex
        const isLast = index === PROCESS_STEPS.length - 1

        return (
          <li key={step.key} className="relative flex gap-4 pb-8 last:pb-0">
            {!isLast && (
              <span
                className={`absolute left-[15px] top-8 h-[calc(100%-1.5rem)] w-px ${
                  isDone ? 'bg-primary' : 'bg-border-strong'
                }`}
                aria-hidden="true"
              />
            )}

            <span
              className={`relative z-10 flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 text-sm font-medium ${
                isDone
                  ? 'border-primary bg-primary text-white'
                  : isActive
                  ? 'border-primary bg-white text-primary'
                  : 'border-border-strong bg-white text-faint'
              }`}
            >
              {isDone ? (
                <Check className="h-4 w-4" strokeWidth={2.5} />
              ) : isActive ? (
                <Loader2 className="h-4 w-4 animate-spin" strokeWidth={2.5} />
              ) : (
                index + 1
              )}
            </span>

            <div className="pt-0.5">
              <p
                className={`text-sm font-medium ${
                  isDone || isActive ? 'text-ink' : 'text-faint'
                }`}
              >
                {step.label}
              </p>
              <p className={`text-xs ${isActive ? 'text-muted' : 'text-faint'}`}>
                {step.description}
              </p>
            </div>
          </li>
        )
      })}
    </ol>
  )
}
