# Publishing optimized media

Install build dependencies with `python -m pip install -r requirements-build.txt`, then run `python publish_site.py`. Preview the generated site with `python -m http.server 8765 --directory _site`.

The build generates WebP images only for referenced artwork, Marvel archive, and cartridge-label thumbnails, and rewrites the published catalogs to use those WebPs. Generated images live solely in the ignored `_site` directory. Original downloads and source catalogs retain their existing formats; running `sync_database.py` does not undo the publishing optimization. No second thumbnail collection is committed to Git, and unused JPEG thumbnails are not copied into the deployment.

The silent hero video has a 1280-pixel desktop version and a 640-pixel mobile version. Both are H.264 MP4 at 24 fps with the index moved to the start for streaming. The original video is retained in the ignored local `_archive_performance` folder. The portrait uses animated WebP. The unused mute button was removed because the video has no audio.

The labels catalog is loaded once when the labels section is within 400 pixels of the viewport, or when a visitor interacts with its search/filter controls. Loading failures expose a retry button. The script-loading approach preserves local file preview support. Search and filter selections made while loading are applied when the catalog arrives.

Music loading behavior is unchanged. Optimized media reduces the current deployment and future transfer size; it does not shrink existing Git history.
