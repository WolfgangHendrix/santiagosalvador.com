"""Prepare local letter-size print proofs; never publish production files."""
import json
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "_archive_print_proofs"
SELECTION = [
    "dancing-dragon-artwork-santiago-salvador.jpg",
    "calm-blue-ocean-artwork-santiago-salvador.jpg",
    "angel-vs-devil-pattern-artwork-santiago-salvador.jpg",
    "wild-style-artwork-santiago-salvador.jpg",
]


def main():
    OUTPUT.mkdir(exist_ok=True)
    catalog = json.loads((ROOT / "assets/data/artworks.json").read_text())
    by_filename = {item["filename"]: item for item in catalog}
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except OSError:
        font = ImageFont.load_default(size=30)
    for filename in SELECTION:
        item = by_filename[filename]
        with Image.open(ROOT / item["url"]) as source:
            art = ImageOps.exif_transpose(source).convert("RGB")
            art.thumbnail((2250, 2700), Image.Resampling.LANCZOS)
            sheet = Image.new("RGB", (2550, 3300), "white")
            sheet.paste(art, ((2550 - art.width) // 2, 150 + (2700 - art.height) // 2))
            draw = ImageDraw.Draw(sheet)
            draw.text((1275, 2970), item["title"], font=font, fill="#333333", anchor="mt")
            draw.text((1275, 3020), "Santiago Salvador", font=font, fill="#333333", anchor="mt")
            output = OUTPUT / (Path(filename).stem + "-letter-proof.pdf")
            sheet.save(output, "PDF", resolution=300, quality=95)
            print(f"Prepared {output.name}: image {art.width / 300:.2f} x {art.height / 300:.2f} inches")


if __name__ == "__main__":
    main()
