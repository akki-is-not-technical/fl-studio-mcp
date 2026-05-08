# Read-Only Probe Test Plan

## Goal

Confirm what FL Studio state can be read safely from a MIDI script on the Windows music laptop.

## Preconditions

- FL Studio installed on Windows.
- Repo pulled or downloaded on Windows.
- Probe installed using `docs/WINDOWS_PROBE_INSTALL.md`.
- Disposable/sandbox `.flp` open.
- FL Studio version recorded below.

```text
FL Studio version:
Windows version:
Probe version: 0.1.0
Date tested:
```

## Sandbox Project Setup

Create a simple test project:

- Rename the project title if you want to test metadata.
- Create or rename 2-4 mixer tracks.
- Create or rename 2-4 channels.
- Add only stock/safe plugins if you want plugin-slot visibility.
- Add 1-2 patterns.
- Add 1-2 playlist track names if desired.
- Save as a disposable test project only if you want, with an obvious name like `FL MCP Sandbox.flp`.

Do not use a real song session.

## Test Steps

1. Open the sandbox project.
2. Enable `Akki Read-Only MCP Probe (user)` in MIDI Settings.
3. Open `View -> Script output`.
4. Confirm an initialization message appears.
5. Wait 5-10 seconds.
6. Check the snapshot output folder.
7. Confirm at least one `.json` snapshot exists.
8. Open the latest snapshot in a text editor.
9. Check whether these sections are populated:
   - `environment`
   - `project`
   - `transport`
   - `mixer.tracks`
   - `channels.items`
   - `plugins`
   - `playlist.tracks`
   - `patterns`
   - `errors`
10. Make a small safe sandbox change, such as renaming a mixer track.
11. Wait for another snapshot or reload the script from Script output.
12. Check whether the new name appears.

## What To Copy Back To Codex

Copy back:

- FL Studio version.
- Whether the script appears in MIDI Settings.
- Any Script output errors.
- The latest snapshot JSON after removing any private song/client names.
- Whether mixer/channel/plugin/playlist sections looked useful.
- Whether project changed state stayed safe.

Do not copy snapshots from real songs.

## Pass Criteria

- Probe loads without compile/runtime errors.
- Snapshot file is created.
- Snapshot contains at least project/environment/transport data.
- No real project files are changed.
- No audio export or UI automation occurs.

## Fail Criteria

- Probe does not appear in MIDI Settings.
- Probe errors on import.
- Snapshot folder is not created.
- FL Studio shows project changes caused by the probe.
- Any unexpected control/write behavior occurs.

If fail criteria occur, remove the probe folder and report the Script output text.
