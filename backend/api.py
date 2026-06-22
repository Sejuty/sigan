"""
Sigan FastAPI server.
Run: uvicorn api:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from validator import validate, ParseNode, TokenInfo
from translator import sigan_to_english, english_to_sigan
from lexicon import (
    LEXICON, VERB_EN,
    NOUN_EN, ADJ_EN, PRON_EN, PRON_OBJ_EN, POSS_EN,
    DET_EN, PREP_EN, TIME_EN, QN_EN,
)

app = FastAPI(title="Sigan API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Conjugation table  (tense, aspect) → suffix
# ---------------------------------------------------------------------------

_CONJUGATIONS: list[tuple[str, str, str]] = [
    ("past",    "simple",     "ov"),
    ("past",    "continuous", "ovrak"),
    ("past",    "completed",  "ovdor"),
    ("past",    "habitual",   "ovzun"),
    ("present", "simple",     ""),
    ("present", "continuous", "rak"),
    ("present", "completed",  "dor"),
    ("present", "habitual",   "zun"),
    ("future",  "simple",     "en"),
    ("future",  "continuous", "enrak"),
    ("future",  "completed",  "endor"),
    ("future",  "habitual",   "enzun"),
]

_POS_LABEL: dict[str, str] = {
    "V":     "Verbs",
    "N":     "Nouns",
    "Adj":   "Adjectives",
    "Pron":  "Pronouns",
    "PossN": "Possessives",
    "Det":   "Determiners",
    "P":     "Prepositions",
    "T":     "Time Words",
    "QN":    "Question Words",
    "Neg":   "Negation",
    "CAUS_V":"Causative",
    "VOC":   "Vocative",
}


def _english_for(word: str, pos: str) -> Optional[str]:
    if pos == "N":      return NOUN_EN.get(word)
    if pos == "V":
        e = VERB_EN.get(word)
        return e[0] if e else None
    if pos == "Adj":    return ADJ_EN.get(word)
    if pos == "Pron":   return PRON_EN.get(word)
    if pos == "PossN":  return POSS_EN.get(word)
    if pos == "Det":    return DET_EN.get(word)
    if pos == "P":      return PREP_EN.get(word)
    if pos == "T":      return TIME_EN.get(word)
    if pos == "QN":     return QN_EN.get(word)
    if pos == "Neg":    return "not"
    if pos == "CAUS_V": return "cause / make"
    if pos == "VOC":    return "(vocative marker)"
    return None


def _node_to_dict(node: ParseNode) -> dict:
    result: dict = {"symbol": node.symbol, "children": []}
    if node.is_leaf():
        tok = node.token
        result["token"]  = tok.surface
        result["tense"]  = tok.tense  or None
        result["aspect"] = tok.aspect or None
    else:
        if node.left:
            result["children"].append(_node_to_dict(node.left))
        if node.right:
            result["children"].append(_node_to_dict(node.right))
    return result


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/vocab")
def get_vocab():
    categories: dict[str, list] = {}

    for word, pos in LEXICON.items():
        label = _POS_LABEL.get(pos, pos)
        categories.setdefault(label, [])

        entry: dict = {
            "sigan":   word,
            "pos":     pos,
            "english": _english_for(word, pos),
        }

        if pos == "V":
            entry["conjugations"] = [
                {
                    "tense":  tense,
                    "aspect": aspect,
                    "form":   word + suffix,
                }
                for tense, aspect, suffix in _CONJUGATIONS
            ]

        categories[label].append(entry)

    for label in categories:
        categories[label].sort(key=lambda x: x["sigan"])

    return {"categories": categories}


class TranslateRequest(BaseModel):
    text: str
    direction: str  # "to_english" | "to_sigan"


@app.post("/translate")
def translate(req: TranslateRequest):
    if req.direction == "to_english":
        r = sigan_to_english(req.text)
        return {
            "success": r["success"],
            "result":  r.get("english", ""),
            "error":   r.get("error"),
        }
    else:
        r = english_to_sigan(req.text)
        return {
            "success": r["success"],
            "result":  r.get("sigan", ""),
            "error":   r.get("error"),
        }


class ValidateRequest(BaseModel):
    sentence: str


@app.post("/validate")
def validate_sentence(req: ValidateRequest):
    r = validate(req.sentence)

    tokens = [
        {
            "surface": t.surface,
            "pos":     t.pos,
            "stem":    t.stem,
            "tense":   t.tense  or None,
            "aspect":  t.aspect or None,
        }
        for t in r["tokens"]
    ]

    tree = _node_to_dict(r["parse_tree"]) if r["parse_tree"] else None

    return {
        "valid":  r["valid"],
        "tokens": tokens,
        "tree":   tree,
        "errors": r["errors"],
    }
