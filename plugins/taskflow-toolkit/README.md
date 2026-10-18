# taskflow-toolkit

Plugin לדוגמה של המדריך "מדריך פיתוח ב-Claude Code". אורז שלושה רכיבים לצוות של פרויקט TaskFlow:

| רכיב | נתיב | מה הוא מוסיף |
|------|------|--------------|
| Skill בשם `pr-ready` | `skills/pr-ready/SKILL.md` | בדיקת מוכנות ל-Pull Request: בדיקות, Lint, עדכון Changelog ושאריות Debug. הפעלה: `/taskflow-toolkit:pr-ready` |
| Hook לסריקת סודות | `hooks/hooks.json` + `scripts/secrets_scan.py` | PreToolUse על `Write|Edit`: חוסם כתיבת מפתחות API וסודות לקבצים |
| Subagent בשם `db-reviewer` | `agents/db-reviewer.md` | סוקר Read-Only של סכמות, מיגרציות ושאילתות SQL. הפעלה: `@taskflow-toolkit:db-reviewer` |

## מבנה

```text
taskflow-toolkit/
├── .claude-plugin/
│   └── plugin.json          # Manifest: שם, גרסה, מחבר
├── skills/
│   └── pr-ready/
│       └── SKILL.md
├── agents/
│   └── db-reviewer.md
├── hooks/
│   └── hooks.json           # מפנה לסקריפט דרך ${CLAUDE_PLUGIN_ROOT}
├── scripts/
│   └── secrets_scan.py
└── README.md
```

## התקנה לפיתוח (בלי Marketplace)

```bash
claude --plugin-dir ./taskflow-toolkit
```

בתוך ה-Session: `/taskflow-toolkit:pr-ready` להפעלת ה-Skill, `/hooks` לאימות שה-Hook נטען, ו-`/context` לבדיקה שה-Agent מופיע. אחרי שינוי בקבצי ה-Plugin הריצו `/reload-plugins`.

## התקנה דרך Marketplace

הוסיפו את ה-Plugin ל-`marketplace.json` של הצוות והתקינו:

```bash
claude plugin marketplace add your-org/claude-plugins
claude plugin install taskflow-toolkit@your-marketplace --scope project
```

## אימות

```bash
claude plugin validate ./taskflow-toolkit
```

## הערות עיצוב

- הסקריפט `secrets_scan.py` זהה ל-Hook העצמאי בתיקיית `hooks/secrets-scan/` של המדריך; ב-Plugin הנתיב אליו עובר דרך `${CLAUDE_PLUGIN_ROOT}` כי Plugins מותקנים מ-Marketplace מועתקים ל-Cache מקומי.
- ה-Agent הוא גרסה מותאמת של `subagents/database-reviewer.md` מהמדריך: הוסרו ה-Frontmatter של `hooks:` והכלי Bash, כי Plugin Agents לא תומכים ב-hooks, ב-mcpServers וב-permissionMode משיקולי אבטחה. בלי Hook שאוכף שאילתות Read-Only, אין להעניק ל-Agent גישת Bash.
- הסיכון העיקרי: Hook של Plugin רץ עם הרשאות המשתמש בכל פרויקט שבו ה-Plugin פעיל. סקרו את הקוד לפני התקנה.
