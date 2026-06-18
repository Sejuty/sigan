"""
Sigan lexicon and English translation tables.
Add new words here; validator and translator pick them up automatically.
"""

# ---------------------------------------------------------------------------
# Sigan → POS  (word → tag)
# ---------------------------------------------------------------------------

LEXICON: dict[str, str] = {
    # --- Core nouns (singular) ---
    "manu": "N", "childa": "N", "watra": "N", "stonu": "N",
    "truku": "N", "burda": "N", "homu": "N", "rotha": "N",
    "fudo": "N", "sunu": "N", "handu": "N", "rivna": "N",
    "mounta": "N", "worda": "N", "besta": "N", "fyru": "N",
    # --- Core nouns (plural) ---
    "manun": "N", "childan": "N", "watran": "N", "stonun": "N",
    "trukun": "N", "burdan": "N", "homun": "N", "rothan": "N",
    "fudon": "N", "sunun": "N", "handun": "N", "rivnan": "N",
    "mountan": "N", "wordan": "N", "bestan": "N", "fyrun": "N",
    # --- Body parts (singular / plural) ---
    "dava": "N", "davan": "N",       # head
    "oku": "N",  "okun": "N",        # eye
    "mova": "N", "movan": "N",       # mouth
    "nasu": "N", "nasun": "N",       # nose
    "braku": "N", "brakun": "N",     # arm
    "legu": "N",  "legun": "N",      # leg
    "fotu": "N",  "fotun": "N",      # foot
    "kordu": "N", "kordun": "N",     # heart
    "ventra": "N", "ventran": "N",   # stomach / belly
    "chesta": "N", "chestan": "N",   # chest
    "doru": "N",  "dorun": "N",      # back
    "skinu": "N", "skinun": "N",     # skin
    # --- Nature & environment (singular / plural) ---
    "skavu": "N",  "skavun": "N",    # sky
    "winda": "N",  "windan": "N",    # wind
    "ertha": "N",  "erthan": "N",    # earth / ground
    "ranu": "N",   "ranun": "N",     # rain
    "snova": "N",  "snovan": "N",    # snow
    "kluda": "N",  "kludan": "N",    # cloud
    "noku": "N",   "nokun": "N",     # night
    "dayo": "N",   "dayon": "N",     # day
    "staru": "N",  "starun": "N",    # star
    "sova": "N",   "sovan": "N",     # sea
    "valu": "N",   "valun": "N",     # valley
    "dusta": "N",  "dustan": "N",    # dust
    "rocha": "N",  "rochan": "N",    # rock (large)
    "sanda": "N",  "sandan": "N",    # sand
    "foresta": "N", "forestan": "N", # forest
    "fielda": "N", "fieldan": "N",   # field
    # --- Abstract concepts (singular / plural) ---
    "tima": "N",   "timan": "N",     # time
    "truta": "N",  "trutan": "N",    # truth
    "lifa": "N",   "lifan": "N",     # life
    "morta": "N",  "mortan": "N",    # death
    "powra": "N",  "powran": "N",    # power
    "knowu": "N",  "knowun": "N",    # knowledge
    "fathu": "N",  "fathun": "N",    # faith / belief
    "ritu": "N",   "ritun": "N",     # right / justice
    "duta": "N",   "dutan": "N",     # duty
    "sekru": "N",  "sekrun": "N",    # secret
    "dreamu": "N", "dreamun": "N",   # dream
    "memorya": "N", "memoryan": "N", # memory
    # --- Social & relational (singular / plural) ---
    "famla": "N",  "famlan": "N",    # family
    "frenda": "N", "френdan": "N",   # friend
    "enemu": "N",  "enemun": "N",    # enemy
    "chefa": "N",  "chefan": "N",    # leader
    "koma": "N",   "koman": "N",     # community / group
    "gesta": "N",  "gestan": "N",    # guest
    "voka": "N",   "vokan": "N",     # voice
    "namu": "N",   "namun": "N",     # name
    "rula": "N",   "rulan": "N",     # rule / law
    "wara": "N",   "waran": "N",     # war
    "paka": "N",   "pakan": "N",     # peace (agreement)
    "giftu": "N",  "giftun": "N",    # gift
    # --- Emotion nouns (singular / plural) ---
    "joya": "N",   "joyan": "N",     # joy
    "soru": "N",   "sorun": "N",     # sorrow
    "ragu": "N",   "ragun": "N",     # anger
    "dreda": "N",  "dredan": "N",    # fear
    "lovu": "N",   "lovun": "N",     # love (noun)
    "hatu": "N",   "hatun": "N",     # hate (noun)
    "shamu": "N",  "shamun": "N",    # shame
    "pisu": "N",   "pisun": "N",     # peace (inner)
    "kalu": "N",   "kalun": "N",     # loneliness
    "glayu": "N",  "glayun": "N",    # happiness / gladness
    "thoru": "N",  "thorun": "N",    # grief
    "ventu": "N",  "ventun": "N",    # pride
    "envu": "N",   "envun": "N",     # envy
    "remu": "N",   "remun": "N",     # regret
    "hopa": "N",   "hopan": "N",     # hope (noun)
    "trusta": "N", "trustan": "N",   # trust (noun)
    "kura": "N",   "kuran": "N",     # courage
    "duba": "N",   "duban": "N",     # doubt
    "wundu": "N",  "wundun": "N",    # wonder / awe
    "komforta": "N", "komfortan": "N", # comfort
    "nostu": "N",  "nostun": "N",    # longing / nostalgia
    # --- Core verb stems ---
    "sigan": "V", "givak": "V", "karyad": "V", "spekor": "V",
    "walkag": "V", "etak": "V", "bildag": "V", "findar": "V",
    "restak": "V", "folur": "V", "holdag": "V", "knowar": "V",
    "dethrak": "V",
    # --- Communication verbs ---
    "askar": "V",    # ask
    "answad": "V",   # answer
    "herad": "V",    # hear
    "ridan": "V",    # read
    "writag": "V",   # write
    "singak": "V",   # sing
    "criyad": "V",   # cry out / shout
    "whispar": "V",  # whisper
    # --- Motion verbs ---
    "runak": "V",    # run
    "jumbad": "V",   # jump
    "retorn": "V",   # return
    "entrak": "V",   # enter
    "leavak": "V",   # leave
    "climbag": "V",  # climb
    "falan": "V",    # fall
    "throwan": "V",  # throw
    "pushak": "V",   # push
    "pulad": "V",    # pull
    # --- Mental verbs ---
    "thinkar": "V",  # think
    "remembrak": "V", # remember
    "forgetak": "V", # forget
    "belivan": "V",  # believe
    "wantak": "V",   # want
    "chosar": "V",   # choose
    "planak": "V",   # plan
    "imagak": "V",   # imagine
    # --- Emotion verbs ---
    "lovak": "V",    # love (to love)
    "hatak": "V",    # hate (to hate)
    "fearan": "V",   # fear (to fear)
    "joyan": "V",    # rejoice
    "mournad": "V",  # mourn
    "hopak": "V",    # hope (to hope)
    "trustad": "V",  # trust (to trust)
    # --- Social & physical verbs ---
    "helpak": "V",   # help
    "figtak": "V",   # fight
    "rulad": "V",    # rule
    "tradak": "V",   # trade
    "sharad": "V",   # share
    "joinak": "V",   # join
    "makad": "V",    # make / create
    "brekan": "V",   # break
    "fixar": "V",    # fix / repair
    "openak": "V",   # open
    "klozad": "V",   # close
    # --- Prepositions ---
    "tov": "P", "from": "P", "nak": "P", "wid": "P",
    "thov": "P", "for": "P",
    # --- Determiners ---
    "gar": "Det", "brath": "Det",
    # --- Time words ---
    "nowom": "T", "yestom": "T", "morom": "T",
    "evrom": "T", "nevrom": "T", "wonsom": "T",
    # --- Core adjectives ---
    "bigrath": "Adj", "oldrath": "Adj", "darkoth": "Adj", "swifth": "Adj",
    "smaloth": "Adj", "koldrith": "Adj", "strongath": "Adj", "wethrakh": "Adj",
    # --- Size & shape adjectives ---
    "longrath": "Adj",   # long
    "shoroth": "Adj",    # short
    "roundath": "Adj",   # round
    "deeprith": "Adj",   # deep
    "widrath": "Adj",    # wide
    "narrath": "Adj",    # narrow
    "talloth": "Adj",    # tall
    "flatrath": "Adj",   # flat
    # --- Sensory adjectives ---
    "hotrath": "Adj",    # hot
    "brightrath": "Adj", # bright
    "loudoth": "Adj",    # loud
    "sharpoth": "Adj",   # sharp
    "dulrith": "Adj",    # dull / blunt
    "smoothath": "Adj",  # smooth
    "roughoth": "Adj",   # rough
    # --- Evaluative adjectives ---
    "godrath": "Adj",    # good
    "badoth": "Adj",     # bad
    "newrath": "Adj",    # new
    "truerath": "Adj",   # true
    "falsoth": "Adj",    # false
    "holyrath": "Adj",   # holy
    "wisrath": "Adj",    # wise
    "fooloth": "Adj",    # foolish
    "noblrath": "Adj",   # noble
    # --- Emotion adjectives ---
    "jorath": "Adj",     # joyful
    "sorath": "Adj",     # sorrowful
    "ragoth": "Adj",     # angry
    "dredath": "Adj",    # fearful
    "lovrath": "Adj",    # loving
    "hatoth": "Adj",     # hateful
    "kalerith": "Adj",   # lonely
    "glayrath": "Adj",   # glad / happy
    "thoroth": "Adj",    # grieving
    "hoprath": "Adj",    # hopeful
    "kurrath": "Adj",    # courageous
    "wundrath": "Adj",   # awestruck
    "duboth": "Adj",     # doubtful
    "venturith": "Adj",  # proud
    # --- Pronouns (singular / plural) ---
    "ayu": "Pron", "yu": "Pron", "hiru": "Pron",
    "ayun": "Pron", "yun": "Pron", "hirun": "Pron",
    # --- Possessives ---
    "ayugar": "PossN", "yugar": "PossN", "hirugar": "PossN",
    "ayungar": "PossN", "yungar": "PossN", "hirungar": "PossN",
    # --- Question words ---
    "huzh": "QN", "wazh": "QN", "werazh": "QN", "wenazh": "QN",
    # --- Closed class ---
    "noth": "Neg",
    "kawzad": "CAUS_V",
    "hey": "VOC",
}

