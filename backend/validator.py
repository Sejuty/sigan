"""
Sigan language validator: tokenizes, POS-tags, and CKY-parses a Sigan sentence.
Usage: python validator.py "ayu sigan gar truku"
"""

import sys
from typing import Optional

from lexicon import LEXICON, VERB_STEMS
from grammar import BINARY_RULES, UNARY_RULES, SUFFIX_TABLE


# ---------------------------------------------------------------------------
# Tense / aspect suffix stripping
# ---------------------------------------------------------------------------

def strip_verb_suffix(token: str) -> Optional[tuple[str, str, str]]:
    """
    Match a verb token against known stems + suffixes.
    Returns (stem, tense, aspect) or None.
    """
    for suffix, tense, aspect in SUFFIX_TABLE:
        if token.endswith(suffix):
            candidate = token[: len(token) - len(suffix)]
            if candidate in VERB_STEMS:
                return candidate, tense, aspect
    if token in VERB_STEMS:
        return token, "present", "simple"
    return None


# ---------------------------------------------------------------------------
# Pre-computed rule lookup maps
# ---------------------------------------------------------------------------

# binary_by_children[(B, C)] → [A, ...]  where A → B C
_BINARY_BY_CHILDREN: dict[tuple[str, str], list[str]] = {}
for _lhs, _b, _c in BINARY_RULES:
    _BINARY_BY_CHILDREN.setdefault((_b, _c), []).append(_lhs)

# unary_by_child[B] → [A, ...]  where A → B
_UNARY_BY_CHILD: dict[str, list[str]] = {}
for _lhs, _rhs in UNARY_RULES:
    _UNARY_BY_CHILD.setdefault(_rhs, []).append(_lhs)


# ---------------------------------------------------------------------------
# Token data class
# ---------------------------------------------------------------------------

class TokenInfo:
    __slots__ = ("surface", "pos", "stem", "tense", "aspect")

    def __init__(self, surface: str, pos: str,
                 stem: str = "", tense: str = "", aspect: str = ""):
        self.surface = surface
        self.pos = pos
        self.stem = stem or surface
        self.tense = tense
        self.aspect = aspect

    def __repr__(self) -> str:
        if self.tense:
            return f"TokenInfo({self.surface!r}, {self.pos}, {self.tense}-{self.aspect})"
        return f"TokenInfo({self.surface!r}, {self.pos})"


def tokenize_and_tag(sentence: str) -> tuple[list[TokenInfo], list[str]]:
    """Return (token_list, error_list). error_list is empty on success."""
    tokens: list[TokenInfo] = []
    errors: list[str] = []

    for raw_word in sentence.split():
        word = raw_word.lower()
        if word in LEXICON:
            pos = LEXICON[word]
            if pos == "V":
                # Bare verb stem in lexicon — still needs tense/aspect (present simple)
                stem, tense, aspect = strip_verb_suffix(word) or (word, "present", "simple")
                tokens.append(TokenInfo(word, pos, stem=stem, tense=tense, aspect=aspect))
            else:
                tokens.append(TokenInfo(word, pos))
        else:
            result = strip_verb_suffix(word)
            if result:
                stem, tense, aspect = result
                tokens.append(TokenInfo(word, "V", stem=stem, tense=tense, aspect=aspect))
            elif raw_word[0].isupper():
                # Capitalized word not in lexicon → proper noun
                tokens.append(TokenInfo(raw_word, "PropN"))
            else:
                errors.append(f"Unknown word: '{raw_word}'")

    return tokens, errors


# ---------------------------------------------------------------------------
# CKY parse tree node
# ---------------------------------------------------------------------------

class ParseNode:
    __slots__ = ("symbol", "start", "end", "left", "right", "token")

    def __init__(self, symbol: str, start: int, end: int,
                 left: "Optional[ParseNode]" = None,
                 right: "Optional[ParseNode]" = None,
                 token: "Optional[TokenInfo]" = None):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.left = left
        self.right = right
        self.token = token

    def is_leaf(self) -> bool:
        return self.token is not None


