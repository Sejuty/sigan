"""
Sigan interactive REPL — combines validator and translator.
Commands:
  :validate <sentence>   validate a Sigan sentence
  :to-en    <sentence>   translate Sigan → English
  :to-sig   <sentence>   translate English → Sigan
  :history               show session history
  :help                  show this help
  :quit / :exit          exit
"""

import sys

try:
    import readline  # noqa: F401  — enables arrow-key editing on Unix
except ImportError:
    pass

from backend.validator import validate, tree_to_str
from backend.translator import sigan_to_english, english_to_sigan


# ---------------------------------------------------------------------------
# Session history entry
# ---------------------------------------------------------------------------

class HistoryEntry:
    __slots__ = ("command", "input_text", "result_summary", "success")

    def __init__(self, command: str, input_text: str,
                 result_summary: str, success: bool):
        self.command = command
        self.input_text = input_text
        self.result_summary = result_summary
        self.success = success

    def __str__(self) -> str:
        status = "OK" if self.success else "FAIL"
        return f"[{status}] :{self.command}  {self.input_text!r}  →  {self.result_summary}"


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_validate(sentence: str, history: list[HistoryEntry]) -> None:
    result = validate(sentence)
    if result["valid"]:
        print("VALID")
        print("\nParse tree:")
        print(tree_to_str(result["parse_tree"], result["tokens"]))
        history.append(HistoryEntry("validate", sentence, "VALID", True))
    else:
        print("INVALID")
        for err in result["errors"]:
            print(f"  Error: {err}")
        history.append(HistoryEntry("validate", sentence,
                                    "; ".join(result["errors"]), False))


def cmd_to_en(sentence: str, history: list[HistoryEntry]) -> None:
    result = sigan_to_english(sentence)
    if result["success"]:
        print(result["english"])
        history.append(HistoryEntry("to-en", sentence, result["english"], True))
    else:
        errors = result["error"] if isinstance(result["error"], list) else [result["error"]]
        print("Translation failed:")
        for e in errors:
            print(f"  {e}")
        history.append(HistoryEntry("to-en", sentence,
                                    "; ".join(str(e) for e in errors), False))


def cmd_to_sig(sentence: str, history: list[HistoryEntry]) -> None:
    result = english_to_sigan(sentence)
    if result["success"]:
        print(result["sigan"])
        history.append(HistoryEntry("to-sig", sentence, result["sigan"], True))
    else:
        err = result["error"] or "unknown error"
        print(f"Translation failed: {err}")
        history.append(HistoryEntry("to-sig", sentence, str(err), False))


def cmd_history(history: list[HistoryEntry]) -> None:
    if not history:
        print("(no history yet)")
        return
    for i, entry in enumerate(history, 1):
        print(f"  {i:3}.  {entry}")


HELP_TEXT = """\
Sigan REPL commands:
  :validate <sentence>   — validate a Sigan sentence (CKY parse)
  :to-en    <sentence>   — translate Sigan → English
  :to-sig   <sentence>   — translate English → Sigan
  :history               — show session history
  :help                  — show this message
  :quit  / :exit         — exit the REPL
"""


# ---------------------------------------------------------------------------
# REPL main loop
# ---------------------------------------------------------------------------

def repl() -> None:
    print("Sigan REPL  (type :help for commands, :quit to exit)")
    history: list[HistoryEntry] = []

    while True:
        try:
            raw = input("sigan> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not raw:
            continue

        if not raw.startswith(":"):
            print("Commands start with ':'.  Try :help")
            continue

        # Split command from argument
        parts = raw.split(None, 1)
        cmd = parts[0][1:].lower()        # strip leading ':'
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ("quit", "exit", "q"):
            break
        elif cmd == "help":
            print(HELP_TEXT)
        elif cmd == "history":
            cmd_history(history)
        elif cmd == "validate":
            if not arg:
                print("Usage: :validate <sigan sentence>")
            else:
                cmd_validate(arg, history)
        elif cmd == "to-en":
            if not arg:
                print("Usage: :to-en <sigan sentence>")
            else:
                cmd_to_en(arg, history)
        elif cmd == "to-sig":
            if not arg:
                print("Usage: :to-sig <english sentence>")
            else:
                cmd_to_sig(arg, history)
        else:
            print(f"Unknown command: :{cmd}  (try :help)")

    print("Goodbye.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    repl()
