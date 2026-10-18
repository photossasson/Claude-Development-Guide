# מדריך חיבור Connectors צעד אחר צעד (connect-guide.md)

מסמך נלווה לפרק 24 במדריך "מדריך פיתוח ב-Claude Code". מכסה חיבור, אימות, בדיקה וניתוק של Connectors בשלושה משטחים: Claude Web, Claude Desktop ו-Claude Code. כל עובדה מסתמכת על המקורות הרשמיים המפורטים בסוף; מטריצת הזמינות המלאה נמצאת ב-connector-availability-matrix.md. שוחזר ונבדק: 29.07.2026.

## לפני שמתחילים

- ודאו שה-Connector זמין במוצר וב-Plan שלכם לפי מטריצת הזמינות. אין להסיק מ-Claude Web על Claude Code ולהפך.
- החליטו מראש: אילו יכולות קריאה נדרשות, והאם בכלל נדרשת כתיבה. חברו במינימום הדרוש.
- ב-Team/Enterprise: ודאו ש-Owner או Primary Owner הפעיל את ה-Connector ברמת הארגון. חבר צוות ללא הרשאת ניהול יראה כפתור Request במקום Connect, והבקשה נשלחת ל-Admin.

## משטח 1: Claude Web (claude.ai)

1. פתחו את מסך החיבורים: Settings ואז Customize > Connectors, או ישירות בכתובת claude.ai/customize/connectors. דרך חלופית מתוך שיחה: כפתור "+" (או הקלדת "/"), ריחוף על Connectors, ואז Manage connectors.
2. אתרו את ה-Connector ב-Directory לפי שם או קטגוריה. שימו לב לתווית Verified (נסקר על ידי Anthropic) מול Community (בדיקות אוטומטיות בלבד), ולתוויות המוצרים הנתמכים.
3. לחצו Connect. תועברו לדף ההתחברות של הספק (OAuth).
4. קראו את מסך ההסכמה בעיון: הוא מפרט אילו הרשאות מוענקות. אצל חלק מהספקים הניסוח רחב מהמימוש בפועל (Google מציג הרשאת שליחה, אך התיעוד קובע ש-Claude יוצר טיוטות בלבד ואינו שולח; support 10166901).
5. אם אתם מחוברים לכמה חשבונות אצל הספק (אישי וארגוני), בחרו במודע את החשבון הנכון. חיבור חשבון אישי לסביבת עבודה הוא מקור נפוץ לדליפת מידע.
6. אימות: ה-Connector מופיע כמחובר ב-Customize > Connectors, והכלים שלו נראים בתפריט Search and tools בשיחה.
7. שליטה בטעינת כלים (אופציונלי): במוצרי הצ'אט קיימים מצבי Tool access: Auto (ברירת מחדל), Always available, On demand. זהו מנגנון טעינת Context, לא מנגנון הרשאות (support 13730515).

### הוספת Custom connector (שרת MCP מרוחק לפי URL)

- Free/Pro/Max: Customize > Connectors, ואז Add custom connector והזנת ה-URL של שרת ה-MCP. משתמשי Free מוגבלים ל-Custom connector אחד (support 11175166).
- Team/Enterprise: רק Owner מוסיף, דרך Organization settings > Connectors > Add > Custom > Web, הזנת URL ואישור. לאחר מכן כל חבר צוות מתחבר אישית דרך Customize > Connectors > Connect.
- אזהרה רשמית: בפיצ'ר Research, ציטוט: "During the research process, Claude can invoke tools from your connectors automatically without further approval". השביתו כלי כתיבה לפני שימוש ב-Research עם Connectors.

## משטח 2: Claude Desktop

