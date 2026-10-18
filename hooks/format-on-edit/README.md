# format-on-edit

## מה ה-Hook עושה
Hook מסוג <b>PostToolUse</b> עם Matcher של `Edit|Write`: אחרי כל עריכה או כתיבה של קובץ, הסקריפט מפעיל Formatter על הקובץ שנערך. קבצי Python מפורמטים עם black, וקבצי JavaScript, TypeScript, JSON, CSS, Markdown ועוד מפורמטים עם prettier (דרך `npx --no-install`, כלומר רק אם prettier מותקן בפרויקט).

הסקריפט קורא את ה-JSON מ-stdin, שולף את `tool_input.file_path` עם jq, ובוחר Formatter לפי הסיומת. הוא תמיד מסיים עם Exit Code 0: כשל בפירמוט לא אמור לחסום את ה-Session.

## התקנה
```bash
mkdir -p .claude/hooks
cp format-on-edit.sh .claude/hooks/
chmod +x .claude/hooks/format-on-edit.sh
```
מזגו את התוכן של `hooks.json` לתוך `.claude/settings.json` בפרויקט (אם כבר קיים מפתח `hooks`, הוסיפו את `PostToolUse` כאח לאירועים הקיימים). אימות: הריצו `/hooks` בתוך Claude Code ובדקו שה-Hook מופיע תחת PostToolUse.

## דרישות
jq מותקן; black או prettier לפי סוגי הקבצים בפרויקט.

## סיכונים ומגבלות
- הסקריפט משנה קבצים בפרויקט (מפרמט אותם). ודאו שהגדרות ה-Formatter (למשל `.prettierrc`) תואמות לסטנדרט של הצוות.
- Claude יכול לערוך קבצים גם דרך פקודות Bash; ה-Hook לא יתפוס מקרים כאלה כי ה-Matcher מכסה רק את הכלים Edit ו-Write.
- הפירמוט רץ אחרי כל עריכה, כולל עריכות ביניים; בפרויקטים גדולים מאוד ייתכן עיכוב קל.
