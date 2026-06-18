"use client";

import { useState } from "react";

type Conjugation = {
  tense: string;
  aspect: string;
  form: string;
};

export type VocabEntry = {
  sigan: string;
  pos: string;
  english: string | null;
  conjugations?: Conjugation[];
};

const TENSE_ORDER = ["past", "present", "future"] as const;
const ASPECT_ORDER = ["simple", "continuous", "completed", "habitual"] as const;
const ASPECT_LABEL: Record<string, string> = {
  simple:     "Simple",
  continuous: "Continuous",
  completed:  "Completed",
  habitual:   "Habitual",
};

const POS_BADGE: Record<string, string> = {
  V:      "bg-violet-500/15 text-violet-300",
  N:      "bg-sky-500/15    text-sky-300",
  Adj:    "bg-amber-500/15  text-amber-300",
  Pron:   "bg-teal-500/15   text-teal-300",
  PossN:  "bg-teal-500/15   text-teal-200",
  Det:    "bg-slate-700     text-slate-300",
  P:      "bg-orange-500/15 text-orange-300",
  T:      "bg-cyan-500/15   text-cyan-300",
  QN:     "bg-pink-500/15   text-pink-300",
  Neg:    "bg-red-500/15    text-red-300",
  CAUS_V: "bg-fuchsia-500/15 text-fuchsia-300",
  VOC:    "bg-slate-700     text-slate-300",
};

function ConjugationGrid({ conjugations }: { conjugations: Conjugation[] }) {
  const byKey: Record<string, string> = {};
  for (const c of conjugations) {
    byKey[`${c.tense}_${c.aspect}`] = c.form;
  }

  return (
    <div className="mt-4">
      <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Conjugations</p>
      <div className="overflow-x-auto">
        <table className="w-full text-xs border-collapse">
          <thead>
            <tr>
              <th className="text-left pb-1.5 text-slate-500 font-normal w-28" />
              {TENSE_ORDER.map(t => (
                <th key={t} className="pb-1.5 text-slate-400 font-semibold text-center capitalize">
                  {t}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {ASPECT_ORDER.map(aspect => (
              <tr key={aspect}>
                <td className="py-1.5 pr-3 text-slate-500">{ASPECT_LABEL[aspect]}</td>
                {TENSE_ORDER.map(tense => (
                  <td key={tense} className="py-1.5 text-center">
                    <span className="sigan text-violet-300 text-xs">
                      {byKey[`${tense}_${aspect}`] ?? "—"}
                    </span>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default function WordCard({ entry }: { entry: VocabEntry }) {
  const [open, setOpen] = useState(false);
  const badge = POS_BADGE[entry.pos] ?? "bg-slate-700 text-slate-300";

  return (
    <div
      className={`rounded-lg border transition-colors cursor-pointer select-none ${
        open
          ? "border-slate-700 bg-slate-900"
          : "border-slate-800 bg-slate-900/50 hover:border-slate-700 hover:bg-slate-900"
      }`}
      onClick={() => setOpen(o => !o)}
    >
      <div className="flex items-center gap-3 px-4 py-3">
        <span className="sigan text-slate-100 font-medium text-sm min-w-[8rem]">
          {entry.sigan}
        </span>
        <span className="text-slate-400 text-sm flex-1 truncate">
          {entry.english ?? "—"}
        </span>
        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${badge}`}>
          {entry.pos}
        </span>
        <span className="text-slate-600 text-xs ml-1">{open ? "▲" : "▼"}</span>
      </div>

      {open && (
        <div
          className="px-4 pb-4 border-t border-slate-800"
          onClick={e => e.stopPropagation()}
        >
          {entry.conjugations ? (
            <ConjugationGrid conjugations={entry.conjugations} />
          ) : (
            <div className="mt-3">
              <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">Details</p>
              <div className="flex gap-6 text-sm">
                <div>
                  <span className="text-slate-500 text-xs">Sigan </span>
                  <span className="sigan text-violet-300">{entry.sigan}</span>
                </div>
                {entry.english && (
                  <div>
                    <span className="text-slate-500 text-xs">English </span>
                    <span className="text-slate-200">{entry.english}</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
