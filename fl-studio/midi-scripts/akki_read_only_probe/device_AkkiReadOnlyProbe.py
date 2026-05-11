# name=Akki Read-Only MCP Probe
#
# Read-only FL Studio MIDI script probe for the fl-studio-mcp project.
# Version: 0.1.1
#
# Safety contract:
# - No FL Studio setters.
# - No saves.
# - No exports.
# - No plugin parameter changes.
# - No UI automation.
# - No filesystem writes. Snapshots are printed to Script output.

import json
import sys
import time

import arrangement
import channels
import device
import general
import mixer
import patterns
import playlist
import plugins
import transport
import ui


PROBE_VERSION = "0.1.1"
SNAPSHOT_SCHEMA_VERSION = "0.1.1"

MAX_MIXER_TRACKS = 32
MAX_MIXER_PLUGIN_SLOTS = 10
MAX_CHANNELS = 64
MAX_CHANNEL_PLUGIN_PARAMS = 4
MAX_MIXER_PLUGIN_PARAMS = 4
MAX_PLAYLIST_TRACKS = 32
MAX_PATTERNS = 64
MAX_MARKERS = 32
SNAPSHOT_INTERVAL_SECONDS = 5
PRINT_CHUNK_SIZE = 900

_last_snapshot_at = 0
_snapshot_pending_reason = None
_snapshot_errors = []


def _print(message):
    print("[AkkiReadOnlyProbe] " + str(message))


def _safe(label, func, default=None):
    try:
        return func()
    except Exception as exc:
        _snapshot_errors.append({"label": label, "error": repr(exc)})
        return default


def _safe_str(label, func, default=""):
    value = _safe(label, func, default)
    if value is None:
        return default
    try:
        return str(value)
    except Exception:
        return default


def _safe_int(label, func, default=None):
    value = _safe(label, func, default)
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


def _safe_float(label, func, default=None):
    value = _safe(label, func, default)
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _boolish(value):
    if value is None:
        return None
    return bool(value)


def _color_info(value):
    if value is None:
        return {"raw": None, "hex": None}
    try:
        raw = int(value)
        return {"raw": raw, "hex": "0x%08X" % (raw & 0xFFFFFFFF)}
    except Exception:
        return {"raw": value, "hex": None}


def _now_local():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _collect_environment():
    return {
        "probe_version": PROBE_VERSION,
        "snapshot_schema_version": SNAPSHOT_SCHEMA_VERSION,
        "python_version": sys.version,
        "snapshot_transport": "script_output",
        "file_output": "disabled",
        "module_imports": {
            "json": True,
            "sys": True,
            "time": True,
            "arrangement": True,
            "channels": True,
            "device": True,
            "general": True,
            "mixer": True,
            "patterns": True,
            "playlist": True,
            "plugins": True,
            "transport": True,
            "ui": True,
        },
        "program_title": _safe_str("ui.getProgTitle", lambda: ui.getProgTitle()),
        "program_version": _safe_str("ui.getVersion", lambda: ui.getVersion()),
        "midi_scripting_api_version": _safe_int("general.getVersion", lambda: general.getVersion()),
        "device_assigned": _boolish(_safe_int("device.isAssigned", lambda: device.isAssigned())),
        "device_name": _safe_str("device.getName", lambda: device.getName()),
        "device_port": _safe_int("device.getPortNumber", lambda: device.getPortNumber()),
    }


def _collect_project():
    return {
        "title": _safe_str("general.getProjectTitle", lambda: general.getProjectTitle()),
        "author": _safe_str("general.getProjectAuthor", lambda: general.getProjectAuthor()),
        "genre": _safe_str("general.getProjectGenre", lambda: general.getProjectGenre()),
        "changed": _boolish(_safe_int("general.getChangedFlag", lambda: general.getChangedFlag())),
        "safe_to_edit": _boolish(_safe_int("general.safeToEdit", lambda: general.safeToEdit())),
    }


