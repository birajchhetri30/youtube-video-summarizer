"use client";

import { useState } from "react";
import UrlInput from "@/components/UrlInput";
import SummaryCard from "@/components/SummaryCard";
import QaCard from "@/components/QaCard";
import { processVideo } from "@/lib/api";

export default function Home() {
  const [summary, setSummary] = useState<string | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (url: string) => {
    setLoading(true);
    setSummary(null);
    setVideoUrl(null);

    try {
      const data = await processVideo(url);
      setSummary(data.summary);
      setVideoUrl(url);
    } catch (err) {
      alert("Failed to process video");
    }

    setLoading(false);
  };

  return (
    <main style={{ padding: 40 }}>
      <h1>🎥 YouTube Transcript RAG</h1>

      <UrlInput onSubmit={handleSubmit} loading={loading} />

      {summary && <SummaryCard summary={summary} />}

      {videoUrl && <QaCard url={videoUrl} />}
    </main>
  );
}
