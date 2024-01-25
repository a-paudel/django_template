import { defineConfig } from "unocss";

export default defineConfig({
    cli: {
        entry: {
            outFile: "./static/css/uno.css",
            patterns: ["./**/*.{html,j2,py}"]
        }
    }
})