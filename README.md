# WALO: UNISG Command & Operations v1.0.3

A UNISG headquarters, native faction services and scientific escort missions for **S.T.A.L.K.E.R. Anomaly GAMMA + Warfare ALife Overhaul (WALO) 1.6.11**.

This unofficial add-on is intended for contribution to WALO. It requires the GAMMA installation and its resources; it is not a standalone Anomaly mod or an official WALO release.

## Features

- **Jupiter headquarters at `jup_b208`:** two initial UNISG squads and four effective squad slots at initialization/restoration, using WALO's population and ownership systems.
- WALO-native trader, technician, medic and barman; furnished work positions, campfires, a bed and a PDA sleep marker.
- Saving inside the friendly UNISG headquarters and a filter preventing newly generated DAO anomalies there. Existing saved anomalies are not removed.
- Repeatable faction contracts, the medic's drug-making kit chain, and native trader/barman stash searches.
- **Protocol Contour** and **Biological Reconnaissance**, with dedicated researcher squads and saved expedition state. Biological research credits five unique bodies after 12 seconds of safe proximity per body; animation completion is not the credit condition.
- iTheon Taskboard offer metadata and a scoped acceptance wrapper, without a full replacement of Taskboard scripts.
- English and Russian text. French and Spanish use English fallbacks; Ukrainian retains its translated return notification alongside the fallback.

## Requirements

- **Anomaly GAMMA and WALO 1.6.11**, including WALO's GAMMA integration. Follow WALO's own installation and preset instructions first.
- GAMMA's DLTX, companion/task systems, furniture resources and APIs. Base-saving and anomaly protection integrate with YACS/`ish_campfire_saving` and Dynamic Anomalies Overhaul respectively; those mods are not bundled.
- **Warfare ON / Story Mode OFF.** Use a **new UNISG game** for headquarters initialization and the full medic chain. Turn **Random Starting Locations OFF** to use the headquarters start and normal HQ seeding path.

The exact GAMMA release, engine and DLTX versions used in the author's test were not recorded. Compatibility with another WALO/GAMMA version is not established.

## Installation with Mod Organizer 2

1. Back up saves and retain the previous working package.
2. Install **`WALO_UNISG_Command_and_Operations_1.0.3_FULL_MO2.zip`** as one mod. The archive has `gamedata/` directly at its root.
3. Disable duplicate UNISG installations and add-ons supplying the same headquarters or missions.
4. Give this mod higher file priority than WALO and the corresponding GAMMA providers. In MO2's left pane, verify the intended winners for all four full-file overrides:

   | File relative to `gamedata/` | Integration |
   |---|---|
   | `scripts/warfare.script` | WALO 1.6.11 controller |
   | `scripts/ui_mm_faction_select.script` | GAMMA/ZCP new-game menu |
   | `configs/scripts/beh_companion.ltx` | GAMMA companion behavior |
   | `configs/gameplay/profiles/character_desc_isg_2.xml` | GAMMA UNISG NPC profile |

5. Another controller or AI/profile override requires a deliberate merge. MO2 priority alone does not combine code. **With WALO SIN HQ 2.0.1**, follow SIN HQ's instructions: its combined WALO/UNISG/SIN `warfare.script` must win; keep the remaining UNISG files enabled. This is not a compatibility claim for every SIN build.
6. Restart the game, then start **UNISG / Warfare ON / Story Mode OFF / Random Starting Locations OFF**.

Do not install the source repository ZIP in place of the release asset. To uninstall or roll back, disable the mod and load a **pre-installation save**. Spawned A-Life objects remain in saved games after the mod is disabled; arbitrary old saves are not automatically migrated into a new HQ game.

## Story Mode, tasks and saves

HQ initialization reads the new-game Story checkbox before saved infoportions exist. Ordinary loading uses both `story_mode_disabled` and `IsStoryMode()`. WALO restores opted-in HQ metadata and services without repeating the initial squad spawn, and clears its temporary registration when switching saves.

The HQ simulation is not restricted to an UNISG player; the player start, contracts and scientific expeditions have their own UNISG restrictions. WALO retains control of service spawning, ownership, capture and resurrection. The base can be captured, and later population-setting changes can alter its effective capacity.

The added mechanics target non-Story Warfare. Original Story/UNISG storyline task definitions are not replaced, and the escorts use their own squad IDs. **Complete Story Mode isolation is not established:** the bundled companion file also changes the forced-dialogue distance in three stock escort tasks from 3 to 6 metres without a mode check. No complete UNISG storyline playthrough is claimed.

Preserve task/squad IDs, infoportions and save keys when integrating. Scientific missions share native anomaly/expedition state with stock tasks. A known Taskboard stale-offer guard has an `and/or` fallback weakness; its in-game impact has not been reproduced. See the [integration notes](INTEGRATION/UPSTREAM_EN.md) for these limitations and wrapper-order risks.

## Validation and source

The author **successfully tested the combined v1.0.3 archive in game as a single mod**. This preparation preserves all 37 gameplay files byte for byte against the existing [game-file manifest](INTEGRATION/GAME_FILES_SHA256.txt). It adds documentation, targeted source checks and a verified MO2 package; it does not establish exhaustive regression coverage or compatibility with all GAMMA/WALO versions.

All installable script/configuration source is in `gamedata/`. Integration patches and maintainer instructions are included for WALO review. Upstream WALO/Anomaly/GAMMA code remains attributable to its respective authors; see [third-party notices](THIRD_PARTY_NOTICES.md) for permissions and unresolved redistribution terms.

- [English installation summary](README_EN.txt) · [Русская инструкция](README_RU.txt)
- [Changelog](CHANGELOG.md) · [Release notes](RELEASE_NOTES.md)
- [WALO integration guide](INTEGRATION/UPSTREAM_EN.md) · [Development and packaging](DEVELOPMENT.md)

