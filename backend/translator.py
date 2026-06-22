"""
Sigan ↔ English bidirectional translator.
Usage:
  python translator.py --to-english "ayu siganovrak gar truku"
  python translator.py --to-sigan   "I was seeing the tree"
"""

import sys
from typing import Optional

from validator import validate, ParseNode, TokenInfo
from lexicon import (
    LEXICON, VERB_STEMS,
    VERB_EN, PAST_SIMPLE, PAST_PARTICIPLE,
    NOUN_EN, PRON_EN, PRON_OBJ_EN, POSS_EN, DET_EN, ADJ_EN, PREP_EN, TIME_EN, QN_EN,
    LOC_EN, GREET_EN,
)

# ---------------------------------------------------------------------------
# Tense / aspect → English verb phrase
# ---------------------------------------------------------------------------

_TENSE_ASPECT_EN: dict[tuple[str, str], tuple[str, bool]] = {
    ("present", "simple"):      ("",             False),
    ("present", "continuous"):  ("is",           True),
    ("present", "completed"):   ("has",          False),
    ("present", "habitual"):    ("usually",      False),
    ("past",    "simple"):      ("",             False),
    ("past",    "continuous"):  ("was",          True),
    ("past",    "completed"):   ("had",          False),
    ("past",    "habitual"):    ("used to",      False),
    ("future",  "simple"):      ("will",         False),
    ("future",  "continuous"):  ("will be",      True),
    ("future",  "completed"):   ("will have",    False),
    ("future",  "habitual"):    ("will usually", False),
}


def verb_to_english(stem: str, tense: str, aspect: str) -> str:
    """Convert a Sigan verb stem + tense/aspect to an English verb phrase."""
    base, ing = VERB_EN.get(stem, (stem, stem + "ing"))
    aux, use_ing = _TENSE_ASPECT_EN.get((tense, aspect), ("", False))

    if use_ing:
        v_form = ing
    elif tense == "past" and aspect == "simple":
        v_form = PAST_SIMPLE.get(base, base + "ed")
    elif aspect == "completed":
        v_form = PAST_PARTICIPLE.get(base, base + "ed")
    else:
        v_form = base

    return f"{aux} {v_form}".strip()


# ---------------------------------------------------------------------------
# English → Sigan suffix table
# ---------------------------------------------------------------------------

_SIGAN_SUFFIX: dict[tuple[str, str], str] = {
    ("present", "simple"):     "",
    ("present", "continuous"): "rak",
    ("present", "completed"):  "dor",
    ("present", "habitual"):   "zun",
    ("past",    "simple"):     "ov",
    ("past",    "continuous"): "ovrak",
    ("past",    "completed"):  "ovdor",
    ("past",    "habitual"):   "ovzun",
    ("future",  "simple"):     "en",
    ("future",  "continuous"): "enrak",
    ("future",  "completed"):  "endor",
    ("future",  "habitual"):   "enzun",
}

# ---------------------------------------------------------------------------
# English → Sigan reverse lookup (built from lexicon tables)
# ---------------------------------------------------------------------------

# Non-verb words: English → (Sigan, POS)
_EN_TO_SIGAN: dict[str, tuple[str, str]] = {}
# Verb words only: English base/ing → Sigan stem (kept separate to avoid noun/verb collision)
_EN_VERB_STEM_MAP: dict[str, str] = {}


