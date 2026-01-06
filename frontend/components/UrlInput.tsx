"use client";

import { useState } from "react";

type Props = {
  onSubmit: (urls: string[]) => void;
  loading: boolean;
};

export default function UrlInput({ onSubmit, loading }: Props) {
  const [urlsText, setUrlsText] = useState("");

  const handleSubmit = () => {
    const urls = urlsText.split('\n').map(url => url.trim()).filter(url => url);
    if (urls.length === 0) return;
    onSubmit(urls);
  };

  return (
    <div className="flex flex-col gap-3">
      <textarea
        placeholder="Paste YouTube URLs (one per line, max 3)"
        value={urlsText}
        onChange={(e) => setUrlsText(e.target.value)}
        className="rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black resize-none"
        rows={4}
      />
      <button
        onClick={handleSubmit}
        disabled={loading}
        className="rounded-lg bg-black px-6 py-3 text-white font-medium hover:bg-gray-800 disabled:opacity-50 self-start"
      >
        {loading ? "Processing..." : "Submit"}
      </button>
    </div>
  );
}
