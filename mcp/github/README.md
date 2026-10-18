# GitHub MCP (שרת רשמי מרוחק)

## הסבר שדות

- type: "http": שרת מתארח מרוחק; ה-Transport המומלץ.
- url: הכתובת הרשמית המתועדת https://api.githubcopilot.com/mcp/.
- headers.Authorization: Personal Access Token דרך משתנה הסביבה GITHUB_MCP_PAT; הקובץ נקי מסודות.

## אבטחה והרשאה מינימלית

צרו Fine-grained PAT מוגבל ל-Repositories ספציפיים עם הרשאות Read בלבד (Contents, Issues, Pull requests). הוסיפו Write רק אם רוצים ש-Claude ייצור PRs. תוכן Issues ו-PRs הוא קלט לא מהימן.

## הבדלי מערכות הפעלה

Bash: export GITHUB_MCP_PAT="YOUR_GITHUB_PAT"
PowerShell: [Environment]::SetEnvironmentVariable("GITHUB_MCP_PAT", "YOUR_GITHUB_PAT", "User")

## התקנה

העתיקו את .mcp.json לשורש הפרויקט (או מזגו לקיים), הגדירו את משתני הסביבה, ופתחו Session חדש. בדקו עם `claude mcp list`. מקור: פרק 23 במדריך; נבדק 28.07.2026.
