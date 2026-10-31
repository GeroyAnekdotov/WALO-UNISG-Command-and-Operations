"""Focused source and Lua 5.1 release checks. No game execution or installation writes."""
import argparse
import re
import sys
from pathlib import Path

from build_release import ROOT, validate_sources


def reverse_patch(source, patch):
    """Require exact hunk contexts; compare text after line-ending normalization only."""
    lines, output, cursor = source.splitlines(), [], 0
    chunks = re.split(r"(?m)^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@[^\n]*\n", patch)
    if len(chunks) == 1:
        raise ValueError("No integration hunks")
    for start, body in zip(chunks[1::2], chunks[2::2]):
        position = int(start) - 1
        if position < cursor:
            raise ValueError("Overlapping integration hunks")
        output.extend(lines[cursor:position])
        cursor = position
        for line in body.splitlines():
            if not line or line.startswith("\\ No newline"):
                continue
            operation, text = line[0], line[1:]
            if operation in " +":
                if cursor >= len(lines) or lines[cursor] != text:
                    raise ValueError(f"Integration patch does not match line {cursor + 1}")
                cursor += 1
            if operation in " -":
                output.append(text)
            if operation not in " +-":
                raise ValueError("Unexpected patch record")
    return "\n".join(output + lines[cursor:]) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lua-deps", type=Path, default=ROOT / "_reference/python-test-deps",
                        help="Optional local Python package directory containing lupa.lua51")
    parser.add_argument("--walo-root", type=Path,
                        default=ROOT.parent / "_shared_reference/upstream/WALO_1.6.11/src",
                        help="Read-only WALO 1.6.11 root containing gamedata")
    parser.add_argument("--menu-baseline", type=Path, help="Optional matching GAMMA/ZCP menu source")
    args = parser.parse_args()
    validate_sources()
    print("PASS: original 37-file manifest, XML/LTX, five localization ID sets and documentation links")
    sources = {p.stem: p.read_bytes().decode("latin1").replace("\r\n", "\n")
               for p in (ROOT / "gamedata/scripts").glob("*.script")}
    restored = reverse_patch(sources["warfare"], (ROOT / "INTEGRATION/WALO_1.6.11_warfare.patch").read_text())
    upstream = (args.walo_root / "gamedata/scripts/warfare.script").read_bytes().decode("latin1")
    if restored.splitlines() != upstream.splitlines():
        raise ValueError("Controller changes exceed the supplied WALO patch/baseline")
    native = (args.walo_root / "gamedata/scripts/smart_terrain_warfare.script").read_bytes().decode("latin1")
    for function in ("is_main_base", "get_main_base_faction", "set_main_base", "set_max_population", "bootstrap_smart", "check_unique_npcs"):
        if not re.search(r"^function " + function + r"\(", native, re.M):
            raise ValueError(f"WALO API missing: {function}")
    menu = reverse_patch(sources["ui_mm_faction_select"], (ROOT / "INTEGRATION/GAMMA_faction_select.patch").read_text())
    if args.menu_baseline and menu.splitlines() != args.menu_baseline.read_bytes().decode("latin1").splitlines():
        raise ValueError("Menu changes exceed the supplied GAMMA patch/baseline")
    print("PASS: exact WALO patch reversal and native APIs; menu patch contexts" + (" and baseline" if args.menu_baseline else " (external menu baseline not supplied)"))
    sys.path.insert(0, str(args.lua_deps))
    try:
        from lupa.lua51 import LuaRuntime
    except ImportError as exc:
        raise SystemExit("Lupa lua51 is required; install it locally or pass --lua-deps. No tests were skipped silently.") from exc
    runtime = LuaRuntime(unpack_returned_tuples=True)
    compile_lua = runtime.eval("function(s,n) local f,e=loadstring(s,n); assert(f,e); return true end")
    for name, source in sources.items():
        if name != "warfare":
            compile_lua(source, "@" + name + ".script")
    print("PASS: 11 scripts compile as Lua 5.1; unchanged warfare.script uses X-Ray's continue dialect")
    controller = sources["warfare"]
    start = controller.index("-- UNISG HQ extension")
    hq = controller[start:controller.index("\nfunction actor_on_first_update()", start)]
    gates = {}
    for name, source in sources.items():
        if name in ("warfare", "ui_mm_faction_select", "zzzzzz_walo_unisg_hq_base_saving"):
            continue
        match = re.search(r"^local function (enabled|active)\(\)\n.*?^end", source, re.M | re.S)
        if not match:
            raise ValueError(f"Mode gate not located: {name}")
        gates[name] = match[0] + "\nreturn " + match[1]
    menu_gate = re.search(r"local unisg_hq_allowed = .*?(?=\n\s*if value)", sources["ui_mm_faction_select"], re.S)[0]
    runtime.globals().sources = runtime.table_from({
        "hq": hq, "gates": runtime.table_from(gates),
        "menu_gate": "return function(self) " + menu_gate + "\nreturn unisg_hq_allowed end",
        "saving": sources["zzzzzz_walo_unisg_hq_base_saving"],
        "dao": sources["zzzzzz_walo_unisg_hq_dao_guard"],
    })
    count = runtime.execute((ROOT / "tests/release_spec.lua").read_text(encoding="utf-8"))
    print(f"PASS: {count} mocked source scenarios (mode gates, HQ/services restoration, saving/DAO wrapper scope and idempotence)")
    print("No engine/VFS/DLTX/animation or complete storyline playthrough was performed.")


if __name__ == "__main__":
    main()
