import 'vite/modulepreload-polyfill';
import "./unpoly_extensions.js"
import "../css/app.css";
import Alpine from "alpinejs"

// @ts-ignore
window.Alpine = Alpine
Alpine.start()