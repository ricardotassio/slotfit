import type { Demo, Research, ReviewCommand, ReviewResult } from './types'

export async function fetchEvidence(): Promise<{ demo: Demo; research: Research }> {
  const [demoResponse, researchResponse] = await Promise.all([
    fetch('/api/v1/demos/global-conflict'),
    fetch('/api/v1/research/development-decision'),
  ])
  if (!demoResponse.ok || !researchResponse.ok) {
    throw new Error('evidence request failed')
  }
  return {
    demo: (await demoResponse.json()) as Demo,
    research: (await researchResponse.json()) as Research,
  }
}

export async function sha256(value: string): Promise<string> {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value))
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('')
}

export async function postReview(command: ReviewCommand): Promise<ReviewResult> {
  const response = await fetch('/api/v1/reviews', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(command),
  })
  if (!response.ok) {
    throw new Error('review request failed')
  }
  return (await response.json()) as ReviewResult
}