def _build_reverse_lookup() -> None:
    for sig, pos in LEXICON.items():
        if pos == "N":
            en = NOUN_EN.get(sig)
            if en:
                _EN_TO_SIGAN[en] = (sig, "N")
        elif pos == "Pron":
            en = PRON_EN.get(sig)
            if en:
                _EN_TO_SIGAN[en.lower()] = (sig, "Pron")
        elif pos == "Det":
            en = DET_EN.get(sig)
            if en:
                _EN_TO_SIGAN[en] = (sig, "Det")
        elif pos == "Adj":
            en = ADJ_EN.get(sig)
            if en:
                _EN_TO_SIGAN[en] = (sig, "Adj")
        elif pos == "P":
            en = PREP_EN.get(sig)
            if en:
                _EN_TO_SIGAN[en] = (sig, "P")
        elif pos == "T":
            en = TIME_EN.get(sig)
            if en:
                _EN_TO_SIGAN[en] = (sig, "T")
        elif pos == "QN":
            en = QN_EN.get(sig)
            if en:
                _EN_TO_SIGAN[en] = (sig, "QN")

    # Explicit pronoun overrides — singular "you" wins over plural
    _EN_TO_SIGAN.update({
        "he":   ("hiru",  "Pron"), "she":  ("hiru",  "Pron"), "it":   ("hiru",  "Pron"),
        "they": ("hirun", "Pron"),
        "you":  ("yu",    "Pron"),
        "me":   ("ayu",   "Pron"), "us":   ("ayun",  "Pron"),
        "him":  ("hiru",  "Pron"), "her":  ("hiru",  "Pron"), "them": ("hirun", "Pron"),
    })

    # Verbs go into their own separate map
    for stem, (base, ing) in VERB_EN.items():
        _EN_VERB_STEM_MAP[base] = stem
        _EN_VERB_STEM_MAP[ing]  = stem


_build_reverse_lookup()

_EN_PAST_TO_BASE:     dict[str, str] = {past: base for base, past in PAST_SIMPLE.items()}
_EN_PAST_PART_TO_BASE: dict[str, str] = {pp:   base for base, pp   in PAST_PARTICIPLE.items()}

_EN_TENSE_MAP: list[tuple[str, str, str]] = [
    ("will be",      "future",  "continuous"),
    ("will have",    "future",  "completed"),
    ("will usually", "future",  "habitual"),
    ("will",         "future",  "simple"),
    ("was",          "past",    "continuous"),
    ("were",         "past",    "continuous"),
    ("had",          "past",    "completed"),
    ("used to",      "past",    "habitual"),
    ("is",           "present", "continuous"),
    ("am",           "present", "continuous"),
    ("are",          "present", "continuous"),
    ("has",          "present", "completed"),
    ("have",         "present", "completed"),
    ("usually",      "present", "habitual"),
    ("did",          "past",    "simple"),
]

# ---------------------------------------------------------------------------
# Sigan → English: recursive parse-tree walker
# ---------------------------------------------------------------------------


