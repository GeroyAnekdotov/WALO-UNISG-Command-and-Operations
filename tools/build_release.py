"""Build the unchanged v1.0.3 MO2 payload; never stage, publish or overwrite a different ZIP."""
import hashlib
import io
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
DOCS = (
    "README.md", "README_EN.txt", "README_RU.txt", "RELEASE_INFO.txt",
    "CHANGELOG.md", "RELEASE_NOTES.md", "THIRD_PARTY_NOTICES.md", "DEVELOPMENT.md",
    "INTEGRATION/UPSTREAM_EN.md", "INTEGRATION/GAME_FILES_SHA256.txt",
    "INTEGRATION/WALO_1.6.11_warfare.patch", "INTEGRATION/GAMMA_faction_select.patch",
)


def read_manifest():
    result = {}
    for line in (ROOT / "INTEGRATION/GAME_FILES_SHA256.txt").read_text().splitlines():
        match = re.fullmatch(r"([a-f0-9]{64})  (gamedata/\S+)", line)
        if match:
            digest, name = match.groups()
            if name in result or ".." in Path(name).parts:
                raise ValueError(f"Invalid baseline entry: {name}")
            result[name] = digest
    if len(result) != 37:
        raise ValueError("Expected the original 37-file v1.0.3 gameplay manifest")
    return result


def validate_sources():
    baseline = read_manifest()
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "gamedata").rglob("*") if p.is_file()}
    if actual != set(baseline):
        raise ValueError(f"Runtime allowlist mismatch: missing={set(baseline)-actual}; extra={actual-set(baseline)}")
    payload = {}
    for name in (*sorted(baseline), *DOCS):
        path = ROOT / name
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != ROOT.parent):
            raise ValueError(f"Release inputs must not be symlinks: {name}")
        payload[name] = path.read_bytes()
        if name in baseline and hashlib.sha256(payload[name]).hexdigest() != baseline[name]:
            raise ValueError(f"Gameplay changed from tested v1.0.3: {name}")
    title = payload["RELEASE_INFO.txt"].decode("utf-8-sig").splitlines()[0]
    match = re.fullmatch(r"WALO: UNISG Command & Operations \| v(\d+\.\d+\.\d+)", title)
    if not match or match[1] != "1.0.3":
        raise ValueError("Unexpected project/version; do not reset release history")
    version = match[1]
    strings = {}
    dialogs = None
    for name in sorted(baseline):
        data = payload[name]
        if name.endswith(".xml"):
            if "/profiles/" in name:
                # X-Ray include fragment, not an independent XML document.
                text = re.sub(r"^#include[^\n]*", "", data.decode("cp1251"), flags=re.M)
                tree = ET.fromstring("<fragment>" + text + "</fragment>")
            else:
                tree = ET.fromstring(data)
            ids = [e.attrib["id"] for e in tree.iter("string")]
            if len(ids) != len(set(ids)):
                raise ValueError(f"Duplicate localized string ID: {name}")
            if "/text/" in name:
                language = Path(name).parts[3]
                strings.setdefault(language, []).extend(ids)
            if name.endswith("dialogs_unisg_field_science.xml"):
                dialogs = tree
        elif name.endswith(".ltx"):
            section, sections, keys = None, set(), set()
            for raw in data.decode("latin1").splitlines():
                line = raw.split(";", 1)[0].strip()
                header = re.match(r"!?\[([^]]+)\]", line)
                if header:
                    section = header[1]
                    if section in sections:
                        raise ValueError(f"Duplicate section {section}: {name}")
                    sections.add(section)
                elif section and "=" in line:
                    key = (section, line.split("=", 1)[0].strip())
                    if key in keys:
                        raise ValueError(f"Duplicate key {key}: {name}")
                    keys.add(key)
        elif name.endswith(".script"):
            for module in re.findall(r"\b(z{6,7}_walo_unisg_\w+)(?=\.)", data.decode("latin1")):
                if f"gamedata/scripts/{module}.script" not in actual:
                    raise ValueError(f"Missing private module {module}: {name}")
    if set(strings) != {"eng", "rus", "fra", "spa", "ukr"}:
        raise ValueError("Missing release language")
    if any(len(ids) != len(set(ids)) or set(ids) != set(strings["eng"]) for ids in strings.values()):
        raise ValueError("Localization IDs differ or collide across tables")
    science = payload["gamedata/scripts/zzzzzz_walo_unisg_field_science.script"].decode("latin1")
    for node in dialogs.iter("precondition"):
        module, function = node.text.split(".")
        if module != "zzzzzz_walo_unisg_field_science" or not re.search(r"^function " + function + r"\(", science, re.M):
            raise ValueError(f"Missing dialogue precondition: {node.text}")
    for name in DOCS:
        if b"\r\n" in payload[name]:
            raise ValueError(f"Release documentation must use checkout-stable LF endings: {name}")
        text = payload[name].decode("utf-8-sig")
        if re.search(r"^(?:<{7}|={7}|>{7})(?: |$)", text, re.M):
            raise ValueError(f"Merge marker: {name}")
        if re.search(r"[A-Za-z]:[\\/](?:Users|GAMMA|Anomaly|Modding)(?:[\\/]|\b)", text, re.I):
            raise ValueError(f"Machine-specific path: {name}")
        if name.endswith(".md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if not re.match(r"[a-z]+://|#", target) and not ((ROOT / name).parent / target.split("#")[0]).is_file():
                    raise ValueError(f"Broken documentation link: {name}: {target}")
    return version, payload


def main():
    version, payload = validate_sources()
    manifest = "".join(f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in sorted(payload.items()))
    payload["RELEASE_FILES_SHA256.txt"] = manifest.encode("utf-8")
    buffer = io.BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(payload.items()):
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            archive.writestr(entry, data, compresslevel=9)
    content = buffer.getvalue()
    with ZipFile(io.BytesIO(content)) as archive:
        if len(archive.infolist()) != len(payload) or set(archive.namelist()) != set(payload) or archive.testzip():
            raise ValueError("ZIP path/CRC integrity failure")
        for name, data in payload.items():
            if archive.read(name) != data:
                raise ValueError(f"ZIP/source mismatch: {name}")
    target = ROOT / "dist" / f"WALO_UNISG_Command_and_Operations_{version}_FULL_MO2.zip"
    if target.exists() and target.read_bytes() != content:
        raise FileExistsError(f"A different package already uses this filename: {target.name}")
    target.parent.mkdir(exist_ok=True)
    if not target.exists():
        with target.open("xb") as output:
            output.write(content)
    (ROOT / "RELEASE_FILES_SHA256.txt").write_bytes(payload["RELEASE_FILES_SHA256.txt"])
    digest = hashlib.sha256(content).hexdigest()
    target.with_suffix(".zip.sha256").write_text(f"{digest}  {target.name}\n", encoding="utf-8")
    print(f"PASS: 37 unchanged runtime files; XML/LTX/localization/dependencies; {len(payload)} ZIP entries; CRC and exact source equality")
    print(target)
    print(f"SHA256: {digest}")


if __name__ == "__main__":
    main()
