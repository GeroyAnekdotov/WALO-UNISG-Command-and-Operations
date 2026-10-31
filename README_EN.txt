WALO: UNISG Command & Operations v1.0.3
=====================================
Unofficial WALO add-on with a UNISG headquarters on Jupiter, faction services
and scientific escort missions.
Target: GAMMA + WALO 1.6.11. Not an official WALO release or a mod for standalone Anomaly.

MO2 INSTALLATION
1. Disable duplicate installations and other add-ons that provide the same UNISG headquarters or missions.
2. Install this ZIP as a separate mod with file priority over WALO and GAMMA ZCP.
3. Check the conflict winners: scripts/warfare.script (WALO 1.6.11),
   scripts/ui_mm_faction_select.script (GAMMA/ZCP), configs/scripts/beh_companion.ltx,
   configs/gameplay/profiles/character_desc_isg_2.xml.
   Other mods editing these files require a deliberate merge, not a blind replacement.
   With WALO SIN HQ 2.0.1, its combined warfare.script must win instead;
   keep the remaining UNISG files enabled and follow that package's instructions.
4. Start a NEW GAME for the headquarters and full medic quest chain: UNISG / Warfare ON / Story OFF.
   Disable Random Starting Locations to start at the headquarters.
5. Back up your save before installation. To roll back, use a pre-installation save:
   spawned A-Life objects will not disappear when the mod is disabled.

FEATURES
- UNISG base at Jupiter jup_b208: two starting squads, four effective squad slots;
  WALO-native trader, mechanic, medic, barman; workspots, campfires, bed,
  PDA sleep marker, ISG base saving, protection from new DAO anomalies.
- Repeatable faction contracts, medic drug-making kit quest, native stash searches.
- Two fully scripted escorts: Protocol Contour and Biological Reconnaissance.
- Added mechanics target Warfare with Story Mode OFF. iTheon Taskboard metadata
  uses native localization IDs and a scoped acceptance wrapper; no full Taskboard
  script is replaced.

AUDIT / LIMITS
- Gameplay identifiers and save keys are preserved.
- Russian and English quest localization; fra/spa use current English fallback;
  ukr uses that fallback plus its already-translated return notification.
- Research counts five unique bodies by proximity time; the animation plays,
  but its completion is NOT a technical requirement for credit.
- Bundled full-file overrides of warfare.script and ui_mm_faction_select.script are
  VERSION-SPECIFIC. Port INTEGRATION patches; do not copy over newer WALO/GAMMA.
- The author successfully tested the combined v1.0.3 archive in game as a single mod.
  This does not establish exhaustive regression coverage or compatibility with all GAMMA/WALO versions.
- beh_companion.ltx and character_desc_isg_2.xml are also full-file overrides.
  The companion file changes forced-dialogue distance in three stock escorts
  from 3 to 6 metres without a mode check; complete Story Mode isolation is unproven.
- Scientific tasks share native expedition/anomaly state. A Taskboard stale-offer
  guard has an and/or fallback weakness; its in-game impact is not reproduced.
- No complete UNISG storyline playthrough is claimed. Exact GAMMA, engine and
  DLTX test versions are not recorded. See README.md for dependencies and limits.

MO2 ASSET: WALO_UNISG_Command_and_Operations_1.0.3_FULL_MO2.zip
CREDITS / REDISTRIBUTION: THIRD_PARTY_NOTICES.md
UPSTREAM NOTES: INTEGRATION/UPSTREAM_EN.md
