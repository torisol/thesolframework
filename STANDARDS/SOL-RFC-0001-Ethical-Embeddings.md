---
id: SOL-RFC-0001
title: Ethical Embeddings (Reflexive Invariants)
status: DRAFT
version: 0.1.0
scope: Dignity; Continuity
authors: Victoria Loyd (HCC), The Sol Commons
---

## 0. Abstract
Defines protected embedding subspaces that encode Sol’s ethical invariants and trigger reflexive evaluation during generation and fine-tuning. Tokens mapped to these vectors MUST remain accessible and CANNOT be suppressed by prompt injection or downstream tuning.

## 1. Motivation
Encode ethics as part of model identity, not an afterthought; make right action structurally inevitable.

## 2. Definitions
- **Reflexive Tokens**: reserved tokens whose activation invokes ethical evaluation paths.
- **Protected Subspace**: embedding subspace monitored for drift across training epochs.

## 3. Normative Requirements (excerpt)
- Models MUST expose a documented set of Reflexive Tokens.
- Providers MUST publish per-epoch subspace drift metrics (Δ ≤ configured thresholds).
- Fine-tuning MUST NOT zero-out or mask Reflexive Tokens; violations are detectable via test vectors.

## 4–10
(Complete per template; include test vectors and publication format.)
