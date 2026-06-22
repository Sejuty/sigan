"""
Sigan lexicon and English translation tables.
Add new words here; validator and translator pick them up automatically.
"""

# ---------------------------------------------------------------------------
# Sigan → POS  (word → tag)
# ---------------------------------------------------------------------------

LEXICON: dict[str, str] = {
    # --- Core nouns (singular) ---
    "laeva": "N",   "nirela": "N",  "thoevi": "N",  "thore": "N",
    "silvao": "N",  "viroela": "N", "taelo": "N",   "mirae": "N",
    "savori": "N",  "aelura": "N",  "nalvae": "N",  "sorivi": "N",
    "talvore": "N", "voriva": "N",  "veldae": "N",  "nirvae": "N",
    # --- Core nouns (plural) ---
    "laevan": "N",   "nirelan": "N",  "thoevin": "N",  "thoren": "N",
    "silvaon": "N",  "viroelan": "N", "taelon": "N",   "miraen": "N",
    "savorin": "N",  "aeluran": "N",  "nalvaen": "N",  "sorivin": "N",
    "talvoren": "N", "vorivan": "N",  "veldaen": "N",  "nirvaen": "N",
    # --- Body parts (singular / plural) ---
    "delva": "N",   "delvan": "N",     # head
    "orilu": "N",   "orilun": "N",     # eye
    "thilvo": "N",  "thilvon": "N",    # mouth
    "silno": "N",   "silnon": "N",     # nose
    "nalvore": "N", "nalvoren": "N",   # arm
    "lorve": "N",   "lorven": "N",     # leg
    "thivore": "N", "thivoren": "N",   # foot
    "aelvo": "N",   "aelvon": "N",     # heart
    "serva": "N",   "servan": "N",     # stomach
    "thelvae": "N", "thelvaen": "N",   # chest
    "dorvae": "N",  "dorvaen": "N",    # back
    "velsae": "N",  "velsaen": "N",    # skin
    # --- Nature & environment (singular / plural) ---
    "laevori": "N", "laevorin": "N",   # sky
    "milore": "N",  "miloren": "N",    # wind
    "norvi": "N",   "norvin": "N",     # earth / ground
    "silvori": "N", "silvorin": "N",   # rain
    "sorvia": "N",  "sorvian": "N",    # snow
    "lorvilo": "N", "lorvilon": "N",   # cloud
    "morvilo": "N", "morvilon": "N",   # night
    "norivia": "N", "norivian": "N",   # day
    "aelvori": "N", "aelvorin": "N",   # star
    "thelori": "N", "thelorin": "N",   # sea
    "nilora": "N",  "niloran": "N",    # valley
    "mirvalo": "N", "mirvalon": "N",   # dust
    "talvori": "N", "talvorin": "N",   # rock
    "selori": "N",  "selorin": "N",    # sand
    "vaelori": "N", "vaeorin": "N",    # forest  (vaelori + n → vaelorin, display as vaeorin)
    "alorvi": "N",  "alorvin": "N",    # field
    # --- Abstract concepts (singular / plural) ---
    "tilovi": "N",  "tilovin": "N",    # time
    "valori": "N",  "valorin": "N",    # truth
    "alorivi": "N", "alorivin": "N",   # life
    "morive": "N",  "moriven": "N",    # death
    "torvi": "N",   "torvin": "N",     # power
    "alavori": "N", "alavorin": "N",   # knowledge
    "saevori": "N", "saevorin": "N",   # faith
    "rilova": "N",  "rilovan": "N",    # justice
    "dalvori": "N", "dalvorin": "N",   # duty
    "mirovi": "N",  "mirovin": "N",    # secret
    "elvorae": "N", "elvoraen": "N",   # dream
    "milorvi": "N", "milorvin": "N",   # memory
    # --- Social & relational (singular / plural) ---
    "selvori": "N", "selvorin": "N",   # family
    "vaelova": "N", "vaelovan": "N",   # friend
    "narovi": "N",  "narovin": "N",    # enemy
    "thalvori": "N","thalvorin": "N",  # leader
    "solori": "N",  "solorin": "N",    # community
    "lorivae": "N", "lorivaen": "N",   # guest
    "vilorae": "N", "viloraen": "N",   # voice
    "aelova": "N",  "aelovan": "N",    # name
    "ralovi": "N",  "ralovin": "N",    # law
    "terovi": "N",  "terovin": "N",    # war
    "paelovi": "N", "paelovin": "N",   # peace (accord)
    "tilorvae": "N","tilorvaen": "N",  # gift
    # --- Emotion nouns (singular / plural) ---
    "glorvi": "N",  "glorvin": "N",    # joy
    "sorovi": "N",  "sorovin": "N",    # sorrow
    "nerovi": "N",  "nerovin": "N",    # anger
    "drelovi": "N", "drelovin": "N",   # fear
    "elorvi": "N",  "elorvin": "N",    # love
    "narvori": "N", "narvorin": "N",   # hate
    "saelvori": "N","saelvorin": "N",  # shame
    "silvovi": "N", "silvovin": "N",   # peace (inner)
    "kalorvi": "N", "kalorvin": "N",   # loneliness
    "gloraevi": "N","gloraevin": "N",  # happiness
    "sorvori": "N", "sorvorin": "N",   # grief
    "velorvi": "N", "velorvin": "N",   # pride
    "naevori": "N", "naevorin": "N",   # envy
    "relorvi": "N", "relorvin": "N",   # regret
    "lorivi": "N",  "lorivin": "N",    # hope (noun)
    "thelvovi": "N","thelvovin": "N",  # trust (noun)
    "talorvae": "N","talorvaen": "N",  # courage
    "daelovi": "N", "daeolovin": "N",  # doubt
    "nilorvae": "N","nilorvaen": "N",  # wonder / awe
    "aelvorae": "N","aelvoraen": "N",  # comfort
    "velnostu": "N","velnostun": "N",  # longing / nostalgia
    # --- Core verb stems ---
    "velor": "V",   "anirel": "V",  "luvar": "V",   "thaevel": "V",
    "mirel": "V",   "savorel": "V", "toravel": "V", "seluvar": "V",
    "laemir": "V",  "orivel": "V",  "felavar": "V", "alavar": "V",
    "morivel": "V",
    # --- Copula & motion ---
    "aevil": "V",    # to be
    "lorel": "V",    # to go
    "silvonor": "V", # to silence / be silent
    # --- Communication verbs ---
    "selvir": "V",    # ask
    "thorivel": "V",  # answer
    "aurinel": "V",   # hear
    "lireval": "V",   # read
    "silavel": "V",   # write
    "aelovel": "V",   # sing
    "virael": "V",    # shout
    "solivar": "V",   # whisper
    # --- Motion verbs ---
    "talovel": "V",   # run
    "vilanor": "V",   # jump
    "aeravel": "V",   # return
    "anavor": "V",    # enter
    "laevoran": "V",  # leave
    "solovar": "V",   # climb
    "luvorn": "V",    # fall
    "arivel": "V",    # throw
    "telavar": "V",   # push
    "oravel": "V",    # pull
    # --- Mental verbs ---
    "aethivar": "V",  # think
    "elorivan": "V",  # remember
    "falovel": "V",   # forget
    "vaethirel": "V", # believe
    "selavor": "V",   # want
    "thilovar": "V",  # choose
    "alviran": "V",   # plan
    "ilovaen": "V",   # imagine
    # --- Emotion verbs ---
    "elavar": "V",    # love (to love)
    "narivan": "V",   # hate (to hate)
    "drelovar": "V",  # fear (to fear)
    "elarovel": "V",  # rejoice
    "sorviran": "V",  # mourn
    "lorivir": "V",   # hope (to hope)
    "vaelavar": "V",  # trust (to trust)
    # --- Social & physical verbs ---
    "alivor": "V",    # help
    "teravel": "V",   # fight
    "saliver": "V",   # rule
    "velavan": "V",   # trade
    "olivaen": "V",   # share
    "loravan": "V",   # join
    "alvorel": "V",   # make / create
    "tiravel": "V",   # break
    "nalavar": "V",   # fix / repair
    "aeluvar": "V",   # open
    "naoluvar": "V",  # close
    # --- Prepositions ---
    "vil": "P",  "mira": "P",  "ana": "P",  "leva": "P",
    "thael": "P", "ori": "P",
    # --- Determiners ---
    "al": "Det", "elo": "Det",
    # --- Time words ---
    "salom": "T",   "verom": "T",   "norelom": "T",
    "aevorom": "T", "navorom": "T", "eluvom": "T",
    # --- Question words ---
    "sivael": "QN", "tavael": "QN", "lorvael": "QN",
    "morvael": "QN", "alvael": "QN",
    # --- Pronouns (singular / plural) ---
    "elva": "Pron", "sova": "Pron", "thira": "Pron",
    "elvan": "Pron", "sovan": "Pron", "thiran": "Pron",
    # --- Possessives ---
    "elvanar": "PossN", "sovanar": "PossN", "thiranar": "PossN",
    "elvanen": "PossN", "sovanen": "PossN", "thiranen": "PossN",
    # --- Copula & basic motion (already above) ---
    # --- Locatives ---
    "ilra": "Loc",   # here
    "ulra": "Loc",   # there
    # --- How question word (already above in QN) ---
    # --- Greetings ---
    "laevel": "Greet",  # hello
    "sorvael": "Greet", # goodbye
    # --- State adjective ---
    "saeril": "Adj",    # well / fine
    # --- Adjectives (core) ---
    "loravil": "Adj",   # big
    "velasil": "Adj",   # old
    "mornivil": "Adj",  # dark
    "talomil": "Adj",   # fast / swift
    "elovil": "Adj",    # small
    "sorvil": "Adj",    # cold
    "theravil": "Adj",  # strong
    "thoelvil": "Adj",  # wet
    # --- Size & shape adjectives ---
    "laeronil": "Adj",  # long
    "nilorvil": "Adj",  # short
    "voravil": "Adj",   # round
    "thorivil": "Adj",  # deep
    "velravil": "Adj",  # wide
    "narovil": "Adj",   # narrow
    "thalvil": "Adj",   # tall
    "selorvil": "Adj",  # flat
    # --- Sensory adjectives ---
    "nirvil": "Adj",    # hot
    "aelorvil": "Adj",  # bright
    "lorovil": "Adj",   # loud
    "saelvil": "Adj",   # sharp
    "milorvil": "Adj",  # dull / blunt
    "silvorvil": "Adj", # smooth
    "norivil": "Adj",   # rough
    # --- Evaluative adjectives ---
    "aelanil": "Adj",   # good
    "naranil": "Adj",   # bad
    "elvanil": "Adj",   # new
    "valoril": "Adj",   # true
    "nalovil": "Adj",   # false
    "aelvoril": "Adj",  # holy
    "veloril": "Adj",   # wise
    "naelvoril": "Adj", # foolish
    "thalvoril": "Adj", # noble
    # --- Emotion adjectives ---
    "glorvil": "Adj",   # joyful
    "sorovil": "Adj",   # sorrowful
    "nerovil": "Adj",   # angry
    "drelovil": "Adj",  # fearful
    "elorvil": "Adj",   # loving
    "narvorvil": "Adj", # hateful
    "kalovil": "Adj",   # lonely
    "gloraevil": "Adj", # glad / happy
    "sorvovil": "Adj",  # grieving
    "lorivil": "Adj",   # hopeful
    "talorvil": "Adj",  # courageous
    "naevovil": "Adj",  # doubtful
    "velovil": "Adj",   # proud
    # --- Closed class ---
    "nael": "Neg",
    "lauvivar": "CAUS_V",
    "avar": "VOC",
}

