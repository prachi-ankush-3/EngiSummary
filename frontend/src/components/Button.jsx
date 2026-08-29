const VARIANTS = {
  primary:
    'bg-primary text-white hover:bg-primary-dark disabled:bg-border disabled:text-faint',
  secondary:
    'bg-white text-ink border border-border-strong hover:border-primary hover:text-primary disabled:text-faint disabled:hover:border-border-strong disabled:hover:text-faint',
  ghost: 'text-muted hover:text-ink hover:bg-black/[0.03] disabled:text-faint',
}

export default function Button({
  as: Component = 'button',
  variant = 'primary',
  icon: Icon,
  iconPosition = 'left',
  className = '',
  children,
  ...props
}) {
  return (
    <Component
      className={`inline-flex items-center justify-center gap-2 rounded-md px-4 py-2.5 text-sm font-medium transition-colors duration-150 disabled:cursor-not-allowed ${VARIANTS[variant]} ${className}`}
      {...props}
    >
      {Icon && iconPosition === 'left' && <Icon className="h-4 w-4" strokeWidth={2.2} />}
      {children}
      {Icon && iconPosition === 'right' && <Icon className="h-4 w-4" strokeWidth={2.2} />}
    </Component>
  )
}
