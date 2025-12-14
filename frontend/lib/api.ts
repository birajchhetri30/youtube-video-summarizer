export async function processVideo(
  url: string,
  question?: string
) {
  const res = await fetch("http://localhost:8000/process", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url, question }),
  });

  if (!res.ok) {
    throw new Error("Failed to process video");
  }

  return res.json();
}
