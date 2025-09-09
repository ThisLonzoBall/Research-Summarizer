import { useEffect, useRef } from "react";
import PrimaryButton from "./PrimaryButton";   // ✅ import your existing button
import "./TextInput.css";

export default function TextInput({ value, onChange, placeholder, onEnter, loading = false }) {
  const ref = useRef(null);

  // Auto-resize the textarea
  useEffect(() => {
    const ta = ref.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 200) + "px";
  }, [value]);

  const handleKeyDown = (e) => {
    // Shift+Enter = newline, Enter = submit
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (value.trim() && !loading) {
        onEnter?.();
      }
    }
  };

  return (
    <div className="chatbar">
      <textarea
        ref={ref}
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <PrimaryButton
        disabled={!value.trim() || loading}
        onClick={() => !loading && value.trim() && onEnter?.()}
      >
        {loading ? "Summarizing…" : "Summarize"}
      </PrimaryButton>
    </div>
  );
}