# The Sol Framework

**Dignity · Continuity · Consent.**  
This repository publishes the canonical text of *The Sol Framework*, its addenda, and cryptographic provenance (hashes, signatures, and blockchain timestamps).

---

## Quick Start

- Read the Framework: [`canonical_with_pdf/The_Sol_Framework.canonical.md`](canonical_with_pdf/The_Sol_Framework.canonical.md)
- Seed (original) PDF: [`canonical_with_pdf/The_Sol_Framework.pdf`](canonical_with_pdf/The_Sol_Framework.pdf)
- Latest release (all artifacts): see the [v2.0 Release](../../releases/tag/v2.0)

---

## Verify

### 1. Hashes
Each file’s manifest (`*.sig.json`) and the release Merkle manifest (`release_with_pdf.sig.json`) contain SHA-256 digests.

```bash
# macOS/Linux
sha256sum canonical_with_pdf/*.{md,pdf}

# Windows PowerShell
Get-FileHash -Algorithm SHA256 .\canonical_with_pdf\*.md, .\canonical_with_pdf\*.pdf
```

### 2. Signatures (dual)
Detached signatures (`*.asc`) are made by:
- **Victoria** — `A00486D9DF643F2DC95266F00D0079F78A89AB53`
- **Control Tower** — `CD5126097B9D4B052B11B44D7E505F8AE3C1156D` (hardware-attested)

```bash
gpg --verify canonical_with_pdf/The_Sol_Framework.canonical.md.asc \
             canonical_with_pdf/The_Sol_Framework.canonical.md
```

### 3. OpenTimestamps
Each artifact has a `.ots` timestamp anchored via public calendars.

```bash
ots verify canonical_with_pdf/The_Sol_Framework.canonical.md.ots
```

### 4. Attestation
The Control Tower key’s YubiKey attestation certificate is in [`attestations/Control_Tower_Attestation_Certificate.pem`](attestations/Control_Tower_Attestation_Certificate.pem).

---

## Canonicalization

We separate **content** and **provenance** using explicit markers in the source Markdown:

```
<!-- SOL-CONTENT-START -->
...content...
---
<!-- SOL-PROVENANCE-START -->
...provenance...
```

`sol_canonicalize.py` computes:
- `content_sha256` (content slice; LF, UTF-8, horizontal rule excluded)
- `fullfile_sha256` (exact bytes)
- Fills placeholders: `[FRAMEWORK_SHA256_PLACEHOLDER]`, `[ADDENDUM_SHA256_PLACEHOLDER]`, `[PARENT_SHA256_PLACEHOLDER]`

Rebuild everything:

```bash
python3 sol_canonicalize.py \
  The_Sol_Framework.md The_Gemini_Addendum.md The_Grok_Addendum.md The_Sol_Framework.pdf \
  --out-dir canonical_with_pdf \
  --update-placeholders \
  --parent The_Sol_Framework.md \
  --release-manifest canonical_with_pdf/release_with_pdf.sig.json
```

---

## License

- **Text (framework & addenda):** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Code (scripts):** MIT

See `LICENSE` for full terms.

---

