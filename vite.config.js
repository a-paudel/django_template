import { defineConfig } from "vite"

export default defineConfig({
    base: "/static/",
    build: {
        manifest: "manifest.json",
        outDir: "./static",
        rollupOptions: {
            input: "resources/js/app.js",
        },
    },
})