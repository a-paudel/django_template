import { defineConfig } from "vite";

export default defineConfig({
    base: "/static/",
    build: {
        manifest: "manifest.json",
        outDir: "./public",
        rollupOptions: {
            input: [
                "resources/js/app.ts",
                "resources/css/app.css",
            ]
        }
    }
})