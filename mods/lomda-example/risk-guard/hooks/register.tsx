import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { GuardCounts } from '../types'
import { riskOf } from './risk'

const counts = atom({ plugin: 'risk-guard', key: 'counts' } as const, { held: 0, allowed: 0, last: null } as GuardCounts)
const ALLOW = 'Allow once'
const BLOCK = 'Block'

export const register: Register = (on, options) => {
  const mode = options.mode === 'deny' ? 'deny' : 'ask'

  // 1. The guard: a risky Bash command waits for a person, or is refused.
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const risk = riskOf(e.command)
    if (risk === undefined) {
      return next(e)
    }
    let answer = BLOCK
    if (mode === 'ask') {
      try {
        answer = await $.ui.ask(`risk-guard: allow "${e.command.slice(0, 80)}" (${risk})?`, [ALLOW, BLOCK])
      } catch {
        answer = BLOCK // dismissed, or nobody to ask (claude -p)
      }
    }
    if (answer === ALLOW) {
      await update($, counts, c => ({ ...c, allowed: c.allowed + 1 }))
      return next(e)
    }
    await update($, counts, c => ({ ...c, held: c.held + 1, last: risk }))
    return { deny: `risk-guard held a "${risk}" command. Ask the person to run it themselves, or find a safer way.` }
  }).catch(($, e, next) =>
    // Fail closed: if the guard itself broke before deciding, refuse.
    next.called ? next(e) : { deny: 'risk-guard failed, so the command was refused.' },
  )

  // 2. A slash command, registered when the session starts.
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'guard-status', description: 'Show what risk-guard held in this session' })
    return next(e)
  })

  on('command.run', { command: 'guard-status' }, async $ => {
    const c = await read($, counts)
    return {
      text: `risk-guard (${mode}): held ${c.held}, allowed ${c.allowed}` + (c.last ? `, last: ${c.last}` : ''),
    }
  })

  // 3. A band above the prompt, drawn only once something was held.
  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const c = await read($, counts)
    if (c.held === 0 || e.props.hasSurvey) {
      return next(e)
    }
    const { Box, Text } = $.ui.resolve(e)
    return (
      <Box>
        <Text color="yellow">risk-guard</Text>
        <Text dimColor> held {c.held} risky command{c.held === 1 ? '' : 's'}; last: {c.last}</Text>
      </Box>
    )
  })
}