1. Connectors מרוחקים: אותה זרימה כמו ב-Web, דרך Settings > Customize > Connectors. חיבור שבוצע ב-claude.ai נודד עם החשבון.
2. Desktop Extensions (הרחבות מקומיות): מותקנות דרך Settings > Extensions ב-Claude Desktop, כחבילת MCPB. הן רצות מקומית וזמינות רק ב-Claude Desktop וב-Claude Code, לא ב-Web ולא ב-Mobile (support 11725091). הן מעניקות גישה למשאבי המחשב (קבצים, localhost, אפליקציות), ולכן דורשות זהירות כפולה: התקינו רק הרחבות ממקור שאתם סומכים עליו.

## משטח 3: Claude Code

ל-Claude Code שני מסלולים נפרדים אל שירותים חיצוניים. אל תערבבו ביניהם.

### מסלול א: Connectors של claude.ai נטענים אוטומטית

לפי code.claude.com/docs/en/mcp (אומת 28.07.2026):

1. תנאי מוקדם: התחברות ל-Claude Code עם חשבון claude.ai (מנוי). עם ANTHROPIC_API_KEY, Bedrock, Vertex או Token של claude setup-token, ה-Connectors לא נטענים כלל. בדיקה: הקלידו /status וודאו ששיטת האימות הפעילה היא חשבון claude.ai.
2. Connectors בניהול Anthropic, ובהם Microsoft 365, Gmail ו-Google Calendar, אינם תומכים ב-OAuth מקומי מהטרמינל. חברו אותם קודם ב-claude.ai (Settings > Connectors), והם יופיעו אוטומטית ב-Claude Code.
3. הקלידו /mcp כדי לראות את הרשימה: Connectors של claude.ai מופיעים עם סימון מקור. Connectors שמעולם לא השתמשתם בהם מקופלים תחת "Show unused connectors" בסוף הרשימה.
4. סדר עדיפויות בהתנגשות שמות או Endpoints: local, אחר כך project, אחר כך user, אחר כך שרתי Plugins, ורק בסוף Connectors של claude.ai. שרת שהגדרתם ידנית עם אותו Endpoint גובר על ה-Connector, וה-/mcp יציג את הכפילות כמוסתרת.
5. בקרות ארגוניות פר כלי (Always allow / Needs approval / Blocked) נאכפות מקומית ב-Claude Code כ-ask/blocked.

### מסלול ב: הוספה ידנית של שרת מה-Directory (הדרך המתועדת לכלי פיתוח)

תיעוד ה-Directory הרשמי קובע: "Directory connectors use the same MCP infrastructure as Claude Code, so you can add any remote server listed there with claude mcp add". דוגמאות עם Endpoints שאומתו בתיעוד הרשמי של Claude Code:

