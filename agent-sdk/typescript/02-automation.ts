/**
 * 02-automation.ts
 *
 * Batch processing with the Claude Agent SDK (TypeScript): run the same
 * read-only scan over many repositories with a double budget, one cap per
 * repository and one cap for the whole batch. Companion file for chapter 33
 * of the guide (מדריך פיתוח ב-Claude Code), section "עיבוד אצווה על הרבה
 * Repositories"; it is the SDK version of the batch-scan.sh pattern there.
 *
 * What it does, for every subdirectory of the repositories root:
 *   - Runs one query() with read-only tools (Read, Grep, Glob) in dontAsk
 *     mode, so anything not pre-approved is denied without a prompt.
 *   - Loads no filesystem settings (settingSources: []), the SDK equivalent
 *     of `claude --bare`: hooks, plugins and CLAUDE.md of scanned
 *     repositories cannot change the agent's behavior.
 *   - Asks for structured output (TODO/FIXME count, files whose functions
 *     have no tests, a short report) validated against REPORT_SCHEMA.
 *   - Writes reports/<repo>.md, accumulates the estimated cost, and stops the
 *     batch before the next repository once the total budget is reached.
 *   - Runs sequentially on purpose: it spreads load, respects rate limits and
 *     keeps the cost accounting readable.
 *   - A failure in one repository is logged and the batch continues.
 *
 * Usage:
 *   npm install
 *   export ANTHROPIC_API_KEY=your-api-key        # or a claude.ai login via `claude`
 *   npx tsx 02-automation.ts --root ~/work/repos --out reports
 *   npx tsx 02-automation.ts --root ~/work/repos --total-budget 2 --per-repo-budget 0.20
 *
 * Exit codes: 0 all repositories scanned, 1 at least one repository failed
 * or the batch stopped on budget, 2 bad usage.
 *
 * Read-only by design. If a batch ever needs to write (for example fixing a
 * config file everywhere), turn every change into its own branch and pull
 * request; never let a batch write to main directly.
 *
 * Verified against:
 *   https://code.claude.com/docs/en/agent-sdk/typescript (checked 29.07.2026)
 *   https://code.claude.com/docs/en/agent-sdk/structured-outputs
 *   https://code.claude.com/docs/en/agent-sdk/cost-tracking
 *   Package: @anthropic-ai/claude-agent-sdk 0.3.233. Rebuilt 18.10.2026 from
 *   the description in chapter 33; tsc --noEmit strict against the installed
 *   package. No end-to-end run against the API in the authoring environment
 *   (no API key), see qa-findings F-001.
 */

