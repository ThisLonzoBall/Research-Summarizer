import Layout from "../components/Layout";
import ErrorBanner from "../components/ErrorBanner";
import SummaryCard from "../components/SummaryCard";
import PdfUpload from "../components/PdfUpload";
import useSummarizePdf from "../hooks/useSummarize";

function Home() {
  const { loading, summary, error, summarizePdf, setError } = useSummarizePdf();

  return (
    <Layout>
      <PdfUpload onSubmit={summarizePdf} loading={loading} />

      <ErrorBanner message={error} onClose={() => setError("")} />
      <SummaryCard body={summary} />
    </Layout>
  );
}

export default Home;