# Verb stems (uninflected) — derived automatically, used during suffix stripping
VERB_STEMS: set[str] = {w for w, pos in LEXICON.items() if pos == "V"}

# ---------------------------------------------------------------------------
# English surface forms for Sigan verb stems
# stem → (base_form, progressive_form)
# ---------------------------------------------------------------------------

VERB_EN: dict[str, tuple[str, str]] = {
    # Core
    "sigan":    ("see",       "seeing"),
    "givak":    ("give",      "giving"),
    "karyad":   ("carry",     "carrying"),
    "spekor":   ("speak",     "speaking"),
    "walkag":   ("walk",      "walking"),
    "etak":     ("eat",       "eating"),
    "bildag":   ("build",     "building"),
    "findar":   ("find",      "finding"),
    "restak":   ("rest",      "resting"),
    "folur":    ("follow",    "following"),
    "holdag":   ("hold",      "holding"),
    "knowar":   ("know",      "knowing"),
    "dethrak":  ("die",       "dying"),
    "kawzad":   ("cause",     "causing"),
    # Communication
    "askar":    ("ask",       "asking"),
    "answad":   ("answer",    "answering"),
    "herad":    ("hear",      "hearing"),
    "ridan":    ("read",      "reading"),
    "writag":   ("write",     "writing"),
    "singak":   ("sing",      "singing"),
    "criyad":   ("shout",     "shouting"),
    "whispar":  ("whisper",   "whispering"),
    # Motion
    "runak":    ("run",       "running"),
    "jumbad":   ("jump",      "jumping"),
    "retorn":   ("return",    "returning"),
    "entrak":   ("enter",     "entering"),
    "leavak":   ("leave",     "leaving"),
    "climbag":  ("climb",     "climbing"),
    "falan":    ("fall",      "falling"),
    "throwan":  ("throw",     "throwing"),
    "pushak":   ("push",      "pushing"),
    "pulad":    ("pull",      "pulling"),
    # Mental
    "thinkar":  ("think",     "thinking"),
    "remembrak":("remember",  "remembering"),
    "forgetak": ("forget",    "forgetting"),
    "belivan":  ("believe",   "believing"),
    "wantak":   ("want",      "wanting"),
    "chosar":   ("choose",    "choosing"),
    "planak":   ("plan",      "planning"),
    "imagak":   ("imagine",   "imagining"),
    # Emotion
    "lovak":    ("love",      "loving"),
    "hatak":    ("hate",      "hating"),
    "fearan":   ("fear",      "fearing"),
    "joyan":    ("rejoice",   "rejoicing"),
    "mournad":  ("mourn",     "mourning"),
    "hopak":    ("hope",      "hoping"),
    "trustad":  ("trust",     "trusting"),
    # Social & physical
    "helpak":   ("help",      "helping"),
    "figtak":   ("fight",     "fighting"),
    "rulad":    ("rule",      "ruling"),
    "tradak":   ("trade",     "trading"),
    "sharad":   ("share",     "sharing"),
    "joinak":   ("join",      "joining"),
    "makad":    ("make",      "making"),
    "brekan":   ("break",     "breaking"),
    "fixar":    ("fix",       "fixing"),
    "openak":   ("open",      "opening"),
    "klozad":   ("close",     "closing"),
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
}

