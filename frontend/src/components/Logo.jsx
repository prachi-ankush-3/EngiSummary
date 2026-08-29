import { Ruler } from 'lucide-react'

export default function Logo({ size = 'md' }) {
  const isLarge = size === 'lg'

  return (
    <div className="flex items-center gap-2.5">
      <span
        className={`flex items-center justify-center rounded-md bg-primary text-white ${
          isLarge ? 'h-11 w-11' : 'h-8 w-8'
        }`}
      >
        <Ruler className={isLarge ? 'h-6 w-6' : 'h-[18px] w-[18px]'} strokeWidth={2.2} />
      </span>
      <span
        className={`font-semibold tracking-tight text-ink ${isLarge ? 'text-2xl' : 'text-lg'}`}
      >
        Engi<span className="text-primary">Summary</span>
      </span>
    </div>
  )
}
