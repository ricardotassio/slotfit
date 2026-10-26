<script setup lang="ts">
import { labelFor } from '../format'
import type { Demo, Plan, Research } from '../types'
import AssignmentTable from './AssignmentTable.vue'

defineProps<{ demo: Demo; research: Research; selectedPlan: Plan }>()
const selectedStrategy = defineModel<string>('selectedStrategy', { required: true })
</script>

<template>
  <section class="evidence" aria-labelledby="evidence-title">
    <div class="evidence-intro">
      <p class="eyebrow">Inspect the evidence</p>
      <h2 id="evidence-title">Change the reference rule</h2>
      <p>
        Select a strategy to compare its result with the controlled candidate. This changes only
        the local visualization.
      </p>
    </div>
    <fieldset class="plan-picker">
      <legend class="sr-only">Plan shown</legend>
      <label v-for="plan in demo.plans" :key="plan.strategy" class="plan-choice">
        <input v-model="selectedStrategy" type="radio" name="plan" :value="plan.strategy" />
        <span>
          <strong>{{ labelFor(plan.strategy) }}</strong>
          <small>{{ plan.recovered_minutes }} min recovered</small>
        </span>
      </label>
    </fieldset>
    <AssignmentTable :plan="selectedPlan" />
    <p class="disclosure">{{ demo.disclosure }} {{ research.evidence_boundary }}</p>
  </section>
</template>
