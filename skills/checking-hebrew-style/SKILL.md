---
name: checking-hebrew-style
description: Checks Hebrew technical text for em and en dashes and for spacing and punctuation errors around English terms. Use when writing, editing or reviewing Hebrew docs, Markdown or HTML.
---

# Checking Hebrew style

Find and fix style errors in Hebrew technical writing that mixes in English terms.
The bundled checker finds the errors; you fix them by rewriting, then check again.

## Workflow

Copy this checklist into your reply and tick it off:

```
- [ ] 1. Identify the target
- [ ] 2. Run the checker
- [ ] 3. Fix every finding
- [ ] 4. Run the checker again until it exits 0
- [ ] 5. Report
```

1. **Identify the target.** Use the files the user named. If the user pasted text
   instead, save it to a temporary `.md` file first so the checker can read it.
2. **Run the checker.** It prints one line per finding: `file:line:col: CODE message`.
   - In Claude Code: `python3 ${CLAUDE_SKILL_DIR}/scripts/check_style.py <file> [<file> ...]`
   - In Claude chat (claude.ai): `python3 scripts/check_style.py <file>`, relative to this SKILL.md.
   - Exit code 0 means clean, 1 means findings, 2 means a file could not be read.
3. **Fix every finding** using the rules and examples in
   [references/rules.md](references/rules.md). For `E001` and `E002` (long dashes),
   rewrite the sentence with a period, comma, colon or parentheses. Never replace a
   long dash with a hyphen surrounded by spaces, because the checker reports that as `W005`.
4. **Run the checker again** on the same files. Repeat steps 3 and 4 until it exits 0,
   or until only warnings you deliberately keep remain.
5. **Report** in Hebrew: the files you checked, how many findings you fixed per code,
   and any warning you kept with the reason.

## Rules

- Do not change code blocks, inline code, URLs, file paths or commands. The checker
  already skips fenced code in Markdown and `<pre>`, `<code>` in HTML.
- Keep accepted technical terms in English (Skill, Prompt, Repository). Never translate
  or transliterate them.
- Keep the author's meaning. Change punctuation and spacing, not content.
