import { FileText, Github } from "lucide-react";

const REPO_URL = "https://github.com/ThisLonzoBall/Research-Summarizer";

function Layout({ children }) {
  return (
    <div className="mx-auto flex min-h-screen max-w-3xl flex-col px-4 py-10 sm:py-16">
      <header className="mb-8">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-indigo-600 p-2 text-white">
            <FileText className="size-6" />
          </div>
          <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Research Summarizer</h1>
        </div>
        <p className="mt-3 text-slate-600 dark:text-slate-400">
          Upload a paper or paste its text to get an abstract-style summary from a Pegasus model fine-tuned on arXiv.
        </p>
      </header>

      <main className="flex-1 space-y-4">{children}</main>

      <footer className="mt-12 border-t border-slate-200 pt-6 text-sm text-slate-500 dark:border-slate-800">
        <p>
          <span className="font-medium text-slate-700 dark:text-slate-300">How it works: </span>
          text is extracted from the PDF (with OCR for scanned pages), split into overlapping 1024-token windows,
          summarized window by window, then the partial summaries are summarized again.
        </p>
        <a
          href={REPO_URL}
          target="_blank"
          rel="noreferrer"
          className="mt-3 inline-flex items-center gap-1.5 font-medium text-indigo-600 hover:underline dark:text-indigo-400"
        >
          <Github className="size-4" /> Source on GitHub
        </a>
      </footer>
    </div>
  );
}

export default Layout;
