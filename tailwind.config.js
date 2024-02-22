import typography from "@tailwindcss/typography"
import { addDynamicIconSelectors } from "@iconify/tailwind"
import daisyui from "daisyui"

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.html',
    './**/*.py',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    typography,
    daisyui,
    addDynamicIconSelectors(),
  ],
}

