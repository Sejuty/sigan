"use client";

import { useState, useEffect, useRef } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const HISTORY_KEY = "sigan_translate_history";
const MAX_HISTORY = 10;

type Direction = "to_english" | "to_sigan";
type HistoryItem = { input: string; output: string; direction: Direction };

export default function TranslatePage() {
  const [direction, setDirection] = useState<Direction>("to_english");
  const [input, setInput]         = useState("");
  const [output, setOutput]       = useState("");
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState("");
  const [history, setHistory]     = useState<HistoryItem[]>([]);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const saved = localStorage.getItem(HISTORY_KEY);
    if (saved) setHistory(JSON.parse(saved));
    inputRef.current?.focus();
  }, []);

  const pushHistory = (item: HistoryItem) => {
    setHistory(prev => {
      const next = [item, ...prev.filter(h => h.input !== item.input || h.direction !== item.direction)].slice(0, MAX_HISTORY);
      localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
      return next;
    });
  };

  const translate = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError("");
    setOutput("");
    try {
      const res = await fetch(`${API}/translate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input.trim(), direction }),
      });
      const data = await res.json();
      if (data.success) {
        setOutput(data.result);
        pushHistory({ input: input.trim(), output: data.result, direction });
      } else {
        const err = Array.isArray(data.error) ? data.error.join(" · ") : String(data.error);
        setError(err);
      }
    } catch {
      setError("Could not reach API — is the server running?");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") translate();
  };

  const flipDirection = () => {
    setDirection(d => d === "to_english" ? "to_sigan" : "to_english");
    setInput(output);
    setOutput("");
    setError("");
  };

  const fromLabel = direction === "to_english" ? "Sigan"   : "English";
  const toLabel   = direction === "to_english" ? "English" : "Sigan";
  const isSigan   = (dir: Direction, role: "in" | "out") =>
    (role === "in"  && dir === "to_english") ||
    (role === "out" && dir === "to_sigan");

  return (
    <div className="mx-auto max-w-3xl px-6 py-10 flex flex-col gap-8">
      {/* Direction toggle */}
      <div className="flex justify-center">
        <div className="flex bg-slate-900 border border-slate-800 rounded-xl p-1 gap-1">
          {(["to_english", "to_sigan"] as Direction[]).map(d => (
            <button
              key={d}
              onClick={() => { setDirection(d); setOutput(""); setError(""); }}
              className={`px-5 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                direction === d
                  ? "bg-violet-500/20 text-violet-300"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {d === "to_english" ? "Sigan → English" : "English → Sigan"}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="flex flex-col gap-2">
        <label className="text-xs text-slate-500 uppercase tracking-wider">{fromLabel}</label>
        <textarea
          ref={inputRef}
          rows={4}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={
            direction === "to_english"
              ? "ayu siganovrak gar truku"
              : "I was seeing the tree"
          }
          className={`w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm outline-none focus:border-violet-500 transition-colors resize-none placeholder-slate-700 ${
            isSigan(direction, "in") ? "sigan" : ""
          }`}
        />
        <div className="flex items-center justify-between">
          <p className="text-xs text-slate-600">Ctrl+Enter to translate</p>
          <button
            onClick={translate}
            disabled={loading || !input.trim()}
            className="px-5 py-1.5 bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors"
          >
            {loading ? "…" : "Translate"}
          </button>
        </div>
      </div>

      {/* Output */}
      {(output || error) && (
        <div className="flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <label className="text-xs text-slate-500 uppercase tracking-wider">{toLabel}</label>
            {output && (
              <button
                onClick={flipDirection}
                className="text-xs text-slate-500 hover:text-violet-300 transition-colors"
              >
                ⇄ flip direction
              </button>
            )}
          </div>
          {error ? (
            <div className="bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3 text-red-400 text-sm">
              {error}
            </div>
          ) : (
            <div className={`bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-slate-100 text-sm min-h-[3rem] ${
              isSigan(direction, "out") ? "sigan" : ""
            }`}>
              {output}
            </div>
          )}
        </div>
      )}

      {/* History */}
      {history.length > 0 && (
        <div className="flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <h2 className="text-xs text-slate-500 uppercase tracking-wider">Recent</h2>
            <button
              onClick={() => { setHistory([]); localStorage.removeItem(HISTORY_KEY); }}
              className="text-xs text-slate-600 hover:text-slate-400 transition-colors"
            >
              Clear
            </button>
          </div>
          <div className="space-y-1">
            {history.map((h, i) => (
              <button
                key={i}
                onClick={() => { setDirection(h.direction); setInput(h.input); setOutput(h.output); setError(""); }}
                className="w-full text-left flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-900/60 hover:bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors group"
              >
                <span className={`text-xs text-slate-300 truncate ${
                  (h.direction === "to_english") ? "sigan" : ""
                }`}>
                  {h.input}
                </span>
                <span className="text-slate-600 shrink-0 text-xs">→</span>
                <span className={`text-xs text-slate-400 truncate flex-1 ${
                  (h.direction === "to_sigan") ? "sigan" : ""
                }`}>
                  {h.output}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
