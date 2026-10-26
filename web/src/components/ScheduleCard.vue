<script setup lang="ts">
import { assignmentFor, formatTime, requestName } from '../format'
import type { Interval, Plan } from '../types'

defineProps<{
  plan: Plan
  intervals: Interval[]
  stepLabel: string
  title: string
  subtitle: string
  listLabel: string
  footer: string
  cardClass: string
  pillClass: string
  appointmentClass: string
  swatchClass: string
  showEmptySlots: boolean
}>()
</script>

<template>
  <article class="schedule" :class="cardClass">
    <header class="schedule-header">
      <div>
        <span class="step-label">{{ stepLabel }}</span>
        <h3>{{ title }}</h3>
      </div>
      <div class="capacity-pill" :class="pillClass">{{ plan.recovered_minutes }} / 120 min</div>
    </header>
    <div class="calendar-date">
      <div><span>WED</span><strong>04</strong></div>
      <p>November 2026<br /><small>{{ subtitle }}</small></p>
    </div>
    <div class="timeline" role="list" :aria-label="listLabel">
      <div v-for="interval in intervals" :key="interval.interval_id" class="time-row" role="listitem">
        <time>{{ formatTime(interval.window.start) }}</time>
        <div
          v-if="assignmentFor(plan, interval.interval_id)"
          class="appointment"
          :class="appointmentClass"
        >
          <span>{{ interval.interval_id }}</span>
          <strong>{{ requestName(assignmentFor(plan, interval.interval_id)!.request_id) }}</strong>
          <small>{{ assignmentFor(plan, interval.interval_id)!.request_id }}</small>
        </div>
        <div v-else-if="showEmptySlots" class="appointment empty-slot">
          <span>{{ interval.interval_id }}</span>
          <strong>Capacity left unused</strong>
          <small>{{ interval.window.duration_minutes }} minutes available</small>
        </div>
      </div>
    </div>
    <footer><i class="swatch" :class="swatchClass"></i>{{ footer }}</footer>
  </article>
</template>
