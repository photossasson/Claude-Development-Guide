import { describe, expect, test } from 'claude-code/testing'

// The test's own hooks sit beneath the mod and stand for the engine.
const ranBash = { result: { stdout: 'ok', stderr: '', interrupted: false } }
const status = {
  command: 'guard-status',
  args: '',
  origin: { kind: 'composer' },
  presentation: { isFullscreen: false, columns: 100 },
} as const

describe('risk-guard', () => {
  test('a safe command runs untouched', async ($, on) => {
    on('tool.call', { tool: 'Bash' }, () => ranBash)
    const r = await $.tool.call({ tool: 'Bash', command: 'ls -la' })
    expect(r.deny).toBeUndefined()
  })

  test('a risky command is refused when nobody can answer', async ($, on) => {
    on('tool.call', { tool: 'Bash' }, () => ranBash)
    on('tool.call', { tool: 'AskUserQuestion' }, () => ({ deny: 'no one to ask' }))
    const r = await $.tool.call({ tool: 'Bash', command: 'rm -rf build' })
    expect(r.deny).toContain('rm -rf')
    const s = await $.command.run(status)
    expect(s.text).toContain('held 1')
  })

  test('a risky command runs after "Allow once"', async ($, on) => {
    on('tool.call', { tool: 'Bash' }, () => ranBash)
    on('tool.call', { tool: 'AskUserQuestion' }, (_$, e) => ({
      result: { questions: e.questions, answers: { [e.questions[0]!.question]: 'Allow once' } },
    }))
    const r = await $.tool.call({ tool: 'Bash', command: 'git reset --hard HEAD~1' })
    expect(r.deny).toBeUndefined()
    const s = await $.command.run(status)
    expect(s.text).toContain('allowed 1')
  })

  test('mode "deny" refuses without asking', { options: { mode: 'deny' } }, async ($, on) => {
    on('tool.call', { tool: 'Bash' }, () => ranBash)
    on('tool.call', { tool: 'AskUserQuestion' }, () => {
      throw new Error('the guard must not ask in deny mode')
    })
    const r = await $.tool.call({ tool: 'Bash', command: 'git push --force origin main' })
    expect(r.deny).toContain('git push --force')
  })
})
