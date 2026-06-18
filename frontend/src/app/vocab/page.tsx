"use client";

import { useEffect, useState, useMemo } from "react";
import WordCard, { type VocabEntry } from "@/components/WordCard";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const CATEGORY_ORDER = [
  "Verbs", "Nouns", "Adjectives",
  "Pronouns", "Possessives", "Determiners",
  "Prepositions", "Time Words", "Question Words",
  "Negation", "Causative", "Vocative",
];

export default function VocabPage() {
  const [data, setData]       = useState<Record<string, VocabEntry[]>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState("");
  const [active, setActive]   = useState("Verbs");
  const [query, setQuery]     = useState("");

  useEffect(() => {
    fetch(`${API}/vocab`)
      .then(r => r.json())
      .then(d => { setData(d.categories); setLoading(false); })
      .catch(() => { setError("Could not reach API — is the server running?"); setLoading(false); });
  }, []);

  const categories = useMemo(
    () => CATEGORY_ORDER.filter(c => data[c]?.length),
    [data],
  );

  const entries = useMemo(() => {
    const list = data[active] ?? [];
    if (!query.trim()) return list;
    const q = query.toLowerCase();
    return list.filter(
      e => e.sigan.includes(q) || e.english?.toLowerCase().includes(q),
    );
  }, [data, active, query]);

  return (
    <div className="mx-auto max-w-6xl px-6 py-8 flex gap-6 h-[calc(100vh-3.5rem)]">
      {/* Sidebar */}
      <aside className="w-44 shrink-0 flex flex-col gap-0.5 overflow-y-auto scrollbar-thin pt-1">
        {loading ? (
          <div className="text-slate-500 text-sm">Loading…</div>
        ) : (
          categories.map(cat => (
            <button
              key={cat}
              onClick={() => { setActive(cat); setQuery(""); }}
              className={`text-left px-3 py-1.5 rounded-md text-sm transition-colors ${
                active === cat
                  ? "bg-violet-500/15 text-violet-300 font-medium"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
              }`}
            >
              <span>{cat}</span>
              <span className="ml-1.5 text-xs text-slate-600">
                {data[cat]?.length}
              </span>
            </button>
          ))
        )}
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0">
        <div className="flex items-center gap-3 mb-5">
          <h1 className="text-lg font-semibold text-slate-100">{active}</h1>
          <span className="text-slate-500 text-sm">{entries.length} words</span>
          <div className="ml-auto">
            <input
              type="text"
              placeholder="Search…"
              value={query}
              onChange={e => setQuery(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-sm text-slate-200 placeholder-slate-600 outline-none focus:border-violet-500 transition-colors w-48"
            />
          </div>
        </div>

        {error && (
          <div className="text-red-400 text-sm bg-red-500/10 border border-red-500/20 rounded-lg p-4 mb-4">
            {error}
          </div>
        )}

        <div className="flex-1 overflow-y-auto scrollbar-thin space-y-1.5 pr-1">
          {entries.length === 0 && !loading && (
            <p className="text-slate-500 text-sm mt-4">No matches.</p>
          )}
          {entries.map(entry => (
            <WordCard key={entry.sigan} entry={entry} />
          ))}
        </div>
      </div>
    </div>
  );
}
