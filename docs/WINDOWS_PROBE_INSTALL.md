# Windows Probe Install

## Before You Start

Use a disposable/sandbox FL Studio project.

Do not use a real song, client session, or unreleased project for the first probe test.

## Find The FL Studio MIDI Script Folder

The usual Windows user script location is:

```text
%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\
```

The probe should end up here:

```text
%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\AkkiReadOnlyProbe\device_AkkiReadOnlyProbe.py
```

If your FL Studio user data folder is custom, use that folder's:

```text
Settings\Hardware\
```

## Install

1. On Windows, pull or download this repo.
2. Copy this folder:

```text
fl-studio\midi-scripts\akki_read_only_probe\
```

3. Paste/rename it so the final installed folder is:

```text
%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\AkkiReadOnlyProbe\
```

4. Confirm this file exists:

```text
%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\AkkiReadOnlyProbe\device_AkkiReadOnlyProbe.py
```

## Optional Output Folder Override

By default, the probe writes snapshots to:

```text
%USERPROFILE%\Documents\FL Studio MCP Probe\Snapshots\
```

To choose a different output folder, set a Windows user environment variable:

```text
FL_MCP_PROBE_OUTPUT_DIR=C:\Users\YOUR_USER\Documents\FL Studio MCP Probe
```

Restart FL Studio after changing environment variables.

## Enable In FL Studio

1. Open FL Studio.
2. Open a disposable/sandbox project.
3. Go to `Options -> MIDI settings`.
4. Pick an unused input/controller entry.
5. In `Controller type`, choose `Akki Read-Only MCP Probe (user)`.
6. Open `View -> Script output`.
7. Confirm you see an initialization message.

## Expected Output

Snapshot JSON files should appear in:

```text
%USERPROFILE%\Documents\FL Studio MCP Probe\Snapshots\
```

File names look like:

```text
fl_snapshot_20260508_031500_OnInit.json
```

## Remove

Close FL Studio, then delete:

```text
%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\AkkiReadOnlyProbe\
```

The probe does not modify `.flp` files. Removing the folder disables the script.
