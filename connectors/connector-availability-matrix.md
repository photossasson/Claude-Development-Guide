# מטריצת זמינות Connectors (connector-availability-matrix.md)

מסמך עבודה של המדריך "מדריך פיתוח ב-Claude Code". המטריצה מרכזת את כל ה-Connectors שאומתו פוזיטיבית מול מקורות רשמיים בלבד, עם מקור ותאריך לכל שורה. שוחזר ב-29.07.2026 לאחר אובדן קבצים (ראו F-017 ב-qa-findings), על בסיס control/mcp-connectors-matrix.md (אימות מקורי: 28.07.2026) ואחזור חוזר של מקורות ב-29.07.2026.

## מתודולוגיית אימות

- כל תא בטבלה נתמך במקור רשמי: support.claude.com, claude.com/connectors, claude.com/docs/connectors/directory, או code.claude.com/docs.
- תא שלא נמצא לו מקור רשמי מסומן "לא אומת". עדיף חור מסומן מאשר עובדה מומצאת.
- מקורות שאוחזרו מחדש ב-29.07.2026: מאמרי support מספר 10166901, 12542951, 11176164, 11725091, 11175166, 15537633, 13730515, וכן דפי claude.com/connectors/slack ו-claude.com/connectors/notion.
- מאמר 11724452 (Directory) לא היה נגיש לאחזור חוזר ב-29.07.2026 (חסימת Proxy בסביבת העבודה); הציטוטים ממנו מובאים כפי שאומתו חיים ב-28.07.2026 ותועדו ב-control/mcp-connectors-matrix.md וב-ch24.
- "Claude" בעמודת המוצרים פירושו האפליקציה ב-claude.ai (Web).

## מטריצת הזמינות