# ---------------------------------------------------------------------------
# CKY parser
# ---------------------------------------------------------------------------

def _apply_unary_closure(cell: dict[str, ParseNode], start: int, end: int) -> None:
    """Saturate unary rules for a chart cell (fixed-point iteration)."""
    changed = True
    while changed:
        changed = False
        for child_sym, child_node in list(cell.items()):
            for parent_sym in _UNARY_BY_CHILD.get(child_sym, []):
                if parent_sym not in cell:
                    cell[parent_sym] = ParseNode(parent_sym, start, end, left=child_node)
                    changed = True


def cky_parse(tokens: list[TokenInfo]) -> Optional[ParseNode]:
    """
    Standard CKY chart parser.
    Returns the S ParseNode spanning the full input, or None.
    """
    n = len(tokens)
    if n == 0:
        return None

    chart: list[list[dict[str, ParseNode]]] = [
        [{} for _ in range(n)] for _ in range(n)
    ]

    for i, tok in enumerate(tokens):
        cell = chart[i][i]
        cell[tok.pos] = ParseNode(tok.pos, i, i, token=tok)
        _apply_unary_closure(cell, i, i)

    for span in range(2, n + 1):
        for start in range(n - span + 1):
            end = start + span - 1
            cell = chart[start][end]

            for split in range(start, end):
                left_cell = chart[start][split]
                right_cell = chart[split + 1][end]

                for (b_sym, c_sym), parents in _BINARY_BY_CHILDREN.items():
                    if b_sym in left_cell and c_sym in right_cell:
                        for parent in parents:
                            if parent not in cell:
                                cell[parent] = ParseNode(
                                    parent, start, end,
                                    left=left_cell[b_sym],
                                    right=right_cell[c_sym],
                                )

            _apply_unary_closure(cell, start, end)

    return chart[0][n - 1].get("S")


# ---------------------------------------------------------------------------
# Parse tree pretty-printer
# ---------------------------------------------------------------------------

def tree_to_str(node: ParseNode, tokens: list[TokenInfo], indent: int = 0) -> str:
    prefix = "  " * indent
    if node.is_leaf():
        tok = node.token
        suffix_info = f" [{tok.tense}-{tok.aspect}]" if tok.tense else ""
        return f"{prefix}({node.symbol} '{tok.surface}'{suffix_info})"

    lines = [f"{prefix}({node.symbol}"]
    if node.left:
        lines.append(tree_to_str(node.left, tokens, indent + 1))
    if node.right:
        lines.append(tree_to_str(node.right, tokens, indent + 1))
    lines[-1] += ")"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate(sentence: str) -> dict:
    """
    Validate a Sigan sentence.
    Returns dict: valid (bool), tokens, parse_tree, errors.
    """
    tokens, lex_errors = tokenize_and_tag(sentence)

    if lex_errors:
        return {"valid": False, "tokens": tokens, "parse_tree": None, "errors": lex_errors}

    if not tokens:
        return {"valid": False, "tokens": [], "parse_tree": None, "errors": ["Empty sentence"]}

    tree = cky_parse(tokens)

    if tree is None:
        return {
            "valid": False, "tokens": tokens, "parse_tree": None,
            "errors": ["No valid parse: sentence violates Sigan grammar rules"],
        }

    return {"valid": True, "tokens": tokens, "parse_tree": tree, "errors": []}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python validator.py "<sigan sentence>"')
        sys.exit(1)

    result = validate(" ".join(sys.argv[1:]))

    if result["valid"]:
        print("VALID\n\nParse tree:")
        print(tree_to_str(result["parse_tree"], result["tokens"]))
    else:
        print("INVALID")
        for err in result["errors"]:
            print(f"  Error: {err}")


if __name__ == "__main__":
    main()
