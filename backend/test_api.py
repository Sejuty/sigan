"""
API layer tests — exercises every endpoint via FastAPI's TestClient
(no live server required).

Run: python3 test_api.py
"""

import sys
from fastapi.testclient import TestClient
from api import app

GREEN = "\033[92m"
RED   = "\033[91m"
CYAN  = "\033[96m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"

client  = TestClient(app)
results: list[tuple[bool, str, str]] = []


def _record(passed: bool, label: str, detail: str = "") -> bool:
    results.append((passed, label, detail))
    icon = f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"
    print(f"  {icon}  {label}")
    if not passed:
        print(f"       {RED}{detail}{RESET}")
    return passed

def section(title: str) -> None:
    print(f"\n{BOLD}{CYAN}{'─'*62}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*62}{RESET}")

# ── helpers ──────────────────────────────────────────────────────────────────

def post_validate(sentence: str) -> dict:
    return client.post("/validate", json={"sentence": sentence}).json()

def post_translate(text: str, direction: str) -> dict:
    return client.post("/translate", json={"text": text, "direction": direction}).json()

def get_vocab() -> dict:
    return client.get("/vocab").json()


# ════════════════════════════════════════════════════════════════
# 1.  HTTP STATUS CODES
# ════════════════════════════════════════════════════════════════

section("1. HTTP status codes")

def check_status(method: str, path: str, body, expected: int, note: str):
    r = client.request(method, path, json=body)
    ok = r.status_code == expected
    _record(ok, f"[{method} {path}] {note} → {expected}",
            f"Got {r.status_code}")

check_status("GET",  "/vocab",     None,                                200, "OK")
check_status("POST", "/validate",  {"sentence": "elva velor sova"},     200, "valid input")
check_status("POST", "/validate",  {"sentence": "blork"},               200, "invalid sigan still 200")
check_status("POST", "/translate", {"text": "elva velor sova",
                                    "direction": "to_english"},          200, "sigan→en OK")
check_status("POST", "/translate", {"text": "I see you",
                                    "direction": "to_sigan"},            200, "en→sigan OK")
check_status("POST", "/validate",  {},                                   422, "missing sentence field")
check_status("POST", "/translate", {"text": "hello"},                   422, "missing direction field")
check_status("GET",  "/notfound",  None,                                404, "unknown route")


# ════════════════════════════════════════════════════════════════
# 2.  POST /validate — response shape & semantics
# ════════════════════════════════════════════════════════════════

section("2. POST /validate — response shape")

def check_validate_shape(sentence: str, expect_valid: bool, note: str):
    r = post_validate(sentence)
    ok = True
    detail = []
    # required keys
    for k in ("valid", "tokens", "tree", "errors"):
        if k not in r:
            ok = False; detail.append(f"missing key '{k}'")
    if ok:
        if r["valid"] != expect_valid:
            ok = False; detail.append(f"valid={r['valid']!r}, want {expect_valid}")
        if expect_valid:
            if r["tree"] is None:
                ok = False; detail.append("tree is None for valid sentence")
            if r["errors"]:
                ok = False; detail.append(f"errors non-empty: {r['errors']}")
        else:
            if r["tree"] is not None:
                ok = False; detail.append("tree should be None for invalid sentence")
            if not r["errors"]:
                ok = False; detail.append("errors should be non-empty for invalid sentence")
    _record(ok, f"[shape] {note}", "; ".join(detail))
    return r

check_validate_shape("elva velor sova",      True,  "basic valid sentence")
check_validate_shape("elvan alivor sovan",   True,  "we help you")
check_validate_shape("elva nael thaevel",    True,  "negation")
check_validate_shape("elva aevil Sejuty",    True,  "copula + proper noun")
check_validate_shape("laevel",               True,  "standalone greeting")
check_validate_shape("blork sova",           False, "unknown word")
check_validate_shape("",                     False, "empty sentence")
check_validate_shape("velor elva sova",      False, "VSO word order")

section("2b. POST /validate — token shape")

def check_token_shape(sentence: str, note: str):
    r = post_validate(sentence)
    ok = True; detail = []
    for tok in r.get("tokens", []):
        for k in ("surface", "pos", "stem", "tense", "aspect"):
            if k not in tok:
                ok = False; detail.append(f"token missing '{k}'")
                break
    _record(ok, f"[tokens] {note}", "; ".join(detail))

check_token_shape("elva velor sova",         "SVO — 3 tokens")
check_token_shape("elva velorov sova",       "inflected verb token")
check_token_shape("elva nael velor sova",    "negation — 4 tokens")
check_token_shape("sivael velor sova",       "question word token")

section("2c. POST /validate — tree shape")

