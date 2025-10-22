# Schemas

This directory contains JSON Schemas used by the Memory Sovereignty Pattern:

- `memory_event.schema.json` — validation for append-only memory entries
- `audit_event.schema.json` — validation for audit log records
- `consent_token.schema.json` — optional schema for pre-JWT scoped consent tokens

Use these to validate bridge outputs in CI and to normalize interop across Commons implementations.
