import { useRef, useState } from "react";
import { Plus } from "lucide-react";
import PrimaryButton from "./PrimaryButton";

export default function PdfUpload({ onSubmit, loading }) {
  const [file, setFile] = useState(null);
  const inputRef = useRef(null);

  const pick = (e) => {
    const f = e.target.files?.[0];
    setFile(f || null);
  };

  const clear = () => {
    setFile(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const triggerInput = () => {
    inputRef.current?.click();
  };

  return (
    <div className="flex items-center gap-3">
      {/* Hidden file input */}
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        onChange={pick}
        aria-label="Upload PDF"
        className="hidden"
      />

      {/* Custom Add button */}
      <button
        type="button"
        onClick={triggerInput}
        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-full shadow hover:bg-blue-700 transition"
      >
        <Plus size={20} />
        {file ? "Change PDF" : "Add PDF"}
      </button>

      {/* Submit button */}
      <PrimaryButton
        disabled={loading || !file}
        onClick={() => onSubmit(file)}
      >
        {loading ? "Summarizing…" : "Upload & Summarize"}
      </PrimaryButton>

      {/* Clear button */}
      {file && (
        <button
          type="button"
          onClick={clear}
          className="text-gray-500 hover:text-red-600 transition"
          aria-label="Clear file"
          title="Clear"
        >
          ✕
        </button>
      )}
    </div>
  );
}