def check_tree_node(node: dict, path: str = "root") -> list[str]:
    errs = []
    if "symbol" not in node:
        errs.append(f"{path}: missing 'symbol'")
        return errs
    if "children" not in node:
        errs.append(f"{path}: missing 'children'")
        return errs
    is_leaf = "token" in node
    if is_leaf:
        for k in ("tense", "aspect"):
            if k not in node:
                errs.append(f"{path}: leaf missing '{k}'")
    for i, child in enumerate(node["children"]):
        errs.extend(check_tree_node(child, f"{path}.children[{i}]"))
    return errs

sentences_for_tree = [
    ("elva velor sova",         "SVO"),
    ("elva nael velor sova",    "negated SVO"),
    ("sivael velor sova",       "question"),
    ("elva lorel ulra",         "locative"),
    ("elva velor al laeva",     "Det NP object"),
    ("elva velorov sova",       "inflected past"),
]
for sent, note in sentences_for_tree:
    r = post_validate(sent)
    if r["tree"]:
        errs = check_tree_node(r["tree"])
        _record(not errs, f"[tree] {note} — {sent!r}", "; ".join(errs))
    else:
        _record(False, f"[tree] {note}", "tree is None")

section("2d. POST /validate — token values")

def check_token_values(sentence: str, expected_pos: list[str], note: str):
    r = post_validate(sentence)
    tokens = r.get("tokens", [])
    got_pos = [t["pos"] for t in tokens]
    ok = got_pos == expected_pos
    _record(ok, f"[token-pos] {note}",
            f"expected {expected_pos}, got {got_pos}")

check_token_values("elva velor sova",       ["Pron","V","Pron"],      "SVO pronouns")
check_token_values("elva nael thaevel",     ["Pron","Neg","V"],       "Pron Neg V")
check_token_values("al savori",             ["Det","N"],              "Det N (invalid parse, valid tokens)")
check_token_values("laevel",               ["Greet"],                "greeting token")
check_token_values("elva velorov sova",    ["Pron","V","Pron"],      "inflected verb keeps pos=V")

def check_verb_token(sentence: str, stem: str, tense: str, aspect: str, note: str):
    r = post_validate(sentence)
    tokens = r.get("tokens", [])
    verbs = [t for t in tokens if t["pos"] == "V"]
    if not verbs:
        _record(False, f"[verb-tok] {note}", "no V token found")
        return
    v = verbs[0]
    ok = v["stem"] == stem and v["tense"] == tense and v["aspect"] == aspect
    _record(ok, f"[verb-tok] {note}",
            f"stem={v['stem']!r} tense={v['tense']!r} aspect={v['aspect']!r}")

check_verb_token("elva velor sova",       "velor",  "present", "simple",     "present simple")
check_verb_token("elva velorov sova",     "velor",  "past",    "simple",     "past simple")
check_verb_token("elva velorenrak sova",  "velor",  "future",  "continuous", "future continuous")
check_verb_token("elva velordor sova",    "velor",  "present", "completed",  "present completed")


# ════════════════════════════════════════════════════════════════
# 3.  POST /translate — response shape & semantics
# ════════════════════════════════════════════════════════════════

section("3a. POST /translate — response shape (to_english)")

def check_translate_shape(text: str, direction: str,
                           expect_success: bool, expect_result: str, note: str):
    r = post_translate(text, direction)
    ok = True; detail = []
    for k in ("success", "result", "error"):
        if k not in r:
            ok = False; detail.append(f"missing key '{k}'")
    if ok:
        if r["success"] != expect_success:
            ok = False; detail.append(f"success={r['success']}, want {expect_success}")
        if expect_success and r["result"].lower() != expect_result.lower():
            ok = False; detail.append(f"result={r['result']!r}, want {expect_result!r}")
        if expect_success and r["error"] is not None:
            ok = False; detail.append(f"error should be None on success, got {r['error']!r}")
        if not expect_success and not r["error"]:
            ok = False; detail.append("error should be non-None on failure")
    _record(ok, f"[translate] {note}", "; ".join(detail))

# Sigan → English successes
check_translate_shape("elva velor sova",    "to_english", True,  "I see you",       "basic SVO")
check_translate_shape("elva elavar sova",   "to_english", True,  "I love you",      "emotion verb")
check_translate_shape("elva aevil saeril",  "to_english", True,  "I am well",       "copula")
check_translate_shape("elva nael thaevel",  "to_english", True,  "I do not speak",  "negation")
check_translate_shape("elva velorov sova",  "to_english", True,  "I saw you",       "irregular past")
check_translate_shape("elva veloren sova",  "to_english", True,  "I will see you",  "future")
check_translate_shape("sivael velor sova",  "to_english", True,  "Who sees you?",   "question")
check_translate_shape("laevel",             "to_english", True,  "Hello",           "greeting")

