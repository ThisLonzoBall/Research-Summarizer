import { useRef, useState } from "react";
import axios from "axios";
import { errorMessage, summarizePdf, summarizeText } from "../services/api";

const MAX_PDF_MB = 20;

export default function useSummarize() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const controller = useRef(null);

  const run = async (request) => {
    controller.current?.abort();
    controller.current = new AbortController();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      setResult(await request(controller.current.signal));
    } catch (err) {
      if (!axios.isCancel(err)) setError(errorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const fromPdf = (file) => {
    if (!file) return setError("Please choose a PDF file.");
    if (file.type !== "application/pdf") return setError("Only PDF files are supported.");
    if (file.size > MAX_PDF_MB * 1024 * 1024) return setError(`PDFs must be under ${MAX_PDF_MB}MB.`);
    return run((signal) => summarizePdf(file, signal));
  };

  const fromText = (text) => run((signal) => summarizeText(text, signal));

  const cancel = () => controller.current?.abort();

  return { loading, result, error, setError, fromPdf, fromText, cancel };
}
