<script setup lang="ts">
import { ref } from 'vue'

const animationKey = ref(0)

function replayAnimation() {
  animationKey.value += 1
}
</script>

<template>
  <section class="agenda-replay" aria-labelledby="replay-title">
    <div class="replay-header">
      <div>
        <span class="step-label">Optimization replay</span>
        <h3 id="replay-title">Watch the unused opening become usable</h3>
      </div>
      <button class="replay-button" type="button" @click="replayAnimation">↻ Replay</button>
    </div>
    <div :key="animationKey" class="replay-stage" aria-live="polite">
      <div class="replay-times" aria-hidden="true">
        <span>14:00</span><span>15:00</span><span>15:30</span><span>16:30</span>
      </div>
      <div class="replay-lane">
        <strong>Local rule</strong>
        <div class="replay-track">
          <span class="replay-block flexible-before">Flexible request</span>
          <span class="replay-gap">60 min gap</span>
        </div>
      </div>
      <div class="replay-lane">
        <strong>Candidate</strong>
        <div class="replay-track">
          <span class="replay-block constrained-after">Constrained request</span>
          <span class="replay-block flexible-after">Flexible request</span>
        </div>
      </div>
      <p class="replay-caption">
        <span>Preserve the only compatible opening</span>
        <strong>Gap recovered · +60 min</strong>
      </p>
    </div>
    <p class="sr-only">
      The local rule puts the flexible request at 14:00 and leaves the 15:30 opening unused.
      The candidate plan puts the constrained request at 14:00 and moves the flexible request
      to 15:30, using both openings.
    </p>
  </section>
</template>
