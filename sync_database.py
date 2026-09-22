import os
import json
import re
import time
import sys

def sync():
    t0 = time.time()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    site_dir = base_dir
    websites_dir = os.path.dirname(base_dir)
    data_dir = os.path.join(site_dir, "assets", "data")
    os.makedirs(data_dir, exist_ok=True)

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

    featured_slugs = {
        'cowboykaboom', '3eyedragon', 'afrowoman', 'solice', 'angelsareinmydreams',
        'buddhablack', 'buddhabuddha', 'coraline', 'jimihendrix', 'hendrix',
        'benderbitcoin', 'toxi', 'splatterhousedoom', 'activision_csqa',
        'antieterniaheman', 'battlecatwhitetiger', 'anarchistgorilla', 'dancingdragon',
        'euthanasia', 'drjeck', 'doom', 'dragon', 'angryhorizon', 'forestofdespair',
        'thedryingsoul', 'inquisition', 'twin despair', 'octopuscloud'
    }

    # 2. SCAN ARTWORKS DIRECTORY
    art_dir = os.path.join(site_dir, "Art") if os.path.exists(os.path.join(site_dir, "Art")) else os.path.join(websites_dir, "Art")
    valid_img_exts = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

    categories = [
        ("Paintings_Illustrations", "paintings", "Paintings & Illustrations"),
        ("Custom_Figures_Toys", "figures", "Custom Figures & MOTU"),
        ("Game_Art_Screenshots", "games", "Game Art & Concepts"),
        ("Cards_Collectibles", "cards", "Trading Cards")
    ]

    artworks = []
    cat_counts = {}
    art_catalog = {}
    art_id = 1

    for folder_name, cat_filter, cat_label in categories:
        folder_path = os.path.join(art_dir, folder_name)
        cat_files = []
        if os.path.exists(folder_path):
            for root, _, files in os.walk(folder_path):
                for f in sorted(files):
                    ext = os.path.splitext(f)[1].lower()
                    if ext in valid_img_exts:
                        full_p = os.path.join(root, f)
                        rel_p = os.path.relpath(full_p, folder_path).replace("\\", "/")
                        cat_files.append(rel_p)

                        title = clean_art_title(f)
                        slug = re.sub(r'[^a-zA-Z0-9]', '', title).lower()
                        is_featured = (slug in featured_slugs) or (cat_filter == 'figures')
                        url_rel = f"Art/{folder_name}/{rel_p}".replace("\\", "/")

                        artworks.append({
                            "id": art_id,
                            "title": title,
                            "category": cat_filter,
                            "categoryLabel": cat_label,
                            "filename": f,
                            "url": url_rel,
                            "featured": is_featured
                        })
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
    print(f"    - Paintings & Illustrations: {cat_counts.get('paintings', 0)}")
    print(f"    - Custom Figures & MOTU:     {cat_counts.get('figures', 0)}")
    print(f"    - Game Art & Concepts:       {cat_counts.get('games', 0)}")
    print(f"    - Trading Cards:             {cat_counts.get('cards', 0)}")

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
                info = curated_music_info.get(f, {})
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
    packs_dir = os.path.join(labels_dir, "packs")

    console_names = {
        "SNES": "Super Nintendo",
        "NES": "Nintendo Entertainment System",
        "N64": "Nintendo 64",
        "Genesis_MegaDrive": "Sega Genesis & Mega Drive",
        "GameBoy": "Game Boy Color & Advance",
        "NeoGeo": "Neo-Geo AES & MVS",
        "Famicom_SFC": "Famicom & Super Famicom"
    }

    labels_list = []
    console_counts = {}

    if os.path.exists(fulls_dir):
        for console in os.listdir(fulls_dir):
            c_full_path = os.path.join(fulls_dir, console)
            if not os.path.isdir(c_full_path):
                continue
            
            c_thumb_path = os.path.join(thumbs_dir, console)
            os.makedirs(c_thumb_path, exist_ok=True)
            
            count = 0
            for idx, f in enumerate(sorted(os.listdir(c_full_path))):
                ext = os.path.splitext(f)[1].lower()
                if ext not in valid_img_exts:
                    continue
                
                title = os.path.splitext(f)[0].replace('_', ' ').replace('-', ' ').strip()
                download_rel = f"Labels/fulls/{console}/{f}".replace("\\", "/")
                
                if not os.path.exists(os.path.join(c_thumb_path, f)):
                    thumb_rel = download_rel
                else:
                    thumb_rel = f"Labels/thumbs/{console}/{f}".replace("\\", "/")

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

    # Scan packs with exact console matching
    packs_list = []
    if os.path.exists(packs_dir):
        for console, display_name in console_names.items():
            for zf in sorted(os.listdir(packs_dir)):
                if f"_{console}_".lower() in zf.lower() and zf.lower().endswith('.zip'):
                    zpath = os.path.join(packs_dir, zf)
                    size_mb = os.path.getsize(zpath) / (1024 * 1024)
                    packs_list.append({
                        "console": console,
                        "title": f"{display_name} Pack ({console_counts.get(console, 0)} Labels)",
                        "count": console_counts.get(console, 0),
                        "url": f"Labels/packs/{zf}".replace("\\", "/"),
                        "size": f"{size_mb:.0f} MB" if size_mb >= 1 else f"{size_mb*1024:.0f} KB"
                    })

    labels_data = {
        "counts": console_counts,
        "total": len(labels_list),
        "labels": labels_list,
        "packs": packs_list
    }

    with open(os.path.join(labels_dir, "labels_catalog.json"), "w", encoding="utf-8") as fp:
        json.dump(labels_data, fp, indent=2)
    with open(os.path.join(data_dir, "labels.json"), "w", encoding="utf-8") as fp:
        json.dump(labels_data, fp, indent=2)
    with open(os.path.join(data_dir, "labels.js"), "w", encoding="utf-8") as fp:
        fp.write("window.LABELS_DATA = " + json.dumps(labels_data) + ";\n")

    print(f"[+] Retro Game Labels indexed: {len(labels_list)} total")
    print(f"[+] Console Packs indexed: {len(packs_list)} packs")

    # 5. UPDATE HTML FILTER BADGES & COUNTERS
    total_art = len(artworks)
    p_cnt = cat_counts.get('paintings', 0)
    f_cnt = cat_counts.get('figures', 0)
    g_cnt = cat_counts.get('games', 0)
    c_cnt = cat_counts.get('cards', 0)

    html_files = [
        os.path.join(site_dir, "index.html"),
        os.path.join(websites_dir, "index.html")
    ]

    for hpath in html_files:
        if os.path.exists(hpath):
            with open(hpath, 'r', encoding='utf-8') as fp:
                content = fp.read()
            
            content = re.sub(r'(data-filter=\"all\">All Works\s*)\(\d+\)', rf'\g<1>({total_art})', content)
            content = re.sub(r'(data-filter=\"paintings\">Paintings & Illustrations\s*)\(\d+\)', rf'\g<1>({p_cnt})', content)
            content = re.sub(r'(data-filter=\"figures\">Custom Figures & MOTU\s*)\(\d+\)', rf'\g<1>({f_cnt})', content)
            content = re.sub(r'(data-filter=\"games\">Game Art & Concepts\s*)\(\d+\)', rf'\g<1>({g_cnt})', content)
            content = re.sub(r'(data-filter=\"cards\">Trading Cards\s*)\(\d+\)', rf'\g<1>({c_cnt})', content)
            content = re.sub(r'Over \d+ paintings, dark art illustrations', f'Over {total_art} paintings, dark art illustrations', content)

            with open(hpath, 'w', encoding='utf-8') as fp:
                fp.write(content)

    print("[+] Updated category filter pill counts in HTML files")
    print(f"[OK] SYNC COMPLETED IN {time.time() - t0:.2f} SECONDS!")
    print("=" * 65)

if __name__ == "__main__":
    sync()