import { mkdir, readdir, stat, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { basename, join, resolve } from "node:path";
import { parseArgs } from "node:util";

import { query } from "@anthropic-ai/claude-agent-sdk";
import type { Options, SDKResultMessage } from "@anthropic-ai/claude-agent-sdk";

// ---------------------------------------------------------------------------
// Configuration and guardrails
// ---------------------------------------------------------------------------

const DEFAULT_TOTAL_BUDGET_USD = 5.0; // cap for the whole batch (client-side estimate)
const DEFAULT_PER_REPO_BUDGET_USD = 0.25; // cap for one repository, enforced by the SDK
const MAX_TURNS_PER_REPO = 10;
const REPO_TIMEOUT_MS = 10 * 60 * 1000; // abort a single repository after 10 minutes

const ALLOWED_TOOLS = ["Read", "Grep", "Glob"];
const DENIED_TOOLS = [
  "Bash", // bare names remove the tools from the context entirely
  "Edit",
  "Write",
  "WebFetch",
  "WebSearch",
  "Read(.env)",
  "Read(**/.env)",
];

const PROMPT =
  "Scan this repository, read-only. Count TODO and FIXME comments in source " +
  "files (ignore dependencies, build output and vendored code). List source " +
  "files that define functions none of which is exercised by any test. " +
  "Finish with a short report of at most ten lines for a maintainer.";

const REPORT_SCHEMA = {
  type: "object",
  properties: {
    todo_count: { type: "number" },
    fixme_count: { type: "number" },
    untested_files: { type: "array", items: { type: "string" } },
    report: { type: "string" },
  },
  required: ["todo_count", "fixme_count", "report"],
} as const;

interface ScanReport {
  todo_count: number;
  fixme_count: number;
  untested_files?: string[];
  report: string;
}

interface RepoOutcome {
  repo: string;
  status: "ok" | "failed" | "skipped";
  costUsd: number;
  turns: number;
  detail: string;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function expandHome(path: string): string {
  return path === "~" || path.startsWith("~/") ? join(homedir(), path.slice(1)) : path;
}

function parseBudget(value: string | undefined, fallback: number, name: string): number {
  if (value === undefined) return fallback;
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    throw new Error(`--${name} must be a positive number, got "${value}"`);
  }
  return parsed;
}

function isScanReport(value: unknown): value is ScanReport {
  if (typeof value !== "object" || value === null) return false;
  const v = value as Record<string, unknown>;
  return (
    typeof v.todo_count === "number" &&
    typeof v.fixme_count === "number" &&
    typeof v.report === "string"
  );
}

async function listRepositories(root: string): Promise<string[]> {
  const entries = await readdir(root, { withFileTypes: true });
  const repos: string[] = [];
  for (const entry of entries) {
    if (!entry.isDirectory() || entry.name.startsWith(".")) continue;
    const path = join(root, entry.name);
    try {
      await stat(join(path, ".git"));
      repos.push(path);
    } catch {
      console.error(`skip (not a Git repository): ${path}`);
    }
  }
  return repos.sort();
}

function toMarkdown(repo: string, scan: ScanReport, result: SDKResultMessage): string {
  const untested = scan.untested_files ?? [];
  return [
    `# Scan report: ${basename(repo)}`,
    "",
    `- TODO comments: ${scan.todo_count}`,
    `- FIXME comments: ${scan.fixme_count}`,
    `- Files without tested functions: ${untested.length === 0 ? "none" : untested.length}`,
    ...untested.map((file) => `  - ${file}`),
    "",
    "## Report",
    "",
    scan.report,
    "",
    "---",
    `Turns: ${result.num_turns}. Estimated cost: $${result.total_cost_usd.toFixed(4)} (client-side estimate).`,
    "",
  ].join("\n");
}

// ---------------------------------------------------------------------------
// One repository = one query() with its own budget and timeout
// ---------------------------------------------------------------------------

async function scanRepository(repo: string, perRepoBudget: number): Promise<{
  result: SDKResultMessage;
  scan: ScanReport | null;
}> {
  const abortController = new AbortController();
  const timer = setTimeout(() => abortController.abort(), REPO_TIMEOUT_MS);

  const options: Options = {
    cwd: repo,
    allowedTools: ALLOWED_TOOLS,
    disallowedTools: DENIED_TOOLS,
    permissionMode: "dontAsk", // anything not pre-approved is denied
    settingSources: [], // isolation: ignore the scanned repo's settings and CLAUDE.md
    maxTurns: MAX_TURNS_PER_REPO,
    maxBudgetUsd: perRepoBudget,
    outputFormat: { type: "json_schema", schema: REPORT_SCHEMA },
    abortController,
  };

  let result: SDKResultMessage | null = null;
  try {
    for await (const message of query({ prompt: PROMPT, options })) {
      if (message.type === "assistant" && message.message?.content) {
        for (const block of message.message.content) {
          if ("name" in block) console.error(`  [${basename(repo)}] tool: ${block.name}`);
        }
      } else if (message.type === "result") {
        result = message;
      }
    }
  } catch (err) {
    // A one-shot query() may throw after an error result; keep the result if we have it.
    if (result === null) throw err;
  } finally {
    clearTimeout(timer);
  }

  if (result === null) throw new Error("no result message received");
  const scan =
    result.subtype === "success" && isScanReport(result.structured_output)
      ? result.structured_output
      : null;
  return { result, scan };
}

// ---------------------------------------------------------------------------
// The batch: sequential, double budget, failures logged and skipped
// ---------------------------------------------------------------------------

async function main(): Promise<number> {
  const { values } = parseArgs({
    options: {
      root: { type: "string", default: "~/work/repos" },
      out: { type: "string", default: "reports" },
      "total-budget": { type: "string" },
      "per-repo-budget": { type: "string" },
    },
  });

  let totalBudget: number;
  let perRepoBudget: number;
  try {
    totalBudget = parseBudget(values["total-budget"], DEFAULT_TOTAL_BUDGET_USD, "total-budget");
    perRepoBudget = parseBudget(
      values["per-repo-budget"],
      DEFAULT_PER_REPO_BUDGET_USD,
      "per-repo-budget",
    );
  } catch (err) {
    console.error(err instanceof Error ? err.message : String(err));
    return 2;
  }

  const root = resolve(expandHome(values.root ?? "~/work/repos"));
  const outDir = resolve(values.out ?? "reports");
  await mkdir(outDir, { recursive: true });

  const repos = await listRepositories(root);
  if (repos.length === 0) {
    console.error(`No Git repositories found under ${root}`);
    return 2;
  }

  let spent = 0;
  const outcomes: RepoOutcome[] = [];

  for (const repo of repos) {
    // Stop the batch once the total budget is reached.
    if (spent >= totalBudget) {
      console.error(`batch budget reached (~$${spent.toFixed(2)}); stopping`);
      outcomes.push({ repo, status: "skipped", costUsd: 0, turns: 0, detail: "batch budget reached" });
      continue;
    }

    console.error(`scanning ${repo}`);
    try {
      const { result, scan } = await scanRepository(repo, perRepoBudget);
      spent += result.total_cost_usd;
      if (scan === null) {
        const detail =
          result.subtype === "success" ? "no valid structured output" : result.subtype;
        console.error(`FAILED: ${repo} (${detail})`);
        outcomes.push({ repo, status: "failed", costUsd: result.total_cost_usd, turns: result.num_turns, detail });
        continue;
      }
      await writeFile(join(outDir, `${basename(repo)}.md`), toMarkdown(repo, scan, result), "utf8");
      outcomes.push({
        repo,
        status: "ok",
        costUsd: result.total_cost_usd,
        turns: result.num_turns,
        detail: `${scan.todo_count} TODO, ${scan.fixme_count} FIXME`,
      });
    } catch (err) {
      const detail = err instanceof Error ? err.message : String(err);
      console.error(`FAILED: ${repo} (${detail})`);
      outcomes.push({ repo, status: "failed", costUsd: 0, turns: 0, detail });
    }
  }

  // Summary for people (stdout) and for machines (summary.json).
  console.log("\n=== Batch summary (client-side cost estimates) ===");
  for (const o of outcomes) {
    console.log(
      `  ${o.status.padEnd(7)} ${basename(o.repo).padEnd(30)} turns=${o.turns} cost=$${o.costUsd.toFixed(4)} ${o.detail}`,
    );
  }
  console.log(`Total: ~$${spent.toFixed(2)} of $${totalBudget.toFixed(2)} budget`);
  await writeFile(
    join(outDir, "summary.json"),
    JSON.stringify({ root, totalBudget, perRepoBudget, spent, outcomes }, null, 2) + "\n",
    "utf8",
  );

  return outcomes.every((o) => o.status === "ok") ? 0 : 1;
}

main()
  .then((code) => {
    process.exitCode = code;
  })
  .catch((err: unknown) => {
    console.error(err);
    process.exitCode = 1;
  });
