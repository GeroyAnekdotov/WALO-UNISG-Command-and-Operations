# WALO: UNISG Command & Operations v1.0.3

An unofficial WALO add-on for **S.T.A.L.K.E.R. Anomaly GAMMA + WALO 1.6.11**. It adds a UNISG headquarters on Jupiter, faction services and contracts, and two scripted scientific escort missions.

This is not an official WALO release or a mod for standalone Anomaly. Internal identifiers and save keys are preserved.

## Features

- **UNISG headquarters at Jupiter `jup_b208`:** two starting squads, four effective squad slots, native WALO trader, mechanic, medic and barman, workspots, campfires, a bed and a PDA sleep marker.
- Saving at the UNISG base and protection from newly generated DAO anomalies.
- Repeatable faction contracts, the medic's drug-making kit quest chain, and native stash searches from the trader and barman.
- Two scripted escort missions: **Protocol Contour** and **Biological Reconnaissance**.
- iTheon Taskboard metadata using native localization IDs and colored fields, without overriding Taskboard scripts.
- Russian and English localization. French and Spanish use the current English fallback; Ukrainian uses that fallback with its existing translated return notification.

## Requirements and game modes

- **GAMMA + WALO 1.6.11**, installed through Mod Organizer 2 (MO2).
- **Warfare ON and Story Mode OFF.** Story Mode and non-Warfare play are excluded by design to avoid interfering with scripted progression, quest NPCs and A-Life.
- A **new game as UNISG** for the headquarters and the full medic quest chain. Disable **Random Starting Locations** to start at the headquarters.

## Installation with MO2

1. Back up your saves before installation.
2. Disable duplicate installations and other add-ons that provide the same UNISG headquarters or missions.
3. Install the v1.0.3 ZIP as one separate mod with file priority over WALO and GAMMA ZCP.
4. Check that this mod wins the intended conflicts for:

   - `scripts/warfare.script` — WALO 1.6.11 baseline.
   - `scripts/ui_mm_faction_select.script` — GAMMA/ZCP menu script.
   - `configs/scripts/beh_companion.ltx` — companion behavior integration.

5. If other mods edit those files, merge the changes deliberately. For a different WALO/GAMMA version, port the supplied integration patches into the matching upstream sources before use.
6. Start a new UNISG game with **Warfare ON / Story Mode OFF** and **Random Starting Locations OFF** to start at the headquarters.

To roll back, disable the mod and return to a save made before installation. Spawned A-Life objects do not disappear merely because the mod is disabled.

## Testing status

The author **successfully tested the combined v1.0.3 archive in game as a single mod**. This does not establish exhaustive regression coverage or compatibility with all GAMMA/WALO versions. The documented target is GAMMA + WALO 1.6.11; an exact GAMMA version is not specified in these documents.

## Compatibility and technical notes

- Bundled `warfare.script` and `ui_mm_faction_select.script` are **version-specific full-file overrides**. Do not copy them over newer WALO/GAMMA scripts. Port `INTEGRATION/WALO_1.6.11_warfare.patch` and `INTEGRATION/GAMMA_faction_select.patch` into the current sources instead.
- Merge the `beh_companion.ltx` integration carefully; do not override global GAMMA/Useful Idiots AI or Taskboard scripts.
- Scientific research credits five unique bodies by proximity time, with credit after 12 seconds of safe proximity to a body. Animation completion is not a technical condition for credit.
- Preserve all task, squad and state IDs and one-time A-Life save keys when integrating or updating. The integration notes retain the exact keys and the checklist for re-testing after porting.

## Documentation

- [English readme](README_EN.txt)
- [Русская инструкция](README_RU.txt)
- [Release information](RELEASE_INFO.txt)
- [Upstream integration, save compatibility and re-test checklist](INTEGRATION/UPSTREAM_EN.md)

