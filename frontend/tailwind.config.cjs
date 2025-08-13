module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,html}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          500: '#6366f1',
          700: '#4f46e5'
        },
        brand: {
          50: '#f0fdf4',
          100: '#dcfce7',
          500: '#10b981'
        }
      },
      borderRadius: { xl: '1rem' }
    }
  },
  plugins: []
};