# ---------------------------------------------------------------------------
# Sigan → English translation tables
# ---------------------------------------------------------------------------

NOUN_EN: dict[str, str] = {
    # Core
    "manu": "person", "childa": "child", "watra": "water",
    "stonu": "stone", "truku": "tree", "burda": "bird",
    "homu": "house", "rotha": "path", "fudo": "food",
    "sunu": "sun", "handu": "hand", "rivna": "river",
    "mounta": "mountain", "worda": "word", "besta": "animal",
    "fyru": "fire",
    "manun": "people", "childan": "children", "watran": "waters",
    "stonun": "stones", "trukun": "trees", "burdan": "birds",
    "homun": "houses", "rothan": "paths", "fudon": "foods",
    "sunun": "suns", "handun": "hands", "rivnan": "rivers",
    "mountan": "mountains", "wordan": "words", "bestan": "animals",
    "fyrun": "fires",
    # Body parts
    "dava": "head", "davan": "heads",
    "oku": "eye", "okun": "eyes",
    "mova": "mouth", "movan": "mouths",
    "nasu": "nose", "nasun": "noses",
    "braku": "arm", "brakun": "arms",
    "legu": "leg", "legun": "legs",
    "fotu": "foot", "fotun": "feet",
    "kordu": "heart", "kordun": "hearts",
    "ventra": "stomach", "ventran": "stomachs",
    "chesta": "chest", "chestan": "chests",
    "doru": "back", "dorun": "backs",
    "skinu": "skin", "skinun": "skins",
    # Nature
    "skavu": "sky", "skavun": "skies",
    "winda": "wind", "windan": "winds",
    "ertha": "earth", "erthan": "earths",
    "ranu": "rain", "ranun": "rains",
    "snova": "snow", "snovan": "snows",
    "kluda": "cloud", "kludan": "clouds",
    "noku": "night", "nokun": "nights",
    "dayo": "day", "dayon": "days",
    "staru": "star", "starun": "stars",
    "sova": "sea", "sovan": "seas",
    "valu": "valley", "valun": "valleys",
    "dusta": "dust", "dustan": "dusts",
    "rocha": "rock", "rochan": "rocks",
    "sanda": "sand", "sandan": "sands",
    "foresta": "forest", "forestan": "forests",
    "fielda": "field", "fieldan": "fields",
    # Abstract
    "tima": "time", "timan": "times",
    "truta": "truth", "trutan": "truths",
    "lifa": "life", "lifan": "lives",
    "morta": "death", "mortan": "deaths",
    "powra": "power", "powran": "powers",
    "knowu": "knowledge", "knowun": "knowledges",
    "fathu": "faith", "fathun": "faiths",
    "ritu": "justice", "ritun": "justices",
    "duta": "duty", "dutan": "duties",
    "sekru": "secret", "sekrun": "secrets",
    "dreamu": "dream", "dreamun": "dreams",
    "memorya": "memory", "memoryan": "memories",
    # Social
    "famla": "family", "famlan": "families",
    "frenda": "friend", "френdan": "friends",
    "enemu": "enemy", "enemun": "enemies",
    "chefa": "leader", "chefan": "leaders",
    "koma": "community", "koman": "communities",
    "gesta": "guest", "gestan": "guests",
    "voka": "voice", "vokan": "voices",
    "namu": "name", "namun": "names",
    "rula": "law", "rulan": "laws",
    "wara": "war", "waran": "wars",
    "paka": "accord", "pakan": "accords",
    "giftu": "gift", "giftun": "gifts",
    # Emotion nouns
    "joya": "joy", "joyan": "joys",
    "soru": "sorrow", "sorun": "sorrows",
    "ragu": "anger", "ragun": "angers",
    "dreda": "fear", "dredan": "fears",
    "lovu": "love", "lovun": "loves",
    "hatu": "hate", "hatun": "hates",
    "shamu": "shame", "shamun": "shames",
    "pisu": "peace", "pisun": "peaces",
    "kalu": "loneliness", "kalun": "lonelinesses",
    "glayu": "happiness", "glayun": "happinesses",
    "thoru": "grief", "thorun": "griefs",
    "ventu": "pride", "ventun": "prides",
    "envu": "envy", "envun": "envies",
    "remu": "regret", "remun": "regrets",
    "hopa": "hope", "hopan": "hopes",
    "trusta": "trust", "trustan": "trusts",
    "kura": "courage", "kuran": "courages",
    "duba": "doubt", "duban": "doubts",
    "wundu": "wonder", "wundun": "wonders",
    "komforta": "comfort", "komfortan": "comforts",
    "nostu": "longing", "nostun": "longings",
}

