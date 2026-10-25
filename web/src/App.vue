<script setup lang="ts">
import FullCalendar from '@fullcalendar/vue3'
import timeGridPlugin from '@fullcalendar/vue3/timegrid'
import '@fullcalendar/vue3/skeleton.css'
import { computed, onMounted, ref } from 'vue'

type Assignment = {
  request_id: string
  interval_id: string
  scheduled_window: { start: string; end: string; duration_minutes: number }
}

type Evaluation = {
  request_id: string
  interval_id: string
  eligible: boolean
  reason_codes: string[]
}

type Plan = {
  strategy: string
  assignments: Assignment[]
  recovered_minutes: number
  remaining_gap_minutes: number
  evaluations: Evaluation[]
}

type Demo = {
  schema_version: string
  scenario_id: string
  synthetic: true
  automatic_action: 'none'
  intervals: Array<{
    interval_id: string
    window: { start: string; end: string; duration_minutes: number }
  }>
  requests: Array<{ request_id: string; duration_minutes: number }>
  plans: Plan[]
  disclosure: string
}

type DevelopmentDecision = {
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

type ReviewDecision = 'accept' | 'reject' | 'request_alternative'

const demo = ref<Demo | null>(null)
const research = ref<DevelopmentDecision | null>(null)
const selectedStrategy = ref('')
const loading = ref(true)
const loadError = ref('')
const reviewPending = ref(false)
const reviewMessage = ref('')
const reviewError = ref('')
const commandIdentity = ref<{ fingerprint: string; key: string } | null>(null)

const selectedPlan = computed(() =>
  demo.value?.plans.find((plan) => plan.strategy === selectedStrategy.value) ?? null,
)

const planLabels: Record<string, string> = {
  'fifo-eligible@0.2.0': 'FIFO baseline',
  'local-best-fit@0.2.0': 'Local best-fit baseline',
  'cp-sat-lexicographic@0.1.0': 'CP-SAT controlled plan',
}

const calendarOptions = computed(() => ({
  plugins: [timeGridPlugin],
  initialView: 'timeGridDay',
  initialDate: demo.value?.intervals[0]?.window.start ?? '2026-11-04',
  headerToolbar: false as const,
  allDaySlot: false,
  slotMinTime: '13:30:00',
  slotMaxTime: '17:00:00',
  height: 'auto',
  events: selectedPlan.value?.assignments.map((assignment) => ({
    id: `${assignment.request_id}-${assignment.interval_id}`,
    title: `${assignment.request_id} · ${assignment.interval_id}`,
    start: assignment.scheduled_window.start,
    end: assignment.scheduled_window.end,
    backgroundColor: '#334563',
    borderColor: '#334563',
    textColor: '#ffffff',
  })) ?? [],
}))

function labelFor(strategy: string): string {
  return planLabels[strategy] ?? strategy
}

function formatTime(value: string): string {
  return new Intl.DateTimeFormat('en-CA', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'America/Toronto',
  }).format(new Date(value))
}

async function loadEvidence(): Promise<void> {
  loading.value = true
  loadError.value = ''
  try {
    const [demoResponse, researchResponse] = await Promise.all([
      fetch('/api/v1/demos/global-conflict'),
      fetch('/api/v1/research/development-decision'),
    ])
    if (!demoResponse.ok || !researchResponse.ok) {
      throw new Error('evidence request failed')
    }
    demo.value = await demoResponse.json() as Demo
    research.value = await researchResponse.json() as DevelopmentDecision
    selectedStrategy.value = demo.value.plans[0]?.strategy ?? ''
  } catch {
    demo.value = null
    research.value = null
    selectedStrategy.value = ''
    loadError.value = 'Could not load the synthetic evidence. Nothing was changed.'
  } finally {
    loading.value = false
  }
}

async function sha256(value: string): Promise<string> {
  const bytes = new TextEncoder().encode(value)
  const digest = await crypto.subtle.digest('SHA-256', bytes)
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('')
}

async function recordReview(decision: ReviewDecision): Promise<void> {
  if (!demo.value || !selectedPlan.value || reviewPending.value) return
  reviewPending.value = true
  reviewMessage.value = ''
  reviewError.value = ''
  const fingerprint = `${demo.value.scenario_id}:${selectedPlan.value.strategy}:${decision}`
  if (commandIdentity.value?.fingerprint !== fingerprint) {
    commandIdentity.value = { fingerprint, key: crypto.randomUUID() }
  }
  try {
    const response = await fetch('/api/v1/reviews', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        schema_version: '1.0',
        idempotency_key: commandIdentity.value.key,
        scenario_id: demo.value.scenario_id,
        strategy: selectedPlan.value.strategy,
        plan_checksum: await sha256(JSON.stringify(selectedPlan.value)),
        decision,
        rationale: 'Simulated review from the local evidence UI.',
      }),
    })
    if (!response.ok) throw new Error('review request failed')
    const result = await response.json() as {
      event: { event_id: string }
      created: boolean
      replayed: boolean
    }
    reviewMessage.value = `Review ${result.replayed ? 'replayed' : 'created'}: ${result.event.event_id}. No external action occurred.`
  } catch {
    reviewError.value = 'Review was not recorded. No external action occurred.'
  } finally {
    reviewPending.value = false
  }
}

onMounted(loadEvidence)
</script>

