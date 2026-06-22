"use client";

import { useState } from "react";
import Link from "next/link";
import ParseTree, { type TreeNode } from "@/components/ParseTree";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Example = { sigan: string; english: string; group: string };

const EXAMPLES: Example[] = [
  { sigan: "gretu",                  english: "Hello",              group: "Greetings" },
  { sigan: "valedu",                 english: "Goodbye",            group: "Greetings" },
  { sigan: "kovazh izak yu",         english: "How are you?",       group: "Greetings" },
  { sigan: "ayu izak welath",        english: "I am well",          group: "Greetings" },
  { sigan: "ayu izak Sejuty",        english: "I am Sejuty",        group: "Identity"  },
  { sigan: "silend",                 english: "Silence!",           group: "Commands"  },
  { sigan: "ayu govan theva",        english: "I go there",         group: "Motion"    },
  { sigan: "ayu govan heva",         english: "I go here",          group: "Motion"    },
  { sigan: "ayu sigan yu",           english: "I see you",          group: "Everyday"  },
  { sigan: "ayu lovak yu",           english: "I love you",         group: "Everyday"  },
  { sigan: "ayu noth spekor",        english: "I do not speak",     group: "Everyday"  },
  { sigan: "ayu etak fudo",          english: "I eat food",         group: "Everyday"  },
  { sigan: "hiru walkag gar rotha",  english: "He walks the path",  group: "Everyday"  },
  { sigan: "huzh sigan yu",          english: "Who sees you?",      group: "Questions" },
  { sigan: "ayu wantak fudo",        english: "I want food",        group: "Everyday"  },
  { sigan: "ayu spekor worda",       english: "I speak word",       group: "Everyday"  },
];

// Hardcoded default — shows instantly without needing the API running
const DEFAULT_IDX = 6; // "ayu govan theva"
const DEFAULT_TREE: TreeNode = {
  symbol: "S",
  children: [
    {
      symbol: "NP",
      children: [
        { symbol: "Pron", token: "ayu", tense: null, aspect: null, children: [] },
      ],
    },
    {
      symbol: "VP_LOC",
      children: [
        {
          symbol: "VP",
          children: [
            { symbol: "V", token: "govan", tense: "present", aspect: "simple", children: [] },
          ],
        },
        { symbol: "Loc", token: "theva", tense: null, aspect: null, children: [] },
      ],
    },
  ],
};

const SUFFIXES = [
  { pattern: "bare present",      suffix: "—",      example: "sigan"      },
  { pattern: "is/am/are + -ing",  suffix: "-rak",   example: "siganrak"   },
  { pattern: "has/have + -ed",    suffix: "-dor",   example: "sigandor"   },
  { pattern: "past (saw / went)", suffix: "-ov",    example: "siganov"    },
  { pattern: "was/were + -ing",   suffix: "-ovrak", example: "siganovrak" },
  { pattern: "will + verb",       suffix: "-en",    example: "siganen"    },
  { pattern: "will be + -ing",    suffix: "-enrak", example: "siganenrak" },
];

const PRONOUNS = [
  { sigan: "ayu",   en: "I / me"      },
  { sigan: "yu",    en: "you (sg)"    },
  { sigan: "hiru",  en: "he / she / it" },
  { sigan: "ayun",  en: "we / us"     },
  { sigan: "yun",   en: "you (pl)"   },
  { sigan: "hirun", en: "they / them" },
];

const GROUP_COLORS: Record<string, string> = {
  Greetings: "text-sky-400",
  Identity:  "text-violet-400",
  Commands:  "text-red-400",
  Motion:    "text-emerald-400",
  Everyday:  "text-slate-400",
  Questions: "text-pink-400",
};

