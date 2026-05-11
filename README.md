# FL Studio MCP

Repo-ready source for an eventual Codex-to-FL-Studio control bridge.

Current status: read-only capability probe only. v0.1.2 prints snapshots to FL Studio Script output, avoids FL Studio filesystem writes, starts playlist scanning at track 1, and reports both raw and normalized tempo.

## Environment Model

- MacBook: Codex, Brain, planning, architecture, repo editing, documentation, fixture-based MCP development.
- GitHub repo: source of truth for code.
- Windows music laptop: FL Studio, plugins/templates, manual install, and real testing.
- Brain: logs, roadmap, research, approvals, decisions, and task tracking.

Do not assume FL Studio is installed on the Mac. Do not install this probe into real FL Studio folders from Mac-side Codex.

## What Exists Now

- A read-only FL Studio MIDI script probe.
- Windows install/removal instructions.
- A sandbox test plan.
- Snapshot schema and redacted example output.
- Placeholder docs for the future bridge and MCP server.
- A repo rulebook for future Codex/research/build sessions.
- A design-only read-only bridge protocol proposal.

## Repo Structure

```text
fl-studio-mcp/
  README.md
  AGENTS.md
  .gitignore
  docs/
    ARCHITECTURE.md
    SAFETY.md
    MAC_TO_WINDOWS_WORKFLOW.md
    BRIDGE_PROTOCOL_PROPOSAL.md
    WINDOWS_PROBE_INSTALL.md
    READ_ONLY_PROBE_TEST_PLAN.md
  fl-studio/
    midi-scripts/
      akki_read_only_probe/
        device_AkkiReadOnlyProbe.py
        README.md
  schemas/
    fl_session_snapshot.schema.json
  examples/
    snapshots/
      README.md
      redacted_snapshot.example.json
  bridge/
    README.md
  mcp-server/
    README.md
  tests/
    fixtures/
      README.md
```

## Read-Only Probe

The first probe is a normal FL Studio MIDI script. It attempts to read:

- FL Studio scripting/runtime information.
- Project metadata that FL Studio exposes.
- Transport state.
- Mixer track names, colors, arm/mute/solo/enabled state, and basic levels.
- Channel rack names, colors, volume, pan, mute/solo, type, and target mixer track.
- Generator and mixer effect plugin slot names and parameter counts.
- Playlist track names/colors/mute/solo state where available.
- Pattern and arrangement marker information where available.

The probe does not:

- Save projects.
- Export audio.
- Rename tracks.
- Route channels.
- Arm tracks.
- Load plugins.
- Change plugin parameters.
- Use UI automation.

## Quick Windows Install

See [docs/WINDOWS_PROBE_INSTALL.md](docs/WINDOWS_PROBE_INSTALL.md).

Default FL Studio user script target:

```text
%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\AkkiReadOnlyProbe\device_AkkiReadOnlyProbe.py
```

Snapshot output is printed in `View -> Script output` as `SNAPSHOT_BEGIN`, `SNAPSHOT_CHUNK`, and `SNAPSHOT_END` lines. FL Studio MIDI script filesystem writes are not used.

## GitHub Setup

If the GitHub repo does not exist yet:

1. Create a public GitHub repo named `fl-studio-mcp`.
2. From this local folder, run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/fl-studio-mcp.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with the GitHub owner.

## Safety Rule

Use a disposable/sandbox FL Studio project for all first tests. Do not test against real music projects until the probe has been confirmed harmless.
