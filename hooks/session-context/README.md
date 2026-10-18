# session-context

## מה ה-Hook עושה
Hook מסוג <b>SessionStart</b> עם Matcher של `startup|resume`: בתחילת כל Session (או חזרה אליו), הסקריפט מדפיס ל-stdout תמונת מצב של ה-Repository: ה-Branch הנוכחי, פלט `git status --short`, חמשת ה-Commits האחרונים, ואם ה-CLI של GitHub (gh) מותקן ומחובר, גם רשימת Pull Requests פתוחים.

באירוע SessionStart, כל מה שנכתב ל-stdout עם Exit Code 0 מוזרק ל-Context של Claude. כך Claude מתחיל כל Session כשהוא כבר יודע על אילו קבצים עובדים ואילו PRs פתוחים, בלי להריץ פקודות בעצמו.

## התקנה
```bash
mkdir -p .claude/hooks
cp session-context.sh .claude/hooks/
chmod +x .claude/hooks/session-context.sh
```
מזגו את `hooks.json` לתוך `.claude/settings.json` ואמתו עם `/hooks`. בדיקה: פתחו Session חדש ושאלו את Claude "על איזה Branch אנחנו?"; הוא אמור לענות בלי להריץ פקודה.

## דרישות
git. אופציונלי: gh מחובר (`gh auth status`) להצגת PRs.

## סיכונים ומגבלות
- ההזרקה צורכת Tokens בכל Session; הפלט חתוך (30 שורות Status, 5 Commits, 5 PRs) כדי לשמור על עלות נמוכה.
- הפלט של gh עלול לכלול כותרות PR עם מידע רגיש; אל תשתמשו ב-Hook הזה אם כותרות ה-PR בארגון סודיות.
- SessionStart אינו אירוע חוסם: אם הסקריפט נכשל, ה-Session נפתח כרגיל בלי התקציר.
- להזרקת הקשר גם אחרי Compaction, הוסיפו קבוצת Matcher נוספת עם הערך `compact`.
