# Mac-To-Windows Workflow

## Roles

- MacBook: Codex, Brain, repo editing, docs, architecture, MCP development against fixture snapshots.
- GitHub: source of truth for code.
- Windows music laptop: FL Studio and real tests.
- Brain: logs, decisions, tasks, approvals, and research notes.

## Normal Loop

1. Update code/docs on Mac.
2. Commit and push to GitHub.
3. Pull or download the repo on Windows.
4. Install the probe manually into FL Studio's MIDI scripting folder.
5. Test in a disposable/sandbox `.flp`.
6. Copy sanitized probe output back to Codex.
7. Update Brain with findings, blockers, and next steps.

## What Not To Do

- Do not assume FL Studio is installed on Mac.
- Do not keep product code inside Brain.
- Do not copy scripts into real FL Studio folders from Mac-side Codex.
- Do not test against real FL Studio projects until sandbox tests are proven safe.

## Sync Options

### Option A: Git On Windows

```powershell
git clone https://github.com/YOUR_USERNAME/fl-studio-mcp.git
cd fl-studio-mcp
git pull
```

### Option B: Download ZIP

1. Open the public GitHub repo in a browser.
2. Use Code -> Download ZIP.
3. Extract it somewhere easy, such as `Documents\Code\fl-studio-mcp`.

Option A is better once Git is set up on Windows.
