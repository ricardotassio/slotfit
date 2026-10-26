export type Window = { start: string; end: string; duration_minutes: number }

export type Assignment = { request_id: string; interval_id: string; scheduled_window: Window }

export type Evaluation = {
  request_id: string
  interval_id: string
  eligible: boolean
  reason_codes: string[]
}

export type Plan = {
  strategy: string
  assignments: Assignment[]
  recovered_minutes: number
  remaining_gap_minutes: number
  evaluations: Evaluation[]
}

export type Interval = { interval_id: string; window: Window }

export type Demo = {
  schema_version: string
  scenario_id: string
  synthetic: true
  automatic_action: 'none'
  intervals: Interval[]
  requests: Array<{ request_id: string; duration_minutes: number }>
  plans: Plan[]
  disclosure: string
}

export type Research = {
  candidate_accepted: false
  calibration_open: false
  final_frozen_set_exists: false
  decision: string
  evidence_boundary: string
  guardrail: { limit_percentage_points: number }
  candidates: Array<{
    candidate: string
    worst_supported_degradation_percentage_points: number
    decision: 'reject'
  }>
}

export type ReviewDecision = 'accept' | 'reject' | 'request_alternative'

export type ReviewCommand = {
  schema_version: '1.0'
  idempotency_key: string
  scenario_id: string
  strategy: string
  plan_checksum: string
  decision: ReviewDecision
  rationale: string
}

export type ReviewResult = { event: { event_id: string }; replayed: boolean }
