# AGENTS.md - FL Studio MCP Integration

This repo is the code source of truth for the FL Studio MCP Integration project. Brain/Obsidian is project memory only.

## Mission

Build one coherent, safe path from Codex to FL Studio:

```text
Codex -> MCP tools -> companion/bridge process -> FL Studio MIDI script -> FL Studio context/actions
```

The immediate project state is read-only. The working FL Studio probe is `v0.1.2` and has been confirmed on Windows FL Studio 2025 with `LoopBe Internal MIDI`.

## Required Context Before Work

Before proposing or changing anything, read the current repo files relevant to the task and the Brain project notes:

- `Projects/FL Studio MCP Integration/Development Log.md`
- `Projects/FL Studio MCP Integration/Roadmap.md`
- `Projects/FL Studio MCP Integration/Task Queue.md`
- `Projects/FL Studio MCP Integration/Approval Queue.md`
- `Projects/FL Studio MCP Integration/Research Notes.md`
- `Projects/FL Studio MCP Integration/Architecture Decisions.md`
- `Projects/FL Studio MCP Integration/Risk Register.md`

Treat Brain research as input, not automatic approval.

## Source Of Truth

- GitHub repo: actual source code, docs, schemas, examples, and tests.
- Brain: logs, research, decisions, task queues, approval queues, and review memory.
- Windows music laptop: the only trusted runtime test surface for FL Studio behavior.
- MacBook/Codex: planning, docs, repo editing, fixture-based development.

Do not assume FL Studio is installed on the Mac.

## Current Architecture Rules

- Bridge before MCP.
- Read-only before write/control actions.
- Companion process owns files, logs, validation, and safety policy.
- FL Studio script stays small, auditable, and focused on FL API access.
- Do not rely on FL Studio MIDI scripts writing files.
- Prefer MIDI/SysEx or another FL-supported transport for live communication.
- Do not expose arbitrary FL API forwarding to Codex.
- Do not expose arbitrary Python execution inside FL Studio.

## Safety Rules

Do not silently:

- Touch real `.flp` projects.
- Save `.flp` files.
- Export audio.
- Rename, route, arm, mute, solo, recolor, or otherwise change FL Studio state.
- Load plugins, presets, mixer states, or templates.
- Change plugin parameters.
- Use UI automation.
- Install dependencies.
- Add network/listening services.

Write/control actions require separate approval, dry-run design, sandbox testing, logs, and readback.

## Approved Work Classes

Safe without separate implementation approval:

- Read existing repo files.
- Read Brain project notes.
- Write research or design notes when requested.
- Update docs/rulebooks when explicitly approved.
- Validate JSON/schema/examples locally.

Requires Akki approval:

- Any code change.
- Any dependency addition.
- Any bridge implementation.
- Any MCP server implementation.
- Any FL Studio script behavior change.
- Any Windows setup change.
- Any write/control action.
- Any UI automation.

## Specialist Session Rules

Specialist chats may research or build only within an explicit task boundary.

Research specialist:

- Read Brain and GitHub.
- Log findings in Brain.
- Cite sources.
- Do not change code.
- Do not move tasks into Approved.
- Do not make final architecture decisions.

Builder specialist:

- Work only from an approved task spec.
- Prefer a branch/PR workflow once available.
- Do not broaden scope.
- Do not change architecture without returning to Akki/main architect.
- Update docs/tests for the exact change.

Main architect chat:

- Owns direction synthesis.
- Reviews research.
- Requests Akki approval.
- Keeps Brain, repo, roadmap, risks, and approvals coherent.

## Branch And PR Guidance

For future multi-agent work:

- One task per branch.
- One specialist per branch.
- Main architect reviews before merge.
- No direct work on risky/control features without explicit approval.
- PR descriptions must state safety boundaries and what was not changed.

## Data Privacy

Do not commit:

- Real `.flp` files.
- Real audio, stems, bounces, or exports.
- Real session snapshots unless explicitly sanitized and approved.
- Personal paths, secrets, tokens, or private project/client names.

Use synthetic or redacted fixtures only.

## Current Milestone Gate

The project has passed:

- Read-only Script-output probe works on Windows.
- Mixer track rename and mixer plugin detection are confirmed.

The next gate is design approval for a read-only bridge protocol. Implementation is not approved by this file.
