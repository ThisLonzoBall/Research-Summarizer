import { useState } from "react";
import { FileUp, Type } from "lucide-react";
import Layout from "../components/Layout";
import ErrorBanner from "../components/ErrorBanner";
import LoadingCard from "../components/LoadingCard";
import PdfUpload from "../components/PdfUpload";
import SummaryCard from "../components/SummaryCard";
import TextInput from "../components/TextInput";
import useSummarize from "../hooks/useSummarize";

const TABS = [
  { id: "pdf", label: "Upload PDF", icon: FileUp },
  { id: "text", label: "Paste text", icon: Type },
];

function Home() {
  const [tab, setTab] = useState("pdf");
  const [text, setText] = useState("");
  const { loading, result, error, setError, fromPdf, fromText, cancel } = useSummarize();

  return (
    <Layout>
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <div role="tablist" className="mb-5 inline-flex rounded-lg bg-slate-100 p-1 dark:bg-slate-800">
          {TABS.map(({ id, label, icon }) => {
            const Icon = icon;
            return (
              <button
                key={id}
                role="tab"
                type="button"
                aria-selected={tab === id}
                onClick={() => setTab(id)}
                className={`inline-flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium transition ${
                  tab === id
                    ? "bg-white shadow-sm dark:bg-slate-700"
                    : "text-slate-500 hover:text-slate-900 dark:hover:text-slate-100"
                }`}
              >
                <Icon className="size-4" />
                {label}
              </button>
            );
          })}
        </div>

        {tab === "pdf" ? (
          <PdfUpload onSubmit={fromPdf} loading={loading} />
        ) : (
          <TextInput value={text} onChange={setText} onSubmit={() => fromText(text)} loading={loading} />
        )}
      </div>

      <ErrorBanner message={error} onClose={() => setError("")} />
      {loading ? <LoadingCard onCancel={cancel} /> : <SummaryCard result={result} />}
    </Layout>
  );
}

export default Home;
