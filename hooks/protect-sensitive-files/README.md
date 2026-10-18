# protect-sensitive-files

## מה ה-Hook עושה
Hook מסוג <b>PreToolUse</b> עם Matcher של `Edit|Write|NotebookEdit`: לפני כל עריכת קובץ, הסקריפט בודק את הנתיב וחוסם עריכות של:
1. קובצי סביבה עם סודות: `.env` וכל `.env.*`;
2. כל קובץ תחת תיקיית `secrets/`;
3. קבצים קיימים תחת `migrations/` (מיגרציות הן Append-Only; יוצרים מיגרציה חדשה במקום לערוך ישנה).

חסימה מתבצעת עם Exit Code 2 והסבר ב-stderr. ההסבר מוזן חזרה ל-Claude, כך שהוא מבין למה נחסם ומציע דרך פעולה אחרת. חסימת PreToolUse בדרך זו נאכפת בכל Permission Mode, כולל `bypassPermissions`.

## התקנה
```bash
mkdir -p .claude/hooks
cp protect-sensitive-files.sh .claude/hooks/
chmod +x .claude/hooks/protect-sensitive-files.sh
```
מזגו את `hooks.json` לתוך `.claude/settings.json` ואמתו עם `/hooks`.

## דרישות
jq בלבד.

## סיכונים ומגבלות
- ההגנה מכסה רק את כלי העריכה הישירים. Claude יכול לשנות קבצים גם דרך Bash (למשל `echo ... > .env`); להגנה קשיחה שלמו אותה עם חוקי Deny במערכת ה-Permissions, למשל `"deny": ["Read(.env)", "Edit(.env)"]`.
- הבדיקה מבוססת נתיב טקסטואלי; נתיב עקיף (Symlink) לא יזוהה.
- כדי לחסום גם קריאה של הקבצים האלה (ולא רק כתיבה), הוסיפו חוקי Deny על הכלי Read.
