# WALO: UNISG Command & Operations v1.0.3 — upstream integration

## Purpose and baseline

Contribute a non-Story Warfare UNISG headquarters at `jup_b208`, WALO-native services, contracts and two scientific escorts to WALO. The controller baseline is **WALO 1.6.11**; the menu, companion and character-profile baselines are GAMMA-specific. An exact GAMMA release is not documented.

The author successfully tested the combined v1.0.3 archive in game as one mod. All 37 game files remain unchanged during GitHub release preparation. This is not exhaustive regression coverage or proof of compatibility with every WALO/GAMMA version.

## Full-file overrides

| File under `gamedata/` | Functions/data and reason |
|---|---|
| `scripts/warfare.script` | `unisg_hq_mode()` and HQ/service helpers; additions to `fill_start_position()`, `actor_on_first_update()` and `on_game_start()`. Register the HQ, seed through WALO's existing pass and restore transient state. See `WALO_1.6.11_warfare.patch`. |
| `scripts/ui_mm_faction_select.script` | `UINewGame:LoadMap()` filters the HQ start by UNISG/Warfare/Story settings; `on_game_load()` records its orientation and `actor_on_first_update()` passes it to `ChangeLevel`. See `GAMMA_faction_select.patch`. |
| `configs/scripts/beh_companion.ltx` | Routes the two private researcher squads into their behavior sections; adds scanning/return-dialogue logic. Also contains three ungated stock dialogue-distance changes described below. No dedicated integration patch is supplied for this file. |
| `configs/gameplay/profiles/character_desc_isg_2.xml` | Appends four science-dialogue IDs to a shared GAMMA NPC profile. Dialogue preconditions identify the private expedition NPCs. Preserve GAMMA's existing ranks, supplies and includes. No dedicated integration patch is supplied. |

Port the supplied patches into matching current sources; **do not replace newer WALO/GAMMA files wholesale**. Merge companion/profile changes separately. This project does not modify the source files `smart_terrain_warfare.script`, `tm_warfare.ltx`, `tm_dynamic.ltx`, `tm_yantar.ltx`, `xr_conditions.script`, `xr_effects.script` or Taskboard, but it does extend shared runtime tables/functions.

## Why the WALO controller is changed

WALO's ordinary `IsStoryMode()` / `story_mode_disabled` state is not authoritative during early new-game seeding. The menu has written its checkbox to `axr_main.config` before `ui_mm_faction_select.on_game_load()` creates the infoportion.

- **New game:** while transient `new_game_faction` is present, read `axr_main.config:r_value("character_creation", "new_game_story_mode", 1)`. A true value excludes the HQ; unchecked is stored as nil.
- **Loaded save:** require `has_alife_info("story_mode_disabled") and not IsStoryMode()`.
- **Both paths:** require `IsWarfare()`. Do not replace one stage with the other or use an old save's infoportion as the new-game checkbox.

The added initialization runs inside `fill_start_position()`, before WALO's ownership commit. It attempts two `isg_sim_squad_novice` squads only for an unmarked new game, an eligible empty base and enabled ISG new-game spawning. The marker is saved after the first successful spawn; if a later attempt fails, two squads are not guaranteed. Do not retry initial spawning on load or add a parallel spawner. Random Starting Locations uses an earlier return and bypasses this normal seeding path.

`unisg_hq_restore()` requires the existing opt-in marker; it restores registration/services/capacity without spawning squads. `on_game_start()` reverses this add-on's temporary registration and service-slot changes before another save is initialized. Preserve that cleanup for save switching within the same process.

## WALO APIs and ownership

No new exported WALO API is required. The extension consumes WALO 1.6.11's existing interfaces:

- `smart_terrain_warfare.is_main_base()`, `get_main_base_faction()` and `set_main_base()`: register `jup_b208` with `faction="isg", protect=false, resurrect=true`, avoiding another add-on's existing entry.
- `smart_terrain_warfare.uniques["jup_b208"]`: retain trader/mechanic slots and enable native medic/barman slots. Snapshot and restore only the changed slots; keep `check_unique_npcs()` in charge of service creation and replacement.
- `get_stalker_pop_factor()` and `smart_terrain_warfare.set_max_population()`: compute raw capacity as four divided by the population factor so normal bootstrap/restoration yields four effective slots. Later WALO population-setting changes can resize the base.
- `SIMBOARD`, `spawn_squad()` and `alife_storage_manager.get_state()`: reuse WALO's smart ownership, initial squad pass and save state.

WALO retains production, unique-service checks, capture and resurrection. HQ simulation is not limited to an UNISG actor; the menu, base-saving exception and science/contracts apply their separate actor restrictions. Do not silently unify these scopes.

## Runtime dependencies and wrappers

