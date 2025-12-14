type Props = {
  summary: string;
};

export default function SummaryCard({ summary }: Props) {
  return (
    <div style={{ marginTop: 20 }}>
      <h2>📌 Summary</h2>
      <pre style={{ whiteSpace: "pre-wrap" }}>{summary}</pre>
    </div>
  );
}