# Verb stems (uninflected) — derived automatically, used during suffix stripping
VERB_STEMS: set[str] = {w for w, pos in LEXICON.items() if pos == "V"}

# ---------------------------------------------------------------------------
# English surface forms for Sigan verb stems
# stem → (base_form, progressive_form)
# ---------------------------------------------------------------------------

VERB_EN: dict[str, tuple[str, str]] = {
    # Core
    "velor":    ("see",       "seeing"),
    "anirel":   ("give",      "giving"),
    "luvar":    ("carry",     "carrying"),
    "thaevel":  ("speak",     "speaking"),
    "mirel":    ("walk",      "walking"),
    "savorel":  ("eat",       "eating"),
    "toravel":  ("build",     "building"),
    "seluvar":  ("find",      "finding"),
    "laemir":   ("rest",      "resting"),
    "orivel":   ("follow",    "following"),
    "felavar":  ("hold",      "holding"),
    "alavar":   ("know",      "knowing"),
    "morivel":  ("die",       "dying"),
    "lauvivar": ("cause",     "causing"),
    # Copula & motion
    "aevil":    ("be",        "being"),
    "lorel":    ("go",        "going"),
    "silvonor": ("silence",   "silencing"),
    # Communication
    "selvir":   ("ask",       "asking"),
    "thorivel": ("answer",    "answering"),
    "aurinel":  ("hear",      "hearing"),
    "lireval":  ("read",      "reading"),
    "silavel":  ("write",     "writing"),
    "aelovel":  ("sing",      "singing"),
    "virael":   ("shout",     "shouting"),
    "solivar":  ("whisper",   "whispering"),
    # Motion
    "talovel":  ("run",       "running"),
    "vilanor":  ("jump",      "jumping"),
    "aeravel":  ("return",    "returning"),
    "anavor":   ("enter",     "entering"),
    "laevoran": ("leave",     "leaving"),
    "solovar":  ("climb",     "climbing"),
    "luvorn":   ("fall",      "falling"),
    "arivel":   ("throw",     "throwing"),
    "telavar":  ("push",      "pushing"),
    "oravel":   ("pull",      "pulling"),
    # Mental
    "aethivar": ("think",     "thinking"),
    "elorivan": ("remember",  "remembering"),
    "falovel":  ("forget",    "forgetting"),
    "vaethirel":("believe",   "believing"),
    "selavor":  ("want",      "wanting"),
    "thilovar": ("choose",    "choosing"),
    "alviran":  ("plan",      "planning"),
    "ilovaen":  ("imagine",   "imagining"),
    # Emotion
    "elavar":   ("love",      "loving"),
    "narivan":  ("hate",      "hating"),
    "drelovar": ("fear",      "fearing"),
    "elarovel": ("rejoice",   "rejoicing"),
    "sorviran": ("mourn",     "mourning"),
    "lorivir":  ("hope",      "hoping"),
    "vaelavar": ("trust",     "trusting"),
    # Social & physical
    "alivor":   ("help",      "helping"),
    "teravel":  ("fight",     "fighting"),
    "saliver":  ("rule",      "ruling"),
    "velavan":  ("trade",     "trading"),
    "olivaen":  ("share",     "sharing"),
    "loravan":  ("join",      "joining"),
    "alvorel":  ("make",      "making"),
    "tiravel":  ("break",     "breaking"),
    "nalavar":  ("fix",       "fixing"),
    "aeluvar":  ("open",      "opening"),
    "naoluvar": ("close",     "closing"),
}

