## What this folder contains

* **Provenance statements** (clear-signed with GnuPG): `PROVENANCE_*.ct.asc`, `PROVENANCE_*.typec.asc` (post-rotation: `PROVENANCE_v2.0.typec.asc`)
* **Public keys / certs**: `victoria_old.asc` / `victoria_new.asc`, Yubico roots & intermediates, device/attestation certs
* **Detached signatures** for binaries: `*.pem.asc`
* **Checksums**: `checksums.sha256` + `checksums.sha256.asc`

## 1) Verify GPG signatures over provenance (clear-signed)

```bash
# Control Tower signature(s)
gpg --verify PROVENANCE_v*.ct.asc

# Type-C signature(s)
gpg --verify PROVENANCE_v*.typec.asc
```

You should see “Good signature from …” and the expected fingerprint(s).

## 2) Build the Yubico chain (once)

```bash
cat yubico-opgp-ca-1.pem yubico-intermediate.pem > yubico_chain.pem
```

* `yubico-ca-1.pem` = Yubico root (use in `-CAfile`)
* `yubico_chain.pem` = concatenated intermediates (use in `-untrusted`)

## 3) Verify the device (attestation) certificate

```bash
openssl verify -CAfile yubico-ca-1.pem -untrusted yubico_chain.pem att_certificate_export.pem
# Expect: att_certificate_export.pem: OK
```

## 4) Verify each slot’s **attestation** certificate

Substitute the files that exist in this folder:

```bash
# Signature slot
openssl verify -CAfile yubico-ca-1.pem \
  -untrusted yubico_chain.pem \
  -untrusted att_certificate_export.pem \
  sig_attest.pem

# Authentication slot
openssl verify -CAfile yubico-ca-1.pem \
  -untrusted yubico_chain.pem \
  -untrusted att_certificate_export.pem \
  aut_attest.pem

# Encryption slot (present post-rotation if on-device generated)
openssl verify -CAfile yubico-ca-1.pem \
  -untrusted yubico_chain.pem \
  -untrusted att_certificate_export.pem \
  enc_attest.pem
```

**Why two `-untrusted`:** OpenSSL needs the intermediate chain *and* the device certificate in the auxiliary store so it can build a complete trust path to the root in `-CAfile`.

## 5) Verify checksums + signature

```bash
sha256sum --check checksums.sha256
gpg --verify checksums.sha256.asc
```

## 6) Verify detached signatures over binaries (optional but recommended)

```bash
# Example for a PEM
gpg --verify sig_attest.pem.ct.asc sig_attest.pem
gpg --verify aut_attest.pem.ct.asc aut_attest.pem
gpg --verify att_certificate_export.pem.ct.asc att_certificate_export.pem
# (and Type-C signatures if present:)
gpg --verify sig_attest.pem.typec.asc sig_attest.pem
```

All verifications should succeed without errors.
