# taskflow-tasks: שרת MCP לדוגמה

שרת MCP קטן בפייתון שחושף לפרויקט TaskFlow שני כלים, משאב אחד ו-prompt אחד. הוא רץ ב-stdio ושומר את הנתונים בקובץ `tasks.json`.

| יכולת | שם ב-Claude Code | מה היא עושה |
|---|---|---|
| Tool | `mcp__taskflow__list_tasks` | מחזירה משימות, עם סינון אופציונלי לפי status |
| Tool | `mcp__taskflow__add_task` | מוסיפה משימה פתוחה וכותבת לקובץ |
| Resource | `@taskflow:tasks://summary` | ספירה של משימות לפי status |
| Prompt | `/mcp__taskflow__standup` | מנסח סטנדאפ קצר מהמשימות שלא הסתיימו |

## התקנה

```bash
python3 -m venv .venv
.venv/bin/pip install "mcp>=2,<3"
.venv/bin/python check_client.py          # בדיקה בלי Claude Code
claude mcp add --scope project taskflow -- "$PWD/.venv/bin/python" server.py
claude mcp list                           # יופיע Pending approval עד שתאשרו בהפעלה הבאה של claude
```

`mcp.json.example` מראה את אותה הגדרה עם הרחבת משתנים (`${TASKFLOW_PY:-python3}`).

## הרשאות

```bash
claude -p "הצג משימות פתוחות" --allowedTools "mcp__taskflow__list_tasks"   # קריאה בלבד
claude -p "הוסף משימה" --allowedTools "mcp__taskflow__*"                   # כל הכלים של השרת
```

## הערות

* stdout שמור לפרוטוקול. הודעות יומן נכתבות ל-stderr.
* כדי שהמודל יראה סיבת כשל, זרקו `ToolError`. חריגה אחרת מוצגת רק כ-`Error executing tool <name>`.
* `tasks.seed.json` הוא מצב התחלתי. העתיקו אותו מעל `tasks.json` כדי לאפס.
