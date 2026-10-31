# WALO: UNISG Command & Operations v1.0.3

UNISG headquarters at Jupiter with WALO-native services, faction contracts, a medic drug-making kit chain and two scientific escorts: **Protocol Contour** and **Biological Reconnaissance**.

This first GitHub release preparation retains the previously tested v1.0.3 gameplay payload. Documentation and packaging have been updated; the version history has not been reset.

## Installation

Install **`WALO_UNISG_Command_and_Operations_1.0.3_FULL_MO2.zip`** through MO2. Requires **Anomaly GAMMA + WALO 1.6.11**, including the required GAMMA resources/APIs. Back up saves, disable duplicate UNISG packages and verify all four full-file conflicts listed in the README.

Use a **new UNISG game / Warfare ON / Story Mode OFF / Random Starting Locations OFF**. When used with **WALO SIN HQ 2.0.1**, its combined `warfare.script` must win; keep the remaining UNISG files enabled. Do not blindly overwrite other WALO/GAMMA versions. Uninstalling does not remove saved objects; roll back to a pre-installation save.

## Validation and limits

The author successfully tested the combined v1.0.3 archive in game as a single mod. Preparation checks cover unchanged gameplay hashes, source/configuration integrity, mocked mode/restoration scenarios and ZIP contents. No new engine run, exhaustive regression test or complete UNISG storyline playthrough is claimed.

Known limits include three ungated stock escort dialogue-distance changes, shared scientific-task state and a Taskboard stale-offer guard weakness whose in-game impact is unverified. Exact GAMMA/engine/DLTX test versions and live MO2 VFS/wrapper order remain unverified. See `README.md` and `INTEGRATION/UPSTREAM_EN.md`.

## Assets and integration

- `WALO_UNISG_Command_and_Operations_1.0.3_FULL_MO2.zip` — complete package, including editable source and WALO integration notes/patches.
- `WALO_UNISG_Command_and_Operations_1.0.3_FULL_MO2.zip.sha256` — archive checksum.

Upstream attribution and unresolved Anomaly/GAMMA redistribution terms are recorded in `THIRD_PARTY_NOTICES.md`. Confirm those terms before publication; this draft grants no blanket license.
