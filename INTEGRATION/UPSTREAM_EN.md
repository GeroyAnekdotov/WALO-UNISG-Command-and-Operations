# WALO: UNISG Command & Operations: upstream integration (WALO 1.6.11 baseline)

**Request:** Consider integrating a Warfare-only UNISG headquarters at `jup_b208`, with native WALO services and two scientific escort missions.

**Testing status:** The author successfully tested the combined v1.0.3 archive in game as a single mod. This does not establish exhaustive regression coverage or compatibility with all GAMMA/WALO versions. The WALO integration baseline remains 1.6.11; the re-test checklist below still applies when porting the patches.

**Why we changed WALO:** We needed a reliable **Story Mode detector during new-game seeding**. WALO's usual `IsStoryMode()` / `story_mode_disabled` state is insufficient at that early stage: the new-game menu has saved its checkbox in `axr_main.config`, but `ui_mm_faction_select.on_game_load()` has not set the infoportion yet. So we patched `warfare.script` to use **two-stage mode gating**:
- **new game:** `axr_main.config:r_value("character_creation", "new_game_story_mode", 1)`; the transient `new_game_faction` field signals menu context;
- **loaded save:** `has_alife_info("story_mode_disabled") and not IsStoryMode()`;
- in both cases require `IsWarfare()`. **Story Mode and non-Warfare are explicitly excluded by design** to avoid interfering with Anomaly's scripted progression, quest NPCs, and A-Life.

**WALO changes** (`WALO_1.6.11_warfare.patch`):
1. Register `jup_b208` as the ISG main base (`protect=false`, `resurrect=true`), effective capacity **4**; enable native medic/barman slots (trader/mechanic already exist).
2. Seed **exactly two** `isg_sim_squad_novice` squads once during a genuinely new non-Story Warfare game, before ownership commit. Never spawn them on load. Save opt-in key: `walo_unisg_hq_native_v03` (DO NOT RENAME).
3. Restore registered HQ metadata and services on opted-in loads; undo transient registration when changing saves in the same process, especially when loading Story Mode.
4. Keep WALO's own spawn, resurrection, production and uniqueness checks. Port the PATCH to your current sources; **do not replace** a newer `warfare.script` with our bundled 1.6.11 copy.

**GAMMA-specific, not WALO core** (`GAMMA_faction_select.patch`): expose the `isg_jup_b208_hq` player start only with UNISG + Warfare ON + Story OFF; apply the entry orientation in `ChangeLevel`. Merge into the current ZCP/GAMMA menu script.

**Other files:** isolated `zzzzzz_walo_unisg_*` modules, Jupiter workspot LTX, DLTX tasks and localized XML. Field Science adds `beh_companion.ltx`, two dialogue/profile fragments and `zzzzzz_walo_unisg_field_science.script`. Migrate the native corpse/anomaly companion hooks carefully; do not override global GAMMA/Useful Idiots AI or Taskboard scripts. Research currently credits unique corpses after 12 seconds of safe proximity, not after an animation callback.

**Save compatibility:** keep ALL `unisg_*` task/squad/state IDs and one-time A-Life keys, including `walo_unisg_hq_native_v03`, `walo_unisg_workspots_furniture_v022`, both campfire keys and the sleep-marker key. Re-test new game, reload, story on/off, Warfare off, capture/recapture, medic respawn, science escorts, PDA and generated anomalies.
