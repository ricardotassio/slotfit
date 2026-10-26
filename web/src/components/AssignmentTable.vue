<script setup lang="ts">
import { formatTime } from '../format'
import type { Plan } from '../types'

defineProps<{ plan: Plan }>()
</script>

<template>
  <div class="evidence-grid">
    <div class="assignment-table">
      <h3>Selected assignments</h3>
      <table aria-label="Selected plan assignments">
        <thead>
          <tr>
            <th>Request</th>
            <th>Opening</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="assignment in plan.assignments" :key="assignment.request_id">
            <th>{{ assignment.request_id }}</th>
            <td>{{ assignment.interval_id }}</td>
            <td>
              {{ formatTime(assignment.scheduled_window.start) }}–{{
                formatTime(assignment.scheduled_window.end)
              }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <details class="reason-details">
      <summary>Eligibility trace</summary>
      <ul>
        <li
          v-for="evaluation in plan.evaluations"
          :key="`${evaluation.request_id}-${evaluation.interval_id}`"
        >
          <strong>{{ evaluation.request_id }} → {{ evaluation.interval_id }}</strong>
          <span>{{ evaluation.eligible ? 'Eligible' : evaluation.reason_codes.join(', ') }}</span>
        </li>
      </ul>
    </details>
  </div>
</template>