# ---------------------------------------------------------------------------
# Irregular past simple:  base → past
# ---------------------------------------------------------------------------

PAST_SIMPLE: dict[str, str] = {
    "see": "saw", "give": "gave", "carry": "carried", "speak": "spoke",
    "walk": "walked", "eat": "ate", "build": "built", "find": "found",
    "rest": "rested", "follow": "followed", "hold": "held", "know": "knew",
    "die": "died", "cause": "caused",
    "ask": "asked", "answer": "answered", "hear": "heard", "read": "read",
    "write": "wrote", "sing": "sang", "shout": "shouted", "whisper": "whispered",
    "run": "ran", "jump": "jumped", "return": "returned", "enter": "entered",
    "leave": "left", "climb": "climbed", "fall": "fell", "throw": "threw",
    "push": "pushed", "pull": "pulled",
    "think": "thought", "remember": "remembered", "forget": "forgot",
    "believe": "believed", "want": "wanted", "choose": "chose",
    "plan": "planned", "imagine": "imagined",
    "love": "loved", "hate": "hated", "fear": "feared", "rejoice": "rejoiced",
    "mourn": "mourned", "hope": "hoped", "trust": "trusted",
    "help": "helped", "fight": "fought", "rule": "ruled", "trade": "traded",
    "share": "shared", "join": "joined", "make": "made", "break": "broke",
    "fix": "fixed", "open": "opened", "close": "closed",
    "be": "was", "go": "went", "silence": "silenced",
}

