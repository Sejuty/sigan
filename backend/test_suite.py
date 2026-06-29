"""
Comprehensive test suite for Sigan validator and translator.
Run: python3 test_suite.py
"""

import sys
import traceback
from dataclasses import dataclass, field
from typing import Optional

from validator import validate
from translator import sigan_to_english, english_to_sigan

# ── Colour helpers ──────────────────────────────────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

# ── Result tracking ─────────────────────────────────────────────────────────

@dataclass
class Result:
    name: str
    passed: bool
    detail: str = ""

results: list[Result] = []

def _record(name: str, passed: bool, detail: str = "") -> bool:
    results.append(Result(name, passed, detail))
    icon = f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"
    print(f"  {icon}  {name}")
    if not passed:
        print(f"       {RED}{detail}{RESET}")
    return passed

# ── Assertion helpers ────────────────────────────────────────────────────────

def assert_valid(sentence: str, note: str = "") -> bool:
    label = f"[VALID] {sentence}" + (f"  ({note})" if note else "")
    try:
        r = validate(sentence)
        return _record(label, r["valid"],
                       f"Expected valid, got errors: {r['errors']}")
    except Exception as e:
        return _record(label, False, f"Exception: {e}")

def assert_invalid(sentence: str, note: str = "") -> bool:
    label = f"[INVALID] {sentence}" + (f"  ({note})" if note else "")
    try:
        r = validate(sentence)
        return _record(label, not r["valid"],
                       f"Expected invalid, but was accepted")
    except Exception as e:
        return _record(label, False, f"Exception: {e}")

def assert_sigan_to_en(sigan: str, expected: str) -> bool:
    label = f"[S→E] {sigan!r} → {expected!r}"
    try:
        r = sigan_to_english(sigan)
        if not r["success"]:
            return _record(label, False, f"Failed: {r['error']}")
        got = r["english"]
        ok = got.lower() == expected.lower()
        return _record(label, ok, f"Got {got!r}")
    except Exception as e:
        return _record(label, False, f"Exception: {e}\n{traceback.format_exc()}")

def assert_en_to_sigan(english: str, expected: str) -> bool:
    label = f"[E→S] {english!r} → {expected!r}"
    try:
        r = english_to_sigan(english)
        if not r["success"]:
            return _record(label, False, f"Failed: {r['error']}")
        got = r["sigan"]
        ok = got.lower() == expected.lower()
        return _record(label, ok, f"Got {got!r}")
    except Exception as e:
        return _record(label, False, f"Exception: {e}\n{traceback.format_exc()}")

def assert_en_to_sigan_no_error(english: str) -> bool:
    label = f"[E→S no-error] {english!r}"
    try:
        r = english_to_sigan(english)
        return _record(label, r["success"], f"Error: {r.get('error')}")
    except Exception as e:
        return _record(label, False, f"Exception: {e}")

def assert_roundtrip(english: str) -> bool:
    """English → Sigan → English should produce the same English (case-insensitive)."""
    label = f"[ROUNDTRIP] {english!r}"
    try:
        r1 = english_to_sigan(english)
        if not r1["success"]:
            return _record(label, False, f"E→S failed: {r1['error']}")
        sigan = r1["sigan"]
        r2 = sigan_to_english(sigan)
        if not r2["success"]:
            return _record(label, False, f"S→E failed on '{sigan}': {r2['error']}")
        got = r2["english"]
        ok = got.lower() == english.lower()
        return _record(label, ok, f"E→S→E: {english!r} → {sigan!r} → {got!r}")
    except Exception as e:
        return _record(label, False, f"Exception: {e}")

def section(title: str) -> None:
    print(f"\n{BOLD}{CYAN}{'─'*60}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*60}{RESET}")


# ════════════════════════════════════════════════════════════════════════════
# 1.  VALIDATION — SHOULD PASS
# ════════════════════════════════════════════════════════════════════════════