```bash
# GitHub: שרת רשמי עם Fine-grained PAT (צרו Token מוגבל ל-Repos הדרושים)
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"

# Sentry: שרת רשמי עם OAuth
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
claude mcp login sentry

# Notion: Endpoint רשמי מדוגמאות התיעוד
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Asana: דוגמת SSE מהתיעוד (שימו לב: Transport מסוג SSE מסומן Deprecated, עדיין עובד)
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

פקודות ניהול: claude mcp list (רשימה וסטטוס), claude mcp get NAME (פרטים), claude mcp remove NAME (הסרה), claude mcp login NAME / logout NAME (ניהול OAuth). בתוך Session: /mcp מציג סטטוס, רשימת כלים, אימות מחדש ו-Toggle פר פרויקט.

### שליטה וכיבוי

- הרשאות פר כלי בקובץ settings: חוקי allow/ask/deny על שמות מלאים בתבנית mcp__SERVER__TOOL (את השמות המדויקים רואים ב-/mcp; אל תנחשו). deny גובר על ask, ו-ask גובר על allow.
- כיבוי Connector פר פרויקט: Toggle ב-/mcp (נשמר כ-disabledMcpServers).
- כיבוי כולל של Connectors מ-claude.ai: הגדרת "disableClaudeAiConnectors": true בקובץ settings (true מכל מקור גובר), או משתנה סביבה ENABLE_CLAUDEAI_MCP_SERVERS=false.
- ברמת הארגון: deniedMcpServers לפי שם תצוגה (למשל "claude.ai Slack") או תבנית URL, ו-managed-mcp.json לשליטה בלעדית ברשימת השרתים (code.claude.com/docs/en/managed-mcp).

## אימות מסכם אחרי כל חיבור

הריצו את שמונת התרחישים מקובץ test-scenarios.md. מינימום מיידי: ה-Connector מופיע כמחובר; קריאת בדיקה מחזירה נתון אמיתי; פעולת כתיבה מבקשת אישור; ניתוק ניסיוני מונע גישה בשיחה חדשה.

## ניתוק מלא: תמיד בשני הצדדים

ניתוק בצד Claude אינו בהכרח שולל את הרשאת ה-OAuth אצל הספק. חיבור מת באמת רק אחרי שני שלבים.

### שלב 1: ניתוק בצד Claude

- Claude Web / Desktop: Customize > Connectors, בחירת ה-Connector, Disconnect (או Remove ל-Custom connector). ב-Team/Enterprise, Owner יכול להסיר ברמת הארגון.
- Claude Code, שרת ידני: claude mcp remove NAME (מוחק את התצורה המקומית בלבד; ה-Token או ה-PAT ממשיכים לחיות אצל הספק).
- Claude Code, Connector של claude.ai: הניתוק נעשה ב-claude.ai; מקומית אפשר רק לכבות עם Toggle ב-/mcp או עם disableClaudeAiConnectors.
- Desktop Extension: הסרה דרך Settings > Extensions ב-Claude Desktop.

### שלב 2: שלילת ההרשאה בצד הספק

- Google (Gmail, Calendar, Drive): myaccount.google.com/connections, איתור Claude ושלילת הגישה (מתועד רשמית ב-support 10166901).
- Microsoft 365: ניהול ההסכמות ב-Microsoft Entra. משתמש קצה מסיר דרך פורטל החשבון של הארגון; Admin שולל דרך Enterprise Applications ב-Entra, כולל שלילה סלקטיבית של הרשאות בודדות (support 12542951).
- GitHub: Settings > Applications להסרת הרשאות OAuth/GitHub App; עבור שרת ה-MCP עם PAT: Settings > Developer settings > Fine-grained personal access tokens > Revoke.
- Slack, Notion ושירותים אחרים: מסך Authorized apps (או Connected apps) בהגדרות החשבון או ה-Workspace אצל הספק.
- Enterprise-managed auth (Beta): ציטוט רשמי: "Revoke access by deprovisioning someone in your identity provider, which removes their connector access at the same time" (support 15537633). Sessions קיימים מסתיימים כשה-Tokens פגים או נשללים.

### שלב 3: אימות הניתוק

פתחו שיחה חדשה ובקשו נתון מהשירות המנותק. תשובה תקינה: אין שרת או כלי זמינים. אם הנתון עדיין מגיע, אחד הצדדים לא נותק.

## הערת Offboarding ארגוני

עזיבת עובד מחייבת שלושה צעדים: השבתת חשבון ה-claude.ai; שלילת הרשאות בצד כל ספק (או Deprovisioning ב-IdP תחת Enterprise-managed auth); וסריקת Tokens ארוכי חיים שנוצרו ידנית, כמו PAT של GitHub.

## מקורות

- https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/11724452-browsing-and-connecting-to-tools-from-the-directory (נבדק: 28.07.2026)
- https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/10166901-use-google-workspace-connectors (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/13730515-manage-claude-s-tool-access (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/15537633-authorize-mcp-connectors-for-your-entire-organization (נבדק: 29.07.2026)
- https://code.claude.com/docs/en/mcp (נבדק: 28.07.2026)
- https://code.claude.com/docs/en/managed-mcp (נבדק: 28.07.2026)
- https://claude.com/docs/connectors/directory (נבדק: 28.07.2026)