def _translate_node(node: ParseNode, role: str = "subject") -> str:
    sym = node.symbol

    if node.is_leaf():
        tok = node.token
        surf = tok.surface
        if sym == "V":      return verb_to_english(tok.stem, tok.tense, tok.aspect)
        if sym == "N":      return NOUN_EN.get(surf, surf)
        if sym == "Pron":   return (PRON_OBJ_EN if role == "object" else PRON_EN).get(surf, surf)
        if sym == "Det":    return DET_EN.get(surf, surf)
        if sym == "Adj":    return ADJ_EN.get(surf, surf)
        if sym == "PossN":  return POSS_EN.get(surf, surf)
        if sym == "P":      return PREP_EN.get(surf, surf)
        if sym == "T":      return TIME_EN.get(surf, surf)
        if sym == "QN":     return QN_EN.get(surf, surf)
        if sym == "Loc":    return LOC_EN.get(surf, surf)
        if sym == "Greet":  return GREET_EN.get(surf, surf)
        if sym == "PropN":  return surf   # preserve original capitalisation
        if sym == "Neg":    return "not"
        if sym == "CAUS_V": return "cause"
        return surf

    L, R = node.left, node.right

    if sym == "NP":
        if R is None:
            return _translate_node(L, role=role)
        return f"{_translate_node(L)} {_translate_node(R, role=role)}"

    if sym == "NP_A":
        return f"{_translate_node(L)} {_translate_node(R)}"

    if sym == "VP":
        if R is None:
            return _translate_node(L)
        if R.symbol == "S":
            # complement clause: V S → "hope that <S>" (apply agreement inside clause)
            inner = _fix_agreement(_translate_node(R))
            return f"{_translate_node(L)} that {inner}"
        return f"{_translate_node(L)} {_translate_node(R, role='object')}"

    if sym == "NEG_V":
        return f"do not {_translate_node(R)}"

    if sym == "PP":
        return f"{_translate_node(L)} {_translate_node(R, role='object')}"

    if sym in ("VP_PP", "VP_T", "VP_PP_T", "VP_Q", "VP_LOC"):
        return f"{_translate_node(L)} {_translate_node(R)}"

    if sym == "S":
        if R is None:
            return _translate_node(L)
        return f"{_translate_node(L, role='subject')} {_translate_node(R)}"

    if sym == "S_Q":
        if L.symbol == "QN":
            qn_surf = L.token.surface if L.is_leaf() else ""
            qn_text = _translate_node(L)
            # Subject-position QNs ("who"/"what") act as the grammatical subject;
            # adverbial QNs ("how"/"where"/"when") need the VP's NP for agreement.
            if qn_surf in ("huzh", "wazh"):
                return f"{qn_text} {_translate_node(R)}?"
            # Adverbial QN: derive agreement from NP inside VP (treat as logical subject)
            vp_node = R
            if (vp_node.symbol == "VP" and not vp_node.is_leaf()
                    and vp_node.right is not None):
                v_text  = _translate_node(vp_node.left)
                np_text = _translate_node(vp_node.right, role="subject")
                agreed  = _fix_agreement(f"{np_text} {v_text}").split()
                agreed_v = agreed[1] if len(agreed) > 1 else v_text
                return f"{qn_text} {agreed_v} {np_text}?"
            return f"{qn_text} {_translate_node(R)}?"
        return f"{_translate_node(L, role='subject')} {_translate_node(R)}?"

    if sym == "S_CAUS":
        return f"{_translate_node(L, role='subject')} {_translate_node(R)}"

    if sym == "CAUS_BODY":
        return f"{_translate_node(L)} {_translate_node(R)}"

    if sym == "NP_V":
        return f"{_translate_node(L, role='object')} to {_translate_node(R)}"

    parts = [_translate_node(c) for c in (L, R) if c]
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Subject-verb agreement post-processing
# ---------------------------------------------------------------------------

_PLURAL_SUBJECTS = {"we", "they", "you"}
_THIRD_SINGULAR  = {"he", "she", "it", "who", "what"}   # question subjects also take 3ps
_AUX_WORDS       = {
    "is", "are", "was", "were", "has", "have", "had",
    "will", "do", "does", "did", "be", "been", "being",
    "used", "usually", "can", "could", "would", "should",
    "may", "might", "shall", "must", "not",
}
# Past/participle forms that must not get a 3ps -s added
_KNOWN_PAST_FORMS: frozenset = frozenset(PAST_SIMPLE.values()) | frozenset(PAST_PARTICIPLE.values())


def _add_3ps(verb: str) -> str:
    """Return the 3rd-person singular present form of a bare English verb."""
    if verb == "be":
        return "is"
    if verb.endswith(("o", "s", "x", "z")) or verb.endswith("ch") or verb.endswith("sh"):
        return verb + "es"
    if verb.endswith("y") and len(verb) > 1 and verb[-2] not in "aeiou":
        return verb[:-1] + "ies"
    return verb + "s"


