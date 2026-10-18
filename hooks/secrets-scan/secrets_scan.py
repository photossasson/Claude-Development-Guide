#!/usr/bin/env python3
"""secrets_scan.py

PreToolUse hook (matcher: Write|Edit) that scans the content Claude is
about to write for credential patterns and denies the write when a likely
secret is found.

Scanned fields: tool_input.content (Write) and tool_input.new_string (Edit).

Privacy by design: the deny reason names the PATTERN that matched, never
the matched value itself, so the secret is not echoed back into the
conversation or into any log.

Output semantics (verified against the hooks reference, 28.07.2026):
- exit 0, no stdout                       -> no objection.
- exit 0, permissionDecision "deny" JSON  -> tool call denied with reason.
"""

import json
import re
import sys

PATTERNS = [
    ("AWS Access Key ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    (
        "Hardcoded credential assignment",
        re.compile(
            r"(?i)\b(api[_-]?key|secret|token|passwd|password)\b\s*[:=]\s*['\"][A-Za-z0-9_\-/+=]{16,}['\"]"
        ),
    ),
]

# Obvious placeholders never count as secrets.
PLACEHOLDER = re.compile(
    r"(?i)(YOUR_|XXXX|example|placeholder|dummy|changeme|<[^>]+>|\$\{|%s|REDACTED|test[_-]?key)"
)


def deny(findings) -> None:
    lines = ", ".join(f"{name} (line {line})" for name, line in findings)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "secrets-scan blocked this write. Likely secrets detected: "
                f"{lines}. Move secrets to environment variables or a secrets "
                "manager and reference them by name. Never write secret values "
                "into tracked files."
            ),
        }
    }))
    sys.exit(0)


def scan(text: str):
    findings = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for name, pattern in PATTERNS:
            match = pattern.search(line)
            if match and not PLACEHOLDER.search(match.group(0)) and not PLACEHOLDER.search(line):
                findings.append((name, line_no))
                break  # one finding per line is enough for the report
    return findings


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print("secrets-scan: could not parse hook input", file=sys.stderr)
        sys.exit(1)

    tool_input = data.get("tool_input") or {}
    text_parts = []
    for field in ("content", "new_string"):
        value = tool_input.get(field)
        if isinstance(value, str):
            text_parts.append(value)

    if not text_parts:
        sys.exit(0)

    findings = scan("\n".join(text_parts))
    if findings:
        deny(findings[:5])

    sys.exit(0)


if __name__ == "__main__":
    main()
