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

## Known Working Virtual MIDI Input

Akki's Windows FL Studio setup has confirmed this working configuration:

```text
Input: LoopBe Internal MIDI
Input enabled: Yes
Controller type: Akki Read-Only MCP Probe
Output: LoopBe Internal MIDI visible, but not enabled
Send master sync: Off
```

Keep LoopBe configured as Input only for the read-only probe. Do not enable the same LoopBe port as Output during this phase.

## Enable In FL Studio

1. Open FL Studio.
2. Open a disposable/sandbox project.
3. Go to `Options -> MIDI settings`.
4. In the Input list, select `LoopBe Internal MIDI`.
5. Turn Input Enable on.
6. In `Controller type`, choose `Akki Read-Only MCP Probe (user)`.
7. Leave `LoopBe Internal MIDI` disabled in Output.
8. Keep Send master sync off.
9. Open `View -> Script output`.
10. Confirm you see an initialization message.

## Expected Output

The probe prints snapshots to `View -> Script output`. Look for:

```text
[AkkiReadOnlyProbe] SNAPSHOT_BEGIN reason=OnInit chunks=...
[AkkiReadOnlyProbe] SNAPSHOT_CHUNK 1/... {...}
[AkkiReadOnlyProbe] SNAPSHOT_END
```

No snapshot folder or JSON file is expected in v0.1.2. FL Studio MIDI script filesystem writes are intentionally avoided.

## Remove

Close FL Studio, then delete:

```text
%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\AkkiReadOnlyProbe\
```

The probe does not modify `.flp` files. Removing the folder disables the script.
