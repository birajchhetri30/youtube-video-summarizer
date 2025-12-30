import ReactMarkdown from "react-markdown";

type Props = {
  summary: string;
};

export default function SummaryCard({ summary }: Props) {
  return (
    <div className="prose prose-gray max-w-none">
      <h2 className="text-2xl font-semibold mb-4">📌 Summary</h2>
      <ReactMarkdown>{summary}</ReactMarkdown>
    </div>
  );
}
