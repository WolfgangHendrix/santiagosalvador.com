import os
import json
import re
import time
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    Image = None
    ImageOps = None

def sync():
    t0 = time.time()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    site_dir = base_dir
    websites_dir = os.path.dirname(base_dir)
    data_dir = os.path.join(site_dir, "assets", "data")
    os.makedirs(data_dir, exist_ok=True)
    # Display titles are independent of search-friendly filenames.
    metadata_path = os.path.join(data_dir, "asset-metadata.json")
    asset_metadata = {}
    if os.path.exists(metadata_path):
        with open(metadata_path, encoding="utf-8") as fp:
            asset_metadata = json.load(fp)

    print("=" * 65)
    print("   SANTIAGO SALVADOR - PORTFOLIO & LABELS DATABASE SYNC")
    print("=" * 65)
    print(f"Scanning directory: {site_dir}")

    # 1. CURATED TITLES FROM BACKUP
    backup_html = os.path.join(websites_dir, "SantiagoSalvador.comBACKUP", "index.html")
    curated_titles = {}
    if os.path.exists(backup_html):
        try:
            with open(backup_html, encoding="utf-8", errors="ignore") as fp:
                html = fp.read()
            matches = re.findall(r'href=[\"\']images/fulls/([^\"\']+)[\"\'][\s\S]*?<h3>([^<]*)</h3>', html)
            for m in matches:
                curated_titles[m[0].lower()] = m[1].strip()
        except Exception:
            pass

    def clean_art_title(filename):
        lower = filename.lower()
        if lower in curated_titles and curated_titles[lower]:
            return curated_titles[lower]
        
        base = os.path.splitext(filename)[0]
        base = re.sub(r'^santiago_salvador_', '', base, flags=re.I)
        base = re.sub(r'^sanitago_salvador_', '', base, flags=re.I)
        base = re.sub(r'^copy\s+(of\s+)?', '', base, flags=re.I)
        base = re.sub(r'\s+copy(\s+\(\d+\))?$', '', base, flags=re.I)
        base = base.replace('_', ' ').replace('-', ' ').strip()
        
        words = base.split()
        capitalized = []
        for w in words:
            if w.lower() in ('a', 'an', 'and', 'the', 'in', 'of', 'on', 'at', 'to', 'for', 'by'):
                capitalized.append(w.lower())
            else:
                capitalized.append(w.capitalize())
        title = ' '.join(capitalized)
        return title if title else filename

    # A small editorial selection, keyed by stable paths rather than regenerated IDs.
    featured_urls = {
        'Art/Paintings_Illustrations/afrowoman-artwork-santiago-salvador.jpg',
        'Art/Paintings_Illustrations/anarchist-gorilla-artwork-santiago-salvador-2.jpg',
        'Art/Paintings_Illustrations/cowboy-kaboom-artwork-santiago-salvador-2.jpg',
        'Art/Paintings_Illustrations/dancing-dragon-artwork-santiago-salvador.jpg',
        'Art/Custom_Figures_Toys/anti-eternia-he-man-the-loyal-subjects-custom-figure-santiago-salvador.jpg',
        'Art/Custom_Figures_Toys/battle-cat-white-tiger-artwork-santiago-salvador.jpg',
        'Art/Game_Art_Screenshots/award-winning-activision-custom-csqa-design-game-art.jpg',
        'Art/Game_Art_Screenshots/theseus-vs-the-minotaur-1-game-art.jpg',
    }

    def art_thumb_rel(url_rel):
        inside = url_rel[len("Art/"):]
        return "Art/thumbs/" + os.path.splitext(inside)[0] + ".jpg"

    def save_grid_jpeg(src_path, dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with Image.open(src_path) as im:
            im = ImageOps.exif_transpose(im)
            if getattr(im, "is_animated", False):
                im.seek(0)
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                rgba = im.convert("RGBA")
                background = Image.new("RGB", rgba.size, (6, 7, 9))
                background.paste(rgba, mask=rgba.split()[-1])
                im = background
            elif im.mode != "RGB":
                im = im.convert("RGB")
            im.thumbnail((960, 960), Image.Resampling.LANCZOS)
            im.save(dest_path, "JPEG", quality=76, optimize=True)

    def ensure_art_thumb(src_path, url_rel):
        """Grid images stay small. The lightbox and download still use the master."""
        if Image is None:
            return url_rel
        try:
            if os.path.getsize(src_path) <= 350 * 1024 and os.path.splitext(src_path)[1].lower() in (".jpg", ".jpeg"):
                return url_rel
        except OSError:
            return url_rel
        thumb_rel = art_thumb_rel(url_rel)
        dest = os.path.join(site_dir, thumb_rel.replace("/", os.sep))
        try:
            if os.path.exists(dest) and os.path.getmtime(dest) >= os.path.getmtime(src_path):
                return thumb_rel
            save_grid_jpeg(src_path, dest)
            return thumb_rel
        except Exception as exc:
            print(f"    thumb skipped: {url_rel} ({exc})")
            return url_rel

    # A few older files live in the figures folder but depict other kinds of work.
    category_overrides = {
        'Art/Custom_Figures_Toys/motu-ram-man-game-screenshots-santiago-salvador.jpg': ('games', 'Game Art & Concepts'),
    }

    # 2. SCAN ARTWORKS DIRECTORY
    if Image is not None:
        Image.MAX_IMAGE_PIXELS = None
    art_dir = os.path.join(site_dir, "Art") if os.path.exists(os.path.join(site_dir, "Art")) else os.path.join(websites_dir, "Art")
    valid_img_exts = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

    categories = [
        ("Paintings_Illustrations", "paintings", "Paintings & Illustrations"),
        ("Custom_Figures_Toys", "figures", "Custom Figures & MOTU"),
        ("Game_Art_Screenshots", "games", "Game Art & Concepts")
    ]

    artworks = []
    cat_counts = {}
    art_catalog = {}
    art_id = 1

    for folder_name, cat_filter, cat_label in categories:
        folder_path = os.path.join(art_dir, folder_name)
        cat_files = []
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path):
                dirs.sort()
                for f in sorted(files):
                    ext = os.path.splitext(f)[1].lower()
                    if ext in valid_img_exts:
                        full_p = os.path.join(root, f)
                        rel_p = os.path.relpath(full_p, folder_path).replace("\\", "/")
                        cat_files.append(rel_p)

                        title = clean_art_title(f)
                        url_rel = f"Art/{folder_name}/{rel_p}".replace("\\", "/")
                        metadata = asset_metadata.get(url_rel, {})
                        title = re.sub(r"\s+", " ", metadata.get("title", title)).strip()
                        is_featured = url_rel in featured_urls
                        thumb_rel = ensure_art_thumb(full_p, url_rel)
                        effective_category, effective_label = category_overrides.get(url_rel, (cat_filter, cat_label))
                        if cat_filter == 'figures' and url_rel not in category_overrides and f not in {
                            'abra-custom-plush-doll-santiago-salvador.jpg',
                            'anti-eternia-he-man-the-loyal-subjects-custom-figure-santiago-salvador.jpg',
                            'anti-eternia-he-man-vintage-custom-masters-of-the-universe-figure-santiago-salvador.jpg',
                            'battle-cat-white-tiger-artwork-santiago-salvador.jpg',
                        }:
                            effective_category, effective_label = 'paintings', 'Paintings & Illustrations'

                        artworks.append({
                            "id": art_id,
                            "title": title,
                            "category": effective_category,
                            "categoryLabel": effective_label,
                            "filename": f,
                            "url": url_rel,
                            "thumb": thumb_rel,
                            "featured": is_featured
                        })
                        if art_id % 50 == 0:
                            print(f"    indexed {art_id} artworks...", flush=True)
                        art_id += 1

        cat_counts[cat_filter] = len(cat_files)
        art_catalog[cat_filter] = cat_files

    # Save Art/catalog.json
    try:
        with open(os.path.join(art_dir, "catalog.json"), "w", encoding="utf-8") as fp:
            json.dump(art_catalog, fp, indent=2)
    except Exception as e:
        print(f"Warning saving catalog.json: {e}")

    # Save artworks.json and artworks.js
    with open(os.path.join(data_dir, "artworks.json"), "w", encoding="utf-8") as fp:
        json.dump(artworks, fp, indent=2)
    with open(os.path.join(data_dir, "artworks.js"), "w", encoding="utf-8") as fp:
        fp.write("window.ARTWORKS_DATA = " + json.dumps(artworks) + ";\n")

    print(f"[+] Artworks indexed: {len(artworks)} total")
    for category, label in [('paintings', 'Paintings & Illustrations'), ('figures', 'Custom Figures'),
                            ('games', 'Game Art & Concepts')]:
        print(f"    - {label}: {sum(item['category'] == category for item in artworks)}")

    # 3. SCAN MUSIC DIRECTORY
    music_dir = os.path.join(art_dir, "Music_Audio")
    music_tracks = []
    curated_music_info = {
        "mus_main_brainbludgeoner.mp3": {
            "title": "Mad Man",
            "album": "The Brain Bludgeoner Theme Music"
        },
        "mus_thewearymarch.mp3": {
            "title": "March of the Weary",
            "album": "The Brain Bludgeoner Story Music"
        },
        "mus_boss_tidal_wave.mp3": {
            "title": "Shark Attack",
            "album": "SharkOn! Theme Music"
        },
        "mus_lev1_sliver.mp3": {
            "title": "Journey",
            "album": "Theseus VS The Minotaur Level Music"
        },
        "mus_end_game_funfunfun.mp3": {
            "title": "Jump Jax!",
            "album": "Jump Jax! Game Music & SFX"
        }
    }

    if os.path.exists(music_dir):
        m_id = 1
        for f in sorted(os.listdir(music_dir)):
            f_path = os.path.join(music_dir, f)
            if not os.path.isfile(f_path) or f.startswith(('_', '.')):
                continue
            if f.lower().endswith(('.mp3', '.ogg', '.wav')):
                info = asset_metadata.get(f"Art/Music_Audio/{f}", curated_music_info.get(f, {}))
                title = info.get("title")
                album = info.get("album", "Original Soundscapes")
                if not title:
                    clean_t = re.sub(r'^\d+[\s\-_]*', '', os.path.splitext(f)[0])
                    clean_t = clean_t.replace('_', ' ').replace('-', ' ').strip()
                    title = clean_t if clean_t else f

                music_tracks.append({
                    "id": m_id,
                    "title": title,
                    "artist": "Santiago Salvador",
                    "album": album,
                    "url": f"Art/Music_Audio/{f}".replace("\\", "/")
                })
                m_id += 1

    with open(os.path.join(data_dir, "music.json"), "w", encoding="utf-8") as fp:
        json.dump(music_tracks, fp, indent=2)
    with open(os.path.join(data_dir, "music.js"), "w", encoding="utf-8") as fp:
        fp.write("window.MUSIC_DATA = " + json.dumps(music_tracks) + ";\n")

    print(f"[+] Original Music indexed: {len(music_tracks)} tracks")

    # 4. SCAN RETRO GAME LABELS DIRECTORY
    labels_dir = os.path.join(site_dir, "Labels") if os.path.exists(os.path.join(site_dir, "Labels")) else os.path.join(websites_dir, "Labels")
    fulls_dir = os.path.join(labels_dir, "fulls")
    thumbs_dir = os.path.join(labels_dir, "thumbs")

    labels_list = []
    console_counts = {}

    if os.path.exists(fulls_dir):
        for console in sorted(os.listdir(fulls_dir)):
            c_full_path = os.path.join(fulls_dir, console)
            if not os.path.isdir(c_full_path):
                continue
            
            c_thumb_path = os.path.join(thumbs_dir, console)
            os.makedirs(c_thumb_path, exist_ok=True)
            thumb_by_stem = {}
            if os.path.isdir(c_thumb_path):
                for thumb_name in os.listdir(c_thumb_path):
                    thumb_ext = os.path.splitext(thumb_name)[1].lower()
                    if thumb_ext not in valid_img_exts:
                        continue
                    stem = os.path.splitext(thumb_name)[0].lower()
                    # Masters are often PNG while the grid thumb is a JPEG of the same name.
                    current = thumb_by_stem.get(stem)
                    if current is None or thumb_ext in (".jpg", ".jpeg"):
                        thumb_by_stem[stem] = thumb_name

            count = 0
            for idx, f in enumerate(sorted(os.listdir(c_full_path))):
                ext = os.path.splitext(f)[1].lower()
                if ext not in valid_img_exts:
                    continue
                
                title = os.path.splitext(f)[0].replace('_', ' ').replace('-', ' ').strip()
                download_rel = f"Labels/fulls/{console}/{f}".replace("\\", "/")
                title = re.sub(r"\s+", " ", asset_metadata.get(download_rel, {}).get("title", title)).strip()
                thumb_name = thumb_by_stem.get(os.path.splitext(f)[0].lower())
                if thumb_name:
                    thumb_rel = f"Labels/thumbs/{console}/{thumb_name}".replace("\\", "/")
                elif Image is None:
                    thumb_rel = download_rel
                else:
                    generated_name = os.path.splitext(f)[0] + ".jpg"
                    generated_path = os.path.join(c_thumb_path, generated_name)
                    try:
                        if not os.path.exists(generated_path) or os.path.getmtime(generated_path) < os.path.getmtime(os.path.join(c_full_path, f)):
                            save_grid_jpeg(os.path.join(c_full_path, f), generated_path)
                        thumb_rel = f"Labels/thumbs/{console}/{generated_name}".replace("\\", "/")
                    except Exception as exc:
                        print(f"    label thumb skipped: {download_rel} ({exc})")
                        thumb_rel = download_rel

                labels_list.append({
                    "id": f"{console}_{idx}",
                    "title": title,
                    "console": console,
                    "filename": f,
                    "downloadUrl": download_rel,
                    "thumbUrl": thumb_rel
                })
                count += 1
            console_counts[console] = count

    labels_data = {
        "counts": console_counts,
        "total": len(labels_list),
        "labels": labels_list
    }

    with open(os.path.join(labels_dir, "labels_catalog.json"), "w", encoding="utf-8") as fp:
        json.dump(labels_data, fp, indent=2)
    with open(os.path.join(data_dir, "labels.json"), "w", encoding="utf-8") as fp:
        json.dump(labels_data, fp, indent=2)
    with open(os.path.join(data_dir, "labels.js"), "w", encoding="utf-8") as fp:
        fp.write("window.LABELS_DATA = " + json.dumps(labels_data) + ";\n")

    print(f"[+] Retro Game Labels indexed: {len(labels_list)} total")

    # 5. UPDATE COUNTERS OUTSIDE THE ART GALLERY
    # Art filter counts come from the generated catalog at runtime.

    html_files = [
        os.path.join(site_dir, "index.html")
    ]

    for hpath in html_files:
        if os.path.exists(hpath):
            with open(hpath, 'r', encoding='utf-8') as fp:
                content = fp.read()
            
            label_total = f'{len(labels_list):,}'
            content = re.sub(r'[\d,]+\+?(?= free (?:game cartridge replacement labels|downloadable cartridge labels))', label_total, content)
            content = re.sub(r'(?<=All )[\d,]+\+?(?= (?:cartridge replacement labels|labels are))', label_total, content)
            content = re.sub(r'(data-console="all">All Labels\s*)\([\d,]+\)', lambda m: m[1] + f'({label_total})', content)
            for console, count in console_counts.items():
                pattern = r'(data-console="' + re.escape(console.lower()) + r'">[^<]*?)\([\d,]+\)'
                content = re.sub(pattern, lambda m: m[1] + f'({count:,})', content)
            content = re.sub(r'(Original Soundtrack Playlist\s*)\(\d+\)', lambda m: m[1] + f'({len(music_tracks)})', content)

            with open(hpath, 'w', encoding='utf-8') as fp:
                fp.write(content)

    print("[+] Updated category filter pill counts in HTML files")
    print(f"[OK] SYNC COMPLETED IN {time.time() - t0:.2f} SECONDS!")
    print("=" * 65)

if __name__ == "__main__":
    sync()
