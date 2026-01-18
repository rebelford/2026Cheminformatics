from pathlib import Path
import re

BOOK_ROOT = Path.cwd()
CONTENT = BOOK_ROOT / "content"
TOC = BOOK_ROOT / "_toc.yml"

def numeric_key(name):
    m = re.match(r"(\d+)", name)
    return int(m.group(1)) if m else 999

def collect_chapters(base):
    chapters = []
    for item in sorted(base.iterdir(), key=lambda p: numeric_key(p.name)):
        if item.is_dir():
            files = sorted(
                [f for f in item.iterdir()
                 if f.suffix in (".md", ".ipynb") and not f.name.startswith(".")]
            )
            for f in files:
                chapters.append(f.relative_to(BOOK_ROOT).with_suffix(""))
    return chapters

with open(TOC, "w", encoding="utf-8") as f:
    f.write("format: jb-book\n")
    f.write("root: content/intro\n\n")
    f.write("parts:\n")

    # -------------------------
    # Modules
    # -------------------------
    modules_dir = CONTENT / "modules"
    if modules_dir.exists():
        f.write("  - caption: Core Modules\n")
        f.write("    chapters:\n")
        for ch in collect_chapters(modules_dir):
            f.write(f"      - file: {ch.as_posix()}\n")
        f.write("\n")

    # -------------------------
    # Appendices
    # -------------------------
    appendices_dir = CONTENT / "appendices"
    if appendices_dir.exists():
        f.write("  - caption: Appendices (Reference & Background)\n")
        f.write("    chapters:\n")
        for ch in collect_chapters(appendices_dir):
            f.write(f"      - file: {ch.as_posix()}\n")

print("✅ _toc.yml regenerated from directory structure.")
