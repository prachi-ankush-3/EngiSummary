/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#1B2430',
        muted: '#5B6B7C',
        faint: '#8FA0B3',
        canvas: '#F4F7FA',
        surface: '#FFFFFF',
        border: {
          DEFAULT: '#D9E1E8',
          strong: '#B9C6D3',
        },
        primary: {
          DEFAULT: '#1D4E89',
          dark: '#123258',
          light: '#2E6FBE',
        },
        accent: '#2E6FBE',
        success: {
          DEFAULT: '#2F7A4F',
          bg: '#E7F3EB',
          border: '#BFE0CB',
        },
        danger: {
          DEFAULT: '#B3432B',
          bg: '#FBEDE9',
          border: '#F0C7BB',
        },
      },
      fontFamily: {
        sans: ['"IBM Plex Sans"', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'monospace'],
      },
      backgroundImage: {
        blueprint:
          'linear-gradient(to right, rgba(29,78,137,0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(29,78,137,0.05) 1px, transparent 1px), linear-gradient(to right, rgba(29,78,137,0.09) 1px, transparent 1px), linear-gradient(to bottom, rgba(29,78,137,0.09) 1px, transparent 1px)',
      },
      backgroundSize: {
        blueprint: '16px 16px, 16px 16px, 96px 96px, 96px 96px',
      },
      boxShadow: {
        panel: '0 1px 2px rgba(27, 36, 48, 0.04), 0 8px 24px -12px rgba(27, 36, 48, 0.12)',
      },
      keyframes: {
        'dash-scan': {
          '0%': { backgroundPosition: '0 0' },
          '100%': { backgroundPosition: '32px 0' },
        },
      },
      animation: {
        'dash-scan': 'dash-scan 1s linear infinite',
      },
    },
  },
  plugins: [],
}