| שם רשמי | מוצרי Claude נתמכים | דרישת Plan | מנגנון Auth | יכולות קריאה | יכולות כתיבה / Action | אישור Admin | מגבלות ידועות | מקור (URL) | תאריך אימות |
|---|---|---|---|---|---|---|---|---|---|
| Gmail | "all users on Claude and Claude Desktop"; ב-Claude Code רק דרך חיבור מוקדם ב-claude.ai (טעינה אוטומטית עם התחברות מנוי) | כל המשתמשים (ציטוט הזמינות משמאל) | OAuth (Google), פר משתמש | חיפוש וקריאת מיילים בשפה טבעית, Metadata של מיילים וקבצים מצורפים, רשימת טיוטות, Labels, Threads | טיוטות בלבד. ציטוט: "Claude creates drafts in your Gmail account, but cannot send emails on your behalf" | ב-Team/Enterprise נדרשת הפעלה ארגונית על ידי Owner/Primary Owner; ייתכן סימון Trusted ב-Google Admin | תוכן קבצים מצורפים אינו נגיש (Metadata בלבד); מגבלות Rate של Google API | https://support.claude.com/en/articles/10166901-use-google-workspace-connectors | 29.07.2026 |
| Google Calendar | "all users on Claude and Claude Desktop"; ב-Claude Code דרך claude.ai (כמו Gmail) | כל המשתמשים | OAuth (Google), פר משתמש | צפייה באירועים, יומנים משותפים, איתור זמינות הדדית | יצירה, עדכון ומחיקה של אירועים; ניהול משתתפים; מענה להזמנות; פגישות חוזרות | Owner ב-Team/Enterprise | מחיקת אירועים היא פעולה הרסנית; מגבלות Rate של Google API | https://support.claude.com/en/articles/10166901-use-google-workspace-connectors | 29.07.2026 |
| Google Drive | "all users on Claude and Claude Desktop" | כל המשתמשים | OAuth (Google), פר משתמש | חיפוש ואחזור Docs; קריאת Sheets, Slides, PDF, תמונות, קובצי Office; צפייה בהרשאות; שינויים אחרונים | העלאת קבצים (עם המרה אוטומטית), יצירת תיקיות, הוספת קבצים ל-Chats ול-Projects, שמירת קבצים ש-Claude יצר (בהפעלת Code execution) | Owner ב-Team/Enterprise; ייתכן סימון Trusted ב-Google Admin | חילוץ טקסט בלבד מקבצים; תמונות מוטמעות ב-Docs אינן מעובדות; מגבלות Rate של Google | https://support.claude.com/en/articles/10166901-use-google-workspace-connectors | 29.07.2026 |
| Microsoft 365 | Claude (Web, דרך Customize > Connectors); ב-Claude Code רק דרך חיבור ב-claude.ai (אין OAuth מקומי מהטרמינל) | ציטוט: "The Microsoft 365 connector is available on all Claude plans: Free, Pro, Max, Team, and Enterprise" | OAuth 2.0 דרך Microsoft Entra ID + הסכמת Tenant חד פעמית של Global Administrator; חשבונות Microsoft אישיים (outlook.com, hotmail.com) אינם נתמכים | Outlook (הודעות, Metadata, תיבות משותפות, תיקיות), יומן (כולל יומנים משותפים), Teams (צ'אטים, ערוצים, תמלולים, הקלטות), קבצי OneDrive ו-SharePoint בכל ה-Tenant | Opt-in נפרד ב-Re-consent ארגוני: שליחה והעברה של מייל, טיוטות, Rules; יצירה/עדכון/מחיקה/מענה ביומן; יצירה ועדכון קבצים. מיילים שנשלחים כוללים Header ייחוס: "Emails Claude sends include an attribution header identifying them as agent-initiated" | כן: Entra Global Administrator (הסכמה ראשונית + Re-consent לכתיבה); צמצום לקבוצות משתמשים דרך Enterprise Applications | קבצים מצורפים אינם נתמכים בכלי כתיבה; אין שליחת הודעות Teams; אין הגבלת חיפוש ל-Site ספציפי ב-SharePoint; מגבלות כתיבה פר משתמש | https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector | 29.07.2026 |
| Slack | לפי הדף הרשמי (Used in): Claude, Claude Desktop, Claude Mobile, Claude Code, Claude API | לא אומת (לא צוין בדף הרשמי; ראו F-015) | לא צוין מפורשות בדף ה-Connector; מנגנון ה-Connectors הכללי הוא OAuth פר משתמש עם ירושת הרשאות (support 11176164) | חיפוש ואחזור: הודעות, ערוצים, Threads, קבצים, משתמשים | טיוטת הודעה ועריכה לפני שליחה, שליחה, תזמון הודעות, יצירת Canvas ושיתופו לערוץ | הפעלה ארגונית ב-Team/Enterprise (כלל כללי); ב-Enterprise-managed auth מסומן "coming soon" | הודעה מתוזמנת נערכת או מבוטלת רק דרך "Drafts and sent" של Slack עצמו, לא דרך Claude | https://claude.com/connectors/slack | 29.07.2026 |
| Notion | לפי הדף הרשמי: Claude, Claude Desktop, Claude Mobile, Claude Code, Claude API; Endpoint רשמי mcp.notion.com/mcp מתועד בדוגמאות code.claude.com/docs/en/mcp | לא אומת (לא צוין בדף הרשמי) | OAuth (Notion; שרת "Made by Notion"); ב-Claude Code גם חיבור ידני עם claude mcp add | חיפוש בעמודים ובכל ה-Workspace, אחזור תוכן | Read & write: יצירת עמודים עם תוכן מובנה, עריכה, עדכון Properties (למשל שינוי Status של משימה) | כלל Team/Enterprise הכללי (הפעלה על ידי Owner) | לא תועדו מגבלות בדף הרשמי; לא אומת | https://claude.com/connectors/notion | 29.07.2026 |
| Linear | מופיע ב-Directory; פירוט Surfaces פר מוצר: לא אומת | לא אומת (כפוף לסתירת הניסוחים, ראו F-014) | OAuth פר משתמש; נתמך ב-Enterprise-managed auth דרך Okta (Beta) | קריאת Issues (נגזר מדוגמת השימוש הרשמית) | יצירת Issue: "Create a new issue" מופיעה כדוגמה רשמית במאמר ה-Directory | מנגנון Request לחברי Team ללא הרשאת ניהול; ב-Enterprise-managed auth הרשאה מרוכזת דרך ה-IdP | לא אומת | https://support.claude.com/en/articles/11724452-browsing-and-connecting-to-tools-from-the-directory + https://support.claude.com/en/articles/15537633-authorize-mcp-connectors-for-your-entire-organization | 28.07.2026 (Directory); 29.07.2026 (Ent-auth) |
| Asana | מופיע ב-Directory; ב-Claude Code דרך Endpoint רשמי mcp.asana.com/sse (דוגמת SSE בתיעוד Claude Code) | לא אומת | OAuth; נתמך ב-Enterprise-managed auth דרך Okta (Beta) | לא אומת (לא פורט במקורות שאוחזרו) | לא אומת | כלל Team/Enterprise הכללי; Enterprise-managed auth זמין | Transport מסוג SSE מסומן Deprecated בתיעוד Claude Code (עדיין עובד) | https://code.claude.com/docs/en/mcp + https://support.claude.com/en/articles/15537633-authorize-mcp-connectors-for-your-entire-organization | 28.07.2026 (Endpoint); 29.07.2026 (Ent-auth) |
| Sentry | Claude Code (Endpoint רשמי mcp.sentry.dev/mcp בתיעוד Claude Code); מופיע גם ב-Directory | לא אומת | OAuth 2.0 דרך /mcp או claude mcp login | שגיאות, Stack traces, Deployments (לפי דוגמאות התיעוד הרשמי של Claude Code) | לא אומת | לא אומת | לא אומת | https://code.claude.com/docs/en/mcp | 28.07.2026 |
| Atlassian | מופיע ב-Directory וברשימת Enterprise-managed auth; פירוט Surfaces: לא אומת | לא אומת | OAuth; נתמך ב-Enterprise-managed auth דרך Okta (Beta) | לא אומת | לא אומת | כלל Team/Enterprise הכללי; Enterprise-managed auth זמין | כתובת Endpoint של הספק לא נכללת כאן: לא אומתה מול מקור רשמי (ראו F-012) | https://support.claude.com/en/articles/15537633-authorize-mcp-connectors-for-your-entire-organization | 29.07.2026 (Ent-auth); 28.07.2026 (Directory) |
| GitHub (שרת MCP רשמי מרוחק) | Claude Code (חיבור ידני: claude mcp add אל https://api.githubcopilot.com/mcp/) | אין דרישת Plan מתועדת | Fine-grained Personal Access Token ב-Header (Authorization: Bearer), לא OAuth ולא Connector של claude.ai | Pull Requests, Issues, קוד (בגבולות הרשאות ה-PAT) | יצירת Issues ופתיחת Pull Requests (דוגמאות רשמיות בתיעוד), בגבולות הרשאות ה-PAT | אין אישור Admin ייעודי; כפוף למדיניות MCP ארגונית (managed-mcp.json, deniedMcpServers) | היקף היכולות נגזר כולו מהיקף ה-PAT; ניתוק מלא מחייב גם Revoke של ה-PAT ב-GitHub | https://code.claude.com/docs/en/mcp | 28.07.2026 |
| GitHub (Integration ב-Chats/Projects) | Claude (Web) בלבד: Chats ו-Projects | לא צוין; לא אומת | GitHub App | קבצי Repository בלבד, עם Sync ידני | אין. ללא Pull Requests, ללא Commits, ללא Metadata (גבול מוצר מובחן משרת ה-MCP) | ייתכן אישור Admin ברמת ה-Organization ב-GitHub | הנתונים מתעדכנים רק ב-Sync ידני; קריאה בלבד | https://support.claude.com/en/articles/10167454-use-the-github-integration | 28.07.2026 |
| Desktop Extensions (למשל Filesystem) | ציטוט: "Desktop extensions run locally and are only available in Claude Desktop and Claude Code"; לא ב-Web ולא ב-Mobile | כל המשתמשים: "Desktop extensions are available to all users on Claude Desktop" (כולל Free) | התקנה מקומית (חבילת MCPB) דרך Claude Desktop: Settings > Extensions; ללא OAuth ענן | משאבים מקומיים: קבצים, בסיסי נתונים ב-localhost, אפליקציות Desktop, גישה ברמת מערכת ההפעלה | תלוי בהרחבה הספציפית | אין (התקנה אישית מקומית) | רצות מקומית עם הרשאות המשתמש במחשב; משטח סיכון מקומי מלא | https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors + https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities | 29.07.2026 |

## הערת סתירת ניסוחים (F-014, נרשם ב-qa-findings)

שני מאמרי עזרה רשמיים מנסחים את דרישת ה-Plan אחרת:

- מאמר 11176164 (אוחזר מחדש 29.07.2026): "Web connectors are available for all users on Claude, Cowork, Claude Desktop, and Claude Mobile (iOS and Android)."
- מאמר 11724452 (אומת חי 28.07.2026; אחזור חוזר ב-29.07.2026 נכשל בשל חסימת Proxy): "Remote connectors are available to users on Claude Pro, Max, Team, and Enterprise plans."

הכרעה מעשית מחייבת במדריך: הניסוח פר Connector הוא הקובע. Microsoft 365 זמין מפורשות בכל ה-Plans כולל Free; Google Workspace זמין "for all users on Claude and Claude Desktop". היכן שאין ניסוח פר Connector, עמודת ה-Plan מסומנת "לא אומת".

## הערת תיחום מקור (F-016)

מאמר support מספר 14503689 ("MCP connectors") עוסק ב-Claude for Government בלבד (גבול FedRAMP High; Microsoft 365, Web Search ושרתים מותאמים; הפעלה ארגונית + OAuth פר משתמש). אין לצטט אותו לטענות זמינות במוצר המסחרי של Claude. תועד ב-qa-findings כ-F-016.

## הערות רוחב נוספות

- הקטלוג הרשמי claude.com/connectors מציג תוויות זמינות פר מוצר לכל Connector; באימות 28.07.2026 נמצאו Connectors המסומנים "Claude" בלבד ללא "Claude Code" (למשל Amplitude ו-Adobe for creativity). אין להסיק זמינות ב-Claude Code מזמינות ב-Web.
- Connector מוגדר רשמית: "Connectors let Claude access your apps and services, retrieve your data, and take actions within connected services" (support 11176164). Claude יורש את הרשאות המשתמש בשירות המחובר.
- תיעוד ה-Directory קובע: "The Connectors Directory is a catalog of MCP servers that work across all Claude products", ותיעוד Claude Code מגדיר Connectors כ-"MCP servers you've added in claude.ai" (אומת 28.07.2026).
- Custom connectors: "available on Claude, Cowork, and Claude Desktop for users on Free, Pro, Max, Team, and Enterprise plans. Free users are limited to one custom connector" (support 11175166, אוחזר מחדש 29.07.2026).
- מצבי Tool access (Auto / Always available / On demand) הם מנגנון טעינת Context במוצרי הצ'אט, לא מנגנון הרשאות (support 13730515, אוחזר מחדש 29.07.2026).
- Enterprise-managed auth: Beta בהרשמה, Team/Enterprise בלבד, Okta כספק ההשקה; Connectors נתמכים: Asana, Atlassian, Canva, Figma, Granola, Linear, Supabase; Slack מסומן "coming soon" (support 15537633, אוחזר מחדש 29.07.2026).

## מקורות

- https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/11724452-browsing-and-connecting-to-tools-from-the-directory (נבדק: 28.07.2026; אחזור חוזר נכשל 29.07.2026)
- https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/10166901-use-google-workspace-connectors (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/10167454-use-the-github-integration (נבדק: 28.07.2026)
- https://support.claude.com/en/articles/13730515-manage-claude-s-tool-access (נבדק: 29.07.2026)
- https://support.claude.com/en/articles/15537633-authorize-mcp-connectors-for-your-entire-organization (נבדק: 29.07.2026)
- https://claude.com/connectors/slack (נבדק: 29.07.2026)
- https://claude.com/connectors/notion (נבדק: 29.07.2026)
- https://claude.com/docs/connectors/directory (נבדק: 28.07.2026)
- https://code.claude.com/docs/en/mcp (נבדק: 28.07.2026)
- https://code.claude.com/docs/en/managed-mcp (נבדק: 28.07.2026)
