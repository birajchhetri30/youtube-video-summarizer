"use client";

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
    <div style={{ marginTop: 30 }}>
      <h2>❓ Ask a Question</h2>
      <input
        type="text"
        placeholder="Ask something about the video"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{ width: "70%", padding: 8 }}
      />
      <button onClick={askQuestion} disabled={loading} style={{ marginLeft: 10 }}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <div style={{ marginTop: 15 }}>
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}
