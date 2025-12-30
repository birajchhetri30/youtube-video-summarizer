"use client";

import { useState } from "react";

type Props = {
  onSubmit: (url: string) => void;
  loading: boolean;
};

export default function UrlInput({ onSubmit, loading }: Props) {
  const [url, setUrl] = useState("");

  return (
    <div className="flex gap-3">
      <input
        type="text"
        placeholder="Paste YouTube URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="flex-1 rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black"
      />
      <button
        onClick={() => onSubmit(url)}
        disabled={loading}
        className="rounded-lg bg-black px-6 py-3 text-white font-medium hover:bg-gray-800 disabled:opacity-50"
      >
        {loading ? "Processing..." : "Submit"}
      </button>
    </div>
  );
}
