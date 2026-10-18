# lint-gate

## מה ה-Hook עושה
Hook מסוג <b>PostToolUse</b> עם Matcher של `Edit|Write`: אחרי כל עריכת קובץ, הסקריפט מריץ Linter על הקובץ (ruff לקבצי Python, eslint לקבצי JavaScript ו-TypeScript). אם נמצאו שגיאות, הסקריפט מסיים עם Exit Code 2 וכותב את הממצאים ל-stderr.

בסמנטיקה של PostToolUse, יציאה עם קוד 2 לא מבטלת את הפעולה (הכלי כבר רץ), אבל ה-stderr מוזן חזרה ל-Claude כמשוב, כך ש-Claude מתקן את שגיאות ה-Lint באותו תור. זה ההבדל החשוב מ-PreToolUse, שבו קוד 2 חוסם את הפעולה מראש.

## התקנה
```bash
mkdir -p .claude/hooks
cp lint-gate.sh .claude/hooks/
chmod +x .claude/hooks/lint-gate.sh
```
מזגו את `hooks.json` לתוך `.claude/settings.json` ואמתו עם `/hooks`.

## דרישות
jq; ruff (לפרויקטי Python) או eslint מותקן בפרויקט (לפרויקטי JS/TS). אם ה-Linter לא מותקן, ה-Hook פשוט לא עושה כלום.

## סיכונים ומגבלות
- Linter עם חוקים נוקשים מדי עלול להכניס את Claude ללולאת תיקונים ארוכה; התאימו את קובץ ההגדרות של ה-Linter.
- הפלט נחתך ל-40 שורות כדי לא להציף את ה-Context.
- שינויים שנעשים דרך Bash (למשל `sed`) לא נתפסים; ראו את פרק ה-Hooks במדריך לפתרון עם Stop Hook.