| Module suffix under `gamedata/scripts/zzzzzz_walo_unisg_*` | Integration |
|---|---|
| `hq_base_saving` | Wraps `ish_campfire_saving.is_within_friendly_base`; only an ISG actor inside the bounded ISG-owned Jupiter HQ gets the extra saving allowance. Delegates otherwise. |
| `hq_dao_guard` | Wraps `drx_da_main.drx_da_spawn_anomaly_on_smart`; blocks new `jup_b208` generation on Jupiter in supported modes, regardless of base ownership. Does not remove saved anomalies. |
| `workspots_anchors` | Wraps `axr_beh.action_beh.beh_path`; temporary seat-arrival adjustment restores the target vertex even on errors. Check WALO and other seat wrappers across repeated loads. |
| `field_science` | Wraps `xr_corpse_detection.near_actor`, `evaluator_corpse.find_valid_target/evaluate`, `action_search_corpse.execute`, and `z_taskboard_data.accept_task`. Updates Taskboard caches/metadata and registers private handlers in `xr_effects`, `xr_conditions`, `task_functor` and `task_status_functor`. |

The seven-`z` `zzzzzzz_walo_unisg_hq_trade_spots.script` also wraps `trade_manager.trade_init` for native GAMMA role profiles and owned PDA markers. The wrapper chain must preserve delegation to earlier handlers. Saving/DAO wrappers warn about later replacements; not all wrappers automatically reinstall. Science hooks install at startup when native functions are available. Filename order alone does not prove the final handler chain.

Furniture uses `placeable_furniture.create_object`, `hf_obj_manager.update_data`, GAMMA's `placeable_bed_2`, `placeable_light8`, `placeable_clinic_equipments`, and WALO's chair model. Workspots, the menu start and medic correction depend on measured Jupiter coordinates/vertex IDs. The medic correction targets a generated `sim_default_isg_medic` assigned to the ISG-owned HQ, rather than a named story NPC. The sleep marker requires the real bed. Do not relocate these resources or generalize NPC targeting without a separate task.

DLTX files add private squads, tasks, dialogues, start locations and workspots. Check final section IDs, include resolution and merge order as well as loose-file winners. Stock storyline task files are not replaced; the shared NPC profile and stock companion branches still require review.

## Known limitations retained in v1.0.3

- `beh_companion.ltx` changes `ecolog_companion_task_1`, `ecolog_companion_task_2` and `bandit_companion_task_1` forced-dialogue distance from 3 to 6 metres without a mode restriction (lines 100, 106 and 119). Full Story Mode/UNISG storyline isolation has not been confirmed.
- The private expedition lock does not prove mutual exclusion for every stock consumer of `task_target_anomaly*` and native scientific-expedition state. Test stock escorts alongside the private tasks.
- `field_science.install_pda_science_guard()` uses `tid==MEASURE and measure_available() or research_available()` (line 1116). If the first availability check is false, the research result can be used for a stale Contour offer. This source-level weakness is confirmed; in-game consequences have not been reproduced. The task initializer separately rechecks availability.
- Corpse research credits five distinct bodies through safe proximity, 12 seconds per body, rather than animation completion. Keep the scoped native AI/Useful Idiots hooks and existing saved progress.
- Expected winners from MO2's profile/providers do not confirm running VFS contents, DLTX results or wrapper execution order. Exact engine/GAMMA/DLTX versions and a complete UNISG storyline playthrough remain unverified.

With SIN HQ 2.0.1, use its separately distributed combined WALO/UNISG/SIN controller. Source comparison shows its three SIN lifecycle additions preserve this UNISG controller's remaining code. This is source evidence, not a new joint gameplay test; SIN HQ is not required or bundled by UNISG.

## Save compatibility and porting checks

Preserve ALL task/squad IDs, infoportions and `unisg_*` state, plus these one-time keys:

- `walo_unisg_hq_native_v03`
- `walo_unisg_workspots_furniture_v022` and its retained legacy keys
- `walo_unisg_hq_campfire_jup_b208_v01`, `walo_unisg_hq_campfire_jup_b208_v02`
- `walo_unisg_sleep_marker_jup_b208_v01`
- `walo_unisg_hq_owned_pda_spots_v07`

Removing the mod does not remove A-Life objects already serialized in saves. Roll back to a pre-installation save.

For a port or changed gameplay, check new games, reloads and save switching; Story ON/OFF and Warfare OFF; random starts; population changes; capture/recapture; native services and medic respawn; stock and scientific escorts; Taskboard/PDA; campfire/base saving and new DAO generation. These scenarios remain a maintainer checklist, not a claim that every case was run.

See [development checks](../DEVELOPMENT.md) and [third-party notices](../THIRD_PARTY_NOTICES.md). Keep original attribution and resolve inherited-source redistribution terms before public distribution.
