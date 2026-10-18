# Database Read-Only MCP (DBHub)

## הסבר שדות

- command/args: @bytebase/dbhub@1.0.0 (גרסה מוצמדת) עם --config שמצביע על dbhub.toml.
- env.DSN: מחרוזת החיבור עוברת דרך env (לא args, שגלוי ברשימת התהליכים).
- dbhub.toml: כלי execute_sql מוגדר readonly = true.
- הערת גרסה: ב-1.0.0 הדגל הישן --readonly הוסר; משתמשים בתחביר TOML. נדרש Node.js 22.5.0 ומעלה.

## אבטחה והרשאה מינימלית

שלוש שכבות: (1) תפקיד SELECT בלבד: CREATE ROLE claude_ro LOGIN PASSWORD 'YOUR_PASSWORD'; GRANT CONNECT ON DATABASE taskflow TO claude_ro; GRANT USAGE ON SCHEMA public TO claude_ro; GRANT SELECT ON ALL TABLES IN SCHEMA public TO claude_ro; (2) readonly=true ב-DBHub; (3) כלל ask ב-Claude Code. העדיפו Replica/Staging על פני Production.

## הבדלי מערכות הפעלה

Bash: export TASKFLOW_DB_RO_DSN="postgres://claude_ro:YOUR_PASSWORD@localhost:5432/taskflow"
PowerShell: [Environment]::SetEnvironmentVariable("TASKFLOW_DB_RO_DSN", "postgres://claude_ro:YOUR_PASSWORD@localhost:5432/taskflow", "User")

## התקנה

העתיקו את .mcp.json לשורש הפרויקט (או מזגו לקיים), הגדירו את משתני הסביבה, ופתחו Session חדש. בדקו עם `claude mcp list`. מקור: פרק 23 במדריך; נבדק 28.07.2026.