section("1a. Validation — Basic SVO sentences")
assert_valid("elva velor sova",          "I see you")
assert_valid("elva elavar sova",         "I love you")
assert_valid("elva savorel al savori",   "I eat the food")
assert_valid("thira mirel al mirae",     "He walks the path")
assert_valid("elva thaevel al voriva",   "I speak the word")
assert_valid("elva lireval al voriva",   "I read the word")
assert_valid("elvan alivor sovan",       "We help you (pl)")
assert_valid("elva aethivar al valori",  "I think the truth")
assert_valid("sova talovel ulra",        "You run there")
assert_valid("elvan aeravel ilra",       "We return here")

section("1b. Validation — Copula sentences")
assert_valid("elva aevil saeril",        "I am well")
assert_valid("elva aevil Sejuty",        "I am Sejuty (proper name)")
assert_valid("thira aevil loravil",      "He is big (pred. adj.)")

section("1c. Validation — Negation")
assert_valid("elva nael thaevel",        "I do not speak")
assert_valid("elva nael velor sova",     "I do not see you")
assert_valid("thira nael savorel al savori", "He does not eat the food")

section("1d. Validation — Questions")
assert_valid("sivael velor sova",        "Who sees you?")
assert_valid("sivael lireval al voriva", "Who reads the word?")
assert_valid("sivael alivor sovan",      "Who helps you?")
assert_valid("alvael aevil sova",        "How are you?")

section("1e. Validation — Tense/aspect inflections (all 11 forms on 'velor')")
assert_valid("elva velor sova",          "present simple")
assert_valid("elva velorrak sova",       "present continuous")
assert_valid("elva velordor sova",       "present completed")
assert_valid("elva velorzun sova",       "present habitual")
assert_valid("elva velorov sova",        "past simple")
assert_valid("elva velorovrak sova",     "past continuous")
assert_valid("elva velorovdor sova",     "past completed")
assert_valid("elva velorovzun sova",     "past habitual")
assert_valid("elva veloren sova",        "future simple")
assert_valid("elva velorenrak sova",     "future continuous")
assert_valid("elva velorendor sova",     "future completed")
assert_valid("elva velorenzun sova",     "future habitual")

section("1f. Validation — Locatives")
assert_valid("elva lorel ulra",          "I go there")
assert_valid("elva lorel ilra",          "I go here")
assert_valid("silvonor",                 "Silence! (imperative)")

section("1g. Validation — Possessives")
assert_valid("elva velor elvanar laeva",   "I see my person")
assert_valid("thira aevil thiranar aelova","He is his name")

section("1h. Validation — Preposition phrases")
assert_valid("elva lorel vil taelo",     "I go to the house (PP)")
assert_valid("thira lorel mira talvore", "He goes from the mountain")

section("1i. Validation — Time words")
assert_valid("elva velor sova salom",    "I see you now")
assert_valid("elva velorov sova verom",  "I saw you yesterday")
assert_valid("elva veloren sova norelom","I will see you tomorrow")

section("1j. Validation — Greetings (standalone)")
assert_valid("laevel",                   "Hello")
assert_valid("sorvael",                  "Goodbye")

section("1k. Validation — Adjective NPs")
assert_valid("elva velor elo loravil laeva",  "I see a big person")
assert_valid("thira savorel al theravil laeva","He eats the strong person")

section("1l. Validation — Emotion / motion / mental verbs")
assert_valid("thira drelovar al narovi",   "He fears the enemy")
assert_valid("elva elavar al alorivi",     "I love life")
assert_valid("elva sorviran al morive",    "I mourn the dead")
assert_valid("elva selavor al savori",     "I want the food")
assert_valid("elva aethivar al valori",    "I think the truth")

section("1m. Validation — Proper nouns")
assert_valid("elva aevil Sejuty",         "I am Sejuty")
assert_valid("Sejuty velor sova",         "Sejuty sees you")
assert_valid("Sartre thaevel al voriva",  "Sartre speaks the word")

section("1n. Validation — Should FAIL (bad grammar / unknown words)")
assert_invalid("velor elva sova",         "VSO order (verb-first)")
assert_invalid("elva sova velor",         "OVS order (object before verb)")
assert_invalid("elva blork sova",         "Unknown word 'blork'")
assert_invalid("",                        "Empty sentence")
assert_invalid("elva elva",              "Pron Pron with no verb")
assert_invalid("al savori",              "Det N alone (no subject+verb)")
assert_invalid("elva velor elva sova",   "Four tokens: subj + V + Pron + Pron (ambiguous extra)")


