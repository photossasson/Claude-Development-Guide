# secrets-scan

## מה ה-Hook עושה
Hook מסוג <b>PreToolUse</b> עם Matcher של `Write|Edit`: לפני כל כתיבה, הסקריפט סורק את התוכן שעומד להיכתב (`tool_input.content` בכלי Write ו-`tool_input.new_string` בכלי Edit) מול דפוסי Regex של סודות: מפתחות AWS, GitHub Tokens, מפתחות Anthropic ו-OpenAI, Slack Tokens, בלוקים של Private Key, JWT והשמות מוקשחות בסגנון `api_key = "..."`.

כשנמצא סוד סביר, הכתיבה נדחית עם `permissionDecision: "deny"` והנימוק (`permissionDecisionReason`) מוזן חזרה ל-Claude עם הנחיה להשתמש במשתני סביבה במקום.

## פרטיות בתכנון
הנימוק מציין את שם הדפוס ואת מספר השורה בלבד, לעולם לא את הערך שנתפס, כדי שהסוד לא יהדהד חזרה לשיחה או לקבצי Log. דפוסי Placeholder מובהקים (למשל `YOUR_API_KEY`) לא נחשבים סודות.

## התקנה
```bash
mkdir -p .claude/hooks
cp secrets_scan.py .claude/hooks/
chmod +x .claude/hooks/secrets_scan.py
```
מזגו את `hooks.json` לתוך `.claude/settings.json` ואמתו עם `/hooks`.

## סיכונים ומגבלות
- זיהוי מבוסס Regex מייצר גם False Positives (למשל מחרוזת אקראית ארוכה) וגם False Negatives (סוד בפורמט לא מוכר). זו שכבת הגנה, לא ערובה.
- הסריקה מכסה רק את הכלים Write ו-Edit; כתיבה דרך Bash לא נסרקת.
- ה-Hook לא סורק קבצים קיימים, רק תוכן חדש שנכתב. לסריקת Repository מלאה השתמשו בכלי ייעודי כמו gitleaks ב-CI.
