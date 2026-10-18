import { useState } from "react";
import { Check, Copy } from "lucide-react";

function SummaryCard({ result }) {
  const [copied, setCopied] = useState(false);
  if (!result) return null;

  const copy = async () => {
    await navigator.clipboard.writeText(result.summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="font-semibold">Summary</h2>
        <button
          type="button"
          onClick={copy}
          className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-indigo-600"
        >
          {copied ? <Check className="size-4" /> : <Copy className="size-4" />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <p className="whitespace-pre-line break-words leading-relaxed">{result.summary}</p>
      <dl className="mt-4 flex flex-wrap gap-x-6 gap-y-1 border-t border-slate-100 pt-3 text-xs text-slate-500 dark:border-slate-800">
        <div>
          <dt className="inline">Input: </dt>
          <dd className="inline">{result.input_words.toLocaleString()} words</dd>
        </div>
        <div>
          <dt className="inline">Summary: </dt>
          <dd className="inline">{result.summary.split(/\s+/).length} words</dd>
        </div>
        <div>
          <dt className="inline">Time: </dt>
          <dd className="inline">{result.elapsed_seconds}s</dd>
        </div>
        <div className="truncate">
          <dt className="inline">Model: </dt>
          <dd className="inline">{result.model}</dd>
        </div>
      </dl>
    </section>
  );
}

export default SummaryCard;
