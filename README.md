# מדריך פיתוח ב-Claude Code

מדריך מקצועי, מקיף ומדורג בעברית (RTL) לפיתוח תוכנה עם Claude Code: 43 פרקים, חמש לומדות אינטראקטיביות, ודוגמאות קוד מלאות שאפשר להריץ.

- **קריאה אונליין:** https://photossasson.github.io/Claude-Development-Guide/
- **גרסה:** 1.2, מתאריך 16.10.2026
- **בסיס האימות:** Claude Code בגרסאות 2.1.220 (מחקר מקורי, 28.07.2026), 2.1.300 ו-2.1.301 (עדכוני תחזוקה, אוקטובר 2026). כל עובדה תלוית גרסה מסומנת בפרקים עם מקור ותאריך בדיקה.

## איך פותחים את המדריך

יש שלוש דרכים, לפי מה שנוח לכם:

1. **בדפדפן, דרך GitHub Pages:** פתחו את הכתובת למעלה. אין צורך בהתקנה.
2. **מקומית, בלי שרת:** הורידו את ה-Repository (כפתור Code ואז Download ZIP, או `git clone`) ופתחו את `index.html` בדפדפן. כל הדפים סטטיים, והקישורים ביניהם יחסיים, כך שהם עובדים גם מהדיסק.
3. **מקומית, עם שרת קטן** (מומלץ אם הדפדפן חוסם קבצים מקומיים):

```bash
git clone https://github.com/photossasson/Claude-Development-Guide.git
cd Claude-Development-Guide
python3 -m http.server 8000
# ואז לפתוח http://localhost:8000
```

הניווט: תוכן העניינים בעמוד הראשי, ובתחתית כל פרק קישורי "הפרק הקודם" ו"הפרק הבא". הלומדות נמצאות בתיקייה `interactive/` ומקושרות מהעמוד הראשי.

## מבנה התיקיות

| תיקייה | תוכן |
|--------|------|
| `index.html` | עמוד הבית ותוכן העניינים |
| `chapters/` | 43 פרקי המדריך (HTML, RTL) |
| `interactive/` | חמש לומדות: Skills, Rules, Hooks, Mods, MCP |
| `assets/` | עיצוב וניווט (`guide.css`, `nav.js`) |
| `diagrams/` | 10 תרשימי SVG מקוריים |
| `references/` | רשימת המקורות הרשמיים וטבלת סטטוס ה-Features |
| `examples/taskflow/` | פרויקט הדוגמה TaskFlow (FastAPI, SQLite, React, TypeScript) שמלווה את המדריך |
| `skills/` | שישה Skills מלאים, כולל `checking-hebrew-style` של הלומדה |
| `rules/taskflow-example/` | דוגמת `CLAUDE.md` ו-`.claude/rules/` של לומדת ה-Rules |
| `hooks/` | שבעה Hooks לדוגמה, ובנוסף `lomda-example/` של לומדת ה-Hooks |
| `mods/lomda-example/` | ה-Plugin `risk-guard` של לומדת ה-Mods, כולל בדיקות |
| `mcp/` | חמש תצורות שרתי MCP, ובנוסף `lomda-example/` עם שרת MCP קטן שרץ |
| `connectors/` | מדריך חיבור, מטריצת זמינות ושמונה תרחישי בדיקה ל-Connectors |
| `subagents/` | חמש הגדרות Subagents וסקריפט עזר |
| `plugins/taskflow-toolkit/` | Plugin לדוגמה |
| `agent-sdk/` | דוגמאות Quickstart ל-Agent SDK ב-Python וב-TypeScript |
| `CHANGELOG.md` | היסטוריית הגרסאות של המדריך |

## הרצת הדוגמאות

המדריך עצמו הוא HTML סטטי, אבל כל הדוגמאות בו הן קוד אמיתי. GitHub Pages רק מגיש את הקבצים; כדי להריץ דוגמה, שכפלו את ה-Repository למחשב שלכם והריצו אותה שם. הדרישות הכלליות: Python 3.10 ומעלה, Node.js 22 ומעלה, ו-Claude Code מותקן ומחובר (פרק 2).

### TaskFlow

```bash
cd examples/taskflow/backend
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pytest -q

cd ../frontend
npm install
npm run typecheck
```

### Skill: checking-hebrew-style

```bash
python3 skills/checking-hebrew-style/scripts/check_style.py chapters/ch01.html
```

כדי להשתמש בו כ-Skill, העתיקו את התיקייה ל-`.claude/skills/` של הפרויקט שלכם או ל-`~/.claude/skills/`.

### Rules ו-Hooks

```bash
cd rules/taskflow-example && claude          # Claude Code טוען את CLAUDE.md ואת .claude/rules/
cd hooks/lomda-example && claude             # ה-Hooks מוגדרים ב-.claude/settings.json
```

בהפעלה הראשונה בכל תיקייה Claude Code יבקש אישור Trust. קראו את ההגדרות לפני שאתם מאשרים.

### Mods: risk-guard

```bash
cd mods/lomda-example
claude plugin validate risk-guard
```

הוראות ההתקנה והבדיקות המלאות נמצאות ב-`mods/lomda-example/README.md`.

### MCP: שרת taskflow-tasks

```bash
cd mcp/lomda-example
python3 -m venv .venv
.venv/bin/pip install "mcp>=2,<3"
.venv/bin/python check_client.py
claude mcp add --scope project taskflow -- "$PWD/.venv/bin/python" server.py
```

### Plugin ו-Agent SDK

```bash
claude plugin validate plugins/taskflow-toolkit

cd agent-sdk/python && pip install -r requirements.txt
cd agent-sdk/typescript && npm install && npm run typecheck
```

הרצת דוגמאות ה-Agent SDK דורשת `ANTHROPIC_API_KEY` או התחברות דרך `claude`. אל תשמרו מפתחות בקבצים שנכנסים ל-Git.

## הערות לגבי הגרסה המפורסמת

- קובצי הבקרה הפנימיים של הפרויקט (תיקיית `control/`) ודוחות ה-QA (תיקיית `qa/`) אינם כלולים כאן. במקומות שבהם פרק מזכיר קובץ בקרה, ההפניה היא לתיעוד פנימי של תהליך הכתיבה.
- פרקים 32 ו-33 מצטטים קטעים מהקבצים `agent-sdk/python/02_code_reviewer.py` ו-`agent-sdk/typescript/02-automation.ts`. שני הקבצים המלאים אינם כלולים בגרסה הזו; הקטעים שבפרקים הם החלקים הרלוונטיים, ודוגמאות ה-Quickstart (`01_*`) מלאות.
- כל הקישורים בין הדפים יחסיים, ולכן המדריך עובד גם מ-GitHub Pages וגם מהדיסק.
- הקובץ `.nojekyll` בשורש נחוץ: בלעדיו GitHub Pages מדלג על תיקיות שמתחילות בנקודה (כמו `.claude/` ו-`.claude-plugin/`) שהדוגמאות תלויות בהן.

## מקורות

המקור הראשי לכל עובדה במדריך הוא התיעוד הרשמי של Anthropic: https://code.claude.com/docs ו-https://support.claude.com. הרשימה המלאה, עם תאריכי בדיקה, נמצאת ב-`references/sources.html`.