<template>
  <header class="site-header">
    <div class="header-inner">
      <p class="eyebrow">Synthetic scheduling experiment</p>
      <h1>SlotFit evidence lab</h1>
      <p class="lede">
        A small engineering study of assignment trade-offs—with explicit limits,
        reproducible evidence and a human-owned simulated review.
      </p>
    </div>
  </header>

  <main id="main-content" class="shell">
    <p v-if="loading" class="state-panel" role="status">Loading controlled evidence…</p>

    <section v-else-if="loadError" class="state-panel error-panel" aria-labelledby="load-error-title">
      <h2 id="load-error-title">Evidence unavailable</h2>
      <p role="alert">{{ loadError }}</p>
      <button class="button primary" type="button" @click="loadEvidence">
        Retry loading evidence
      </button>
    </section>

    <template v-else-if="demo && research && selectedPlan">
      <section class="outcome-panel" aria-labelledby="outcome-title" data-testid="research-no-go">
        <div>
          <p class="eyebrow">Development decision · 40 synthetic seeds</p>
          <h2 id="outcome-title">No candidate passed the fixed guardrail</h2>
          <p>{{ research.decision }}</p>
        </div>
        <dl class="outcome-facts">
          <div>
            <dt>Closest candidate</dt>
            <dd>10.80 p.p.</dd>
          </div>
          <div>
            <dt>Declared maximum</dt>
            <dd>{{ research.guardrail.limit_percentage_points.toFixed(2) }} p.p.</dd>
          </div>
          <div>
            <dt>Calibration</dt>
            <dd>Closed</dd>
          </div>
        </dl>
        <p class="boundary-note">{{ research.evidence_boundary }}</p>
      </section>

      <section class="workspace" aria-labelledby="comparison-title">
        <div class="section-heading">
          <div>
            <p class="eyebrow">Controlled counterexample</p>
            <h2 id="comparison-title">Compare the same synthetic opening</h2>
          </div>
          <p class="scenario-id">{{ demo.scenario_id }}</p>
        </div>

        <fieldset class="plan-picker">
          <legend>Plan shown</legend>
          <label v-for="plan in demo.plans" :key="plan.strategy" class="plan-choice">
            <input v-model="selectedStrategy" type="radio" name="plan" :value="plan.strategy" />
            <span>{{ labelFor(plan.strategy) }}</span>
          </label>
        </fieldset>

        <p class="disclosure">{{ demo.disclosure }}</p>

        <dl class="metric-grid" aria-label="Selected plan metrics">
          <div>
            <dt>Recovered time</dt>
            <dd data-testid="recovered-minutes">{{ selectedPlan.recovered_minutes }} min</dd>
          </div>
          <div>
            <dt>Remaining gap</dt>
            <dd>{{ selectedPlan.remaining_gap_minutes }} min</dd>
          </div>
          <div>
            <dt>Requests placed</dt>
            <dd>{{ selectedPlan.assignments.length }}</dd>
          </div>
          <div>
            <dt>Automatic action</dt>
            <dd>None</dd>
          </div>
        </dl>

        <div class="comparison-grid">
          <section class="calendar-panel" aria-labelledby="calendar-title">
            <h3 id="calendar-title">Time-grid view</h3>
            <FullCalendar :key="selectedStrategy" :options="calendarOptions" />
          </section>

          <section class="table-panel" aria-labelledby="table-title">
            <h3 id="table-title">Assignment table</h3>
            <table aria-label="Selected plan assignments">
              <thead>
                <tr>
                  <th scope="col">Request</th>
                  <th scope="col">Opening</th>
                  <th scope="col">Time</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="assignment in selectedPlan.assignments" :key="assignment.request_id">
                  <th scope="row">{{ assignment.request_id }}</th>
                  <td>{{ assignment.interval_id }}</td>
                  <td>
                    {{ formatTime(assignment.scheduled_window.start) }}–{{ formatTime(assignment.scheduled_window.end) }}
                  </td>
                </tr>
              </tbody>
            </table>

            <details class="reason-details">
              <summary>Inspect eligibility reasons</summary>
              <ul>
                <li v-for="evaluation in selectedPlan.evaluations" :key="`${evaluation.request_id}-${evaluation.interval_id}`">
                  <strong>{{ evaluation.request_id }} → {{ evaluation.interval_id }}:</strong>
                  {{ evaluation.eligible ? 'eligible' : evaluation.reason_codes.join(', ') }}
                </li>
              </ul>
            </details>
          </section>
        </div>
      </section>

      <section class="review-panel" aria-labelledby="review-title">
        <div>
          <p class="eyebrow">Human-owned simulation</p>
          <h2 id="review-title">Record how you would assess this plan</h2>
          <p>This stores an audit event only. It does not book, notify or change a schedule.</p>
        </div>
        <div class="review-actions" aria-label="Simulated review decisions">
          <button type="button" :disabled="reviewPending" @click="recordReview('accept')">
            Record accept
          </button>
          <button type="button" :disabled="reviewPending" @click="recordReview('reject')">
            Record reject
          </button>
          <button type="button" :disabled="reviewPending" @click="recordReview('request_alternative')">
            Request alternative
          </button>
        </div>
        <p v-if="reviewPending" role="status">Recording simulated review…</p>
        <p v-if="reviewMessage" class="success-message" role="status">{{ reviewMessage }}</p>
        <p v-if="reviewError" class="error-message" role="alert">{{ reviewError }}</p>
      </section>
    </template>
  </main>
</template>
