"""
Sigan CFG rules (all in Chomsky Normal Form).
Add new rules here; validator picks them up automatically.

Binary rules:  (LHS, B, C)   meaning LHS → B C
Unary rules:   (LHS, RHS)    meaning LHS → RHS  (nonterminal only)
"""

# ---------------------------------------------------------------------------
# Binary rules: A → B C
# ---------------------------------------------------------------------------

BINARY_RULES: list[tuple[str, str, str]] = [
    # Core sentence patterns
    ("S",         "NP",        "VP"),
    ("S",         "NP",        "VP_PP"),
    ("S",         "NP",        "VP_T"),
    ("S",         "NP",        "VP_PP_T"),
    # Intermediate VP combinations
    ("VP_PP",     "VP",        "PP"),
    ("VP_T",      "VP",        "T"),
    ("VP_PP_T",   "VP_PP",     "T"),
    # NP internal structure
    ("NP_A",      "Adj",       "N"),
    # Negation and causative building blocks
    ("NEG_V",     "Neg",       "V"),
    ("NP_V",      "NP",        "V"),
    ("CAUS_BODY", "CAUS_V",    "NP_V"),
    # Question building blocks
    ("VP_Q",      "V",         "QN"),
    # NP expansion
    ("NP",        "Det",       "N"),
    ("NP",        "Det",       "NP_A"),
    ("NP",        "PossN",     "N"),
    ("NP",        "PossN",     "NP_A"),
    # VP expansion
    ("VP",        "V",         "NP"),
    ("VP",        "NEG_V",     "NP"),
    ("VP",        "V",         "S"),       # complement clause: hope/believe/know + S
    ("VP",        "V",         "Adj"),     # predicate adjective: "I am well"
    ("VP_LOC",    "VP",        "Loc"),     # verb + locative: "go there"
    # PP
    ("PP",        "P",         "NP"),
    # Question sentences
    ("S_Q",       "QN",        "VP"),
    ("S_Q",       "NP",        "VP_Q"),
    # Causative sentence
    ("S_CAUS",    "NP",        "CAUS_BODY"),
    # Locative sentences
    ("S",         "NP",        "VP_LOC"),
]

# ---------------------------------------------------------------------------
# Unary rules: A → B  (both sides are nonterminals)
# ---------------------------------------------------------------------------

UNARY_RULES: list[tuple[str, str]] = [
    ("S",   "VP"),       # imperative
    ("S",   "S_Q"),
    ("S",   "S_CAUS"),
    ("S",   "VP_LOC"),   # imperative with locative: "go there!"
    ("S",   "Greet"),    # standalone greeting: "hello"
    ("NP",  "N"),
    ("NP",  "Pron"),
    ("NP",  "PropN"),    # proper noun as NP: "Sejuty"
    ("VP",  "V"),
    ("VP",  "NEG_V"),
]

# ---------------------------------------------------------------------------
# Tense / aspect suffix table
# Stripped longest-first from a verb token to recover the stem.
# Each entry: (suffix_without_dash, tense_label, aspect_label)
# ---------------------------------------------------------------------------

SUFFIX_TABLE: list[tuple[str, str, str]] = [
    ("ovrak",  "past",    "continuous"),
    ("ovdor",  "past",    "completed"),
    ("ovzun",  "past",    "habitual"),
    ("enrak",  "future",  "continuous"),
    ("endor",  "future",  "completed"),
    ("enzun",  "future",  "habitual"),
    ("ov",     "past",    "simple"),
    ("en",     "future",  "simple"),
    ("rak",    "present", "continuous"),
    ("dor",    "present", "completed"),
    ("zun",    "present", "habitual"),
]
