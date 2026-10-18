# Monitoring MCP (Sentry)

## הסבר שדות

- type: "http", url: https://mcp.sentry.dev/mcp. שני שדות; אין Token בקובץ.
- אימות: אחרי ההוספה השרת ב-Needs authentication; claude mcp login sentry או /mcp ואז Authenticate. אפשר להצמיד oauth.scopes.

## אבטחה והרשאה מינימלית

הודעות שגיאה מ-Production הן קלט לא מהימן. תוצאות ניטור גדולות; בקשו שאילתות ממוקדות (MAX_MCP_OUTPUT_TOKENS).

## הבדלי מערכות הפעלה

זהה בכל מערכות ההפעלה.

## התקנה

העתיקו את .mcp.json לשורש הפרויקט (או מזגו לקיים), הגדירו את משתני הסביבה, ופתחו Session חדש. בדקו עם `claude mcp list`. מקור: פרק 23 במדריך; נבדק 28.07.2026.
