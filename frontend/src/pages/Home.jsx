import { useState } from "react";
import Layout from "../components/Layout";
import TextInput from "../components/TextInput";
import PrimaryButton from "../components/PrimaryButton";
import ErrorBanner from "../components/ErrorBanner";
import SummaryCard from "../components/SummaryCard";
import useSummarize from "../hooks/useSummarize";

function Home() {
    const [text, setText]= useState("");
    const { loading, summary, error , summarize, setError} = useSummarize();

    const submit = () => summarize(text);

    return (
        <Layout>
        <div className="search">
            <TextInput
            value={text}
            onChange={setText}
            placeholder="Paste or type text to summarize…"
            onEnter={submit}
            />
            <PrimaryButton disabled={loading || !text.trim()} onClick={submit}>
            {loading ? "Summarizing…" : "Summarize"}
            </PrimaryButton>
        </div>

        <ErrorBanner message={error} onClose={() => setError("")} />
        <SummaryCard body={summary} />
        </Layout>
    );
}

export default Home;