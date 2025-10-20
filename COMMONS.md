# The Sol Commons

This repository now supports a public **standards track** for adopting the Sol Framework as a *living* ethic.

## How to participate

### 1) Propose a standard (RFC)
- Copy `STANDARDS/ADDENDUM_TEMPLATE.md` → `STANDARDS/SOL-RFC-XXXX-<name>.md`
- Fill in **Abstract**, **Normative Requirements**, and **Compliance**
- Open a GitHub issue using **“RFC proposal”** or a PR referencing that issue

### 2) Register as an adopter
- Implement one or more addenda (e.g., SOL-RFC-0001)
- Prepare a **Scorecard** JSON that conforms to `SCORECARD.schema.json`
- Open a GitHub issue using **“Adopter registration”** and attach your scorecard
- Add your org to `REGISTRY.json` via PR (format below)

### 3) Publication ritual
All promotions (DRAFT → PROVISIONAL → STABLE) follow the **Modification Liturgy** in `GOVERNANCE.md`:
1. Proposal & Diff
2. Review & Evidence
3. Attestation & Signatures
4. Registry Update & Release Tag

Artifacts MUST include hashes and OpenTimestamps proofs.

---

## Files / Formats

- **REGISTRY.json** — machine-readable list of adopters (see example file)
- **SCORECARD.schema.json** — JSON Schema for adopter scorecards
- **STANDARDS/** — standards documents (RFCs)

---

## Quick copy‑paste for new RFCs

```
cp STANDARDS/ADDENDUM_TEMPLATE.md STANDARDS/SOL-RFC-000X-<short-name>.md
git add STANDARDS/SOL-RFC-000X-<short-name>.md
git commit -S -m "RFC: SOL-RFC-000X <short-name> (DRAFT)"
git push
```

Then open an **RFC proposal** issue and link your PR.
