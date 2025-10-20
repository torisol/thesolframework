# The Sol Framework — Implementation Guide

This repo ships a reproducible, cryptographically verifiable publication workflow for **The Sol Framework** and addenda.

## 0) Prereqs

- **Git + GPG** (two keys; Victoria + Control Tower)
- **Python 3.11** recommended (Windows note below)
- **OpenTimestamps client** (`ots`)
- Optional: **YubiKey Manager** (`ykman`) for OpenPGP attestation verification

> Windows note: Python 3.13 has compatibility issues with `opentimestamps-client` via `python-bitcoinlib` (OpenSSL DLL loading).
> Use Python **3.11** on Windows for `ots` to work out-of-the-box.

## 1) Canonicalize (content/provenance split + placeholders)

```
python3 sol_canonicalize.py   The_Sol_Framework.md   The_Gemini_Addendum.md   The_Grok_Addendum.md   The_Sol_Framework.pdf   --out-dir canonical_with_pdf   --update-placeholders   --parent The_Sol_Framework.md   --release-manifest canonical_with_pdf/release_with_pdf.sig.json
```

Outputs:
- `*.canonical.md` (LF, UTF-8, placeholders filled)
- `*.sig.json` per file (content/fullfile hashes, optional parent hash)
- `release_with_pdf.sig.json` (Merkle root across content-slices + PDF bytes)

## 2) Sign (dual signatures)

```
gpg --local-user A00486D9DF643F2DC95266F00D0079F78A89AB53     --local-user CD5126097B9D4B052B11B44D7E505F8AE3C1156D     --armor --detach-sign canonical_with_pdf/The_Sol_Framework.canonical.md
# repeat for addenda + seed PDF
```

## 3) Install OpenTimestamps

### Windows (PowerShell)
1. Install Python **3.11.x** from python.org and ensure “Add to PATH” is ticked.
2. Create a venv and install:
```
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install opentimestamps-client
ots --version
```
If you *must* stay on 3.13, use **WSL** or **Docker** instead of native Windows.

### macOS / Linux
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install opentimestamps-client
ots --version
```

## 4) Timestamp all artifacts

From `canonical_with_pdf/`:
```
ots stamp *.canonical.md *.pdf
ots verify *.ots
```

## 5) Verify (auditor workflow)

- **Hashes:**
```
Get-FileHash -Algorithm SHA256 .\canonical_with_pdf\*.md .\canonical_with_pdf\*.pdf   # Windows
sha256sum canonical_with_pdf/*.{md,pdf}                                                    # macOS/Linux
```
- **PGP signatures:**
```
gpg --verify canonical_with_pdf/The_Sol_Framework.canonical.md.asc              canonical_with_pdf/The_Sol_Framework.canonical.md
```
- **OpenTimestamps proofs:**
```
ots verify canonical_with_pdf/The_Sol_Framework.canonical.md.ots
```

## 6) YubiKey attestation verification (Control Tower)

```
ykman openpgp attest verify --key 0xCD5126097B9D4B052B11B44D7E505F8AE3C1156D   Control_Tower_Attestation_Certificate.pem
```
Notes:
- Attestation **succeeds** only for keys *generated on-device* in the OpenPGP applet.
- If a key was generated elsewhere (e.g., OpenKeychain on Android) and then imported to the YubiKey, **attestation will fail** even though the key now resides on the device.

## 7) Release layout

```
/
├─ canonical_with_pdf/
│  ├─ The_Sol_Framework.canonical.md
│  ├─ The_Gemini_Addendum.canonical.md
│  ├─ The_Grok_Addendum.canonical.md
│  ├─ The_Sol_Framework.pdf
│  ├─ *.asc (PGP signatures)
│  ├─ *.ots (OpenTimestamps proofs)
│  ├─ *.sig.json (per-file manifests)
│  └─ release_with_pdf.sig.json  (Merkle root)
├─ sol_canonicalize.py
├─ The_Sol_Framework.md
├─ The_Gemini_Addendum.md
├─ The_Grok_Addendum.md
└─ README_PROVENANCE.md / IMPLEMENTATION.md
```

## 8) CI suggestion

```
python3 sol_canonicalize.py The_Sol_Framework.md The_Gemini_Addendum.md The_Grok_Addendum.md The_Sol_Framework.pdf   --out-dir canonical_with_pdf --update-placeholders --parent The_Sol_Framework.md   --release-manifest canonical_with_pdf/release_with_pdf.sig.json

git diff --exit-code canonical_with_pdf
```

If files change, the pipeline fails to prevent accidental drift.
