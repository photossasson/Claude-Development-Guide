export type GuardCounts = { held: number; allowed: number; last: string | null }

declare module 'claude-code' {
  interface PluginState {
    'risk-guard': { counts: GuardCounts }
  }
}
