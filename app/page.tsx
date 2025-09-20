"use client";
import { useState } from "react";

type Stats = {
  count: number; sum: number; mean: number; median: number;
  min: number; max: number; stdevPopulation: number; stdevSample: number;
  sorted: number[];
};

export default function Home() {
  const [raw, setRaw] = useState("1, 2, 3, 4, 5");
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null); setStats(null); setLoading(true);
    try {
      // Use FastAPI directly when running locally, Vercel route in production
      const isLocal =
      typeof window !== "undefined" &&
      (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1");

      const apiUrl = isLocal ? "http://localhost:8000/" : "/api/stats";

      const res = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ numbers: raw }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || data?.error || "Request failed");
      setStats(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={styles.main}>
      <div style={styles.card}>
        <h1 style={styles.title}>Simple Stats (Python backend)</h1>
        <p style={styles.subtitle}>
          Enter numbers separated by commas or spaces. Example: <code>10, 3.5, -2 7</code>
        </p>

        <form onSubmit={onSubmit} style={styles.form}>
          <textarea
            rows={4}
            value={raw}
            onChange={(e) => setRaw(e.target.value)}
            placeholder="e.g. 10, 3.5, -2, 7"
            style={styles.textarea}
          />
          <button type="submit" style={styles.button} disabled={loading}>
            {loading ? "Calculating…" : "Calculate"}
          </button>
        </form>

        {error && <p style={styles.error}>⚠️ {error}</p>}

        {stats && (
          <div style={styles.results}>
            <h2 style={styles.h2}>Results</h2>
            <ul style={styles.ul}>
              <li><strong>Count:</strong> {stats.count}</li>
              <li><strong>Sum:</strong> {stats.sum}</li>
              <li><strong>Mean:</strong> {stats.mean}</li>
              <li><strong>Median:</strong> {stats.median}</li>
              <li><strong>Min:</strong> {stats.min}</li>
              <li><strong>Max:</strong> {stats.max}</li>
              <li><strong>Std Dev (Population):</strong> {stats.stdevPopulation}</li>
              <li><strong>Std Dev (Sample):</strong> {Number.isNaN(stats.stdevSample) ? "n/a (need ≥2)" : stats.stdevSample}</li>
              <li><strong>Sorted:</strong> {stats.sorted.join(", ")}</li>
            </ul>
          </div>
        )}
      </div>
      <footer style={styles.footer}>
        Next.js frontend → Python (FastAPI) at <code>/api/stats</code> on Vercel
      </footer>
    </main>
  );
}

const styles: Record<string, React.CSSProperties> = {
  main: { minHeight: "100dvh", display: "grid", placeItems: "center", padding: 24, background: "#0b1020" },
  card: { width: "100%", maxWidth: 720, background: "#121933", color: "#e6e9f5", padding: 24, borderRadius: 16, boxShadow: "0 10px 30px rgba(0,0,0,.35)" },
  title: { margin: 0, fontSize: 28 },
  subtitle: { opacity: .9, marginTop: 8 },
  form: { display: "grid", gap: 12, marginTop: 16 },
  textarea: { padding: 12, borderRadius: 10, border: "1px solid #2a335a", background: "#0d1430", color: "#e6e9f5", fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace" },
  button: { padding: "10px 14px", borderRadius: 10, border: "1px solid #3a4590", background: "#25307a", color: "#fff", cursor: "pointer" },
  error: { color: "#ffb4b4", marginTop: 8 },
  results: { marginTop: 16, background: "#0d1430", padding: 16, borderRadius: 12, border: "1px solid #2a335a" },
  h2: { marginTop: 0 },
  ul: { lineHeight: 1.9 },
  footer: { marginTop: 16, color: "#aeb6de", fontSize: 13 },
};
