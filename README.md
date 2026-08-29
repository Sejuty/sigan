# Sigan Language Tools

Parser, validator, and bidirectional translator for **Sigan** — a constructed language with strict SVO word order and suffix-based tense/aspect morphology, parsed with a CKY chart parser.

## Project structure

```
sigan/
├── backend/
│   ├── lexicon.py      Vocabulary and English translation tables
│   ├── grammar.py      CFG production rules and tense/aspect suffixes
│   ├── validator.py    CKY chart parser — checks grammatical validity
│   ├── translator.py   Sigan ↔ English bidirectional translator
│   ├── api.py          FastAPI server (REST bridge for the frontend)
│   ├── cli.py          Interactive REPL combining all tools
│   └── test_*.py       Test suites — parser, grammar coverage, API
└── frontend/
    └── src/app/
        ├── vocab/      Browse and search the lexicon
        ├── translate/  Bidirectional translation with history
        └── validate/   Sentence validator with parse tree view
```

Backend uses Python stdlib only, plus FastAPI for the API server.

## Setup

```bash
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

## Running

```bash
# Validate a sentence
cd backend && python3 validator.py "elva velor al taelo"

# Translate Sigan → English
python3 translator.py --to-english "elva velor al taelo"

# Translate English → Sigan
python3 translator.py --to-sigan "I see the house"

# Interactive REPL
python3 cli.py
```

Full stack:

```bash
cd backend && uvicorn api:app --reload --port 8000   # terminal 1
cd frontend && npm run dev                            # terminal 2
```

Then open `http://localhost:3000`.

## Tests

415 tests, no framework required — each file runs standalone and exits
non-zero on failure.

```bash
cd backend
python3 test_core.py              # 148 — validator and translator core
python3 test_grammar_coverage.py  # 159 — prepositions, aspects, question words
python3 test_api.py               # 108 — every endpoint, via TestClient
```

`test_api.py` needs the dependencies from `requirements.txt` installed; the
other two run on the standard library alone.

## API

| Method | Endpoint | Body |
|---|---|---|
| `GET`  | `/` | — (service info) |
| `GET`  | `/vocab` | — |
| `POST` | `/translate` | `{"text": "...", "direction": "to_english" \| "to_sigan"}` |
| `POST` | `/validate` | `{"sentence": "..."}` |

Interactive docs at `http://localhost:8000/docs`.

## Configuration

The frontend reads the API base URL from `NEXT_PUBLIC_API_URL`, falling back to
`http://localhost:8000` when unset. For local development the fallback is
usually enough; to point at a deployed backend, create `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-host   # no trailing slash
```

`NEXT_PUBLIC_*` values are inlined at build time, so the variable must be set
*before* building — changing it requires a rebuild, not just a restart.

## Tense/aspect suffixes

Applied to the verb stem (e.g. `velor` = see):

| English pattern | Suffix | Example |
|---|---|---|
| present simple | *(none)* | `velor` |
| past | `-ov` | `velorov` |
| past continuous | `-ovrak` | `velorovrak` |
| future | `-en` | `veloren` |

Negation: `nael` immediately before the verb — `elva nael velor al taelo` → *I do not see the house*.

## Language reference

**Pronouns:** `elva`/`elvan` I/we · `sova`/`sovan` you (sg/pl) · `thira`/`thiran` he-she-it/they
**Possessives:** `elvanar` my · `sovanar` your · `thiranar` his/her/its · `elvanen` our · `sovanen` their
**Determiners:** `al` the · `elo` a
**Prepositions:** `vil` to · `mira` from · `ana` in · `leva` with · `thael` about · `ori` for
**Question words:** `sivael` who · `tavael` what · `lorvael` where · `morvael` when · `alvael` how
**Greetings:** `laevel` hello · `sorvael` goodbye

## Extending the language

Add vocabulary in `backend/lexicon.py` (word → POS tag, plus its entry in the matching `*_EN` dict). Add grammar in `backend/grammar.py` (`BINARY_RULES` / `UNARY_RULES`). The validator, translator, and API all pick up changes automatically — no other file needs touching.
