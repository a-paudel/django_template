import { defineConfig, presetIcons, presetUno, presetWebFonts } from "unocss";

export default defineConfig({
    presets: [
        presetUno({
            dark: "media",
        }),
        presetWebFonts({
            provider: "bunny",
            fonts: {
                sans: "Ubuntu",
            }
        }),
        presetIcons({
            collections: {
                carbon: () => import("@iconify-json/carbon/icons.json").then(i => i.default),
            }
        }),
    ],
    cli: {
        entry: {
            outFile: "./static/css/main.css",
            patterns: ["./**/*.{html,j2,py}"]
        }
    },
    theme: {
        colors: {
            dark: "#020817",
            light: "#fafafa",
            primary: "#3b82f6",
        }
    },
    shortcuts: {
        "bg-base": "bg-light dark:bg-dark",
        "text-base": "text-dark dark:text-light",
        "base": "bg-base text-base",
        // 
        "bg-inverse": "bg-dark dark:bg-light",
        "text-inverse": "text-light dark:text-dark",
        "inverse": "bg-inverse !text-inverse",
        // 
        "text-muted": "text-base text-opacity-70 dark:text-opacity-70",
        // 
        "border-base": "border-solid border-dark border-opacity-50 dark:border-light dark:border-opacity-50",
        "border-inverse": "border-solid border-light border-opacity-80 dark:border-dark dark:border-opacity-80",
        // 
        "shadow-base": "shadow-dark dark:shadow-light shadow shadow-opacity-30 dark:shadow-opacity-30",
        // components
        "button": "inverse hover:opacity-80 cursor-pointer p2 border-none rounded",
        "button-inverse": "base hover:opacity-80 cursor-pointer p2 border-base border rounded",
        "card": "base border-base border rounded-lg shadow-base p4",
        "input": "base border-base border rounded p2 focus:outline-none focus:ring-2 focus:ring-primary flex-1",
        "link": "cursor-pointer text-muted hover:text-opacity-100 decoration-none",
    }
})
