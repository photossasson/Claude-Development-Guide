// Patterns of Bash commands that are hard to undo.
export const RISKY: readonly { label: string; re: RegExp }[] = [
  { label: 'rm -rf', re: /\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r|--recursive\s+--force|--force\s+--recursive)\b/ },
  { label: 'git push --force', re: /\bgit\s+push\b.*(\s--force\b|\s-f\b|\s--force-with-lease\b)/ },
  { label: 'git reset --hard', re: /\bgit\s+reset\s+--hard\b/ },
  { label: 'git clean -f', re: /\bgit\s+clean\s+-[a-zA-Z]*f/ },
]

export function riskOf(command: string): string | undefined {
  return RISKY.find(r => r.re.test(command))?.label
}
