# Working Rules for WALO: UNISG Command & Operations

## Project and Change Boundaries

- Current release: **v1.0.3**, targeting S.T.A.L.K.E.R. Anomaly GAMMA + WALO 1.6.11. Do not change the version unless explicitly tasked to do so.
- External installations of GAMMA, MO2, installed mods, profiles, Overwrite, and the game are **read-only sources**, regardless of their location. Do not install mods there, change settings, create files, or run operations that write to those directories.
- Keep mod changes and outputs inside this Git repository and within the scope of the current task. Maintenance of the external shared reference library requires an explicit user task. Permission to read an external installation does not authorize modifying it.
- Shared reference materials are located outside the repository in the sibling `../_shared_reference/` directory. Treat them as read-only inputs when developing this mod; do not edit upstream sources to fix the mod. Keep local environment documentation in `../_shared_reference/environments/GAMMA/ENVIRONMENT.md`.
- Preserve the `/_reference/` rule in `.gitignore` for any future project-local notes. Do not stage reference materials, including through `git add -f`, or copy the shared library into a release. Keep absolute machine-specific paths and local environment contents out of published documentation.
- Do not change gameplay logic, Lua, XML, LTX, or integration patches without a specific task authorizing those changes. A documentation task does not authorize fixing discovered gameplay bugs.
- Do not commit or push without the user's explicit permission. Do not undo or overwrite other contributors' changes or pre-existing changes.

## Sources and Investigation Workflow

- When `../_shared_reference/environments/GAMMA/ENVIRONMENT.md` exists, use it to analyze the user's local game environment, including the installed GAMMA setup and MO2 profile. Read `../_shared_reference/INDEX.md` for preserved baselines, direct installed sources, and the source-resolution and integrity-check tools. Keep machine-specific paths and settings in the external environment map. These local files may be absent from another clone; do not invent their contents.
- Reuse existing audit results. Recheck them when the profile, version, or file set changes, or when the current task requires it; do not automatically repeat the entire analysis.
- Start with the affected files in this mod, the corresponding upstream sources, and their direct callers and callees. Expand searches through specific dependencies and symbols rather than reading thousands of files indiscriminately.
- Distinguish Anomaly sources, files from individual GAMMA mods, the reference-library snapshot, and the actual MO2 configuration. A missing loose file in GAMMA does not imply that a function is absent: it may come from game archives and be modified by Lua patches.
- Separate confirmed facts from inferences and risks. Support technical findings with specific files, functions, and line numbers where possible. Explicitly identify missing sources or information.

## Shared Files and Integration

- Before changing a shared file, compare this mod's copy with the appropriate upstream version and inspect its MO2 file providers and priorities, calling code, configurations, DLTX changes, and Lua wrappers.
- Pay particular attention to the four full-file overrides: `gamedata/scripts/warfare.script`, `gamedata/scripts/ui_mm_faction_select.script`, `gamedata/configs/scripts/beh_companion.ltx`, and `gamedata/configs/gameplay/profiles/character_desc_isg_2.xml`.
- Do not copy this mod's complete files over a different WALO/GAMMA version. When tasked with integration, port the necessary changes into the matching baseline while preserving its remaining code. Follow the patches and limitations in `INTEGRATION/UPSTREAM_EN.md`.
- The order in `modlist.txt` identifies expected file winners, but does not by itself confirm the contents of the running VFS, the result of DLTX merging, or Lua wrapper execution order. Verify these layers separately and state which layer was checked.
- Analyze the complete chain of runtime wrappers: trading, saving at the base, DAO, `axr_beh.action_beh.beh_path`, methods in `xr_corpse_detection`, and `z_taskboard_data.accept_task`. Preserve delegation to previous handlers, scope restrictions, and protection against repeated installation; account for repeated save loads within the same process.
- Do not equate the absence of a full-file override with the absence of changes to a subsystem: Taskboard and other systems are also modified through wrappers and shared tables.
- Check for section collisions and DLTX application order. New filenames alone do not guarantee that identifiers or shared data are free of conflicts.

## Gameplay and Save Compatibility

- Preserve integration with WALO's native ownership tracking, squad spawning and restoration, unique services, capacity, and base capture. Do not add a parallel spawner or repeat initial squad spawning on save load unless explicitly tasked to do so.
- This mod's mechanics are intended for **Warfare ON / Story Mode OFF**. Preserve the two-stage mode check: the new-game selection from `axr_main.config`, followed by saved-state checks during ordinary loading. Do not substitute one stage for the other.
- Avoid breaking Story Mode or normal play without Warfare. When changing shared configurations, check stock tasks and NPCs separately as well as UNISG branches. The audit found dialogue-distance changes in three stock tasks without a mode restriction; do not claim that complete Story Mode isolation has been confirmed, and do not fix this outside the task's scope.
- Player-faction checks and game-mode checks have different scopes. Do not add or remove faction restrictions on the headquarters, tasks, or services without a specific task.
- Preserve gameplay IDs, story IDs, AI sections, task and squad identifiers, infoportions, and save keys, including `walo_unisg_hq_native_v03`, `walo_unisg_workspots_furniture_v022`, campfire, sleep, and PDA keys, and `unisg_*` state. Changes to saved-state formats require an explicit task and a considered backward-compatibility approach.
- Spawned A-Life objects remain in saves after the mod is disabled. Do not delete them or perform migrations outside the task's scope; preserve the warning to roll back to a pre-installation save.
- Check the shared use of `task_target_anomaly*`, scientific-expedition state, and stock escorts. Do not treat a lock on this mod's tasks as global protection for every consumer of those variables.
- For scientific research, distinguish actual AI animation from technical credit: the current code counts five unique bodies through safe proximity, not an animation-completion event. Do not change this behavior or describe it differently without a task authorizing that change.
- Account for fixed coordinates, vertex IDs, models, and GAMMA furniture APIs. A different map or resource version requires corresponding data rather than assumptions.

## Validation and Reporting

- The author reported successful in-game testing of the combined v1.0.3 release as a single mod. Do not turn this into a claim of exhaustive regression coverage or compatibility with all GAMMA/WALO versions.
- Choose checks appropriate to the change. For documentation, review content, links, and the diff. For gameplay changes, perform suitable static checks that are available and describe which in-game scenarios remain for the author to test; do not claim in-game tests were performed without an actual run and recorded results.
- When relevant mechanics are affected, consider new games, loading, switching saves, Story ON/OFF, Warfare OFF, random starts, population changes, base capture and recapture, medic respawn, escorts, and the PDA. These are applicable scenarios, not a requirement to run the entire matrix for every edit.
- Explain results to the user in Russian, using clear language: what changed, why, which files were affected, what was checked, and what remains unknown. Do not present a risk as a reproduced bug.
