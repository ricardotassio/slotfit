"""Frozen evaluation thresholds shared by the comparison, diagnostic and frontier reports."""

from __future__ import annotations

SUPPORT_THRESHOLD = 30
"""Minimum eligible opportunities before a slice is reported as supported."""

STARVATION_K = 3
"""Compatible misses at or above which a request history counts as starved."""

STARVATION_DEGRADATION_LIMIT = 0.05
"""Maximum candidate starvation-rate increase over the better baseline."""

SLICE_GAP_DEGRADATION_LIMIT = 0.10
"""Maximum worst-supported-slice exposure-gap increase over the better baseline."""