PRON_EN: dict[str, str] = {
    "ayu": "I", "yu": "you", "hiru": "he",
    "ayun": "we", "yun": "you", "hirun": "they",
}

PRON_OBJ_EN: dict[str, str] = {
    "ayu": "me", "yu": "you", "hiru": "him",
    "ayun": "us", "yun": "you", "hirun": "them",
}

POSS_EN: dict[str, str] = {
    "ayugar": "my", "yugar": "your", "hirugar": "his/her/its",
    "ayungar": "our", "yungar": "your", "hirungar": "their",
}

DET_EN: dict[str, str] = {"gar": "the", "brath": "a"}

ADJ_EN: dict[str, str] = {
    # Core
    "bigrath": "big", "oldrath": "old", "darkoth": "dark",
    "swifth": "fast", "smaloth": "small", "koldrith": "cold",
    "strongath": "strong", "wethrakh": "wet",
    # Size & shape
    "longrath": "long", "shoroth": "short", "roundath": "round",
    "deeprith": "deep", "widrath": "wide", "narrath": "narrow",
    "talloth": "tall", "flatrath": "flat",
    # Sensory
    "hotrath": "hot", "brightrath": "bright", "loudoth": "loud",
    "sharpoth": "sharp", "dulrith": "dull", "smoothath": "smooth",
    "roughoth": "rough",
    # Evaluative
    "godrath": "good", "badoth": "bad", "newrath": "new",
    "truerath": "true", "falsoth": "false", "holyrath": "holy",
    "wisrath": "wise", "fooloth": "foolish", "noblrath": "noble",
    # Emotion
    "jorath": "joyful", "sorath": "sorrowful", "ragoth": "angry",
    "dredath": "fearful", "lovrath": "loving", "hatoth": "hateful",
    "kalerith": "lonely", "glayrath": "happy", "thoroth": "grieving",
    "hoprath": "hopeful", "kurrath": "courageous", "wundrath": "awestruck",
    "duboth": "doubtful", "venturith": "proud",
}

PREP_EN: dict[str, str] = {
    "tov": "to", "from": "from", "nak": "in", "wid": "with",
    "thov": "about", "for": "for",
}

TIME_EN: dict[str, str] = {
    "nowom": "now", "yestom": "yesterday", "morom": "tomorrow",
    "evrom": "always", "nevrom": "never", "wonsom": "once",
}

QN_EN: dict[str, str] = {
    "huzh": "who", "wazh": "what", "werazh": "where", "wenazh": "when",
}