# Sigan → English failures (invalid input)
check_translate_shape("blork elva sova",    "to_english", False, "", "unknown word → failure")
check_translate_shape("velor elva sova",    "to_english", False, "", "bad word order → failure")
check_translate_shape("",                   "to_english", False, "", "empty string → failure")

section("3b. POST /translate — response shape (to_sigan)")

# English → Sigan successes
check_translate_shape("I see you",          "to_sigan", True,  "elva velor sova",       "basic SVO")
check_translate_shape("I love you",         "to_sigan", True,  "elva elavar sova",      "emotion verb")
check_translate_shape("I am well",          "to_sigan", True,  "elva aevil saeril",     "copula")
check_translate_shape("I am Sejuty",        "to_sigan", True,  "elva aevil Sejuty",     "copula + proper noun")
check_translate_shape("My name is Sartre",  "to_sigan", True,  "elvanar aelova aevil Sartre", "possessive subject")
check_translate_shape("I do not speak",     "to_sigan", True,  "elva nael thaevel",     "negation")
check_translate_shape("I saw you",          "to_sigan", True,  "elva velorov sova",     "irregular past")
check_translate_shape("I will see you",     "to_sigan", True,  "elva veloren sova",     "future")
check_translate_shape("I go there",         "to_sigan", True,  "elva lorel ulra",       "locative")
check_translate_shape("I go here",          "to_sigan", True,  "elva lorel ilra",       "locative here")
check_translate_shape("I usually see you",  "to_sigan", True,  "elva velorzun sova",    "habitual")
check_translate_shape("I speak with you",   "to_sigan", True,  "elva thaevel leva sova","preposition")

# English → Sigan failures
check_translate_shape("",                   "to_sigan", False, "", "empty string → failure")

section("3c. POST /translate — unknown direction")

r = post_translate("I see you", "to_klingon")
# unknown direction falls to else → runs english_to_sigan
_record("success" in r and "result" in r,
        "[translate] unknown direction — response has required keys",
        "missing success/result keys")


# ════════════════════════════════════════════════════════════════
# 4.  GET /vocab — response shape & content
# ════════════════════════════════════════════════════════════════

section("4a. GET /vocab — top-level shape")

vocab = get_vocab()
_record("categories" in vocab,
        "[vocab] response has 'categories' key",
        f"keys: {list(vocab.keys())}")

cats = vocab.get("categories", {})
EXPECTED_CATEGORIES = ["Verbs", "Nouns", "Adjectives", "Pronouns",
                       "Possessives", "Determiners", "Prepositions",
                       "Time Words", "Question Words", "Negation"]
for cat in EXPECTED_CATEGORIES:
    _record(cat in cats, f"[vocab] category '{cat}' present",
            f"available: {list(cats.keys())}")

section("4b. GET /vocab — entry shapes")

def check_vocab_entry(entry: dict, has_conjugations: bool, ctx: str) -> list[str]:
    errs = []
    for k in ("sigan", "pos", "english"):
        if k not in entry:
            errs.append(f"{ctx}: missing '{k}'")
    if has_conjugations:
        if "conjugations" not in entry:
            errs.append(f"{ctx}: missing 'conjugations'")
        else:
            for conj in entry["conjugations"]:
                for ck in ("tense", "aspect", "form"):
                    if ck not in conj:
                        errs.append(f"{ctx}.conjugation: missing '{ck}'")
    return errs

# Verbs — must have conjugations
verb_entries = cats.get("Verbs", [])
_record(len(verb_entries) > 0, "[vocab] Verbs list non-empty",
        "Verbs category is empty")
all_verb_errs = []
for e in verb_entries:
    all_verb_errs.extend(check_vocab_entry(e, has_conjugations=True, ctx=e.get("sigan","?")))
_record(not all_verb_errs, f"[vocab] all {len(verb_entries)} verb entries well-formed",
        "; ".join(all_verb_errs[:5]))

# Non-verb categories — no conjugations expected
for cat_name in ["Nouns", "Adjectives", "Pronouns", "Prepositions"]:
    entries = cats.get(cat_name, [])
    if not entries:
        _record(False, f"[vocab] {cat_name} non-empty", "category empty"); continue
    errs = []
    for e in entries:
        errs.extend(check_vocab_entry(e, has_conjugations=False, ctx=e.get("sigan","?")))
    _record(not errs, f"[vocab] {cat_name} entries well-formed ({len(entries)} entries)",
            "; ".join(errs[:5]))

section("4c. GET /vocab — conjugation correctness (spot-check velor)")

