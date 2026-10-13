"""Build the GitHub Pages site. Full masters stay in git and are not published."""
import json
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "_site"


def publish_thumbnail(rel):
    """Generate only the deployed WebP; keep derivatives out of the repository."""
    src = ROOT / rel
    # Include the source extension to avoid collisions between JPG/PNG variants.
    output = str(Path(rel).with_name(Path(rel).name + ".webp")).replace("\\", "/")
    dest = SITE / output
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as image:
            image = ImageOps.exif_transpose(image)
            image.thumbnail((960, 960), Image.Resampling.LANCZOS)
            image.convert("RGB").save(dest, "WEBP", quality=82, method=4)
    return output


def publish_catalog(name, variable, data):
    payload = json.dumps(data, separators=(",", ":"))
    (SITE / "assets" / "data" / (name + ".json")).write_text(payload, encoding="utf-8")
    (SITE / "assets" / "data" / (name + ".js")).write_text(f"window.{variable} = {payload};\n", encoding="utf-8")


def publish_thumbnails(items, field):
    sources = list(dict.fromkeys(item.get(field) or item["url"] for item in items))
    with ThreadPoolExecutor(max_workers=4) as pool:
        converted = dict(zip(sources, pool.map(publish_thumbnail, sources)))
    for item in items:
        item[field] = converted[item.get(field) or item["url"]]
    print(f"Optimized {len(sources)} thumbnails", flush=True)


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

    for name in ("index.html", "marvel-archive.html", "favicon.ico"):
        copy_rel(name)

    for path in (ROOT / "assets").rglob("*"):
        if path.is_file():
            copy_rel(path.relative_to(ROOT).as_posix())

    art = load_js_or_json(ROOT / "assets" / "data" / "artworks.js")
    publish_thumbnails(art, "thumb")
    for item in art:
        for supporting in item.get("supportingImages", []):
            copy_rel(supporting["url"])
    publish_catalog("artworks", "ARTWORKS_DATA", art)

    # Only the Marvel subfolder belongs in the unlisted personal archive.
    marvel = load_js_or_json(ROOT / "assets" / "data" / "marvel-archive.js")
    for item in marvel:
        if not item["url"].startswith("Art/Cards_Collectibles/Marvel_Universe_Series_1/"):
            raise ValueError("Non-Marvel image in the personal archive")
    publish_thumbnails(marvel, "thumb")
    publish_catalog("marvel-archive", "MARVEL_ARCHIVE_DATA", marvel)

    music = load_js_or_json(ROOT / "assets" / "data" / "music.js")
    for track in music:
        copy_rel(track["url"])

    labels = load_js_or_json(ROOT / "assets" / "data" / "labels.js")
    publish_thumbnails(labels["labels"], "thumbUrl")
    publish_catalog("labels", "LABELS_DATA", labels)

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