def _fix_agreement(text: str) -> str:
    """Patch subject-verb agreement: plurality, I/am, 3rd-singular -s."""
    words = text.split()
    if len(words) < 2:
        return text
    subj = words[0].lower()

    if subj in _PLURAL_SUBJECTS:
        fixes = {"was": "were", "is": "are", "has": "have", "be": "are"}
        if words[1] in fixes:
            words[1] = fixes[words[1]]

    elif subj == "i":
        fixes_i = {"is": "am", "has": "have", "be": "am"}
        if words[1] in fixes_i:
            words[1] = fixes_i[words[1]]

    elif subj in _THIRD_SINGULAR:
        if words[1] == "do":
            # NEG_V: "do not V" → "does not V"
            words[1] = "does"
        elif words[1] == "be":
            # copula bare form — 3rd singular → "is"
            words[1] = "is"
        elif words[1] == "usually" and len(words) > 2 and words[2] not in _AUX_WORDS and words[2] not in _KNOWN_PAST_FORMS:
            # habitual: "He usually see" → "He usually sees"
            words[2] = _add_3ps(words[2])
        elif words[1] not in _AUX_WORDS and words[1].isalpha() and words[1] not in _KNOWN_PAST_FORMS:
            # bare present simple only — guard past forms ("loved" must not become "loveds")
            words[1] = _add_3ps(words[1])

    return " ".join(words)


def sigan_to_english(sentence: str) -> dict:
    result = validate(sentence)
    if not result["valid"]:
        return {"success": False, "english": "", "error": result["errors"]}
    english = _translate_node(result["parse_tree"])
    english = english[0].upper() + english[1:] if english else english
    english = _fix_agreement(english)
    return {"success": True, "english": english, "error": []}


# ---------------------------------------------------------------------------
# English → Sigan: heuristic mapper
# ---------------------------------------------------------------------------


def _en_to_stem(word: str) -> Optional[str]:
    """Return the Sigan verb stem for an English word form, or None."""
    w = word.lower()
    if w in _EN_VERB_STEM_MAP:
        return _EN_VERB_STEM_MAP[w]
    base = _EN_PAST_TO_BASE.get(w) or _EN_PAST_PART_TO_BASE.get(w)
    if base and base in _EN_VERB_STEM_MAP:
        return _EN_VERB_STEM_MAP[base]
    # 3rd-person singular -s/-es
    if w.endswith("es") and len(w) > 3 and w[:-2] in _EN_VERB_STEM_MAP:
        return _EN_VERB_STEM_MAP[w[:-2]]
    if w.endswith("s") and len(w) > 2 and w[:-1] in _EN_VERB_STEM_MAP:
        return _EN_VERB_STEM_MAP[w[:-1]]
    return None


def _words_to_sigan_np(words: list[str]) -> str:
    parts = []
    for w in words:
        sig, _ = _EN_TO_SIGAN.get(w.lower(), (None, None))
        if not sig:
            sig = _EN_VERB_STEM_MAP.get(w.lower())
        parts.append(sig if sig else w)
    return " ".join(parts)


