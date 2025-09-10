
import { useState } from "react";
import api from "../services/api";

export default function useSummarizePdf() {
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");
  const [error, setError] = useState("");

  const summarizePdf = async (file) => {
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }
    if (file.type !== "application/pdf") {
      setError("Only PDF files are allowed.");
      return;
    }

    setLoading(true);
    setError("");
    setSummary("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const { data } = await api.post("/pdf/summary", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setSummary(data?.summary ?? JSON.stringify(data));
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return { loading, summary, error, summarizePdf, setError, setSummary };
}