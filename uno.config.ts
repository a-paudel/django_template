import { defineConfig, presetUno } from "unocss";

export default defineConfig({
    presets: [
        presetUno({
            dark: "class"
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
            "bg": "#f2f2f2",
            "fg": "#000000",
            // accent for shadows, borders, etc.
            "accent": "gray",
            // muted colors
            "muted": "gray",
            // border colros
            "border": "gray",
            "input": "gray",
            // button colors
            "primary": "steelblue",
            "primary-fg": "#ffffff",
            "secondary": "gray",
            "secondary-fg": "#ffffff",
            "success": "green",
            "success-fg": "#ffffff",
            "danger": "red",
            "danger-fg": "#ffffff",
        }
    },
})