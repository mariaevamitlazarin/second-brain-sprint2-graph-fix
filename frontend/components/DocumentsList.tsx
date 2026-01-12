"use client";

import { useEffect, useState } from "react";

type ExtractionMetadata = {
  text_length: number;
  word_count: number;
  page_count?: number | null;
  row_count?: number | null;
  column_count?: number | null;
  sheet_names: string[];
  extraction_engine?: string | null;
};

type DocumentRecord = {
  id: string;
  original_filename: string;
  file_extension: string;
  area?: string | null;
  subject?: string | null;
  status: string;
  duplicate_of?: string | null;
  created_at: string;
  summary?: string | null;
  keywords: string[];
  extraction_metadata: ExtractionMetadata;
  extraction_error?: string | null;
};

type DocumentsResponse = {
  total: number;
  documents: DocumentRecord[];
};

export function DocumentsList() {
  const [data, setData] = useState<DocumentsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [processingId, setProcessingId] = useState<string | null>(null);

  async function loadDocuments() {
    try {
      const response = await fetch("http://localhost:8000/api/documents");
      const payload = await response.json();
      setData(payload);
      setError(null);
    } catch {
      setError("Could not reach the backend at http://localhost:8000.");
    }
  }

  async function reprocess(documentId: string) {
    setProcessingId(documentId);
    try {
      await fetch(`http://localhost:8000/api/documents/${documentId}/reprocess`, {
        method: "POST",
      });
      await loadDocuments();
      window.dispatchEvent(new Event("second-brain-refresh"));
    } finally {
      setProcessingId(null);
    }
  }

  useEffect(() => {
    loadDocuments();
    window.addEventListener("second-brain-refresh", loadDocuments);
    return () => window.removeEventListener("second-brain-refresh", loadDocuments);
  }, []);

  return (
    <section className="panel documentPanel">
      <div className="panelHeader">
        <div>
          <h2>Document Registry</h2>
          <p>Processed files, extraction metadata, summary, keywords, and duplicate status.</p>
        </div>
        <button type="button" onClick={loadDocuments}>Refresh</button>
      </div>

      {error && <p className="error">{error}</p>}
      {!data && !error && <p>Loading documents...</p>}
      {data && data.total === 0 && <p>No documents uploaded yet.</p>}

      {data && data.total > 0 && (
        <div className="documents">
          {data.documents.map((document) => (
            <article key={document.id} className="documentCard expanded">
              <div className="documentMain">
                <div className="documentTitleRow">
                  <strong>{document.original_filename}</strong>
                  <span className={document.status === "duplicate" ? "badge duplicate" : document.status === "failed" ? "badge failed" : "badge"}>
                    {document.status}
                  </span>
                </div>

                <span>{document.area || "No area"} / {document.subject || "No subject"}</span>

                {document.summary && <p className="summary">{document.summary}</p>}
                {document.extraction_error && <p className="error">Extraction error: {document.extraction_error}</p>}

                <div className="metadataGrid">
                  <small>Type: {document.file_extension}</small>
                  <small>Words: {document.extraction_metadata.word_count}</small>
                  <small>Text chars: {document.extraction_metadata.text_length}</small>
                  {document.extraction_metadata.page_count ? <small>Pages: {document.extraction_metadata.page_count}</small> : null}
                  {document.extraction_metadata.row_count ? <small>Rows: {document.extraction_metadata.row_count}</small> : null}
                  {document.extraction_metadata.extraction_engine ? <small>Engine: {document.extraction_metadata.extraction_engine}</small> : null}
                </div>

                {document.keywords.length > 0 && (
                  <div className="keywordRow">
                    {document.keywords.slice(0, 8).map((keyword) => (
                      <span key={keyword} className="keyword">{keyword}</span>
                    ))}
                  </div>
                )}
              </div>

              {document.status !== "duplicate" && (
                <button
                  type="button"
                  className="secondaryButton"
                  onClick={() => reprocess(document.id)}
                  disabled={processingId === document.id}
                >
                  {processingId === document.id ? "Processing..." : "Reprocess"}
                </button>
              )}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