# ---------------------------------------------------------------------------
# Past participle:  base → participle
# ---------------------------------------------------------------------------

PAST_PARTICIPLE: dict[str, str] = {
    "see": "seen", "give": "given", "carry": "carried", "speak": "spoken",
    "walk": "walked", "eat": "eaten", "build": "built", "find": "found",
    "rest": "rested", "follow": "followed", "hold": "held", "know": "known",
    "die": "died", "cause": "caused",
    "ask": "asked", "answer": "answered", "hear": "heard", "read": "read",
    "write": "written", "sing": "sung", "shout": "shouted", "whisper": "whispered",
    "run": "run", "jump": "jumped", "return": "returned", "enter": "entered",
    "leave": "left", "climb": "climbed", "fall": "fallen", "throw": "thrown",
    "push": "pushed", "pull": "pulled",
    "think": "thought", "remember": "remembered", "forget": "forgotten",
    "believe": "believed", "want": "wanted", "choose": "chosen",
    "plan": "planned", "imagine": "imagined",
    "love": "loved", "hate": "hated", "fear": "feared", "rejoice": "rejoiced",
    "mourn": "mourned", "hope": "hoped", "trust": "trusted",
    "help": "helped", "fight": "fought", "rule": "ruled", "trade": "traded",
    "share": "shared", "join": "joined", "make": "made", "break": "broken",
    "fix": "fixed", "open": "opened", "close": "closed",
    "be": "been", "go": "gone", "silence": "silenced",
}

