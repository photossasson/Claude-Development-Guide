# risk-guard: ‏Mod לדוגמה

Mod של Claude Code ‏(2.1.287 ומעלה, נבדק ב-2.1.301) שעוצר פקודות Bash שקשה לבטל (`rm -rf`, ‏`git push --force`, ‏`git reset --hard`, ‏`git clean -f`), שואל את המשתמש, וסופר מה נעצר.

| קובץ | תפקיד |
|---|---|
| `.claude-plugin/plugin.json` | שם, גרסה, חוזה ה-types ואפשרות `mode` (ask או deny) |
| `hooks/hooks.json` | מצביע על מודול ה-hooks: `{ "modules": ["./register.tsx"] }` |
| `hooks/register.tsx` | השומר על `tool.call`, הפקודה `/guard-status` ופס מעל שורת הפרומפט |
| `hooks/risk.ts` | רשימת הדפוסים המסוכנים |
| `types/index.d.ts` | החוזה של הערכים ב-`$.state` |
| `tests/risk-guard.test.ts` | ארבע בדיקות ל-`claude plugin test` |

## הרצה

```bash
claude plugin validate risk-guard
claude plugin test risk-guard
claude --plugin-dir ./risk-guard          # סשן אינטראקטיבי עם טעינה מחדש בשמירה
claude -p "/guard-status" --plugin-dir ./risk-guard
```

## שימו לב

* Mod רץ בלי sandbox, עם ההרשאות שלכם. קראו את הקוד של כל Mod לפני שמפעילים אותו.
* ב-`claude -p` אין את מי לשאול. `$.ui.ask` נדחה, והשומר חוסם.
* השומר מחליט לפני `next(e)`, ולכן ה-`.catch` יכול להחזיר `{ deny }` אם משהו נשבר.
