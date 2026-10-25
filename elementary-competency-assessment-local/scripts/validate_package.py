"""Validate package structure, local links, Python syntax and optional SHA-256 manifest."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

def validate(root):
    errors = []
    source = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", source, re.S)
    if not match:
        errors.append("Missing YAML frontmatter")
    else:
        name = re.search(r"^name:\s*(\S+)\s*$", match[1], re.M)
        description = re.search(r"^description:\s*(.+)$", match[1], re.M)
        if not name or name[1] != root.name or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name[1]) or len(name[1]) > 64:
            errors.append("Invalid skill name or folder")
        if not description or not 1 <= len(description[1]) <= 1024:
            errors.append("Invalid description")
    for rel in ("references/material-intake.md", "references/assessment-criteria.md",
                "references/revision-flow.md", "references/local-delivery.md",
                "references/local-runtime.md", "references/assessment-data.md",
                "templates/student-paper.md", "templates/teacher-paper.md",
                "templates/assessment-blueprint.md", "requirements.txt",
                "scripts/build_assessment.py", "scripts/export_pdf.ps1", "scripts/install.ps1",
                "scripts/doctor.py", "examples/smoke-assessment.json"):
        if not (root / rel).is_file():
            errors.append("Missing " + rel)
    checked_links = 0
    for path in root.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        if "\ufffd" in content:
            errors.append("Replacement character in " + str(path))
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            target = unquote(target.split("#")[0])
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                errors.append("Broken/escaping link: " + str(path.relative_to(root)) + " -> " + target)
            checked_links += 1
    for path in root.rglob("*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as e:
            errors.append(str(e))
    manifest = root / "package-manifest.json"
    if manifest.exists():
        expected = json.loads(manifest.read_text(encoding="utf-8"))["files"]
        actual = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in root.rglob("*") if p.is_file() and p.name != "package-manifest.json"}
        if actual != expected:
            errors.append("Package file manifest mismatch")
    return {"passed": not errors, "checked_local_links": checked_links, "errors": errors}

if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    result = validate(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 2)
