/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './*.html',
    './scripts/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          dark: 'var(--color-dark)',
          slate: 'var(--color-slate)',
          blue: 'var(--color-blue)',
          neon: 'var(--color-neon)',
          purple: 'var(--color-purple)',
          accent: 'var(--color-accent)',
          danger: 'var(--color-danger)',
        },
        gemini: {
          bg: '#131314',
          sidebar: '#1E1F20',
          surface: '#1E1F20',
          input: '#282A2C',
          text: '#E3E3E3',
          blue: '#8AB4F8',
          user: '#191A1A',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Outfit', 'sans-serif'],
      },
      backgroundImage: {
        'radial-glow':
          'radial-gradient(circle at center, var(--color-blue-glow) 0%, transparent 70%)',
      },
    },
  },
  plugins: [],
};
