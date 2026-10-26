<script setup lang="ts">
import { computed } from 'vue'

import type { Research } from '../types'

const props = defineProps<{ research: Research }>()

const closestResult = computed(() =>
  Math.min(
    ...props.research.candidates.map((c) => c.worst_supported_degradation_percentage_points),
  ).toFixed(2),
)
const limit = computed(() => props.research.guardrail.limit_percentage_points.toFixed(2))
</script>

<template>
  <section class="research-strip" aria-labelledby="outcome-title" data-testid="research-no-go">
    <div class="research-mark">!</div>
    <div class="research-copy">
      <p class="eyebrow">Longitudinal research verdict</p>
      <h2 id="outcome-title">No candidate passed the fixed guardrail</h2>
      <p>{{ research.decision }}</p>
    </div>
    <div class="research-number">
      <strong>{{ closestResult }} <small>p.p.</small></strong>
      <span>closest result · limit {{ limit }} p.p.</span>
    </div>
  </section>
</template>
