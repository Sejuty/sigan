export type Example = { sigan: string; english: string; group: string };

export const EXAMPLES: Example[] = [
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
  { sigan: "silvonor",                   english: "Silence",              group: "Commands"  },

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
