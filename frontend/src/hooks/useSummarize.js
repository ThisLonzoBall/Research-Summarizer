import { useState } from "react";
import api from "../services/api";

export default function useSummarize() {
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");
  const [error, setError] = useState("");

  const summarize = async (text) => {
    if (!text?.trim()) return;
    setLoading(true);
    setError("");
    setSummary("");
    try {
      const { data } = await api.post("/predict", { text });
      setSummary(data?.summary ?? JSON.stringify(data));
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return { loading, summary, error, summarize, setError };
}