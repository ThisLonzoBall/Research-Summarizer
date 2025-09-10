import { useRef, useState} from "react";
import PrimaryButton from "./PrimaryButton";

export default function PdfUpload({onSubmit, loading}){
    const [file, setFile]= useState(null);
    const inputRef = useRef(null);

    const pick = (e) => {
        const f = e.target.files?.[0];
        setFile(f || null);
    
    }

    const clear = () => {
        setFile(null);
        if (inputRef.current) inputRef.current.value= '';
    }

    return(
         <div className="search" style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <input
                ref={inputRef}
                type="file"
                accept="application/pdf"
                onChange={pick}
                aria-label="Upload PDF"
            />
            <PrimaryButton
                disabled={loading || !file}
                onClick={() => onSubmit(file)}
            >
                {loading ? "Summarizing…" : "Upload & Summarize"}
            </PrimaryButton>
            {file && (
                <button
                type="button"
                onClick={clear}
                style={{ border: "none", background: "transparent", cursor: "pointer" }}
                aria-label="Clear file"
                title="Clear"
                >
                ✕
                </button>
            )}
            </div>

    );
}