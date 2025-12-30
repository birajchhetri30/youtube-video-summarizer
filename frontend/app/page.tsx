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
    <main className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-6 space-y-8">
        <h1 className="text-4xl font-extrabold text-center text-gray-900">
          🎥 YouTube Transcript RAG
        </h1>

        {/* Input Card */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <UrlInput onSubmit={handleSubmit} loading={loading} />
        </div>

        {/* Summary Card */}
        {summary && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <SummaryCard summary={summary} />
          </div>
        )}

        {/* Q&A Card */}
        {videoUrl && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <QaCard url={videoUrl} />
          </div>
        )}
      </div>
    </main>
  );
}
