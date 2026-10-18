# block-dangerous-commands

## מה ה-Hook עושה
Hook מסוג <b>PreToolUse</b> עם Matcher של `Bash`: לפני כל פקודת Shell, הסקריפט בודק את הפקודה וחוסם שלושה דפוסים הרסניים:
1. מחיקה רקורסיבית כפויה של שורש או תיקיית הבית (`rm -rf /`, `rm -rf ~`, `rm -rf $HOME` וכן הלאה);
2. Force Push ל-main או ל-master (כולל `-f`, `--force` ו-Refspec עם `+`);
3. הזרמת הורדה מהאינטרנט ישירות ל-Shell (בסגנון `curl ... | bash`).

החסימה נעשית עם JSON מובנה: `permissionDecision: "deny"` ועימו `permissionDecisionReason` שמוזן חזרה ל-Claude. חסימת PreToolUse נאכפת בכל Permission Mode, כולל `bypassPermissions`.

## עיצוב בטוח (חשוב)
- הסקריפט רק קורא JSON מ-stdin ומדפיס החלטה ל-stdout. הוא לעולם לא מריץ את הפקודה הנבדקת ואין לו שום Side Effect.
- הוא רק חוסם, לעולם לא מאשר: כשאין התאמה הוא מסיים עם Exit Code 0 בלי פלט, ומנגנון ה-Permissions הרגיל ממשיך לפעול כרגיל.
- קלט לא תקין לא חוסם את העבודה: הסקריפט יוצא עם קוד 1 (שגיאה לא חוסמת) כדי שהתקלה תהיה גלויה.

## התקנה
```bash
mkdir -p .claude/hooks
cp block_dangerous_commands.py .claude/hooks/
chmod +x .claude/hooks/block_dangerous_commands.py
```
מזגו את `hooks.json` לתוך `.claude/settings.json` ואמתו עם `/hooks`.

## סיכונים ומגבלות
- זו רשימת חסימה (Denylist), לא רשימת היתר: פקודה הרסנית שלא ברשימה תעבור. זו שכבת הגנה נוספת, לא תחליף לחוקי Permissions ולגיבויים.
- `git push --force` בלי ציון Branch לא נחסם, כי הסקריפט לא יודע על איזה Branch אתם נמצאים.
- ניתוח הפקודה הוא טקסטואלי; עטיפות מתוחכמות (למשל `bash -c "..."` עם מחרוזת מוצפנת) עלולות לחמוק.
