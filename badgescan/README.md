# iMRI 2026 Badge Scan

Built to streamline how vendors obtain attendee contact information at the
symposium — legally and with the attendee's explicit, in-person opt-in
(scanning their own badge). An installable web app (PWA) that scans the
vCard QR codes printed on the conference badges, stores each attendee
locally in IndexedDB, and exports the scanned list as a CSV — all
on-device, no backend/server required.

Served as part of the main conference site at **https://imri2026.org/badgescan/**
(this folder is copied through as static files by Jekyll — none of it is
processed as a Jekyll page).

Works in the browser on iOS (Safari) and Android (Chrome); can be "installed"
to the home screen on both for a full-screen, app-like experience.

## Files

```
index.html          Main page / UI
css/style.css        Styling (mobile-first, light + dark)
js/vcard.js           vCard text parser
js/db.js               IndexedDB wrapper (add/list/delete/clear scans)
js/csv.js               CSV building + export (download or native share sheet)
js/app.js                UI wiring: camera control, scan handling, list, export
lib/html5-qrcode.min.js  Third-party QR scanning engine (bundled locally, MIT licensed)
manifest.webmanifest  PWA manifest (install/home-screen metadata)
sw.js                Service worker (offline app-shell caching, scoped to /badgescan/)
icons/                 App icons
generate_icons.py    Script that generated icons/ (requires Pillow)
```

## Local testing

From the site root:

```bash
bundle exec jekyll serve
# open http://localhost:4000/badgescan/
```

`http://localhost` is treated as a secure context, so camera access works
for local testing without HTTPS. The live site is HTTPS, so camera access
works there too.

## Using the app

1. Tap **Start Scanning** and point the camera at a badge's QR code.
2. On a successful scan it's parsed, saved to IndexedDB, and added to the
   list below with a toast confirmation. Scanning the same badge again shows
   "Already scanned" instead of creating a duplicate row (matched by email,
   or by the raw QR text if there's no email).
3. Tap **Flip Camera** to switch between front/back cameras if needed.
4. Tap any ✕ next to a row to remove that attendee, or **Clear all** to wipe
   everything — both ask for confirmation first.
5. Tap **Export CSV** to download the file (or, on iOS/Android where
   supported, share it via the native share sheet — to Files, Mail,
   AirDrop, etc.). Columns: Name, Affiliation, Country, Email, Scanned At.

All data lives only in the browser's IndexedDB **on that device** — nothing
is sent to imri2026.org or anywhere else. Data does not sync between devices;
each phone/tablet used at check-in builds its own local list and should
export its own CSV. Clearing Safari/Chrome site data for imri2026.org, or
uninstalling the home-screen app, deletes the scanned list, so export before
doing either.

## Deploying changes

**Whenever you edit `index.html`, `css/`, `js/`, `lib/`, `manifest.webmanifest`,
or any icon, bump `CACHE_NAME` in `sw.js`.** The service worker caches those
files cache-first for offline use; if `CACHE_NAME` doesn't change, browsers
that already visited keep serving the old cached versions indefinitely, even
after the new code is deployed. This bit us once already — see commit
history around "Fix delete-confirm not appearing on already-visited devices."

If a user reports a shipped fix "not working," this is the first thing to
check before assuming the code is wrong.

### Forcing an update on a device that's stuck on stale files

1. Confirm the fix is actually pushed to `main` and live (GitHub Actions
   deploy can take a minute or two).
2. Have the user fully reload: on iOS, force-quit the installed app (swipe
   it away in the app switcher) and reopen it; a background/foreground
   toggle isn't enough. This may take two reloads (one to install the
   updated service worker, one more to actually be served the new files).
3. If that doesn't work, the reliable fix: remove the app from the Home
   Screen, then in Safari go to Settings → Safari → Advanced → Website Data,
   find `imri2026.org`, and delete it (this wipes the old service worker and
   cache). Revisit `https://imri2026.org/badgescan/` and re-add to Home
   Screen.

## Regenerating icons

Icons are composed from the conference logo (`assets/imri-logo.svg`, a local
copy of `images/imri-logo.svg` from the site root) on the brand-navy tile.

```bash
brew install librsvg   # provides rsvg-convert, used to rasterize the SVG
pip install pillow
python3 generate_icons.py
```

## Compatibility notes

- vCard parsing and CSV escaping were unit-tested against the exact vCard
  format produced by the companion `generate_badges.py` script (in the
  `imri2026-badge` repo), including commas/semicolons in affiliation and
  country fields.
- If a scanned QR code isn't a vCard, its raw text is still saved to
  IndexedDB (Name/Affiliation/Country/Email blank) so nothing is lost, even
  though the raw text isn't included in the CSV export.
