<script setup lang="ts">
import { computed } from 'vue'

import { labelFor } from '../format'
import type { Demo, Plan } from '../types'
import ScheduleCard from './ScheduleCard.vue'
import ScheduleReplay from './ScheduleReplay.vue'

const props = defineProps<{ demo: Demo; selectedPlan: Plan; candidatePlan: Plan }>()

const differenceMinutes = computed(
  () => props.candidatePlan.recovered_minutes - props.selectedPlan.recovered_minutes,
)
const differenceLabel = computed(() => {
  if (differenceMinutes.value === 0) return 'same minutes'
  const sign = differenceMinutes.value > 0 ? '+' : ''
  return `${sign}${differenceMinutes.value} min`
})
</script>

<template>
  <section class="story" aria-labelledby="comparison-title">
    <div class="story-heading">
      <div>
        <p class="eyebrow">One day · Two openings · Two requests</p>
        <h2 id="comparison-title">The same openings under each rule.</h2>
      </div>
      <p class="scenario-id">{{ demo.scenario_id }}</p>
    </div>
    <ScheduleReplay />
    <div class="calendar-comparison">
      <ScheduleCard
        :plan="selectedPlan"
        :intervals="demo.intervals"
        step-label="Reference rule"
        :title="labelFor(selectedPlan.strategy)"
        subtitle="Openings evaluated one by one"
        :list-label="`${labelFor(selectedPlan.strategy)} calendar`"
      />
      <div class="optimization-bridge" aria-label="Comparison delta">
        <span>Difference in<br />this fixture</span>
        <div class="bridge-arrow">↔</div>
        <strong>{{ differenceLabel }}</strong>
        <small>candidate minus reference</small>
      </div>
      <ScheduleCard
        :plan="candidatePlan"
        :intervals="demo.intervals"
        step-label="Candidate plan"
        :title="labelFor(candidatePlan.strategy)"
        subtitle="Openings evaluated together"
        list-label="Candidate calendar"
      />
    </div>
    <div class="impact-row">
      <div>
        <span>Reference recovered</span>
        <strong data-testid="recovered-minutes">{{ selectedPlan.recovered_minutes }} min</strong>
      </div>
      <div><span>Candidate recovered</span><strong>{{ candidatePlan.recovered_minutes }} min</strong></div>
      <div><span>Remaining gap</span><strong>{{ candidatePlan.remaining_gap_minutes }} min</strong></div>
      <div><span>External actions</span><strong>0</strong></div>
    </div>
  </section>
</template>
