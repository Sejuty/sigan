"use client";

import { useState, useRef, useEffect } from "react";
import TokenTable from "@/components/TokenTable";
import ParseTree, { type TreeNode } from "@/components/ParseTree";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Token = {
  surface: string;
  pos: string;
  stem: string;
  tense: string | null;
  aspect: string | null;
};

type Result = {
  valid: boolean;
  tokens: Token[];
  tree: TreeNode | null;
  errors: string[];
};

const EXAMPLES = [
  "ayu siganovrak gar truku",
  "hiru walkag tov gar homu yestom",
  "ayu noth spekor worda",
  "huzh findar gar rotha",
  "ayun lovakov hirun",
];

export default function ValidatePage() {
  const [input, setInput]     = useState("");
  const [result, setResult]   = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => { inputRef.current?.focus(); }, []);

  const run = async (sentence?: string) => {
    const text = (sentence ?? input).trim();
    if (!text) return;
    if (sentence) setInput(sentence);
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch(`${API}/validate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sentence: text }),
      });
      setResult(await res.json());
    } catch {
      setError("Could not reach API — is the server running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl px-6 py-10 flex flex-col gap-8">
      {/* Input */}
      <div className="flex flex-col gap-3">
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && run()}
            placeholder="ayu sigan gar truku"
            className="sigan flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-700 outline-none focus:border-violet-500 transition-colors"
          />
          <button
            onClick={() => run()}
            disabled={loading || !input.trim()}
            className="px-5 py-2 bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-medium rounded-xl transition-colors shrink-0"
          >
            {loading ? "…" : "Validate"}
          </button>
        </div>

        {/* Examples */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-slate-600">Try:</span>
          {EXAMPLES.map(ex => (
            <button
              key={ex}
              onClick={() => run(ex)}
              className="sigan text-xs text-slate-500 hover:text-violet-300 transition-colors"
            >
              {ex}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3 text-red-400 text-sm">
          {error}
        </div>
      )}

      {result && (
        <div className="flex flex-col gap-6">
          {/* Verdict */}
          <div className={`flex items-center gap-3 px-4 py-3 rounded-xl border ${
            result.valid
              ? "bg-emerald-500/10 border-emerald-500/20"
              : "bg-red-500/10    border-red-500/20"
          }`}>
            <span className={`text-2xl ${result.valid ? "text-emerald-400" : "text-red-400"}`}>
              {result.valid ? "✓" : "✗"}
            </span>
            <div>
              <p className={`font-semibold ${result.valid ? "text-emerald-300" : "text-red-300"}`}>
                {result.valid ? "VALID" : "INVALID"}
              </p>
              {result.errors.length > 0 && (
                <p className="text-red-400/80 text-sm mt-0.5">{result.errors.join(" · ")}</p>
              )}
            </div>
          </div>

          {/* Token breakdown */}
          {result.tokens.length > 0 && (
            <section className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <h2 className="text-xs text-slate-500 uppercase tracking-wider mb-4">
                Token breakdown
              </h2>
              <TokenTable tokens={result.tokens} />
            </section>
          )}

          {/* Parse tree */}
          {result.tree && (
            <section className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <h2 className="text-xs text-slate-500 uppercase tracking-wider mb-4">
                Parse tree
              </h2>
              <ParseTree tree={result.tree} />
            </section>
          )}
        </div>
      )}
    </div>
  );
}
