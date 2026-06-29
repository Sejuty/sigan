"""
Second comprehensive test suite — covers gaps from test_suite.py:
  prepositions, time words, all question words, irregular pasts,
  object pronouns, plural subjects, habitual aspect, all possessives,
  E→S irregular verbs, round-trips for new patterns, more invalid sentences.

Run: python3 test_suite_2.py
"""

import sys
import traceback
from validator import validate
from translator import sigan_to_english, english_to_sigan

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

results: list[tuple[bool, str, str]] = []

def _record(passed: bool, label: str, detail: str = "") -> bool:
    results.append((passed, label, detail))
    icon = f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"
    print(f"  {icon}  {label}")
    if not passed:
        print(f"       {RED}{detail}{RESET}")
    return passed

def assert_valid(s, note=""):
    label = f"[VALID] {s}" + (f"  ({note})" if note else "")
    try:
        r = validate(s)
        return _record(r["valid"], label, f"Expected valid; errors: {r['errors']}")
    except Exception as e:
        return _record(False, label, f"Exception: {e}")

def assert_invalid(s, note=""):
    label = f"[INVALID] {s}" + (f"  ({note})" if note else "")
    try:
        r = validate(s)
        return _record(not r["valid"], label, "Expected invalid but was accepted")
    except Exception as e:
        return _record(False, label, f"Exception: {e}")

def s2e(sigan: str, expected: str):
    label = f"[S→E] {sigan!r}"
    try:
        r = sigan_to_english(sigan)
        if not r["success"]:
            return _record(False, label, f"Failed: {r['error']}")
        ok = r["english"].lower() == expected.lower()
        return _record(ok, label, f"Expected {expected!r}, got {r['english']!r}")
    except Exception as e:
        return _record(False, label, f"Exception: {e}\n{traceback.format_exc()}")

def e2s(english: str, expected: str):
    label = f"[E→S] {english!r}"
    try:
        r = english_to_sigan(english)
        if not r["success"]:
            return _record(False, label, f"Failed: {r['error']}")
        ok = r["sigan"].lower() == expected.lower()
        return _record(ok, label, f"Expected {expected!r}, got {r['sigan']!r}")
    except Exception as e:
        return _record(False, label, f"Exception: {e}\n{traceback.format_exc()}")

def roundtrip(english: str):
    label = f"[RT] {english!r}"
    try:
        r1 = english_to_sigan(english)
        if not r1["success"]:
            return _record(False, label, f"E→S failed: {r1['error']}")
        r2 = sigan_to_english(r1["sigan"])
        if not r2["success"]:
            return _record(False, label, f"S→E failed on '{r1['sigan']}': {r2['error']}")
        ok = r2["english"].lower() == english.lower()
        return _record(ok, label, f"E→S→E: {english!r}→{r1['sigan']!r}→{r2['english']!r}")
    except Exception as e:
        return _record(False, label, f"Exception: {e}")

def section(title):
    print(f"\n{BOLD}{CYAN}{'─'*62}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*62}{RESET}")


# ════════════════════════════════════════════════════════════════
# A.  PREPOSITION PHRASES — validation & S→E
# ════════════════════════════════════════════════════════════════

section("A. Prepositional phrases — all 6 prepositions")

# Validation
assert_valid("elva lorel vil al taelo",       "go to the house")
assert_valid("elva lorel mira al norvi",      "go from the earth")
assert_valid("elva thaevel ana al taelo",     "speak in the house")
assert_valid("elva thaevel leva sova",        "speak with you")
assert_valid("elva thaevel thael al valori",  "speak about the truth")
assert_valid("elva velor ori sova",           "see for you")

# Translation
s2e("elva lorel vil al taelo",       "I go to the house")
s2e("elva lorel mira al norvi",      "I go from the earth")
s2e("elva thaevel ana al taelo",     "I speak in the house")
s2e("elva thaevel leva sova",        "I speak with you")
s2e("elva thaevel thael al valori",  "I speak about the truth")
s2e("elva velor ori sova",           "I see for you")

# E→S
e2s("I go to the house",             "elva lorel vil al taelo")
e2s("I speak with you",              "elva thaevel leva sova")


# ════════════════════════════════════════════════════════════════
# B.  TIME WORDS — all 6 adverbs
# ════════════════════════════════════════════════════════════════

