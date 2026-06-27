"use client";

import { useState } from "react";
import Link from "next/link";
import ParseTree, { type TreeNode } from "@/components/ParseTree";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Example = { sigan: string; english: string; group: string };

const EXAMPLES: Example[] = [
  // ── Index 0 — shown by default ──────────────────────────────────────────
  { sigan: "elva velor sova",            english: "I see you",             group: "Everyday"  },

  // ── Greetings ─────────────────────────────────────────────────────────
  { sigan: "laevel",                     english: "Hello",                 group: "Greetings" },
  { sigan: "sorvael",                    english: "Goodbye",               group: "Greetings" },
  { sigan: "alvael aevil sova",          english: "How are you?",          group: "Greetings" },
  { sigan: "elva aevil saeril",          english: "I am well",             group: "Greetings" },

  // ── Identity ──────────────────────────────────────────────────────────
  { sigan: "elva aevil Sejuty",          english: "I am Sejuty",           group: "Identity"  },

  // ── Commands ──────────────────────────────────────────────────────────
  { sigan: "silvonor",                   english: "Silence!",              group: "Commands"  },

  // ── Motion ────────────────────────────────────────────────────────────
  { sigan: "elva lorel ulra",            english: "I go there",            group: "Motion"    },
  { sigan: "elva lorel ilra",            english: "I go here",             group: "Motion"    },
  { sigan: "sova talovel ulra",          english: "You run there",         group: "Motion"    },
  { sigan: "elvan aeravel ilra",         english: "We return here",        group: "Motion"    },

  // ── Everyday ──────────────────────────────────────────────────────────
  { sigan: "elva elavar sova",           english: "I love you",            group: "Everyday"  },
  { sigan: "elva nael thaevel",          english: "I do not speak",        group: "Everyday"  },
  { sigan: "elva savorel al savori",     english: "I eat the food",        group: "Everyday"  },
  { sigan: "thira mirel al mirae",       english: "He walks the path",     group: "Everyday"  },
  { sigan: "elva selavor al savori",     english: "I want the food",       group: "Everyday"  },
  { sigan: "elva thaevel al voriva",     english: "I speak the word",      group: "Everyday"  },
  { sigan: "elva lireval al voriva",     english: "I read the word",       group: "Everyday"  },
  { sigan: "elvan alivor sovan",         english: "We help you",           group: "Everyday"  },
  { sigan: "elva aethivar al valori",    english: "I think the truth",     group: "Everyday"  },

  // ── Emotion ───────────────────────────────────────────────────────────
  { sigan: "thira drelovar al narovi",   english: "He fears the enemy",    group: "Emotion"   },
  { sigan: "elva elavar al alorivi",     english: "I love life",           group: "Emotion"   },
  { sigan: "elva sorviran al morive",    english: "I mourn the dead",      group: "Emotion"   },

  // ── Questions ─────────────────────────────────────────────────────────
  { sigan: "sivael velor sova",          english: "Who sees you?",         group: "Questions" },
  { sigan: "sivael lireval al voriva",   english: "Who reads the word?",   group: "Questions" },
  { sigan: "sivael alivor sovan",        english: "Who helps you?",        group: "Questions" },
];

// Hardcoded default — shows instantly without needing the API running
const DEFAULT_IDX = 0; // "elva velor sova"
const DEFAULT_TREE: TreeNode = {
  symbol: "S",
  children: [
    {
      symbol: "NP",
      children: [
        { symbol: "Pron", token: "elva", tense: null, aspect: null, children: [] },
      ],
    },
    {
      symbol: "VP",
      children: [
        { symbol: "V", token: "velor", tense: "present", aspect: "simple", children: [] },
        {
          symbol: "NP",
          children: [
            { symbol: "Pron", token: "sova", tense: null, aspect: null, children: [] },
          ],
        },
      ],
    },
  ],
};

