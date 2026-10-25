"""Check the complete portable skill and publication documentation."""
import ast, hashlib, importlib.util, json, re, sys, zipfile
from pathlib import Path
from urllib.parse import unquote
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "elementary-competency-assessment-local"
spec = importlib.util.spec_from_file_location("package_validator", SKILL / "scripts/validate_package.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
result = mod.validate(SKILL)
assert result["passed"], result
manifest = json.loads((SKILL / "package-manifest.json").read_text(encoding="utf-8"))
version = manifest["version"]
assert 'version: "' + version + '"' in (SKILL / "SKILL.md").read_text(encoding="utf-8")
assert 'VERSION = "' + version + '"' in (SKILL / "scripts/build_assessment.py").read_text(encoding="utf-8")
assert "license: MIT" in (SKILL / "SKILL.md").read_text(encoding="utf-8")
assert (ROOT / "LICENSE").read_bytes() == (SKILL / "LICENSE").read_bytes()
for rel in ("AGENT-START.md", "README.md", "HANDOFF.md", "docs/index.md", "docs/install-codex.md", "docs/install-opencode.md", "docs/workflow.md", "docs/verification.md", "docs/releases.md", "docs/sources.md"):
    assert (ROOT / rel).is_file(), rel
assert (SKILL / "references/install-opencode.md").is_file()
links = 0
for p in [*ROOT.glob("*.md"), *(ROOT / "docs").rglob("*.md")]:
    content = p.read_text(encoding="utf-8")
    assert "\ufffd" not in content, p
    assert not re.search(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+", content), "Private Windows user path: " + str(p)
    for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", link) or link.startswith("#"):
            continue
        dest = (p.parent / unquote(link.split("#")[0])).resolve()
        assert dest.is_relative_to(ROOT.resolve()) and dest.exists(), (p, link)
        links += 1
for p in (ROOT / "tools").glob("*.py"):
    ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
target = ROOT / "dist" / (SKILL.name + "-" + version + ".zip")
if target.exists():
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        expected = {SKILL.name + "/" + p.relative_to(SKILL).as_posix(): p.read_bytes() for p in SKILL.rglob("*") if p.is_file()}
        assert set(archive.namelist()) == set(expected)
        assert all(archive.read(name) == data for name, data in expected.items())
    expected_sha = (ROOT / "dist" / ("SHA256SUMS-" + version + ".txt")).read_text(encoding="utf-8").split()[0]
    assert hashlib.sha256(target.read_bytes()).hexdigest() == expected_sha
print(json.dumps({"passed": True, "version": version, "skill_files": len(manifest["files"]) + 1,
                  "skill_local_links": result["checked_local_links"], "publication_local_links": links,
                  "zip_verified": target.exists()}, ensure_ascii=False, indent=2))
