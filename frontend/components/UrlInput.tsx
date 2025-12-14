"use client";

import { useState } from "react";

type Props = {
  onSubmit: (url: string) => void;
  loading: boolean;
};

export default function UrlInput({ onSubmit, loading }: Props) {
  const [url, setUrl] = useState("");

  return (
    <div style={{ marginBottom: 20 }}>
      <input
        type="text"
        placeholder="Paste YouTube URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: "70%", padding: 8 }}
      />
      <button
        onClick={() => onSubmit(url)}
        disabled={loading}
        style={{ marginLeft: 10, padding: 8 }}
      >
        {loading ? "Processing..." : "Submit"}
      </button>
    </div>
  );
}
