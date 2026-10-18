import PrimaryButton from "./PrimaryButton";

const MIN_CHARS = 50;

function wordCount(text) {
  return text.trim() ? text.trim().split(/\s+/).length : 0;
}

export default function TextInput({ value, onChange, onSubmit, loading }) {
  const ready = value.trim().length >= MIN_CHARS && !loading;

  const handleKeyDown = (e) => {
    // Ctrl/Cmd+Enter submits; plain Enter inserts a newline as usual.
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey) && ready) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="space-y-3">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        rows={10}
        placeholder="Paste the abstract, introduction or full text of a paper…"
        className="w-full resize-y rounded-xl border border-slate-300 bg-white p-4 text-sm leading-relaxed shadow-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-slate-700 dark:bg-slate-900"
      />
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm text-slate-500">
          {wordCount(value).toLocaleString()} words · Ctrl+Enter to submit
        </span>
        <PrimaryButton disabled={!ready} onClick={onSubmit}>
          Summarize text
        </PrimaryButton>
      </div>
    </div>
  );
}
