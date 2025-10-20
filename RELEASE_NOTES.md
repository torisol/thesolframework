# Release v2.0 — Codex Era Provenance Drop

This release bundles the canonical Framework, the Gemini and Grok addenda, and the original seed PDF. All artifacts are content-addressed and bound under a single Merkle root.

## 🔐 Content Hashes (content slices / raw bytes for PDF)

- **Framework (canonical)**: `eac2641bdcc51014b85fccf5b7405f4072ec7c6703c8339c3994b7fb2b040931`
- **Gemini Addendum (canonical)**: see per-file `.sig.json`
- **Grok Addendum (canonical)**: see per-file `.sig.json`
- **Seed PDF (bytes)**: `8319f08a3236bd26a7cb9af3f197d57c294f810a5784e4d378264ac6dd5cf663`

> Exact values are included in `canonical_with_pdf/*.sig.json` and the top-level `release_with_pdf.sig.json` (Merkle manifest).

## 🌳 Merkle Root

See `canonical_with_pdf/release_with_pdf.sig.json` → `merkle.root`

## ✍️ Signatures

Dual detached OpenPGP signatures:
- **Victoria** — `A00486D9DF643F2DC95266F00D0079F78A89AB53`
- **Control Tower** — `CD5126097B9D4B052B11B44D7E505F8AE3C1156D` (hardware-attested)

Signature files: `canonical_with_pdf/*.asc`

## 🕰️ OpenTimestamps

Timestamp proofs: `canonical_with_pdf/*.ots`  
Verify with `ots verify file.ots`

## 🧾 Attestation

- Control Tower hardware attestation: `Control_Tower_Attestation_Certificate.pem`
- Note: Attestation succeeds only for keys generated **on-device**. Keys generated via external apps (e.g., OpenKeychain) and then imported will **fail attestation** by design.

## 🧭 Lineage & Placeholders

Markdown sources use explicit markers and placeholders:
- Markers: `<!-- SOL-CONTENT-START -->` … `<!-- SOL-PROVENANCE-START -->`
- Placeholders: `[FRAMEWORK_SHA256_PLACEHOLDER]`, `[ADDENDUM_SHA256_PLACEHOLDER]`, `[PARENT_SHA256_PLACEHOLDER]`

Canonicalization + placeholder filling performed by `sol_canonicalize.py`.
