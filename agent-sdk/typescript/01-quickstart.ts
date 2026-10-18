/**
 * 01-quickstart.ts
 *
 * Minimal Claude Agent SDK example (TypeScript), matching the official
 * quickstart and chapter 31 of the guide (מדריך פיתוח ב-Claude Code).
 *
 * What it does:
 *   Asks the agent to review utils.py in the current directory for bugs that
 *   would cause crashes and fix them. Read/Edit/Glob are auto-approved and
 *   file edits are auto-accepted (permissionMode: "acceptEdits").
 *
 * Prerequisites:
 *   npm install                       # @anthropic-ai/claude-agent-sdk (pinned)
 *   export ANTHROPIC_API_KEY=...      # or a claude.ai login via `claude`
 *   Create utils.py next to this file (see the official quickstart), then:
 *   npx tsx 01-quickstart.ts
 *
 * Verified against:
 *   https://code.claude.com/docs/en/agent-sdk/typescript (checked 29.07.2026)
 *   Package: @anthropic-ai/claude-agent-sdk 0.3.233 (tsc --noEmit strict;
 *   no API execution inside the authoring sandbox, see qa-findings F-001).
 */

import { query } from "@anthropic-ai/claude-agent-sdk";

const PROMPT =
  "Review utils.py for bugs that would cause crashes. Fix any issues you find.";

async function main(): Promise<void> {
  for await (const message of query({
    prompt: PROMPT,
    options: {
      allowedTools: ["Read", "Edit", "Glob"], // auto-approve these tools
      permissionMode: "acceptEdits", // auto-accept file edits
      maxTurns: 10, // hard stop for the agentic loop
    },
  })) {
    if (message.type === "assistant" && message.message?.content) {
      for (const block of message.message.content) {
        if ("text" in block) {
          console.log(block.text); // Claude's explanation
        } else if ("name" in block) {
          console.log(`Tool: ${block.name}`); // a tool call
        }
      }
    } else if (message.type === "result") {
      console.log(`Done: ${message.subtype}`); // "success" or an error subtype
      console.log(
        `Cost: $${message.total_cost_usd.toFixed(4)} | turns: ${message.num_turns}`,
      );
    }
  }
}

main().catch((err: unknown) => {
  console.error(err);
  process.exitCode = 1;
});
