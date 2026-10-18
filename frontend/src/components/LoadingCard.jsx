import { useEffect, useState } from "react";
import { Loader2 } from "lucide-react";

function LoadingCard({ onCancel }) {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className="mb-4 flex items-center justify-between text-sm">
        <span className="inline-flex items-center gap-2 font-medium">
          <Loader2 className="size-4 animate-spin text-indigo-500" />
          Summarizing… {seconds}s
        </span>
        <button type="button" onClick={onCancel} className="text-slate-500 hover:text-red-600">
          Cancel
        </button>
      </div>
      <div className="animate-pulse space-y-2">
        {["w-full", "w-11/12", "w-full", "w-4/5", "w-2/3"].map((w, i) => (
          <div key={i} className={`h-3 rounded bg-slate-200 dark:bg-slate-800 ${w}`} />
        ))}
      </div>
      {seconds > 20 && (
        <p className="mt-4 text-xs text-slate-500">
          Long papers are summarized in several passes, which can take a minute or two on CPU.
        </p>
      )}
    </section>
  );
}

export default LoadingCard;
