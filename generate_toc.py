from pathlib import Path
import re

# --------------------------------------------------
# Paths
# --------------------------------------------------
BOOK_ROOT = Path.cwd()
CONTENT = BOOK_ROOT / "content"
TOC = BOOK_ROOT / "_toc.yml"

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def numeric_key(name):
    """
    Extract leading integer for numeric sorting.
    Non-numeric names sort last.
    """
    m = re.match(r"(\d+)", name)
    return int(m.group(1)) if m else 9999


def collect_chapter(dir_path: Path):
    """
    Given a directory with README.md, return:
      - chapter file
      - list of section files
    """
    readme = dir_path / "README.md"
    if not readme.exists():
        return None

    sections = []
    for f in sorted(dir_path.iterdir(), key=lambda p: numeric_key(p.name)):
        if (
            f.is_file()
            and f.suffix in (".md", ".ipynb")
            and f.name != "README.md"
            and not f.name.startswith(".")
        ):
            sections.append(f.relative_to(BOOK_ROOT).with_suffix(""))

    return {
        "chapter": readme.relative_to(BOOK_ROOT).with_suffix(""),
        "sections": sections,
    }


def collect_part(base_dir: Path):
    """
    Collect chapters for a top-level directory
    (modules or appendices).
    """
    chapters = []
    for d in sorted(base_dir.iterdir(), key=lambda p: numeric_key(p.name)):
        if d.is_dir():
            ch = collect_chapter(d)
            if ch:
                chapters.append(ch)
    return chapters


# --------------------------------------------------
# Write TOC
# --------------------------------------------------
with open(TOC, "w", encoding="utf-8") as f:
    f.write("format: jb-book\n")
    f.write("root: content/intro\n\n")

    # -------------------------
    # Modules
    # -------------------------
    modules_dir = CONTENT / "modules"
    if modules_dir.exists():
        f.write("parts:\n")
        f.write("  - caption: Core Modules\n")
        f.write("    chapters:\n")

        for ch in collect_part(modules_dir):
            f.write(f"    - file: {ch['chapter'].as_posix()}\n")
            if ch["sections"]:
                f.write("      sections:\n")
                for sec in ch["sections"]:
                    f.write(f"      - file: {sec.as_posix()}\n")

    # -------------------------
    # Appendices
    # -------------------------
    appendices_dir = CONTENT / "appendices"
    if appendices_dir.exists():
        f.write("\n")
        f.write("  - caption: Appendices\n")
        f.write("    chapters:\n")

        for ch in collect_part(appendices_dir):
            f.write(f"    - file: {ch['chapter'].as_posix()}\n")
            if ch["sections"]:
                f.write("      sections:\n")
                for sec in ch["sections"]:
                    f.write(f"      - file: {sec.as_posix()}\n")

print("✅ _toc.yml regenerated from directory structure.")