section("B. Time words — all 6 (salom/verom/norelom/aevorom/navorom/eluvom)")

assert_valid("elva velor sova salom",    "now")
assert_valid("elva velor sova aevorom",  "always")
assert_valid("elva velor sova navorom",  "never")
assert_valid("elva velor sova eluvom",   "once")

s2e("elva velor sova salom",    "I see you now")
s2e("elva velor sova verom",    "I see you yesterday")
s2e("elva velor sova norelom",  "I see you tomorrow")
s2e("elva velor sova aevorom",  "I see you always")
s2e("elva velor sova navorom",  "I see you never")
s2e("elva velor sova eluvom",   "I see you once")

e2s("I see you always",  "elva velor sova aevorom")
e2s("I see you now",     "elva velor sova salom")


# ════════════════════════════════════════════════════════════════
# C.  QUESTION WORDS — all 5
# ════════════════════════════════════════════════════════════════

section("C. Question words — all 5 (sivael/tavael/lorvael/morvael/alvael)")

assert_valid("sivael velor sova",   "who")
assert_valid("tavael velor sova",   "what")
assert_valid("lorvael velor sova",  "where")
assert_valid("morvael velor sova",  "when")
assert_valid("alvael aevil sova",   "how (are you?)")

s2e("sivael velor sova",  "Who sees you?")
s2e("tavael velor sova",  "What sees you?")
s2e("alvael aevil sova",  "How are you?")


# ════════════════════════════════════════════════════════════════
# D.  IRREGULAR PASTS — S→E
# ════════════════════════════════════════════════════════════════

section("D. Irregular past forms — S→E")

# anirel (give) → gave
s2e("elva anirelov sova",           "I gave you")
# savorel (eat) → ate
s2e("elva savorelov al savori",     "I ate the food")
# alavar (know) → knew
s2e("elva alavarov al valori",      "I knew the truth")
# lorel (go) → went
s2e("elva lorelov",                 "I went")
# luvorn (fall) → fell
s2e("elva luvornov ilra",           "I fell here")
# morivel (die) → died
s2e("elva morivelov",               "I died")
# velor (see) → saw (already in suite 1 — re-verify)
s2e("elva velorov sova",            "I saw you")
# aelovel (sing) → sang
s2e("elva aelovelov al vilorae",    "I sang the voice")
# luvar (carry) → carried
s2e("elva luvarov al laeva",        "I carried the person")
# felavar (hold) → held
s2e("elva felavarov al laeva",      "I held the person")


# ════════════════════════════════════════════════════════════════
# E.  OBJECT PRONOUNS — all 6 in object position (S→E)
# ════════════════════════════════════════════════════════════════

section("E. Object pronouns — all 6 (me/you/him/us/you-pl/them)")

s2e("sova velor elva",    "You see me")
s2e("thira velor sova",   "He sees you")
s2e("elva velor thira",   "I see him")
s2e("elva velor elvan",   "I see us")
s2e("elva velor sovan",   "I see you")
s2e("elva velor thiran",  "I see them")


# ════════════════════════════════════════════════════════════════
# F.  PLURAL & ALL-PRONOUN SUBJECT AGREEMENT (S→E)
# ════════════════════════════════════════════════════════════════

section("F. Subject-verb agreement — all 6 subjects")

# 1st singular
s2e("elva velor sova",    "I see you")
# 2nd singular
s2e("sova velor elva",    "You see me")
# 3rd singular — must get -s on verb
s2e("thira velor sova",   "He sees you")
s2e("thira savorel al savori", "He eats the food")
# 1st plural
s2e("elvan velor sova",   "We see you")
# 3rd plural — no -s
s2e("thiran velor sova",  "They see you")
# "were" agreement for past continuous plural
s2e("elvan velorovrak sova", "We were seeing you")
# "have" for present completed plural
s2e("elvan velordor sova",   "We have seen you")
# "am" for I + present continuous
s2e("elva velorrak sova",    "I am seeing you")
# "is" for he + present continuous
s2e("thira velorrak sova",   "He is seeing you")
# "are" for we + present continuous
s2e("elvan velorrak sova",   "We are seeing you")


# ════════════════════════════════════════════════════════════════
# G.  HABITUAL ASPECT — all 4 (present/past × both verbs)
# ════════════════════════════════════════════════════════════════

section("G. Habitual aspect")