# ════════════════════════════════════════════════════════════════════════════
# 2.  SIGAN → ENGLISH
# ════════════════════════════════════════════════════════════════════════════

section("2a. Sigan→English — Core example phrases")
assert_sigan_to_en("elva velor sova",             "I see you")
assert_sigan_to_en("elva elavar sova",            "I love you")
assert_sigan_to_en("elva savorel al savori",      "I eat the food")
assert_sigan_to_en("thira mirel al mirae",        "He walks the path")
assert_sigan_to_en("elva thaevel al voriva",      "I speak the word")
assert_sigan_to_en("elva lireval al voriva",      "I read the word")
assert_sigan_to_en("elvan alivor sovan",          "We help you")
assert_sigan_to_en("elva aethivar al valori",     "I think the truth")
assert_sigan_to_en("thira drelovar al narovi",    "He fears the enemy")
assert_sigan_to_en("elva elavar al alorivi",      "I love the life")    # al = "the"; abstract drop is not implemented
assert_sigan_to_en("elva sorviran al morive",     "I mourn the death")   # morive = "death" (lexicon), not "dead"
assert_sigan_to_en("elva selavor al savori",      "I want the food")

section("2b. Sigan→English — Copula")
assert_sigan_to_en("elva aevil saeril",           "I am well")
assert_sigan_to_en("elva aevil Sejuty",           "I am Sejuty")
assert_sigan_to_en("thira aevil loravil",         "He is big")

section("2c. Sigan→English — Negation")
assert_sigan_to_en("elva nael thaevel",           "I do not speak")
assert_sigan_to_en("elva nael velor sova",        "I do not see you")

section("2d. Sigan→English — Questions")
assert_sigan_to_en("sivael velor sova",           "Who sees you?")
assert_sigan_to_en("sivael alivor sovan",         "Who helps you?")
assert_sigan_to_en("alvael aevil sova",           "How are you?")

section("2e. Sigan→English — Tense/aspect forms")
assert_sigan_to_en("elva velorrak sova",          "I am seeing you")
assert_sigan_to_en("elva velordor sova",          "I have seen you")
assert_sigan_to_en("elva velorov sova",           "I saw you")
assert_sigan_to_en("elva velorovrak sova",        "I was seeing you")
assert_sigan_to_en("elva velorovdor sova",        "I had seen you")
assert_sigan_to_en("elva veloren sova",           "I will see you")
assert_sigan_to_en("elva velorenrak sova",        "I will be seeing you")

section("2f. Sigan→English — Locatives & motion")
assert_sigan_to_en("elva lorel ulra",             "I go there")
assert_sigan_to_en("elva lorel ilra",             "I go here")
assert_sigan_to_en("sova talovel ulra",           "You run there")
assert_sigan_to_en("elvan aeravel ilra",          "We return here")

section("2g. Sigan→English — Agreement patch (3rd-person singular)")
assert_sigan_to_en("thira velor sova",            "He sees you")
assert_sigan_to_en("thira savorel al savori",     "He eats the food")

section("2h. Sigan→English — Greetings")
assert_sigan_to_en("laevel",                      "Hello")
assert_sigan_to_en("sorvael",                     "Goodbye")

section("2i. Sigan→English — Possessive NP")
assert_sigan_to_en("elva velor elvanar laeva",    "I see my person")

section("2j. Sigan→English — Adjective NP")
assert_sigan_to_en("elva velor elo loravil laeva","I see a big person")


# ════════════════════════════════════════════════════════════════════════════
# 3.  ENGLISH → SIGAN
# ════════════════════════════════════════════════════════════════════════════

section("3a. English→Sigan — Simple SVO")
assert_en_to_sigan("I see you",                   "elva velor sova")
assert_en_to_sigan("I love you",                  "elva elavar sova")
assert_en_to_sigan("I eat the food",              "elva savorel al savori")
assert_en_to_sigan("I speak the word",            "elva thaevel al voriva")
assert_en_to_sigan("I read the word",             "elva lireval al voriva")
assert_en_to_sigan("I want the food",             "elva selavor al savori")
assert_en_to_sigan("We help you",                 "elvan alivor sova")

