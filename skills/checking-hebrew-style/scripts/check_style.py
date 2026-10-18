#!/usr/bin/env python3
"""Check Hebrew technical text for long dashes and spacing errors.

Usage:
    python3 check_style.py FILE [FILE ...] [--json]

Prints one finding per line as `file:line:col: CODE message`.
Exit codes: 0 = clean, 1 = findings, 2 = a file could not be read or bad usage.
Fenced code in Markdown and <pre>, <code>, <script>, <style> in HTML are skipped.
Only the Python standard library is used, so nothing has to be installed.
"""

import json
import re
import sys
from pathlib import Path

HEB = "\u05D0-\u05EA"  # Hebrew letters alef to tav

# Each rule: (code, compiled pattern, message). Columns point at the match start.
RULES = [
    ("E001", re.compile("\u2014"), "em dash: rewrite with a period, comma, colon or parentheses"),
    ("E002", re.compile("\u2013"), "en dash: rewrite, or write a range as 'X עד Y'"),
    ("E003", re.compile("[\u2012\u2015\u2E3A\u2E3B\uFE58]"), "long dash character: rewrite the sentence"),
    ("W001", re.compile(f"(?<=\\S)[ \\t]+[,.:;!?](?=\\s|$|[{HEB}])"), "space before punctuation"),
    ("W002", re.compile(r"(?<=\S) {2,}(?=\S)"), "double space between words"),
    ("W003", re.compile(f"[,;](?=[A-Za-z{HEB}])|:(?=[{HEB}])"), "missing space after punctuation"),
    ("W004", re.compile(f"(?<![{HEB}])[בהוכלמש] +- *(?=[A-Za-z])|(?<![{HEB}])[בהוכלמש] *- +(?=[A-Za-z])"),
     "Hebrew prefix and English term: write as ה-Term with no spaces"),
    ("W005", re.compile(f"(?<=[{HEB}]) - (?=[{HEB}])"), "spaced hyphen used as a dash: rewrite"),
]

# Regions to blank out before checking. Newlines are kept so line numbers stay right.
MD_FENCE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.MULTILINE | re.DOTALL)
MD_INLINE_CODE = re.compile(r"`[^`\n]+`")
HTML_SKIP = re.compile(r"<(pre|code|script|style)\b[^>]*>.*?</\1\s*>", re.IGNORECASE | re.DOTALL)
HTML_TAG = re.compile(r"<[^>]+>")
URL = re.compile(r"https?://\S+")


PLACEHOLDER = "\uE000"  # private-use character: not a space, not a letter


def _blank(match):
    """Replace every character except newlines with a neutral placeholder.

    A placeholder (not a space) keeps columns stable and avoids reporting the
    gap left by hidden code or tags as a double space.
    """
    return re.sub(r"[^\n]", PLACEHOLDER, match.group(0))


def mask(text, suffix):
    """Hide code, tags and URLs so they are never reported."""
    if suffix in {".html", ".htm"}:
        text = HTML_SKIP.sub(_blank, text)
        text = HTML_TAG.sub(_blank, text)
    else:
        text = MD_FENCE.sub(_blank, text)
        text = MD_INLINE_CODE.sub(_blank, text)
    return URL.sub(_blank, text)


def check_text(text, suffix=".md"):
    """Return a list of findings (line, col, code, message) for one text."""
    findings = []
    masked = mask(text, suffix)
    for lineno, line in enumerate(masked.splitlines(), start=1):
        for code, pattern, message in RULES:
            for m in pattern.finditer(line):
                findings.append((lineno, m.start() + 1, code, message))
    findings.sort()
    return findings


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"]
    if not paths:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    results, read_error = {}, False
    for raw in paths:
        path = Path(raw)
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"{raw}: error: file not found", file=sys.stderr)
            read_error = True
            continue
        except UnicodeDecodeError:
            print(f"{raw}: error: not UTF-8 text; save it as UTF-8 and run again", file=sys.stderr)
            read_error = True
            continue
        except OSError as exc:
            print(f"{raw}: error: {exc.strerror}", file=sys.stderr)
            read_error = True
            continue
        results[raw] = check_text(text, path.suffix.lower())

    total = sum(len(f) for f in results.values())
    if as_json:
        print(json.dumps({
            "files": {p: [{"line": l, "col": c, "code": k, "message": m} for l, c, k, m in f]
                      for p, f in results.items()},
            "total": total,
        }, ensure_ascii=False, indent=2))
    else:
        for p, found in results.items():
            for line, col, code, message in found:
                print(f"{p}:{line}:{col}: {code} {message}")
        print(f"checked {len(results)} file(s), {total} finding(s)")

    if read_error:
        return 2
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
