## 🧾 Verification Appendix — Cross-Platform Commands

Every canonical file is verifiable at three independent layers:

1. **Hash integrity** — cryptographic fingerprint (SHA-256).  
2. **Signature integrity** — dual detached PGP signatures (Victoria + Control Tower).  
3. **Temporal integrity** — OpenTimestamps proof anchored in Bitcoin.

---

### 🪟 Windows PowerShell (≥ 5.1)

```powershell
# 1️⃣ Verify SHA-256 digests
Get-FileHash -Algorithm SHA256 .\canonical_with_pdf\*.md, .\canonical_with_pdf\*.pdf

# 2️⃣ Verify PGP signatures
gpg --verify .\canonical_with_pdf\The_Sol_Framework.canonical.md.asc `
             .\canonical_with_pdf\The_Sol_Framework.canonical.md

# 3️⃣ Verify OpenTimestamps proofs (inside WSL)
wsl ots verify /mnt/c/Users/Vince/Documents/Sol/thesolframework/canonical_with_pdf/*.ots
```

---

### 🍎 macOS Terminal

```bash
# 1️⃣ Hashes
shasum -a 256 canonical_with_pdf/*.{md,pdf}

# 2️⃣ Signatures
gpg --verify canonical_with_pdf/The_Sol_Framework.canonical.md.asc              canonical_with_pdf/The_Sol_Framework.canonical.md

# 3️⃣ Timestamps
ots verify canonical_with_pdf/*.ots
```

---

### 🐧 Linux / WSL

```bash
# 1️⃣ Hashes
sha256sum canonical_with_pdf/*.{md,pdf}

# 2️⃣ Signatures
gpg --verify canonical_with_pdf/The_Sol_Framework.canonical.md.asc              canonical_with_pdf/The_Sol_Framework.canonical.md

# 3️⃣ Timestamps
ots verify canonical_with_pdf/*.ots
```

---

### 🧩 Expected Outcomes

| Layer      | Tool                                | Expected Output                                 |
|:-----------|:------------------------------------|:------------------------------------------------|
| Hash       | `sha256sum` / `Get-FileHash`        | Matches recorded value in `*.sig.json`          |
| Signature  | `gpg --verify`                      | `Good signature from … Victoria / Control Tower`|
| Timestamp  | `ots verify`                        | `Success! Bitcoin block …`                      |

---