assert_valid("elva velorzun sova",     "present habitual")
assert_valid("elva velorovzun sova",   "past habitual")
assert_valid("elva velorenzun sova",   "future habitual")

s2e("elva velorzun sova",     "I usually see you")
s2e("elva velorovzun sova",   "I used to see you")
s2e("elva mirelzun al mirae", "I usually walk the path")

e2s("I usually see you",      "elva velorzun sova")
e2s("I used to see you",      "elva velorovzun sova")


# ════════════════════════════════════════════════════════════════
# H.  ALL POSSESSIVE FORMS — validation & S→E
# ════════════════════════════════════════════════════════════════

section("H. All 6 possessive forms")

assert_valid("elva velor elvanar laeva",   "my person")
assert_valid("elva velor sovanar laeva",   "your person")
assert_valid("elva velor thiranar laeva",  "his/her person")
assert_valid("elva velor elvanen laeva",   "our person")
assert_valid("elva velor sovanen laeva",   "your-pl person")
assert_valid("elva velor thiranen laeva",  "their person")

s2e("elva velor elvanar laeva",   "I see my person")
s2e("elva velor sovanar laeva",   "I see your person")
s2e("elva velor thiranar laeva",  "I see his/her/its person")
s2e("elva velor elvanen laeva",   "I see our person")
s2e("elva velor sovanen laeva",   "I see your person")
s2e("elva velor thiranen laeva",  "I see their person")

# Possessives as subjects
assert_valid("elvanar laeva velor sova",   "my person sees you")
s2e("elvanar laeva velor sova",   "My person sees you")


# ════════════════════════════════════════════════════════════════
# I.  E→S — irregular verbs & new patterns
# ════════════════════════════════════════════════════════════════

section("I. English→Sigan — irregular pasts & new verbs")

e2s("I gave you",            "elva anirelov sova")
e2s("I ate the food",        "elva savorelov al savori")
e2s("I knew the truth",      "elva alavarov al valori")
e2s("I fell",                "elva luvornov")
e2s("I went",                "elva lorelov")
e2s("I went there",          "elva lorelov ulra")
e2s("I go here",             "elva lorel ilra")
e2s("I go to the house",     "elva lorel vil al taelo")
e2s("I will go there",       "elva lorelen ulra")
e2s("I was seeing you",      "elva velorovrak sova")


# ════════════════════════════════════════════════════════════════
# J.  COPULA — all 6 subject pronouns
# ════════════════════════════════════════════════════════════════

section("J. Copula (aevil) — all 6 pronoun subjects")

s2e("elva aevil saeril",    "I am well")
s2e("sova aevil saeril",    "You are well")
s2e("thira aevil saeril",   "He is well")
s2e("elvan aevil saeril",   "We are well")
s2e("thiran aevil saeril",  "They are well")

e2s("I am well",    "elva aevil saeril")
e2s("You are well", "sova aevil saeril")
e2s("He is well",   "thira aevil saeril")
e2s("We are well",  "elvan aevil saeril")
e2s("They are well","thiran aevil saeril")


# ════════════════════════════════════════════════════════════════
# K.  SUBSET OF UNTESTED VERBS — smoke tests (S→E no-crash)
# ════════════════════════════════════════════════════════════════

section("K. Untested verb stems — S→E smoke tests")

# Maps: Sigan sentence → expected English
verb_smoke = [
    ("elva aelovelov sova",           "I sang you"),           # sing  (aelovel+ov)
    ("elva aurinelov sova",           "I heard you"),           # hear  (aurinel+ov)
    ("elva silavelov al voriva",      "I wrote the word"),      # write (silavel+ov)
    ("elva seluvarov al laeva",       "I found the person"),    # find  (seluvar+ov)
    ("elva felavarov al laeva",       "I held the person"),     # hold  (felavar+ov)
    ("elva alavarov al alavori",      "I knew the knowledge"),  # know  (alavar+ov)
    ("elva alvorel al taelo",         "I make the house"),      # make  (alvorel)
    ("elva tiravelov al taelo",       "I broke the house"),     # break (tiravel+ov)
    ("elva nalavarov al taelo",       "I fixed the house"),     # fix   (nalavar+ov)
    ("elva aeluvarov al taelo",       "I opened the house"),    # open  (aeluvar+ov)
    ("elva naoluvarov al taelo",      "I closed the house"),    # close (naoluvar+ov)
    ("elva talovelov ulra",           "I ran there"),           # run   (talovel+ov)
    ("elva vilanorov ulra",           "I jumped there"),        # jump  (vilanor+ov)
    ("elva selvir sova",              "I ask you"),             # ask   (selvir)
    ("elva alviranov",                "I planned"),             # plan  (alviran+ov)
    ("elva lorivirov",                "I hoped"),               # hope  (lorivir+ov)
    ("elva vaelavarov sova",          "I trusted you"),         # trust (vaelavar+ov)
    ("elva narivanov sova",           "I hated you"),           # hate  (narivan+ov)
]

