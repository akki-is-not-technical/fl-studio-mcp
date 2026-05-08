# Bridge Placeholder

Future home for the local bridge/helper that will connect the FL Studio script to Codex-side tooling.

Current status: placeholder only. No bridge implementation exists yet.

Candidate bridge options:

- File inbox/outbox.
- Localhost socket, if FL Studio embedded Python supports it reliably.
- MIDI loopback for narrow/simple control.

Safety requirements for future implementation:

- Read-only first.
- Local-only communication.
- Explicit command allowlist.
- Logs for all requests/responses.
- Dry-run and approval gates before any future write/control action.
