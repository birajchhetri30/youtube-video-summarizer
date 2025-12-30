"use client";

import ReactMarkdown from "react-markdown";

import { useState } from "react";
import { processVideo } from "@/lib/api";

type Props = {
  url: string;
};

export default function QaCard({ url }: Props) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer(null);

    try {
      const data = await processVideo(url, question);
      setAnswer(data.answer);
    } catch (err) {
      setAnswer("Error fetching answer");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex gap-3">
        <input
          type="text"
          placeholder="Ask something about the video"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="flex-1 rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black"
        />
        <button
          onClick={askQuestion}
          disabled={loading}
          className="rounded-lg bg-black px-6 py-3 text-white font-medium hover:bg-gray-800 disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      {answer && (
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <ReactMarkdown>{answer}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
