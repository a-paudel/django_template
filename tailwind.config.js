import typography from "@tailwindcss/typography"
import { addDynamicIconSelectors } from "@iconify/tailwind"
import daisyui from 'daisyui'

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./**/*.{html,css,js,py,j2}",
    "!./node_modules/**/*",
    "!./.git/**/*",
    "!./.venv/**/*",
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