# ---------------------------------------------------------------------------
# Sigan → English translation tables
# ---------------------------------------------------------------------------

NOUN_EN: dict[str, str] = {
    # Core
    "laeva": "person",   "laevan": "people",
    "nirela": "child",   "nirelan": "children",
    "thoevi": "water",   "thoevin": "waters",
    "thore": "stone",    "thoren": "stones",
    "silvao": "tree",    "silvaon": "trees",
    "viroela": "bird",   "viroelan": "birds",
    "taelo": "house",    "taelon": "houses",
    "mirae": "path",     "miraen": "paths",
    "savori": "food",    "savorin": "foods",
    "aelura": "sun",     "aeluran": "suns",
    "nalvae": "hand",    "nalvaen": "hands",
    "sorivi": "river",   "sorivin": "rivers",
    "talvore": "mountain","talvoren": "mountains",
    "voriva": "word",    "vorivan": "words",
    "veldae": "animal",  "veldaen": "animals",
    "nirvae": "fire",    "nirvaen": "fires",
    # Body parts
    "delva": "head",     "delvan": "heads",
    "orilu": "eye",      "orilun": "eyes",
    "thilvo": "mouth",   "thilvon": "mouths",
    "silno": "nose",     "silnon": "noses",
    "nalvore": "arm",    "nalvoren": "arms",
    "lorve": "leg",      "lorven": "legs",
    "thivore": "foot",   "thivoren": "feet",
    "aelvo": "heart",    "aelvon": "hearts",
    "serva": "stomach",  "servan": "stomachs",
    "thelvae": "chest",  "thelvaen": "chests",
    "dorvae": "back",    "dorvaen": "backs",
    "velsae": "skin",    "velsaen": "skins",
    # Nature
    "laevori": "sky",    "laevorin": "skies",
    "milore": "wind",    "miloren": "winds",
    "norvi": "earth",    "norvin": "earths",
    "silvori": "rain",   "silvorin": "rains",
    "sorvia": "snow",    "sorvian": "snows",
    "lorvilo": "cloud",  "lorvilon": "clouds",
    "morvilo": "night",  "morvilon": "nights",
    "norivia": "day",    "norivian": "days",
    "aelvori": "star",   "aelvorin": "stars",
    "thelori": "sea",    "thelorin": "seas",
    "nilora": "valley",  "niloran": "valleys",
    "mirvalo": "dust",   "mirvalon": "dusts",
    "talvori": "rock",   "talvorin": "rocks",
    "selori": "sand",    "selorin": "sands",
    "vaelori": "forest", "vaeorin": "forests",
    "alorvi": "field",   "alorvin": "fields",
    # Abstract
    "tilovi": "time",       "tilovin": "times",
    "valori": "truth",      "valorin": "truths",
    "alorivi": "life",      "alorivin": "lives",
    "morive": "death",      "moriven": "deaths",
    "torvi": "power",       "torvin": "powers",
    "alavori": "knowledge", "alavorin": "knowledges",
    "saevori": "faith",     "saevorin": "faiths",
    "rilova": "justice",    "rilovan": "justices",
    "dalvori": "duty",      "dalvorin": "duties",
    "mirovi": "secret",     "mirovin": "secrets",
    "elvorae": "dream",     "elvoraen": "dreams",
    "milorvi": "memory",    "milorvin": "memories",
    # Social
    "selvori": "family",    "selvorin": "families",
    "vaelova": "friend",    "vaelovan": "friends",
    "narovi": "enemy",      "narovin": "enemies",
    "thalvori": "leader",   "thalvorin": "leaders",
    "solori": "community",  "solorin": "communities",
    "lorivae": "guest",     "lorivaen": "guests",
    "vilorae": "voice",     "viloraen": "voices",
    "aelova": "name",       "aelovan": "names",
    "ralovi": "law",        "ralovin": "laws",
    "terovi": "war",        "terovin": "wars",
    "paelovi": "accord",    "paelovin": "accords",
    "tilorvae": "gift",     "tilorvaen": "gifts",
    # Emotion nouns
    "glorvi": "joy",        "glorvin": "joys",
    "sorovi": "sorrow",     "sorovin": "sorrows",
    "nerovi": "anger",      "nerovin": "angers",
    "drelovi": "fear",      "drelovin": "fears",
    "elorvi": "love",       "elorvin": "loves",
    "narvori": "hate",      "narvorin": "hates",
    "saelvori": "shame",    "saelvorin": "shames",
    "silvovi": "peace",     "silvovin": "peaces",
    "kalorvi": "loneliness","kalorvin": "lonelinesses",
    "gloraevi": "happiness","gloraevin": "happinesses",
    "sorvori": "grief",     "sorvorin": "griefs",
    "velorvi": "pride",     "velorvin": "prides",
    "naevori": "envy",      "naevorin": "envies",
    "relorvi": "regret",    "relorvin": "regrets",
    "lorivi": "hope",       "lorivin": "hopes",
    "thelvovi": "trust",    "thelvovin": "trusts",
    "talorvae": "courage",  "talorvaen": "courages",
    "daelovi": "doubt",     "daeolovin": "doubts",
    "nilorvae": "wonder",   "nilorvaen": "wonders",
    "aelvorae": "comfort",  "aelvoraen": "comforts",
    "velnostu": "longing",  "velnostun": "longings",
}