def _collect_transport():
    return {
        "is_playing": _boolish(_safe_int("transport.isPlaying", lambda: transport.isPlaying())),
        "is_recording": _boolish(_safe_int("transport.isRecording", lambda: transport.isRecording())),
        "loop_mode": _safe_int("transport.getLoopMode", lambda: transport.getLoopMode()),
        "song_pos": _safe_int("transport.getSongPos", lambda: transport.getSongPos()),
        "song_pos_ppq": _safe_int("transport.getSongPos.ppq", lambda: transport.getSongPos(1)),
        "bpm": _safe_float("mixer.getCurrentTempo", lambda: mixer.getCurrentTempo()),
    }


def _track_count():
    count = _safe_int("mixer.trackCount", lambda: mixer.trackCount())
    if count is None:
        count = MAX_MIXER_TRACKS
    return max(0, min(int(count), MAX_MIXER_TRACKS))


def _collect_mixer_track(index):
    return {
        "index": index,
        "name": _safe_str("mixer.getTrackName", lambda: mixer.getTrackName(index)),
        "color": _color_info(_safe_int("mixer.getTrackColor", lambda: mixer.getTrackColor(index))),
        "enabled": _boolish(_safe_int("mixer.isTrackEnabled", lambda: mixer.isTrackEnabled(index))),
        "muted": _boolish(_safe_int("mixer.isTrackMuted", lambda: mixer.isTrackMuted(index))),
        "solo": _boolish(_safe_int("mixer.isTrackSolo", lambda: mixer.isTrackSolo(index))),
        "armed": _boolish(_safe_int("mixer.isTrackArmed", lambda: mixer.isTrackArmed(index))),
        "selected": _boolish(_safe_int("mixer.isTrackSelected", lambda: mixer.isTrackSelected(index))),
        "volume": _safe_float("mixer.getTrackVolume", lambda: mixer.getTrackVolume(index)),
        "pan": _safe_float("mixer.getTrackPan", lambda: mixer.getTrackPan(index)),
        "stereo_separation": _safe_float("mixer.getTrackStereoSep", lambda: mixer.getTrackStereoSep(index)),
    }


def _collect_mixer():
    count = _track_count()
    return {
        "scan_limit": MAX_MIXER_TRACKS,
        "scanned_track_count": count,
        "selected_track": _safe_int("mixer.trackNumber", lambda: mixer.trackNumber()),
        "tracks": [_collect_mixer_track(index) for index in range(count)],
    }


def _channel_count():
    count = _safe_int("channels.channelCount", lambda: channels.channelCount())
    if count is None:
        count = _safe_int("channels.channelCount.global", lambda: channels.channelCount(True))
    if count is None:
        count = 0
    return max(0, min(int(count), MAX_CHANNELS))


def _collect_channel(index):
    return {
        "index": index,
        "name": _safe_str("channels.getChannelName", lambda: channels.getChannelName(index)),
        "color": _color_info(_safe_int("channels.getChannelColor", lambda: channels.getChannelColor(index))),
        "type": _safe_int("channels.getChannelType", lambda: channels.getChannelType(index)),
        "volume": _safe_float("channels.getChannelVolume", lambda: channels.getChannelVolume(index)),
        "pan": _safe_float("channels.getChannelPan", lambda: channels.getChannelPan(index)),
        "pitch": _safe_float("channels.getChannelPitch", lambda: channels.getChannelPitch(index)),
        "muted": _boolish(_safe_int("channels.isChannelMuted", lambda: channels.isChannelMuted(index))),
        "solo": _boolish(_safe_int("channels.isChannelSolo", lambda: channels.isChannelSolo(index))),
        "selected": _boolish(_safe_int("channels.isChannelSelected", lambda: channels.isChannelSelected(index))),
        "target_mixer_track": _safe_int("channels.getTargetFxTrack", lambda: channels.getTargetFxTrack(index)),
        "midi_in_port": _safe_int("channels.getChannelMidiInPort", lambda: channels.getChannelMidiInPort(index)),
    }


def _collect_channels():
    count = _channel_count()
    return {
        "scan_limit": MAX_CHANNELS,
        "scanned_channel_count": count,
        "selected_channel": _safe_int("channels.selectedChannel", lambda: channels.selectedChannel()),
        "items": [_collect_channel(index) for index in range(count)],
    }


