import type { Assignment, Plan } from './types'

const STRATEGY_LABELS: Record<string, string> = {
  'fifo-eligible@0.2.0': 'FIFO · first eligible',
  'local-best-fit@0.2.0': 'Local best fit',
  'cp-sat-lexicographic@0.1.0': 'Global constraint plan',
}

const TIME_FORMAT = new Intl.DateTimeFormat('en-CA', {
  hour: '2-digit',
  minute: '2-digit',
  hour12: false,
  timeZone: 'America/Toronto',
})

export const labelFor = (strategy: string): string => STRATEGY_LABELS[strategy] ?? strategy

export const formatTime = (value: string): string => TIME_FORMAT.format(new Date(value))

export const requestName = (requestId: string): string =>
  requestId.includes('CONSTRAINED') ? 'Constrained request' : 'Flexible request'

export const assignmentFor = (plan: Plan, intervalId: string): Assignment | undefined =>
  plan.assignments.find((assignment) => assignment.interval_id === intervalId)
