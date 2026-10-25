"""Create a portable release ZIP and hashes from this repository's skill folder."""
import argparse, hashlib, json, re, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "elementary-competency-assessment-local"
def make_manifest():
    version = re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$', (SKILL / "SKILL.md").read_text(encoding="utf-8"), re.M)[1]
    files = {}
    for p in sorted(SKILL.rglob("*")):
        if not p.is_file() or p.name == "package-manifest.json":
            continue
        if p.is_symlink() or "__pycache__" in p.parts or p.suffix == ".pyc":
            raise ValueError("Runtime artifact or symlink in skill: " + str(p))
        files[p.relative_to(SKILL).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = {"name": SKILL.name, "version": version,
                "source_zip_sha256": "99D5B5E3E428B5ADF58534D94D740AD98FF65D0702467AEB93E3C86FC5C7D450", "files": files}
    (SKILL / "package-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    manifest = make_manifest()
    if args.manifest_only:
        print(json.dumps({"version": manifest["version"], "file_count": len(manifest["files"]) + 1}))
        return
    from io import BytesIO
    stream = BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for p in sorted(SKILL.rglob("*")):
            if p.is_file():
                info = zipfile.ZipInfo(SKILL.name + "/" + p.relative_to(SKILL).as_posix(), (2026, 10, 25, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, p.read_bytes())
    payload = stream.getvalue()
    args.output.mkdir(parents=True, exist_ok=True)
    target = args.output / (SKILL.name + "-" + manifest["version"] + ".zip")
    if target.exists() and target.read_bytes() != payload:
        raise ValueError("Refuse to replace a different release ZIP; use a new version.")
    target.write_bytes(payload)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP CRC check failed")
    digest = hashlib.sha256(payload).hexdigest()
    checksum = args.output / ("SHA256SUMS-" + manifest["version"] + ".txt")
    checksum.write_text(digest + "  " + target.name + "\n", encoding="utf-8")
    print(json.dumps({"zip": str(target), "sha256": digest, "file_count": len(manifest["files"]) + 1}, ensure_ascii=False))
if __name__ == "__main__":
    main()
