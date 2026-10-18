# Hebrew style rules

## Contents
- E001, E002, E003: long dashes
- W001: space before punctuation
- W002: double space
- W003: missing space after punctuation
- W004: space around the hyphen after a Hebrew prefix
- W005: spaced hyphen used as a dash

## E001, E002, E003: long dashes

Em dash (U+2014), en dash (U+2013) and other long dashes (U+2012, U+2015,
U+2E3A, U+2E3B, U+FE58) are not allowed anywhere in the text.
Rewrite the sentence instead of swapping the character.

| Before | After |
| --- | --- |
| `ה-Skill נטען רק כשצריך — וזה חוסך Tokens.` | `ה-Skill נטען רק כשצריך, וזה חוסך Tokens.` |
| `שלושה מיקומים — אישי, פרויקט ו-Plugin.` | `שלושה מיקומים: אישי, פרויקט ו-Plugin.` |
| `גרסאות 2.1.200–2.1.300` | `גרסאות 2.1.200 עד 2.1.300` |

## W001: space before punctuation

A period, comma, colon, semicolon, question mark or exclamation mark attaches to
the word before it.

| Before | After |
| --- | --- |
| `מפעילים את ה-Skill .` | `מפעילים את ה-Skill.` |

## W002: double space

Use one space between words.

## W003: missing space after punctuation

After a comma, semicolon or colon that is followed by a Hebrew word, add one space.

| Before | After |
| --- | --- |
| `Skill,Hook,MCP ו-Plugin` | `Skill, Hook, MCP ו-Plugin` |
| `שימו לב:הקובץ חייב...` | `שימו לב: הקובץ חייב...` |

## W004: space around the hyphen after a Hebrew prefix

A Hebrew prefix letter (ב, ה, ו, כ, ל, מ, ש) joins an English term with a hyphen
and no spaces.

| Before | After |
| --- | --- |
| `ה - Skill` | `ה-Skill` |
| `ב - Claude Code` | `ב-Claude Code` |

## W005: spaced hyphen used as a dash

A hyphen with a space on both sides between Hebrew words is a dash in disguise.
Rewrite it the same way as E001.

| Before | After |
| --- | --- |
| `התיאור קובע הכול - בלי תיאור טוב אין הפעלה.` | `התיאור קובע הכול: בלי תיאור טוב אין הפעלה.` |
