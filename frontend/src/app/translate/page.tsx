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
  const [copied, setCopied]       = useState(false);
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

  const flip = () => {
    setDirection(d => d === "to_english" ? "to_sigan" : "to_english");
    setInput(output);
    setOutput("");
    setError("");
    setCopied(false);
  };

  const copyOutput = async () => {
    if (!output) return;
    await navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const changeDirection = (d: Direction) => {
    setDirection(d);
    setOutput("");
    setError("");
    setCopied(false);
  };

  const fromLabel = direction === "to_english" ? "Sigan"   : "English";
  const toLabel   = direction === "to_english" ? "English" : "Sigan";
  const inputIsSigan  = direction === "to_english";
  const outputIsSigan = direction === "to_sigan";

  return (
    <div className="mx-auto max-w-5xl px-6 py-10 flex flex-col gap-8">

      {/* Two-panel translator */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <div className="flex flex-col md:flex-row">

          {/* Input panel */}
          <div className="flex-1 flex flex-col min-w-0">
            <div className="px-4 py-3 border-b border-slate-800">
              <span className="text-xs text-slate-500 uppercase tracking-wider">{fromLabel}</span>
            </div>
            <textarea
              ref={inputRef}
              rows={7}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                direction === "to_english"
                  ? "elva velorovrak al silvao"
                  : "I was seeing the tree"
              }
              className={`w-full bg-transparent px-4 py-4 text-sm outline-none resize-none placeholder-slate-700 text-slate-100 ${
                inputIsSigan ? "sigan" : ""
              }`}
            />
          </div>

          {/* Output panel */}
          <div className="flex-1 flex flex-col min-w-0 border-t md:border-t-0 md:border-l border-slate-800">
            <div className="px-4 py-3 border-b border-slate-800 flex items-center justify-between">
              <span className="text-xs text-slate-500 uppercase tracking-wider">{toLabel}</span>
              {output && (
                <button
                  onClick={copyOutput}
                  className="text-xs text-slate-500 hover:text-violet-300 transition-colors"
                >
                  {copied ? "✓ copied" : "copy"}
                </button>
              )}
            </div>
            <div className={`flex-1 px-4 py-4 text-sm min-h-[7rem] ${outputIsSigan ? "sigan" : ""}`}>
              {loading ? (
                <span className="text-slate-600 animate-pulse">Translating…</span>
              ) : error ? (
                <span className="text-red-400">{error}</span>
              ) : output ? (
                <span className="text-slate-100">{output}</span>
              ) : (
                <span className="text-slate-700">Translation will appear here</span>
              )}
            </div>
          </div>
        </div>

        {/* Footer action bar */}
        <div className="border-t border-slate-800 flex items-center gap-3 px-4 py-3">
          <div className="flex gap-0.5 bg-slate-950 rounded-lg p-0.5">
            {(["to_english", "to_sigan"] as Direction[]).map(d => (
              <button
                key={d}
                onClick={() => changeDirection(d)}
                className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
                  direction === d
                    ? "bg-violet-500/20 text-violet-300"
                    : "text-slate-500 hover:text-slate-300"
                }`}
              >
                {d === "to_english" ? "Sig → En" : "En → Sig"}
              </button>
            ))}
          </div>
          <button
            onClick={flip}
            title="Swap input ↔ output"
            className="text-xs text-slate-500 hover:text-violet-300 transition-colors"
          >
            ⇄ swap
          </button>
          <span className="text-xs text-slate-600 flex-1">Ctrl+Enter</span>
          <button
            onClick={translate}
            disabled={loading || !input.trim()}
            className="px-5 py-1.5 bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors"
          >
            {loading ? "…" : "Translate"}
          </button>
        </div>
      </div>

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
                onClick={() => {
                  setDirection(h.direction);
                  setInput(h.input);
                  setOutput(h.output);
                  setError("");
                  setCopied(false);
                }}
                className="w-full text-left flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-900/60 hover:bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors"
              >
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-500 shrink-0 font-mono">
                  {h.direction === "to_english" ? "Sig→En" : "En→Sig"}
                </span>
                <span className={`text-xs text-slate-300 truncate ${h.direction === "to_english" ? "sigan" : ""}`}>
                  {h.input}
                </span>
                <span className="text-slate-600 shrink-0 text-xs">→</span>
                <span className={`text-xs text-slate-400 truncate flex-1 ${h.direction === "to_sigan" ? "sigan" : ""}`}>
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
