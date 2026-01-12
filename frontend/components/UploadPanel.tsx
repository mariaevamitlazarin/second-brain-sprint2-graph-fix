"use client";

import { FormEvent, useState } from "react";

type UploadResult = {
  message: string;
  is_duplicate: boolean;
  document: {
    id: string;
    original_filename: string;
    status: string;
    sha256: string;
    duplicate_of?: string | null;
    summary?: string | null;
    keywords?: string[];
  };
};

export function UploadPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [area, setArea] = useState("AI");
  const [subject, setSubject] = useState("Second Brain");
  const [source, setSource] = useState("Prototype test");
  const [result, setResult] = useState<UploadResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) return;

    setLoading(true);
    setResult(null);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("area", area);
    formData.append("subject", subject);
    formData.append("source", source);

    try {
      const response = await fetch("http://localhost:8000/api/documents/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }

      setResult(data);
      window.dispatchEvent(new Event("second-brain-refresh"));
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : "Upload failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel">
      <h2>Upload Knowledge</h2>
      <p>
        Upload PDF, Markdown, TXT, CSV, XLS, or XLSX files. Sprint 2 now extracts text,
        creates metadata, generates a first summary, and updates the graph API.
      </p>

      <form onSubmit={handleSubmit} className="uploadForm">
        <label>
          Area
          <input value={area} onChange={(event) => setArea(event.target.value)} />
        </label>

        <label>
          Subject
          <input value={subject} onChange={(event) => setSubject(event.target.value)} />
        </label>

        <label>
          Source
          <input value={source} onChange={(event) => setSource(event.target.value)} />
        </label>

        <label className="fileInput">
          File
          <input
            type="file"
            accept=".md,.txt,.csv,.xls,.xlsx,.pdf"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          />
        </label>

        <button type="submit" disabled={!file || loading}>
          {loading ? "Uploading and processing..." : "Upload and process"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className={result.is_duplicate ? "alert duplicate" : "alert success"}>
          <strong>{result.is_duplicate ? "Duplicate detected" : "Upload complete"}</strong>
          <span>{result.message}</span>
          <small>Status: {result.document.status}</small>
          <small>SHA-256: {result.document.sha256.slice(0, 24)}...</small>
          {result.document.summary && <small>Summary: {result.document.summary}</small>}
        </div>
      )}
    </section>
  );
}
