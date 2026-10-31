# Development and release checks

The existing version source is the first line of `RELEASE_INFO.txt`: **v1.0.3**. The original `INTEGRATION/GAME_FILES_SHA256.txt` is immutable evidence for its 37 gameplay files, not a manifest to regenerate after code changes. This release preparation changes documentation and packaging only; it does not create a new gameplay version or a standalone patch.

`.gitattributes` explicitly reproduces the original gameplay files' mixed LF/CRLF endings in a Git checkout and uses LF for development text. Retain original encodings, including Windows-1251 XML and inherited script data. GitHub's automatically generated source archives may contain Git-normalized endings; use a Git clone to build and the MO2 release asset to install.

## Validate and build

Use Python 3.10 or later. Lua checks additionally require Lupa's `lua51` backend, installed in the Python environment or in an ignored local dependency directory.

```text
python tools/check_release.py
python tools/build_release.py
```

`check_release.py --lua-deps PATH` selects a local Lupa package directory. `--walo-root PATH` selects a read-only WALO 1.6.11 root containing `gamedata/`; the default is the sibling shared reference library's preserved WALO `src/`. `--menu-baseline FILE` optionally checks the matching GAMMA/ZCP menu source. External reference material and test dependencies are not bundled.

Checks verify all original gameplay hashes, XML (including the X-Ray profile fragment), LTX sections/keys, localization ID parity, private dependencies and documentation links. The WALO patch must reverse exactly to the supplied upstream controller; native WALO APIs and GAMMA menu patch contexts are checked separately. Eleven scripts compile with Lua 5.1. The unchanged `warfare.script` uses X-Ray's `continue` dialect, so its complete syntax is not claimed to pass a stock Lua parser.

Mocked tests execute production HQ helpers, module mode gates, the menu's start predicate and complete saving/DAO wrapper modules. They cover early menu choices versus saved-state checks, HQ/service restoration without spawning, save-switch cleanup, preservation of another registration, wrapper scope/delegation and repeated installation. They do not validate engine animation, full task/NPC progression, VFS, DLTX or every runtime wrapper chain.

The builder uses an explicit documentation allowlist plus the original gameplay manifest. It creates one root-`gamedata` MO2 ZIP and its SHA-256 under ignored `dist/`, and a public `RELEASE_FILES_SHA256.txt` for packaged source. It verifies every ZIP entry against source and tests CRCs. It refuses to overwrite different content under an existing filename. Do not rename or replace an already distributed different build silently.

## Focused readiness findings

- WALO integration retains native ownership, unique-service and spawn/load paths; the bundled patch describes the complete controller delta against 1.6.11.
- Story detection has distinct new-game and saved-state stages. Original storyline task files are not replaced, but three stock escort dialogue distances are changed without gating; complete Story/UNISG storyline isolation is not proven.
- Shared scientific-task state, Taskboard fallback logic and runtime wrapper order remain documented compatibility risks. No gameplay fix is included in this preparation.
- The author confirmed successful testing of the combined v1.0.3 mod. No new game run or exhaustive regression is claimed. Exact tested GAMMA/engine/DLTX versions remain unknown.

## Publication handoff

Review the diff and checks, confirm inherited-source redistribution terms, then obtain the owner's approval to commit/push, create tag `v1.0.3` and publish. Recheck GitHub Releases/tags through the owner's authenticated account before creating anything; if a different v1.0.3 asset already exists, do not overwrite it. Use the exact title and body in `RELEASE_NOTES.md`, with the ZIP and checksum as assets. Do not make the repository public without approval.

Keep local environment maps, reference libraries, logs, dumps, saves, MO2 metadata and historical test packages outside public commits and assets. The project is independent of SIN HQ; no SIN source or distribution is bundled.