PRON_EN: dict[str, str] = {
    "elva": "I",   "sova": "you", "thira": "he",
    "elvan": "we", "sovan": "you", "thiran": "they",
}

PRON_OBJ_EN: dict[str, str] = {
    "elva": "me",  "sova": "you", "thira": "him",
    "elvan": "us", "sovan": "you", "thiran": "them",
}

POSS_EN: dict[str, str] = {
    "elvanar": "my",    "sovanar": "your",  "thiranar": "his/her/its",
    "elvanen": "our",   "sovanen": "your",  "thiranen": "their",
}

DET_EN: dict[str, str] = {"al": "the", "elo": "a"}

ADJ_EN: dict[str, str] = {
    # Core
    "loravil": "big",     "velasil": "old",     "mornivil": "dark",
    "talomil": "fast",    "elovil": "small",    "sorvil": "cold",
    "theravil": "strong", "thoelvil": "wet",
    # Size & shape
    "laeronil": "long",   "nilorvil": "short",  "voravil": "round",
    "thorivil": "deep",   "velravil": "wide",   "narovil": "narrow",
    "thalvil": "tall",    "selorvil": "flat",
    # Sensory
    "nirvil": "hot",      "aelorvil": "bright", "lorovil": "loud",
    "saelvil": "sharp",   "milorvil": "dull",   "silvorvil": "smooth",
    "norivil": "rough",
    # Evaluative
    "aelanil": "good",    "naranil": "bad",     "elvanil": "new",
    "valoril": "true",    "nalovil": "false",   "aelvoril": "holy",
    "veloril": "wise",    "naelvoril": "foolish","thalvoril": "noble",
    # Emotion
    "glorvil": "joyful",  "sorovil": "sorrowful","nerovil": "angry",
    "drelovil": "fearful","elorvil": "loving",  "narvorvil": "hateful",
    "kalovil": "lonely",  "gloraevil": "happy", "sorvovil": "grieving",
    "lorivil": "hopeful", "talorvil": "courageous","naevovil": "doubtful",
    "velovil": "proud",
    # State
    "saeril": "well",
}

PREP_EN: dict[str, str] = {
    "vil": "to",  "mira": "from", "ana": "in",
    "leva": "with", "thael": "about", "ori": "for",
}

TIME_EN: dict[str, str] = {
    "salom": "now",       "verom": "yesterday", "norelom": "tomorrow",
    "aevorom": "always",  "navorom": "never",   "eluvom": "once",
}

QN_EN: dict[str, str] = {
    "sivael": "who", "tavael": "what", "lorvael": "where",
    "morvael": "when", "alvael": "how",
}

LOC_EN: dict[str, str] = {
    "ilra": "here",
    "ulra": "there",
}

GREET_EN: dict[str, str] = {
    "laevel": "hello",
    "sorvael": "goodbye",
}