export default function HomePage() {
  const [selected, setSelected]       = useState(DEFAULT_IDX);
  const [tree, setTree]               = useState<TreeNode | null>(DEFAULT_TREE);
  const [translation, setTranslation] = useState(EXAMPLES[DEFAULT_IDX].english);
  const [loading, setLoading]         = useState(false);
  const [apiDown, setApiDown]         = useState(false);

  const pickExample = async (idx: number) => {
    setSelected(idx);
    setLoading(true);
    setTree(null);
    setApiDown(false);
    const ex = EXAMPLES[idx];
    try {
      const [valRes, transRes] = await Promise.all([
        fetch(`${API}/validate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ sentence: ex.sigan }),
        }),
        fetch(`${API}/translate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: ex.sigan, direction: "to_english" }),
        }),
      ]);
      const valData   = await valRes.json();
      const transData = await transRes.json();
      if (valData.valid && valData.tree) setTree(valData.tree);
      setTranslation(transData.success ? transData.result : ex.english);
    } catch {
      setApiDown(true);
      setTranslation(ex.english);
    } finally {
      setLoading(false);
    }
  };

  const ex = EXAMPLES[selected];

  return (
    <div className="mx-auto max-w-5xl px-6 py-16 flex flex-col gap-20">

      {/* ── Hero ── */}
      <section className="flex flex-col items-center text-center gap-6">
        <div className="flex items-center gap-3">
          <span className="sigan text-violet-400 text-5xl leading-none">◈</span>
          <h1 className="text-5xl font-bold tracking-widest text-slate-100">SIGAN</h1>
        </div>
        <p className="text-slate-400 text-lg max-w-lg leading-relaxed">
          A constructed language with strict SVO word order, suffix-based tense
          morphology, and a deterministic CKY chart parser.
        </p>
        <div className="flex flex-wrap justify-center gap-3 mt-1">
          <Link
            href="/translate"
            className="px-6 py-2.5 bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium rounded-lg transition-colors"
          >
            Translate
          </Link>
          <Link
            href="/validate"
            className="px-6 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium rounded-lg transition-colors"
          >
            Validate
          </Link>
          <Link
            href="/vocab"
            className="px-6 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium rounded-lg transition-colors"
          >
            Vocab
          </Link>
        </div>
      </section>

      {/* ── Example sentences + live parse tree ── */}
      <section className="flex flex-col gap-6">
        <h2 className="text-xs uppercase tracking-widest text-slate-500">
          Everyday Phrases — click to see the parse tree
        </h2>

        {/* Cards grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
          {EXAMPLES.map((e, i) => {
            const active = selected === i;
            const dot = GROUP_COLORS[e.group] ?? "text-slate-400";
            return (
              <button
                key={i}
                onClick={() => pickExample(i)}
                className={`text-left p-3 rounded-xl border transition-all ${
                  active
                    ? "bg-violet-500/10 border-violet-500/40"
                    : "bg-slate-900 border-slate-800 hover:border-slate-600"
                }`}
              >
                <div className={`sigan text-sm font-medium truncate ${active ? "text-violet-300" : "text-slate-200"}`}>
                  {e.sigan}
                </div>
                <div className="flex items-center gap-1.5 mt-0.5">
                  <span className={`text-[10px] ${dot}`}>●</span>
                  <span className="text-xs text-slate-500 truncate">{e.english}</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Parse tree panel */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
          {/* Header */}
          <div className="flex items-center gap-3 px-5 py-4 border-b border-slate-800">
            <span className="sigan text-violet-300">{ex.sigan}</span>
            <span className="text-slate-700">→</span>
            <span className="text-slate-300 text-sm">{translation}</span>
            <span className={`ml-auto text-xs uppercase tracking-wider ${GROUP_COLORS[ex.group] ?? "text-slate-500"}`}>
              {ex.group}
            </span>
          </div>

          {/* Tree body */}
          <div className="px-5 py-5 min-h-[8rem]">
            {loading ? (
              <div className="text-slate-600 text-sm animate-pulse">Parsing…</div>
            ) : apiDown ? (
              <div className="text-slate-600 text-sm">
                API unreachable — start the backend to see live parse trees.
              </div>
            ) : tree ? (
              <ParseTree tree={tree} />
            ) : (
              <div className="text-slate-600 text-sm">No parse tree available.</div>
            )}
          </div>
        </div>
      </section>

      {/* ── Grammar quick reference ── */}
      <section className="flex flex-col gap-6">
        <h2 className="text-xs uppercase tracking-widest text-slate-500">Grammar at a Glance</h2>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Tense suffixes */}
          <div className="flex flex-col gap-3">
            <h3 className="text-xs text-slate-600 uppercase tracking-wider">Tense suffixes</h3>
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-500 text-xs">
                    <th className="text-left px-4 py-2.5 font-normal">English pattern</th>
                    <th className="text-left px-4 py-2.5 font-normal">Suffix</th>
                    <th className="text-left px-4 py-2.5 font-normal">Form</th>
                  </tr>
                </thead>
                <tbody>
                  {SUFFIXES.map((row, i) => (
                    <tr key={i} className="border-t border-slate-800/50">
                      <td className="px-4 py-2 text-slate-400">{row.pattern}</td>
                      <td className="px-4 py-2 sigan text-violet-300">{row.suffix}</td>
                      <td className="px-4 py-2 sigan text-slate-300">{row.example}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Pronouns + word order */}
          <div className="flex flex-col gap-3">
            <h3 className="text-xs text-slate-600 uppercase tracking-wider">Pronouns</h3>
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-500 text-xs">
                    <th className="text-left px-4 py-2.5 font-normal">Sigan</th>
                    <th className="text-left px-4 py-2.5 font-normal">English</th>
                  </tr>
                </thead>
                <tbody>
                  {PRONOUNS.map((row, i) => (
                    <tr key={i} className="border-t border-slate-800/50">
                      <td className="px-4 py-2 sigan text-violet-300">{row.sigan}</td>
                      <td className="px-4 py-2 text-slate-400">{row.en}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Word order pill */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 flex flex-col gap-2">
              <span className="text-xs text-slate-600 uppercase tracking-wider">Word order</span>
              <div className="flex items-center gap-1.5 flex-wrap">
                {(
                  [
                    ["Subject",      "bg-sky-500/10     text-sky-300     border-sky-500/20"    ],
                    ["noth?",        "bg-red-500/10     text-red-300     border-red-500/20"    ],
                    ["Verb",         "bg-emerald-500/10 text-emerald-300 border-emerald-500/20"],
                    ["Object",       "bg-sky-500/10     text-sky-300     border-sky-500/20"    ],
                    ["Prep phrase",  "bg-orange-500/10  text-orange-300  border-orange-500/20" ],
                    ["Time",         "bg-slate-500/10   text-slate-400   border-slate-500/20"  ],
                  ] as [string, string][]
                ).map(([label, cls]) => (
                  <span
                    key={label}
                    className={`sigan text-xs px-2.5 py-1 rounded-md border ${cls}`}
                  >
                    {label}
                  </span>
                ))}
              </div>
              <p className="text-xs text-slate-600 mt-1">
                <span className="sigan text-slate-500">noth</span> immediately before the verb negates it.
              </p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}