const SUFFIXES = [
  { pattern: "bare present",      suffix: "—",      example: "velor"      },
  { pattern: "is/am/are + -ing",  suffix: "-rak",   example: "velorrak"   },
  { pattern: "has/have + -ed",    suffix: "-dor",   example: "velordor"   },
  { pattern: "past (saw / went)", suffix: "-ov",    example: "velorov"    },
  { pattern: "was/were + -ing",   suffix: "-ovrak", example: "velorovrak" },
  { pattern: "will + verb",       suffix: "-en",    example: "veloren"    },
  { pattern: "will be + -ing",    suffix: "-enrak", example: "velorenrak" },
];

const PRONOUNS = [
  { sigan: "elva",   en: "I / me"        },
  { sigan: "sova",   en: "you (sg)"      },
  { sigan: "thira",  en: "he / she / it" },
  { sigan: "elvan",  en: "we / us"       },
  { sigan: "sovan",  en: "you (pl)"      },
  { sigan: "thiran", en: "they / them"   },
];

const GROUP_COLORS: Record<string, string> = {
  Greetings: "text-sky-400",
  Identity:  "text-violet-400",
  Commands:  "text-red-400",
  Motion:    "text-emerald-400",
  Everyday:  "text-slate-400",
  Emotion:   "text-rose-400",
  Questions: "text-pink-400",
};

const GROUPS = Array.from(new Set(EXAMPLES.map(e => e.group)));

export default function HomePage() {
  const [selected, setSelected]       = useState(DEFAULT_IDX);
  const [tree, setTree]               = useState<TreeNode | null>(DEFAULT_TREE);
  const [translation, setTranslation] = useState(EXAMPLES[DEFAULT_IDX].english);
  const [loading, setLoading]         = useState(false);
  const [apiDown, setApiDown]         = useState(false);
  const [groupFilter, setGroupFilter] = useState<string | null>(null);

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

  const handleGroupFilter = (group: string | null) => {
    setGroupFilter(group);
    if (group && EXAMPLES[selected].group !== group) {
      const firstIdx = EXAMPLES.findIndex(e => e.group === group);
      if (firstIdx !== -1) {
        setSelected(firstIdx);
        setTree(null);
        setTranslation(EXAMPLES[firstIdx].english);
      }
    }
  };

  const visibleExamples = groupFilter
    ? EXAMPLES.map((e, i) => ({ ...e, i })).filter(e => e.group === groupFilter)
    : EXAMPLES.map((e, i) => ({ ...e, i }));

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
        <div className="flex flex-col gap-3">
          <h2 className="text-xs uppercase tracking-widest text-slate-500">
            Example Phrases — click to see the parse tree
          </h2>
          {/* Group filter pills */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => handleGroupFilter(null)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                !groupFilter
                  ? "bg-violet-500/20 text-violet-300"
                  : "bg-slate-800 text-slate-400 hover:text-slate-200"
              }`}
            >
              All
            </button>
            {GROUPS.map(group => (
              <button
                key={group}
                onClick={() => handleGroupFilter(groupFilter === group ? null : group)}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                  groupFilter === group
                    ? "bg-violet-500/20 text-violet-300"
                    : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                <span className={GROUP_COLORS[group] ?? "text-slate-400"}>●</span>
                {group}
              </button>
            ))}
          </div>
        </div>

        {/* Cards grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
          {visibleExamples.map(({ i, ...e }) => {
            const active = selected === i;
            const dot = GROUP_COLORS[e.group] ?? "text-slate-400";
            return (
              <button
                key={i}
                onClick={() => pickExample(i)}
                className={`text-left p-3 rounded-xl border transition-all ${
                  active
                    ? "bg-amber-500/15 border-amber-500/50"
                    : "bg-slate-900 border-slate-800 hover:border-slate-600"
                }`}
              >
                <div className={`sigan text-sm font-medium truncate ${active ? "text-amber-200" : "text-slate-200"}`}>
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
            <span className="sigan text-amber-300">{ex.sigan}</span>
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
                    ["nael?",        "bg-red-500/10     text-red-300     border-red-500/20"    ],
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
                <span className="sigan text-slate-500">nael</span> immediately before the verb negates it.
              </p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}
