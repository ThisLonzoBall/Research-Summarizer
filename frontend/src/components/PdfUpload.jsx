import { useRef, useState } from "react";
import { FileUp, X } from "lucide-react";
import PrimaryButton from "./PrimaryButton";

function formatSize(bytes) {
  return bytes < 1024 * 1024 ? `${Math.round(bytes / 1024)} KB` : `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

export default function PdfUpload({ onSubmit, loading }) {
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef(null);

  const clear = () => {
    setFile(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped) setFile(dropped);
  };

  return (
    <div className="space-y-3">
      <div
        role="button"
        tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-6 py-10 text-center transition ${
          dragging
            ? "border-indigo-500 bg-indigo-50 dark:bg-indigo-950/40"
            : "border-slate-300 hover:border-indigo-400 dark:border-slate-700"
        }`}
      >
        <FileUp className="mb-3 size-8 text-indigo-500" />
        <p className="font-medium">Drop a PDF here or click to browse</p>
        <p className="mt-1 text-sm text-slate-500">Up to 20 MB · scanned pages are OCR'd automatically</p>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          hidden
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
      </div>

      <div className="flex items-center justify-between gap-3">
        {file ? (
          <div className="flex min-w-0 items-center gap-2 text-sm">
            <span className="truncate font-medium">{file.name}</span>
            <span className="shrink-0 text-slate-500">{formatSize(file.size)}</span>
            <button type="button" onClick={clear} aria-label="Remove file" className="text-slate-400 hover:text-red-600">
              <X className="size-4" />
            </button>
          </div>
        ) : (
          <span className="text-sm text-slate-500">No file selected</span>
        )}
        <PrimaryButton disabled={loading || !file} onClick={() => onSubmit(file)}>
          Summarize PDF
        </PrimaryButton>
      </div>
    </div>
  );
}
