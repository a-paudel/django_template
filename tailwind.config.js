import { addDynamicIconSelectors } from '@iconify/tailwind';
import daisyui from 'daisyui';
import typography from "@tailwindcss/typography";

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./**/*.{html,py,js,css}",
    "!./node_modules/**",
    "!./.venv/**",
  ],
  darkMode: "media",
  theme: {
    extend: {},
  },
  daisyui: {
    themes: ["cupcake"],
  },
  plugins: [
    typography,
    daisyui,
    addDynamicIconSelectors(),
  ],
}