velor_entry = next((e for e in cats.get("Verbs", []) if e["sigan"] == "velor"), None)
_record(velor_entry is not None, "[vocab] 'velor' entry found in Verbs")
if velor_entry:
    conjs = {(c["tense"], c["aspect"]): c["form"] for c in velor_entry.get("conjugations", [])}
    checks = [
        (("present", "simple"),     "velor"),
        (("past",    "simple"),     "velorov"),
        (("future",  "simple"),     "veloren"),
        (("present", "continuous"), "velorrak"),
        (("past",    "continuous"), "velorovrak"),
        (("future",  "completed"),  "velorendor"),
    ]
    for key, expected_form in checks:
        got = conjs.get(key, "<missing>")
        _record(got == expected_form,
                f"[vocab] velor {key[0]}-{key[1]} → {expected_form!r}",
                f"got {got!r}")

section("4d. GET /vocab — sorted order within categories")

for cat_name in ["Verbs", "Nouns", "Adjectives"]:
    entries = cats.get(cat_name, [])
    sigans = [e["sigan"] for e in entries]
    _record(sigans == sorted(sigans),
            f"[vocab] {cat_name} sorted alphabetically",
            f"first 5: {sigans[:5]}")

section("4e. GET /vocab — English glosses present")

for cat_name, sample_sigan, expected_en in [
    ("Verbs",       "velor",   "see"),
    ("Nouns",       "laeva",   "person"),
    ("Adjectives",  "loravil", "big"),
    ("Pronouns",    "elva",    "I"),
    ("Possessives", "elvanar", "my"),
    ("Determiners", "al",      "the"),
    ("Prepositions","vil",     "to"),
    ("Time Words",  "salom",   "now"),
    ("Question Words","sivael","who"),
]:
    entry = next((e for e in cats.get(cat_name, []) if e["sigan"] == sample_sigan), None)
    if entry is None:
        _record(False, f"[vocab] {cat_name} '{sample_sigan}' entry found", "not found")
    else:
        ok = entry["english"] == expected_en
        _record(ok, f"[vocab] {sample_sigan!r} → {expected_en!r}",
                f"got {entry['english']!r}")


# ════════════════════════════════════════════════════════════════
# 5.  EDGE CASES & ROBUSTNESS
# ════════════════════════════════════════════════════════════════

section("5. Edge cases & robustness")

# Long valid sentence
r = post_validate("elva lorel vil al taelo salom")
_record(r["valid"], "[edge] long valid sentence (VP+PP+T) parses")

# Sentence with all tense aspects round-tripping through the API
for suffix, tense, aspect in [
    ("ov","past","simple"), ("enrak","future","continuous"), ("ovzun","past","habitual")
]:
    sent = f"elva velor{suffix} sova"
    rv = post_validate(sent)
    rt = post_translate(sent, "to_english")
    _record(rv["valid"] and rt["success"],
            f"[edge] {tense}-{aspect} validates and translates via API")

# Proper noun round-trip through API
r_val  = post_validate("elva aevil Sejuty")
r_tran = post_translate("elva aevil Sejuty", "to_english")
_record(r_val["valid"],           "[edge] proper noun validates via API")
_record(r_tran["success"] and "Sejuty" in r_tran["result"],
        "[edge] proper noun preserved in API translation",
        f"result: {r_tran.get('result')!r}")

# Extra whitespace handled gracefully
r = post_translate("  elva  velor  sova  ", "to_english")
_record(r["success"], "[edge] extra whitespace in translate request",
        f"error: {r.get('error')}")

# Very short valid input
r = post_validate("laevel")
_record(r["valid"] and r["tree"] is not None,
        "[edge] single greeting token validates and gets tree")

# translate endpoint: result field always present even on failure
for direction in ("to_english", "to_sigan"):
    r = post_translate("", direction)
    _record("result" in r, f"[edge] empty-string failure has 'result' field ({direction})")
    _record("error"  in r, f"[edge] empty-string failure has 'error'  field ({direction})")


# ════════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════════

total  = len(results)
passed = sum(1 for ok, *_ in results if ok)
failed = total - passed

print(f"\n{BOLD}{'═'*62}{RESET}")
print(f"{BOLD}  Results: {GREEN}{passed} passed{RESET}{BOLD}  /  {RED}{failed} failed{RESET}{BOLD}  /  {total} total{RESET}")
print(f"{BOLD}{'═'*62}{RESET}")

if failed:
    print(f"\n{RED}{BOLD}Failed tests:{RESET}")
    for ok, label, detail in results:
        if not ok:
            print(f"  {RED}✗  {label}{RESET}")
            if detail:
                print(f"       {DIM}{detail}{RESET}")

sys.exit(0 if failed == 0 else 1)