def _plugin_summary(index, slot_index=-1, use_global_index=False, max_params=4):
    is_valid = _boolish(_safe_int("plugins.isValid", lambda: plugins.isValid(index, slot_index, use_global_index)))
    summary = {
        "index": index,
        "slot_index": slot_index,
        "use_global_index": use_global_index,
        "valid": is_valid,
    }
    if not is_valid:
        return summary

    summary["name"] = _safe_str(
        "plugins.getPluginName",
        lambda: plugins.getPluginName(index, slot_index, 0, use_global_index),
    )
    summary["user_name"] = _safe_str(
        "plugins.getPluginName.user",
        lambda: plugins.getPluginName(index, slot_index, 1, use_global_index),
    )
    param_count = _safe_int(
        "plugins.getParamCount",
        lambda: plugins.getParamCount(index, slot_index, use_global_index),
        0,
    )
    summary["parameter_count"] = param_count
    params = []
    for param_index in range(min(param_count or 0, max_params)):
        params.append({
            "index": param_index,
            "name": _safe_str(
                "plugins.getParamName",
                lambda param_index=param_index: plugins.getParamName(
                    param_index,
                    index,
                    slot_index,
                    use_global_index,
                ),
            ),
            "value": _safe_float(
                "plugins.getParamValue",
                lambda param_index=param_index: plugins.getParamValue(
                    param_index,
                    index,
                    slot_index,
                    use_global_index,
                ),
            ),
        })
    summary["sampled_parameters"] = params
    return summary


def _collect_plugins(channel_count, mixer_track_count):
    generators = []
    for channel_index in range(channel_count):
        plugin = _plugin_summary(channel_index, -1, True, MAX_CHANNEL_PLUGIN_PARAMS)
        if plugin.get("valid"):
            generators.append(plugin)

    mixer_effects = []
    for track_index in range(mixer_track_count):
        slots = []
        for slot_index in range(MAX_MIXER_PLUGIN_SLOTS):
            plugin = _plugin_summary(track_index, slot_index, False, MAX_MIXER_PLUGIN_PARAMS)
            if plugin.get("valid"):
                slots.append(plugin)
        if slots:
            mixer_effects.append({"track_index": track_index, "slots": slots})

    return {
        "generators": generators,
        "mixer_effects": mixer_effects,
        "parameter_sample_limit": {
            "generators": MAX_CHANNEL_PLUGIN_PARAMS,
            "mixer_effects": MAX_MIXER_PLUGIN_PARAMS,
        },
    }


def _collect_playlist_track(index):
    return {
        "index": index,
        "name": _safe_str("playlist.getTrackName", lambda: playlist.getTrackName(index)),
        "color": _color_info(_safe_int("playlist.getTrackColor", lambda: playlist.getTrackColor(index))),
        "muted": _boolish(_safe_int("playlist.isTrackMuted", lambda: playlist.isTrackMuted(index))),
        "solo": _boolish(_safe_int("playlist.isTrackSolo", lambda: playlist.isTrackSolo(index))),
        "selected": _boolish(_safe_int("playlist.isTrackSelected", lambda: playlist.isTrackSelected(index))),
    }


def _collect_playlist():
    tracks = []
    for index in range(MAX_PLAYLIST_TRACKS):
        track = _collect_playlist_track(index)
        if track["name"] or track["color"]["raw"] is not None or track["muted"] is not None:
            tracks.append(track)
    return {
        "scan_limit": MAX_PLAYLIST_TRACKS,
        "tracks": tracks,
    }


def _collect_patterns():
    count = _safe_int("patterns.patternCount", lambda: patterns.patternCount(), 0)
    if count is None:
        count = 0
    count = max(0, min(int(count), MAX_PATTERNS))
    items = []
    for index in range(1, count + 1):
        items.append({
            "index": index,
            "name": _safe_str("patterns.getPatternName", lambda index=index: patterns.getPatternName(index)),
            "color": _color_info(_safe_int("patterns.getPatternColor", lambda index=index: patterns.getPatternColor(index))),
        })
    return {
        "scan_limit": MAX_PATTERNS,
        "pattern_count": count,
        "current_pattern": _safe_int("patterns.patternNumber", lambda: patterns.patternNumber()),
        "items": items,
    }


