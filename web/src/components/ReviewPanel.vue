<script setup lang="ts">
import type { ReviewDecision } from '../types'

defineProps<{ pending: boolean; message: string; error: string }>()
const emit = defineEmits<{ decide: [decision: ReviewDecision] }>()
</script>

<template>
  <section class="review-panel" aria-labelledby="review-title">
    <div>
      <p class="eyebrow">Human-owned simulation</p>
      <h2 id="review-title">The model proposes. A person decides.</h2>
      <p>Record a local audit event only. Nothing is booked, published, notified or changed.</p>
    </div>
    <div class="review-actions">
      <button :disabled="pending" @click="emit('decide', 'accept')">Record accept</button>
      <button :disabled="pending" @click="emit('decide', 'reject')">Record reject</button>
      <button :disabled="pending" @click="emit('decide', 'request_alternative')">
        Request alternative
      </button>
    </div>
    <p v-if="pending" role="status">Recording simulated review…</p>
    <p v-if="message" class="success-message" role="status">{{ message }}</p>
    <p v-if="error" class="error-message" role="alert">{{ error }}</p>
  </section>
</template>
