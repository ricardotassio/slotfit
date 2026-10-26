<script setup lang="ts">
import { computed } from 'vue'

import { labelFor } from '../format'
import type { Demo, Plan } from '../types'
import ScheduleCard from './ScheduleCard.vue'
import ScheduleReplay from './ScheduleReplay.vue'

const props = defineProps<{ demo: Demo; selectedPlan: Plan; candidatePlan: Plan }>()

const gainedMinutes = computed(() =>
  Math.max(0, props.candidatePlan.recovered_minutes - props.selectedPlan.recovered_minutes),
)
</script>

<template>
  <section class="story" aria-labelledby="comparison-title">
    <div class="story-heading">
      <div>
        <p class="eyebrow">One day · Two openings · Two requests</p>
        <h2 id="comparison-title">The same capacity. A different outcome.</h2>
      </div>
      <p class="scenario-id">{{ demo.scenario_id }}</p>
    </div>
    <ScheduleReplay />
    <div class="calendar-comparison">
      <ScheduleCard
        :plan="selectedPlan"
        :intervals="demo.intervals"
        step-label="01 · Reference rule"
        :title="labelFor(selectedPlan.strategy)"
        subtitle="Two independent openings"
        :list-label="`${labelFor(selectedPlan.strategy)} calendar`"
        footer="Valid one-by-one, but blind to the next request"
        card-class=""
        pill-class="neutral"
        appointment-class="appointment-local"
        swatch-class="local"
        :show-empty-slots="true"
      />
      <div class="optimization-bridge" aria-label="Comparison delta">
        <span>Constraint-aware<br />allocation</span>
        <div class="bridge-arrow">→</div>
        <strong v-if="gainedMinutes">+{{ gainedMinutes }} min</strong>
        <strong v-else>same capacity</strong>
        <small>in this controlled fixture</small>
      </div>
      <ScheduleCard
        :plan="candidatePlan"
        :intervals="demo.intervals"
        step-label="02 · Candidate plan"
        title="Global constraint plan"
        subtitle="Same openings, jointly evaluated"
        list-label="Candidate calendar"
        footer="Both requests placed · zero automatic actions"
        card-class="schedule-after"
        pill-class="optimized"
        appointment-class="appointment-optimized"
        swatch-class="optimized"
        :show-empty-slots="false"
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
