<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { fetchEvidence, postReview, sha256 } from './api'
import EvidenceSection from './components/EvidenceSection.vue'
import PlanComparison from './components/PlanComparison.vue'
import ResearchStrip from './components/ResearchStrip.vue'
import ReviewPanel from './components/ReviewPanel.vue'
import type { Demo, Research, ReviewDecision } from './types'

const demo = ref<Demo | null>(null)
const research = ref<Research | null>(null)
const selectedStrategy = ref('')
const loading = ref(true)
const loadError = ref('')
const reviewPending = ref(false)
const reviewMessage = ref('')
const reviewError = ref('')
const commandIdentity = ref<{ fingerprint: string; key: string } | null>(null)

const selectedPlan = computed(
  () => demo.value?.plans.find((plan) => plan.strategy === selectedStrategy.value) ?? null,
)
const candidatePlan = computed(
  () =>
    demo.value?.plans.find((plan) => plan.strategy.startsWith('cp-sat')) ??
    demo.value?.plans.at(-1) ??
    null,
)

async function loadEvidence() {
  loading.value = true
  loadError.value = ''
  try {
    const evidence = await fetchEvidence()
    demo.value = evidence.demo
    research.value = evidence.research
    selectedStrategy.value = evidence.demo.plans[0]?.strategy ?? ''
  } catch {
    demo.value = null
    research.value = null
    selectedStrategy.value = ''
    loadError.value = 'Could not load the synthetic evidence. Nothing was changed.'
  } finally {
    loading.value = false
  }
}

async function recordReview(decision: ReviewDecision) {
  if (!demo.value || !selectedPlan.value || reviewPending.value) return
  reviewPending.value = true
  reviewMessage.value = ''
  reviewError.value = ''
  const fingerprint = `${demo.value.scenario_id}:${selectedPlan.value.strategy}:${decision}`
  if (commandIdentity.value?.fingerprint !== fingerprint) {
    commandIdentity.value = { fingerprint, key: crypto.randomUUID() }
  }
  try {
    const result = await postReview({
      schema_version: '1.0',
      idempotency_key: commandIdentity.value.key,
      scenario_id: demo.value.scenario_id,
      strategy: selectedPlan.value.strategy,
      plan_checksum: await sha256(JSON.stringify(selectedPlan.value)),
      decision,
      rationale: 'Simulated review from the local evidence UI.',
    })
    const verb = result.replayed ? 'replayed' : 'created'
    reviewMessage.value = `Review ${verb}: ${result.event.event_id}. No external action occurred.`
  } catch {
    reviewError.value = 'Review was not recorded. No external action occurred.'
  } finally {
    reviewPending.value = false
  }
}

onMounted(loadEvidence)
</script>

<template>
  <a class="skip-link" href="#main-content">Skip to evidence</a>
  <header class="topbar">
    <a class="brand" href="#">slot<span>fit</span></a>
    <div class="topbar-meta">
      <span class="live-dot"></span>Controlled simulation<span class="topbar-rule"></span>Toronto · UTC−05
    </div>
  </header>
  <main id="main-content" class="shell">
    <p v-if="loading" class="state-panel" role="status">Loading controlled evidence…</p>
    <section v-else-if="loadError" class="state-panel error-panel">
      <h1>Evidence unavailable</h1>
      <p role="alert">{{ loadError }}</p>
      <button class="primary" @click="loadEvidence">Retry loading evidence</button>
    </section>
    <template v-else-if="demo && research && selectedPlan && candidatePlan">
      <section class="hero" aria-labelledby="page-title">
        <div>
          <p class="eyebrow">Scheduling decision study · Synthetic data</p>
          <h1 id="page-title">Two openings,<br /><em>two requests.</em></h1>
        </div>
        <div class="hero-copy">
          <p>
            A controlled counterexample comparing two greedy rules and a global constraint plan on
            the same synthetic day. Each plan receives the same treatment; a person decides what
            happens next.
          </p>
          <div class="hero-tags">
            <span>Reproducible</span><span>Human reviewed</span><span>No patient data</span>
          </div>
        </div>
      </section>
      <ResearchStrip :research="research" />
      <PlanComparison :demo="demo" :selected-plan="selectedPlan" :candidate-plan="candidatePlan" />
      <EvidenceSection
        v-model:selected-strategy="selectedStrategy"
        :demo="demo"
        :research="research"
        :selected-plan="selectedPlan"
      />
      <ReviewPanel
        :pending="reviewPending"
        :message="reviewMessage"
        :error="reviewError"
        @decide="recordReview"
      />
    </template>
  </main>
</template>
