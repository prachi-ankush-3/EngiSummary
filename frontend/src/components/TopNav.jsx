import { Link } from 'react-router-dom'
import Logo from './Logo.jsx'

export default function TopNav() {
  return (
    <header className="border-b border-border bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link to="/" aria-label="EngiSummary home">
          <Logo />
        </Link>
        <span className="hidden font-mono text-xs uppercase tracking-wider text-faint sm:block">
          Drawing Summary Generator
        </span>
      </div>
    </header>
  )
}
