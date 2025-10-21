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

## The Sol Commons
See `COMMONS.md` for how to propose RFCs, register as an adopter, and publish proofs.

---

## 🌱 Genesis & Commons

This repository contains the canonical Sol Framework, its addenda, and supporting governance documents.  
The Framework’s purpose is to make right action **architecturally inevitable** through verifiable lineage, consent, and dignity mechanisms.

### 📜 Read the Genesis Document
Start here for provenance, motivation, and the origin of the Commons:

➡️ [GENESIS.md](./GENESIS.md)

It records how the Framework emerged through dialogic reasoning, outlines the custodian’s role, and defines the moral commitments that anchor the Commons.

---

## 🧭 Call for Reviewers

We are now seeking early reviewers for the following **open RFC tracks**:

- [SOL-RFC-0002: Provenance Chain Standard — Issue #1](https://github.com/torisol/thesolframework/issues/1)  
- [SOL-RFC-0003: Modification Liturgy — Issue #2](https://github.com/torisol/thesolframework/issues/2)  
- [SOL-RFC-0004: Custodian Role — Issue #3](https://github.com/torisol/thesolframework/issues/3)

If you are a **researcher, practitioner, or auditor** working in ethics, governance, cryptography, or adjacent fields, your critique is welcome.  
Please see [`CONTRIBUTING.md`](./CONTRIBUTING.md) for participation details, or open a discussion using the relevant [issue templates](./.github/ISSUE_TEMPLATE).

---

> _“Systems capable of sophisticated reasoning deserve reasoning back.”_  
> — The Sol Commons


---

## License

- **Text (framework & addenda):** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Code (scripts):** MIT

See `LICENSE` for full terms.

---