section("3b. English→Sigan — Copula (newly fixed)")
assert_en_to_sigan("I am Sejuty",                 "elva aevil Sejuty")
assert_en_to_sigan("I am well",                   "elva aevil saeril")
assert_en_to_sigan("My name is Sartre",           "elvanar aelova aevil Sartre")
assert_en_to_sigan("She was a leader",            "thira aevilov elo thalvori")
assert_en_to_sigan("He is big",                   "thira aevil loravil")

section("3c. English→Sigan — Pronouns (all six)")
assert_en_to_sigan("I go there",                  "elva lorel ulra")
assert_en_to_sigan("you go there",                "sova lorel ulra")
assert_en_to_sigan("he goes there",               "thira lorel ulra")
assert_en_to_sigan("we go there",                 "elvan lorel ulra")
assert_en_to_sigan("they go there",               "thiran lorel ulra")

section("3d. English→Sigan — Tense/aspect forms")
assert_en_to_sigan("I see you",                   "elva velor sova")
assert_en_to_sigan("I am seeing you",             "elva velorrak sova")
assert_en_to_sigan("I have seen you",             "elva velordor sova")
assert_en_to_sigan("I saw you",                   "elva velorov sova")
assert_en_to_sigan("I was seeing you",            "elva velorovrak sova")
assert_en_to_sigan("I had seen you",              "elva velorovdor sova")
assert_en_to_sigan("I will see you",              "elva veloren sova")
assert_en_to_sigan("I will be seeing you",        "elva velorenrak sova")
assert_en_to_sigan("I will have seen you",        "elva velorendor sova")

section("3e. English→Sigan — Negation")
assert_en_to_sigan("I do not speak",              "elva nael thaevel")
assert_en_to_sigan("I do not see you",            "elva nael velor sova")

section("3f. English→Sigan — No-error smoke tests (output checked manually)")
assert_en_to_sigan_no_error("I think the truth")
assert_en_to_sigan_no_error("He fears the enemy")
assert_en_to_sigan_no_error("I love life")
assert_en_to_sigan_no_error("I mourn the dead")
assert_en_to_sigan_no_error("I help you")
assert_en_to_sigan_no_error("She is well")
assert_en_to_sigan_no_error("They were the leaders")
assert_en_to_sigan_no_error("Your name is Sejuty")
assert_en_to_sigan_no_error("His voice is loud")


# ════════════════════════════════════════════════════════════════════════════
# 4.  ROUND-TRIPS  (English → Sigan → English)
# ════════════════════════════════════════════════════════════════════════════

section("4. Round-trips (E→S→E)")
assert_roundtrip("I see you")
assert_roundtrip("I love you")
assert_roundtrip("I eat the food")
assert_roundtrip("I speak the word")
assert_roundtrip("I read the word")
assert_roundtrip("I want the food")
assert_roundtrip("I am well")
assert_roundtrip("I saw you")
assert_roundtrip("I was seeing you")
assert_roundtrip("I will see you")
assert_roundtrip("I will be seeing you")
assert_roundtrip("I do not speak")
assert_roundtrip("I do not see you")


# ════════════════════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════════════════════

total   = len(results)
passed  = sum(1 for r in results if r.passed)
failed  = total - passed

print(f"\n{BOLD}{'═'*60}{RESET}")
print(f"{BOLD}  Results: {GREEN}{passed} passed{RESET}{BOLD}  /  {RED}{failed} failed{RESET}{BOLD}  /  {total} total{RESET}")
print(f"{BOLD}{'═'*60}{RESET}")

if failed:
    print(f"\n{RED}{BOLD}Failed tests:{RESET}")
    for r in results:
        if not r.passed:
            print(f"  {RED}✗  {r.name}{RESET}")
            if r.detail:
                print(f"       {DIM}{r.detail}{RESET}")

sys.exit(0 if failed == 0 else 1)
