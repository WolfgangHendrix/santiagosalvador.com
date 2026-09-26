"""Build the GitHub Pages site. Full masters stay in git and are not published."""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "_site"


def copy_rel(rel):
    rel = str(rel).replace("\\", "/").split("?", 1)[0]
    if not rel or rel.startswith(("#", "mailto:", "http://", "https://", "data:")):
        return
    src = ROOT / rel
    if not src.is_file():
        print(f"missing {rel}")
        return
    dest = SITE / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        shutil.copy2(src, dest)


def load_js_or_json(path):
    text = path.read_text(encoding="utf-8")
    start = text.find("{") if "{" in text[:80] or text.lstrip().startswith("{") else text.find("[")
    if text.lstrip().startswith("window."):
        start = re.search(r"=\s*(\{|\[)", text).start(1)
    return json.loads(text[start:].rstrip().rstrip(";"))


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()

    for name in ("index.html", "marvel-archive.html", "favicon.ico", "santiago-salvador-stained-glass-background.mp4"):
        copy_rel(name)

    for path in (ROOT / "assets").rglob("*"):
        if path.is_file():
            copy_rel(path.relative_to(ROOT).as_posix())

    art = load_js_or_json(ROOT / "assets" / "data" / "artworks.js")
    for item in art:
        copy_rel(item.get("thumb") or item["url"])

    # Only the Marvel subfolder belongs in the unlisted personal archive.
    marvel = load_js_or_json(ROOT / "assets" / "data" / "marvel-archive.js")
    for item in marvel:
        if not item["url"].startswith("Art/Cards_Collectibles/Marvel_Universe_Series_1/"):
            raise ValueError("Non-Marvel image in the personal archive")
        copy_rel(item.get("thumb") or item["url"])

    music = load_js_or_json(ROOT / "assets" / "data" / "music.js")
    for track in music:
        copy_rel(track["url"])

    labels = load_js_or_json(ROOT / "assets" / "data" / "labels.js")
    for item in labels["labels"]:
        copy_rel(item["thumbUrl"])

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for match in re.findall(r'(?:src|href)="([^"]+)"', html):
        copy_rel(match)

    total = sum(path.stat().st_size for path in SITE.rglob("*") if path.is_file())
    files = sum(1 for path in SITE.rglob("*") if path.is_file())
    print(f"Published site: {files} files, {total / 1024 / 1024:.1f} MB")
    if total > 900 * 1024 * 1024:
        raise SystemExit("Published site is too close to GitHub Pages' 1 GB limit.")


if __name__ == "__main__":
    main()
