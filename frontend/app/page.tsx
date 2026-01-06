"use client";

import { useState } from "react";
import UrlInput from "@/components/UrlInput";
import SummaryCard from "@/components/SummaryCard";
import QaCard from "@/components/QaCard";
import { processVideo } from "@/lib/api";

export default function Home() {
  const [summary, setSummary] = useState<string | null>(null);
  const [videoUrls, setVideoUrls] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (urls: string[]) => {
    setLoading(true);
    setSummary(null);
    setVideoUrls([]);
    setError(null);

    try {
      const data = await processVideo(urls);
      setSummary(data.summary);
      setVideoUrls(urls);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    }

    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-6 space-y-8">
        <h1 className="text-4xl font-extrabold text-center text-gray-900">
          🎥 YouTube Video Summarizer and Q&A
        </h1>

        {/* Input Card */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <UrlInput onSubmit={handleSubmit} loading={loading} />
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-2xl p-4 text-red-700">
            {error}
          </div>
        )}

        {/* Summary Card */}
        {summary && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <SummaryCard summary={summary} />
          </div>
        )}

        {/* Q&A Card */}
        {videoUrls.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <QaCard urls={videoUrls} />
          </div>
        )}
      </div>
    </main>
  );
}
