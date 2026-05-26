/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        'divine-gold':   '#D4AF37',
        'faith-blue':    '#1B3A57',
        'spirit-cream':  '#F5E6D3',
        'life-green':    '#7CB342',
        'spirit-purple': '#9575CD',
      },
      fontFamily: {
        scripture: ['Georgia', 'serif'],
        body:      ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
