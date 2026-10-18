# Docs Source MCP (רשמי + Filesystem)

## הסבר שדות

- claude-code-docs: שרת התיעוד הרשמי המתארח, ללא אימות.
- project-docs: @modelcontextprotocol/server-filesystem@2026.7.10; כל ארגומנט אחרי שם החבילה הוא תיקייה מורשית; כאן docs/ בלבד.

## אבטחה והרשאה מינימלית

שרת ה-Filesystem כולל כלי כתיבה. הוסיפו ל-.claude/settings.json: "deny": ["mcp__project-docs__write_file", "mcp__project-docs__edit_file", "mcp__project-docs__move_file", "mcp__project-docs__create_directory"].

## הבדלי מערכות הפעלה

הפקודות זהות; רק כתיב נתיבים שונה (./docs מול .\docs).

## התקנה

העתיקו את .mcp.json לשורש הפרויקט (או מזגו לקיים), הגדירו את משתני הסביבה, ופתחו Session חדש. בדקו עם `claude mcp list`. מקור: פרק 23 במדריך; נבדק 28.07.2026.
