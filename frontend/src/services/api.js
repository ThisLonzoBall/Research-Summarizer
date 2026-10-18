import axios from "axios";

// Empty base URL = same origin: the Vite dev server proxies /api to FastAPI,
// and in production FastAPI serves this app itself. Override with VITE_API_URL.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "",
  timeout: 10 * 60 * 1000, // long PDFs on CPU can take minutes
});

export function summarizeText(text, signal) {
  return api.post("/api/summarize", { text }, { signal }).then((r) => r.data);
}

export function summarizePdf(file, signal) {
  const form = new FormData();
  form.append("file", file);
  return api.post("/api/summarize/pdf", form, { signal }).then((r) => r.data);
}

export function errorMessage(err) {
  const detail = err?.response?.data?.detail;
  if (Array.isArray(detail)) return detail.map((d) => d.msg).join("; ");
  if (detail) return detail;
  if (err?.code === "ECONNABORTED") return "The request timed out. Try a shorter document.";
  if (err?.code === "ERR_NETWORK") return "Can't reach the summarization server. Is the backend running?";
  return err?.message || "Something went wrong.";
}
