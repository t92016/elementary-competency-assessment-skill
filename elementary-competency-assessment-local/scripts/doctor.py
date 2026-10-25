"""Read-only runtime inventory; does not inspect credentials or model configuration."""
import argparse
import importlib.metadata
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

def probe(name):
    path = shutil.which(name)
    if not path:
        return {"available": False}
    command = [path, "--version"]
    if path.lower().endswith((".ps1", ".cmd", ".bat")):
        if path.lower().endswith(".ps1"):
            command = ["powershell.exe", "-NoProfile", "-File", path, "--version"]
        else:
            command = [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c", path, "--version"]
    try:
        r = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
        return {"available": True, "path": path, "exit_code": r.returncode,
                "output": (r.stdout + r.stderr).strip()[:1200]}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"available": True, "path": path, "error": str(e)}

def collect():
    packages = {}
    for name in ("python-docx", "pypdf", "Pillow", "pypdfium2"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    fonts = [str(Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / n)
             for n in ("msjh.ttc", "msjhbd.ttc")]
    word = False
    if os.name == "nt":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Word.Application"):
                word = True
        except OSError:
            pass
    return {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(), "architecture": platform.machine(),
        "python": {"executable": sys.executable, "version": platform.python_version()},
        "packages": packages, "commands": {n: probe(n) for n in ("codex", "opencode", "node", "uv")},
        "word_registered": word, "word_export_test": "not run by doctor",
        "soffice_in_path": shutil.which("soffice"), "pdftoppm_in_path": shutil.which("pdftoppm"),
        "traditional_chinese_fonts": {p: Path(p).is_file() for p in fonts},
        "agent_image_pdf_reading": "requires actual input test",
        "agent_model": "not inspected", "agent_search": "requires actual search and body-read test"
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = collect()
    content = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content + "\n", encoding="utf-8")
        print(args.output)
    else:
        print(content)
    return 0 if all(report["packages"].values()) else 2

if __name__ == "__main__":
    raise SystemExit(main())
