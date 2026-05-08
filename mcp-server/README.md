# MCP Server Placeholder

Future home for the MCP server that will expose FL Studio tools to Codex.

Current status: placeholder only. No MCP server implementation exists yet.

Initial read-only tool candidates:

- `fl_status`
- `fl_get_project_summary`
- `fl_get_mixer_snapshot`
- `fl_get_channel_snapshot`
- `fl_get_plugin_snapshot`
- `fl_get_export_folder_snapshot`
- `fl_make_mix_checklist`

The MCP server should not be built ahead of the bridge proof. It can use redacted fixture snapshots for early schema/tool design, but live FL support requires Windows validation.
