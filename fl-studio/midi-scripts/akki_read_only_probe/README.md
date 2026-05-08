# Akki Read-Only MCP Probe

This folder contains the FL Studio MIDI script probe.

Install this folder manually on the Windows music laptop:

```text
%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\AkkiReadOnlyProbe\
```

The final script path should be:

```text
%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\AkkiReadOnlyProbe\device_AkkiReadOnlyProbe.py
```

See:

- `docs/WINDOWS_PROBE_INSTALL.md`
- `docs/READ_ONLY_PROBE_TEST_PLAN.md`
- `docs/SAFETY.md`

This script is read-only with respect to FL Studio. It writes snapshot JSON files to a normal documents folder but does not save, export, rename, route, arm, or change plugins in FL Studio.
