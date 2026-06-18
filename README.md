# Sigan Language Tools

Parser, validator, and bidirectional translator for **Sigan** — a constructed language with strict SVO word order, suffix-based tense/aspect morphology, and a deterministic CKY chart parser.

---

## Project structure

```
sigan/
├── backend/
│   ├── lexicon.py      All vocabulary and English translation tables
│   ├── grammar.py      CFG production rules and tense/aspect suffix table
│   ├── validator.py    CKY chart parser — checks grammatical validity
│   ├── translator.py   Sigan ↔ English bidirectional translator
│   ├── api.py          FastAPI server (REST bridge for the frontend)
│   └── cli.py          Interactive REPL combining all tools
└── frontend/
    └── src/app/
        ├── vocab/      Browse and search the full lexicon
        ├── translate/  Bidirectional translation with history
        └── validate/   Sentence validator with parse tree view
```

Backend uses **Python stdlib only** (no pip dependencies beyond FastAPI for the API server).

---

## Running

### Backend CLI (no server needed)

```bash
cd backend

# Validate a sentence
python3 validator.py "ayu sigan gar truku"

# Translate Sigan → English
python3 translator.py --to-english "ayu siganovrak gar truku"

# Translate English → Sigan
python3 translator.py --to-sigan "I was seeing the tree"

# Start the interactive REPL
python3 cli.py
```

### Full stack (API + frontend)

```bash
# Terminal 1 — start the API server
cd backend
uvicorn api:app --reload --port 8000

# Terminal 2 — start the frontend
cd frontend
npm run dev
```

Then open `http://localhost:3000`.

---

## validator.py

Tokenizes a sentence, looks up each word's POS tag, strips verb suffixes, then runs a CKY chart parse against the 29 CNF grammar rules.

**Output:** `VALID` with parse tree, or `INVALID` with the reason.

```bash
python3 validator.py "<sentence>"
```

**Examples:**

```
$ python3 validator.py "ayu sigan gar truku"
VALID

Parse tree:
(S
  (NP
    (Pron 'ayu'))
  (VP
    (V 'sigan')
    (NP
      (Det 'gar')
      (N 'truku'))))
```

```
$ python3 validator.py "ayu siganovrak gar truku"
VALID

Parse tree:
(S
  (NP
    (Pron 'ayu'))
  (VP
    (V 'siganovrak' [past-continuous])
    (NP
      (Det 'gar')
      (N 'truku'))))
```

```
$ python3 validator.py "gar sigan ayu"
INVALID
  Error: No valid parse: sentence violates Sigan grammar rules

$ python3 validator.py "ayu sigan gar zorblax"
INVALID
  Error: Unknown word: 'zorblax'
```

---

## translator.py

**Mode 1 — Sigan → English:**
Runs the validator, then walks the parse tree to produce natural English with correct tense, aspect, and subject-verb agreement.

```bash
python3 translator.py --to-english "<sigan sentence>"
```

**Mode 2 — English → Sigan:**
Maps subject, auxiliaries, verb, object, and time word into Sigan word order with the correct verb suffix.

```bash
python3 translator.py --to-sigan "<english sentence>"
```

**Examples:**

```
$ python3 translator.py --to-english "ayu siganovrak gar truku"
I was seeing the tree

$ python3 translator.py --to-english "hirun folurenrak gar rotha"
They will be following the path

$ python3 translator.py --to-english "hiru noth spekor worda"
He does not speak word

$ python3 translator.py --to-english "huzh sigan gar truku"
Who sees the tree?

$ python3 translator.py --to-english "ayu hopak yu dethrak"
I hope that you die

$ python3 translator.py --to-english "ayu kawzad hiru sigan"
I cause him to see
```

```
$ python3 translator.py --to-sigan "I was seeing the tree"
ayu siganovrak gar truku

$ python3 translator.py --to-sigan "she will build a house"
hiru bildagen brath homu

$ python3 translator.py --to-sigan "they will be following the path"
hirun folurenrak gar rotha

$ python3 translator.py --to-sigan "I hope you die"
ayu hopak yu dethrak

$ python3 translator.py --to-sigan "he found the stone"
hiru findarov gar stonu
```

### Tense/aspect suffix table

| English pattern | Sigan suffix | Example |
|---|---|---|
| bare verb (present simple) | *(none)* | `sigan` |
| is/am/are + -ing | `-rak` | `siganrak` |
| has/have + participle | `-dor` | `sigandor` |
| usually + verb | `-zun` | `siganzun` |
| past (saw/walked/etc.) | `-ov` | `siganov` |
| was/were + -ing | `-ovrak` | `siganovrak` |
| had + participle | `-ovdor` | `siganovdor` |
| used to + verb | `-ovzun` | `siganovzun` |
| will + verb | `-en` | `siganen` |
| will be + -ing | `-enrak` | `siganenrak` |
| will have + participle | `-endor` | `siganendor` |
| will usually + verb | `-enzun` | `siganenzun` |

---

## cli.py — Interactive REPL

```bash
python3 cli.py
```

### Commands

| Command | Description |
|---|---|
| `:validate <sentence>` | Validate a Sigan sentence and show its parse tree |
| `:to-en <sentence>` | Translate Sigan → English |
| `:to-sig <sentence>` | Translate English → Sigan |
| `:history` | Show all commands run this session |
| `:help` | Show the command list |
| `:quit` / `:exit` | Exit the REPL |

### Example session

```
$ python3 cli.py
Sigan REPL  (type :help for commands, :quit to exit)

sigan> :validate ayu siganovrak gar truku
VALID

sigan> :to-en ayu siganovrak gar truku
I was seeing the tree

sigan> :to-sig I hope you die
ayu hopak yu dethrak

sigan> :to-en hiru walkag tov gar homu yestom
He walks to the house yesterday

sigan> :quit
Goodbye.
```

---

## Language reference

### Word order

```
[Subject NP]  [noth]  [Verb]  [Object NP]  [PP]  [Time]
ayu           noth    sigan   gar truku    tov gar homu  yestom
I             not     see     the tree     to the house  yesterday
```

### Pronouns

| Sigan | English (subject) | English (object) |
|---|---|---|
| `ayu` / `ayun` | I / we | me / us |
| `yu` / `yun` | you (sg) / you (pl) | you / you |
| `hiru` / `hirun` | he/she/it / they | him/her/it / them |

### Possessives

`ayugar` my · `yugar` your · `hirugar` his/her/its · `ayungar` our · `yungar` your (pl) · `hirungar` their

### Determiners

`gar` the · `brath` a/some

### Negation

`noth` goes immediately before the verb: `ayu noth sigan gar truku` → *I do not see the tree*

### Questions

- Fronted question word: `huzh sigan gar truku` → *Who sees the tree?*
- Inline question word: `hiru sigan wazh` → *He sees what?*

Available: `huzh` who · `wazh` what · `werazh` where · `wenazh` when

### Causative

`ayu kawzad hiru walkag` → *I cause him to walk*

---

## Extending the language

### Adding a word

Edit `backend/lexicon.py`:

```python
# LEXICON — Sigan word → POS tag
"luma": "N",
"luman": "N",   # plural

# NOUN_EN — Sigan → English
"luma": "light",
"luman": "lights",
```

### Adding a grammar rule

Edit `backend/grammar.py`:

```python
# BINARY_RULES: (LHS, left_child, right_child)
("VP_ADV", "VP", "Adv"),

# UNARY_RULES: (LHS, child)
("S", "VP_ADV"),
```

The validator, translator, and API all pick up changes automatically.
