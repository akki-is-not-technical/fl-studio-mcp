# Safety Notes

## Current Probe Scope

The first FL Studio script is read-only.

Allowed:

- Read project/session metadata exposed by FL Studio.
- Read mixer/channel/playlist/plugin summaries.
- Print chunked JSON snapshots and status messages to FL Studio Script output.

Not allowed:

- Saving `.flp` files.
- Exporting audio.
- Renaming tracks.
- Routing channels.
- Arming/disarming recording tracks.
- Loading plugins.
- Changing plugin parameters.
- Applying presets or mixer states.
- UI automation.
- Touching real music projects during first tests.

## Test Project Rule

First tests must use a disposable/sandbox FL Studio project.

Good sandbox:

- Blank project.
- A few renamed mixer tracks.
- A few sample channels or stock plugins.
- No important recordings.
- No client work.
- No unreleased song session that matters.

## Snapshot Privacy

Snapshots may contain:

- Project title/author/genre if set.
- Mixer and channel names.
- Plugin names.
- Pattern/playlist names.

Do not commit real project snapshots. Share sanitized output only.

## Future Write Actions

Future write/control actions must require separate approval and should include:

- Dry-run mode.
- Clear list of intended changes.
- Sandbox testing first.
- Non-overwrite output paths.
- Action logs.
- Backup or save-new-version policy where possible.

## UI Automation Policy

UI automation is a fallback only. It is not part of this phase.

Do not add UI automation without explicit approval.
