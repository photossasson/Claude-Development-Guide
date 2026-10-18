# audit-log

## מה ה-Hook עושה
Hook מסוג <b>PostToolUse</b> עם Matcher של `*` (כל הכלים): אחרי כל הפעלת כלי מוצלחת, הסקריפט מוסיף שורת JSON אחת לקובץ `.claude/audit.log` בפרויקט, עם חותמת זמן UTC, מזהה Session, שם הכלי ותקציר מנוטרל.

## מזעור נתונים (Data Minimization)
הלוג מתעד מי עשה מה ומתי, לא את התוכן עצמו:
- Bash: הפקודה בלבד, חתוכה ל-300 תווים;
- Edit / Write / Read: נתיב הקובץ בלבד;
- כלים אחרים: שמות המפתחות של הקלט בלבד.

תגובות כלים (`tool_response`) ותוכן קבצים לא נרשמים לעולם, כדי שסודות שעברו בשיחה לא ידלפו ללוג.

## התקנה
```bash
mkdir -p .claude/hooks
cp audit_log.py .claude/hooks/
chmod +x .claude/hooks/audit_log.py
```
מזגו את `hooks.json` לתוך `.claude/settings.json` ואמתו עם `/hooks`. צפייה בלוג:
```bash
tail -f .claude/audit.log
```

## סיכונים ומגבלות
- הוסיפו את `.claude/audit.log` ל-`.gitignore` אם אינכם רוצים שהלוג ייכנס ל-Repository.
- פקודת Bash עלולה להכיל סוד שהוקלד בה; החיתוך ל-300 תווים מקטין את הסיכון אך לא מבטל אותו.
- הלוג גדל ללא הגבלה; דאגו ל-Rotation בפרויקטים פעילים.
- PostToolUse לא נורה על כלים שנכשלו; לתיעוד כשלים הוסיפו את אותו Hook גם לאירוע PostToolUseFailure.
