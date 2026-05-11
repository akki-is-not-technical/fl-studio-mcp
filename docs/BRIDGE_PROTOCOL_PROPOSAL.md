# Read-Only Bridge Protocol Proposal

Status: design proposal only. Implementation is not approved by this document.

## Purpose

Move from manual FL Studio Script-output snapshots to a reliable live bridge that can move read-only FL Studio state into an external companion process.

Current proven state:

- Probe `v0.1.2` works in FL Studio 2025 on Windows.
- `LoopBe Internal MIDI` can instantiate the script.
- The probe reads mixer tracks, channel rack, playlist tracks, transport, UI focus, mixer plugins, and sampled plugin parameters.
- FL Studio script file writes are unreliable/restricted.
- Script-output copy/paste is useful for diagnostics but can mangle structured JSON in chat.

## Target Flow

```text
Codex/MCP client
  -> MCP server, later
  -> companion process
  -> MIDI/SysEx bridge
  -> FL Studio MIDI script
  -> FL Studio read-only state
```

## Non-Goals For The First Bridge

The first bridge must not:

- Rename tracks.
- Change routing.
- Arm/disarm recording.
- Start/stop transport.
- Load plugins or presets.
- Change plugin parameters.
- Save `.flp` files.
- Export audio.
- Use UI automation.
- Forward arbitrary FL API calls.
- Execute arbitrary Python inside FL Studio.

## Current Recommendation

Use a two-port MIDI/SysEx bridge for the real live bridge:

- Command port: companion sends requests into FL Studio.
- Response port: FL Studio sends responses back to the companion.

A one-port experiment may be acceptable for a throwaway ping test, but the production bridge should prefer two ports because it is easier to reason about, debug, and protect from feedback loops.

This recommendation should be revisited after the research-head one-port vs two-port pass.

## Companion Responsibilities

The companion process runs outside FL Studio and owns:

- MIDI port discovery and configuration.
- Request IDs and timeouts.
- Chunk reassembly.
- JSON/schema validation.
- Durable snapshot files outside FL Studio.
- Debug logs and audit logs.
- Stale snapshot detection.
- Safety policy for future write actions.
- Future MCP server integration.

The companion should be able to run on Windows for live bridge testing and on Mac against fixtures for development.

## FL Studio Script Responsibilities

The FL Studio MIDI script owns only:

- Minimal bridge initialization.
- Receiving allowlisted bridge commands.
- Calling read-only FL Studio APIs.
- Returning small status messages or chunked read-only snapshot payloads.
- Reporting errors in structured responses.

The FL script should not own:

- File writing.
- Long-running work.
- Threads/async systems.
- Network sockets.
- Safety policy beyond refusing unsupported commands.
- Arbitrary code execution.

## Protocol Shape

Every logical message should include:

```json
{
  "protocol": "akki.fl.bridge",
  "protocol_version": "0.1",
  "request_id": "uuid-or-short-id",
  "direction": "request-or-response",
  "command": "bridge.ping",
  "status": "ok-or-error",
  "payload": {},
  "error": null
}
```

Large payloads should be chunked. Each chunk should include:

```json
{
  "protocol": "akki.fl.bridge",
  "protocol_version": "0.1",
  "request_id": "same-id-for-all-chunks",
  "message_type": "chunk",
  "chunk_index": 1,
  "chunk_count": 12,
  "payload_encoding": "json-or-base64-json",
  "payload_chunk": "...",
  "payload_length": 12345,
  "checksum": "optional-at-first"
}
```

Initial checksum can be optional for the first design, but the protocol should reserve the field. A later version should validate length and checksum before accepting a snapshot.

## Initial Commands

Start with the smallest read-only command set:

### `bridge.ping`

Purpose: prove FL script receives request and companion receives response.

Response payload:

```json
{
  "probe_version": "0.1.2-or-later",
  "protocol_version": "0.1",
  "fl_program_title": "FL Studio 2025",
  "device_name": "LoopBe Internal MIDI"
}
```

### `bridge.get_status`

Purpose: return bridge state without a full session snapshot.

Response payload:

```json
{
  "ok": true,
  "read_only": true,
  "last_snapshot_at": null,
  "capabilities": ["bridge.ping", "bridge.get_status", "snapshot.get_current"]
}
```

### `snapshot.get_current`

Purpose: return the same read-only state currently proven by probe `v0.1.2`.

Response payload:

- Full snapshot JSON, chunked if needed.
- Same or compatible schema as `schemas/fl_session_snapshot.schema.json`.
- Includes `snapshot_meta`, versions, errors, raw values, normalized values, and unsupported fields where applicable.

## Error Shape

Errors should be structured and non-fatal:

```json
{
  "status": "error",
  "error": {
    "code": "unsupported_command",
    "message": "Command is not allowlisted",
    "details": {}
  }
}
```

Important error codes:

- `unsupported_command`
- `bad_request`
- `busy`
- `timeout`
- `chunk_missing`
- `snapshot_failed`
- `schema_invalid`
- `internal_error`

## Timeout And Retry Policy

For the first prototype design:

- `bridge.ping`: 2 second timeout.
- `bridge.get_status`: 2 second timeout.
- `snapshot.get_current`: 10 second timeout.
- Companion may retry a request once if no chunks arrive.
- Companion should not retry indefinitely.
- FL script should ignore duplicate completed request IDs where possible.

## Port Setup Proposal

Recommended live bridge setup:

```text
Companion Output -> FL Input: Akki FL Command
FL Output -> Companion Input: Akki FL Response
```

Current `LoopBe Internal MIDI` works for script instantiation, but a two-port bridge may require loopMIDI or another multi-port virtual MIDI setup if LoopBe1 only exposes one internal port.

Research head is currently assessing one-port vs two-port details. Do not hardcode final port names until that research is reviewed.

## Safety Boundary

The bridge protocol should include a capability registry with states:

- `confirmed_read`
- `docs_candidate_write`
- `runtime_verified_write`
- `unsupported`
- `unknown`
- `blocked`

For v0.1 bridge work, only `confirmed_read` commands are enabled.

## Milestone Gates

1. Design approved.
2. Tiny ping/pong works in sandbox.
3. Status request works.
4. Chunked snapshot request works.
5. Companion validates and writes snapshot outside FL Studio.
6. Fixture tests exist for parser/reassembly/schema validation.
7. Only after this: read-only MCP tools.

## Open Questions

- Will the final bridge use LoopBe1 one-port, loopMIDI two-port, or another virtual MIDI setup?
- Should payload chunks be plain JSON text where possible or base64-encoded JSON from the start?
- What is the first acceptable chunk size on Akki's Windows FL Studio setup?
- Should checksum be implemented in the first prototype or reserved for v0.2?
- Should `snapshot.get_current` trigger a fresh scan every time, or return a cached scan unless stale?

## Recommended Next Approval After Research

Approve a tiny read-only bridge prototype with these exact boundaries:

- No MCP server yet.
- No write/control actions.
- No arbitrary API forwarding.
- No dependencies without separate approval.
- Sandbox FL Studio project only.
- Implement only `bridge.ping` first.
- Then implement `bridge.get_status` if ping is stable.
- Then design chunked `snapshot.get_current` implementation.