def _parse_english(words: list[str]) -> dict:
    result = {
        "subject": None, "verb_stem": None,
        "tense": "present", "aspect": "simple",
        "negated": False, "object_words": [], "time_word": None,
        "complement": None, "error": None,
    }
    i, n = 0, len(words)

    if n == 0:
        result["error"] = "Empty sentence"
        return result

    # Subject
    subj_parts: list[str] = []
    while i < n:
        w = words[i].lower()
        if w in ("i", "we", "you", "he", "she", "it", "they"):
            subj_parts.append(w); i += 1; break
        if w in ("the", "a", "an", "some"):
            subj_parts.append(w); i += 1
        elif w not in ("was", "were", "is", "am", "are", "has", "have",
                       "had", "will", "did", "do", "does", "usually",
                       "not", "never") and _en_to_stem(w) is None:
            subj_parts.append(w); i += 1; break
        else:
            break
    result["subject"] = " ".join(subj_parts) or None

    # Auxiliaries
    aux_words = ("was", "were", "is", "am", "are", "has", "have",
                 "had", "will", "be", "used", "to", "usually", "did", "do", "does")
    auxes: list[str] = []
    while i < n and words[i].lower() in aux_words:
        auxes.append(words[i].lower()); i += 1

    # Negation
    if i < n and words[i].lower() in ("not", "never", "n't"):
        result["negated"] = True; i += 1

    # Tense/aspect from aux phrase
    aux_str = " ".join(auxes)
    for phrase, tense, aspect in _EN_TENSE_MAP:
        if phrase in aux_str:
            result["tense"] = tense
            result["aspect"] = aspect
            break
    else:
        if not auxes and i < n:
            w = words[i].lower()
            if w in _EN_PAST_TO_BASE or w in _EN_PAST_PART_TO_BASE:
                result["tense"] = "past"
                result["aspect"] = "simple"

    # Main verb
    if i >= n:
        result["error"] = "No verb found"
        return result

    raw = words[i].lower()
    stem = _en_to_stem(raw)
    if stem is None and raw.endswith("ing"):
        stem = _en_to_stem(raw[:-3]) or _en_to_stem(raw[:-4] if len(raw) > 4 else "")
    result["verb_stem"] = stem
    i += 1

    # Complement clause detection: pron + verb (e.g. "you die", "he speak")
    complement: Optional[str] = None
    if i < n:
        w0 = words[i].lower()
        if w0 == "that" and i + 1 < n:
            i += 1
            w0 = words[i].lower()
        sig0, pos0 = _EN_TO_SIGAN.get(w0, (None, None))
        if pos0 == "Pron" and i + 1 < n:
            comp_stem = _en_to_stem(words[i + 1].lower())
            if comp_stem:
                complement = f"{sig0} {comp_stem}"
                i += 2

    # Object words (stop at time word)
    obj_words: list[str] = []
    if complement is None:
        while i < n:
            w = words[i].lower()
            sig, pos = _EN_TO_SIGAN.get(w, (None, None))
            if pos == "T":
                result["time_word"] = sig; i += 1; break
            obj_words.append(words[i]); i += 1

    result["object_words"] = obj_words
    result["complement"] = complement
    return result


def english_to_sigan(sentence: str) -> dict:
    words = sentence.strip().split()
    if not words:
        return {"success": False, "sigan": "", "error": "Empty input"}

    parsed = _parse_english(words)
    if parsed["error"]:
        return {"success": False, "sigan": "", "error": parsed["error"]}

    tokens: list[str] = []

    if parsed["subject"]:
        subj_low = parsed["subject"].lower()
        sig, _ = _EN_TO_SIGAN.get(subj_low, (None, None))
        tokens.append(sig if sig else _words_to_sigan_np(parsed["subject"].split()))

    stem = parsed["verb_stem"]
    if not stem:
        return {"success": False, "sigan": "", "error": "Unknown verb"}

    suffix = _SIGAN_SUFFIX.get((parsed["tense"], parsed["aspect"]), "")
    if parsed["negated"]:
        tokens.append("noth")
    tokens.append(stem + suffix)

    if parsed.get("complement"):
        tokens.append(parsed["complement"])

    if parsed["object_words"] and not parsed.get("complement"):
        tokens.append(_words_to_sigan_np(parsed["object_words"]))
    if parsed["time_word"]:
        tokens.append(parsed["time_word"])

    return {"success": True, "sigan": " ".join(tokens), "error": None}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage:")
        print('  python translator.py --to-english "<sigan sentence>"')
        print('  python translator.py --to-sigan   "<english sentence>"')
        sys.exit(1)

    mode, sentence = sys.argv[1], " ".join(sys.argv[2:])

    if mode == "--to-english":
        result = sigan_to_english(sentence)
        if result["success"]:
            print(result["english"])
        else:
            print("Translation failed:")
            for e in result["error"]:
                print(f"  {e}")
            sys.exit(1)

    elif mode == "--to-sigan":
        result = english_to_sigan(sentence)
        if result["success"]:
            print(result["sigan"])
        else:
            print(f"Translation failed: {result['error']}")
            sys.exit(1)

    else:
        print(f"Unknown mode: {mode}  (use --to-english or --to-sigan)")
        sys.exit(1)


if __name__ == "__main__":
    main()