_FAILED_VERB_SMOKES: list[str] = []
for sigan_sent, expected_en in verb_smoke:
    r = sigan_to_english(sigan_sent)
    ok = r["success"] and r["english"].lower() == expected_en.lower()
    label = f"[VERB] {sigan_sent!r}"
    _record(ok, label,
            f"Expected {expected_en!r}, got {r['english']!r}" if r["success"] else f"Error: {r['error']}")


# ════════════════════════════════════════════════════════════════
# L.  ADDITIONAL INVALID SENTENCES
# ════════════════════════════════════════════════════════════════

section("L. Additional invalid sentences")

# Unknown words
assert_invalid("elva blork sova",          "nonsense verb")
assert_invalid("hello elva velor sova",    "English word in Sigan sentence")
assert_invalid("elva velor sova bonjour",  "French word appended")

# Wrong word order
assert_invalid("sova velor elva sova",     "subj V obj obj (double object pron)")
assert_invalid("al elva velor",            "Det Pron V (wrong order)")
assert_invalid("elva al velor sova",       "Pron Det V Pron")

# Bare nouns / partial phrases
assert_valid("laeva velor",                "N V (bare N subject, intransitive VP — valid in Sigan)")
# NOTE: single-token N alone — NP → N is valid but VP is missing, so should fail
assert_invalid("veldae",                   "bare noun — no verb")

# Lowercase proper noun not in lexicon
assert_invalid("elva aevil sartre",        "lowercase unknown word")

# Suffix with wrong base
assert_invalid("elva velorov blork",       "valid verb + unknown word as object")

# Double negation (not in grammar)
assert_invalid("elva nael nael velor sova","double negation")


# ════════════════════════════════════════════════════════════════
# M.  ROUND-TRIPS — new patterns
# ════════════════════════════════════════════════════════════════

section("M. Round-trips — new patterns")

roundtrip("I gave you")
roundtrip("I ate the food")
roundtrip("I went")
roundtrip("I go here")
roundtrip("I go there")
roundtrip("I will go there")
roundtrip("I am well")
roundtrip("I usually see you")
roundtrip("I used to see you")
roundtrip("I speak with you")
roundtrip("I see you always")
roundtrip("I do not speak")
roundtrip("I will have seen you")


# ════════════════════════════════════════════════════════════════
# N.  DETERMINERS — both (al / elo)
# ════════════════════════════════════════════════════════════════

section("N. Both determiners — al (the) and elo (a)")

assert_valid("elva velor al laeva",    "see the person")
assert_valid("elva velor elo laeva",   "see a person")
assert_valid("elva savorel elo loravil laeva", "eat a big person")

s2e("elva velor al laeva",    "I see the person")
s2e("elva velor elo laeva",   "I see a person")
s2e("elva savorel elo loravil laeva", "I eat a big person")

e2s("I see the person",  "elva velor al laeva")
e2s("I see a person",    "elva velor elo laeva")


# ════════════════════════════════════════════════════════════════
# O.  EDGE CASES & TOKENISATION
# ════════════════════════════════════════════════════════════════

section("O. Edge cases — whitespace, capitalisation, single tokens")

# Extra whitespace should still work (split() handles it)
assert_valid("elva  velor  sova",   "extra spaces")
# Capitalised proper noun mid-sentence
assert_valid("elva aevil Sejuty",   "proper noun as pred")
assert_valid("Sartre velor sova",   "proper noun as subject")
# Single imperative verb
assert_valid("silvonor",            "single-word imperative")
# Single greeting
assert_valid("laevel",              "standalone greeting")
# Very long but valid sentence (PP + T)
assert_valid("elva lorel vil al taelo salom", "V + PP + T")


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
