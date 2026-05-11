# Architecture

## Goal

Build a local system where Codex can inspect and eventually control FL Studio through explicit, safe, reversible tools.

Target flow:

```text
Codex -> MCP server -> local bridge/helper -> FL Studio MIDI script -> FL Studio session
                         |
                         -> filesystem scanner for exports, stems, presets, templates, logs
```

Brain is not the runtime. Brain only keeps project memory, decisions, logs, approvals, and research.

## Current Phase

Phase 1 is a read-only FL Studio capability probe.

The probe is intentionally simple:

- Runs inside FL Studio as a MIDI script.
- Reads available session state.
- Prints chunked JSON snapshots to FL Studio Script output.
- Avoids all FL Studio setter/write/control functions.

## Future Layers

### FL Studio MIDI Script

Responsibilities:

- Read live FL Studio state.
- Later, perform approved in-DAW actions only after the read-only layer is proven.
- Stay small and auditable.

### Local Bridge / Helper

Responsibilities:

- Move structured messages between FL Studio and Codex-side tooling.
- Validate commands.
- Keep logs.
- Enforce dry-run/approval/backups for future write actions.

Candidate transports:

- MIDI/SysEx loopback for FL Studio script communication.
- Localhost socket if FL Studio's embedded Python supports it reliably.
- File inbox/outbox only from the external helper side, not from FL Studio's embedded Python unless proven safe.

### Bridge Protocol Proposal

The current bridge direction is documented in [BRIDGE_PROTOCOL_PROPOSAL.md](BRIDGE_PROTOCOL_PROPOSAL.md). It is design-only and does not approve implementation. The current bias is a read-only MIDI/SysEx bridge with explicit request IDs, chunking, timeouts, allowlisted commands, and external companion-side logging.

### MCP Server

Responsibilities:

- Expose Codex tools with clear schemas.
- Start read-only.
- Surface stale-state warnings.
- Never bypass the bridge safety layer.

Initial future tools:

- `fl_status`
- `fl_get_project_summary`
- `fl_get_mixer_snapshot`
- `fl_get_channel_snapshot`
- `fl_get_plugin_snapshot`
- `fl_make_mix_checklist`

## Environment Split

- MacBook: repo editing, docs, architecture, fixture-based MCP development.
- GitHub: code source of truth.
- Windows music laptop: FL Studio installation and actual tests.
- Brain: project memory only.