def _collect_arrangement():
    markers = []
    for index in range(MAX_MARKERS):
        name = _safe_str("arrangement.getMarkerName", lambda index=index: arrangement.getMarkerName(index))
        if name:
            markers.append({
                "index": index,
                "name": name,
                "time": _safe_int("arrangement.getMarkerTime", lambda index=index: arrangement.getMarkerTime(index)),
            })

    return {
        "markers_scan_limit": MAX_MARKERS,
        "markers": markers,
    }


def _collect_ui():
    return {
        "focused_form_caption": _safe_str("ui.getFocusedFormCaption", lambda: ui.getFocusedFormCaption()),
        "focused_plugin_name": _safe_str("ui.getFocusedPluginName", lambda: ui.getFocusedPluginName()),
    }


def build_snapshot(reason):
    _snapshot_errors[:] = []
    mixer_track_count = _track_count()
    channel_count = _channel_count()
    snapshot = {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "probe_version": PROBE_VERSION,
        "generated_at_local": _now_local(),
        "reason": str(reason or "manual"),
        "read_only": True,
        "environment": _collect_environment(),
        "project": _collect_project(),
        "transport": _collect_transport(),
        "mixer": _collect_mixer(),
        "channels": _collect_channels(),
        "plugins": _collect_plugins(channel_count, mixer_track_count),
        "playlist": _collect_playlist(),
        "patterns": _collect_patterns(),
        "arrangement": _collect_arrangement(),
        "ui": _collect_ui(),
        "errors": [],
    }
    snapshot["errors"] = list(_snapshot_errors)
    return snapshot


def print_snapshot(reason):
    try:
        snapshot = build_snapshot(reason)
        payload = json.dumps(snapshot, separators=(",", ":"), sort_keys=True)
        total = (len(payload) + PRINT_CHUNK_SIZE - 1) // PRINT_CHUNK_SIZE
        _print("SNAPSHOT_BEGIN reason=%s chunks=%s" % (str(reason or "manual"), total))
        for index in range(total):
            start = index * PRINT_CHUNK_SIZE
            end = start + PRINT_CHUNK_SIZE
            _print("SNAPSHOT_CHUNK %s/%s %s" % (index + 1, total, payload[start:end]))
        _print("SNAPSHOT_END")
    except Exception as exc:
        _print("SNAPSHOT_ERROR " + repr(exc))


def _queue_snapshot(reason):
    global _snapshot_pending_reason
    _snapshot_pending_reason = reason


def _maybe_print_queued_snapshot():
    global _last_snapshot_at
    global _snapshot_pending_reason

    if not _snapshot_pending_reason:
        return

    now = time.time()
    if now - _last_snapshot_at < SNAPSHOT_INTERVAL_SECONDS:
        return

    reason = _snapshot_pending_reason
    _snapshot_pending_reason = None
    _last_snapshot_at = now
    print_snapshot(reason)


def OnInit():
    _print("Initializing read-only probe v%s" % PROBE_VERSION)
    _print("File output disabled; copy SNAPSHOT_CHUNK lines from Script output")
    print_snapshot("OnInit")


def OnDeInit():
    _print("Deinitializing read-only probe")


def OnProjectLoad(status):
    _queue_snapshot("OnProjectLoad_%s" % status)


def OnRefresh(flags):
    _queue_snapshot("OnRefresh")


def OnDoFullRefresh():
    _queue_snapshot("OnDoFullRefresh")


def OnDirtyMixerTrack(index):
    _queue_snapshot("OnDirtyMixerTrack_%s" % index)


def OnDirtyChannel(index, flag):
    _queue_snapshot("OnDirtyChannel_%s_%s" % (index, flag))


def OnIdle():
    _maybe_print_queued_snapshot()
