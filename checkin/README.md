# iMRI 2026 Check-In

An installable web app (PWA) that scans the vCard QR codes printed on the
conference badges, stores each attendee locally in IndexedDB, and exports
the scanned list as a CSV — all on-device, no backend/server required.

Served as part of the main conference site at **https://imri2026.org/checkin/**
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
sw.js                Service worker (offline app-shell caching, scoped to /checkin/)
icons/                 App icons
generate_icons.py    Script that generated icons/ (requires Pillow)
```

## Local testing

From the site root:

```bash
bundle exec jekyll serve
# open http://localhost:4000/checkin/
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
   everything (asks for confirmation first).
5. Tap **Export CSV** to download the file (or, on iOS/Android where
   supported, share it via the native share sheet — to Files, Mail,
   AirDrop, etc.). Columns: Name, Affiliation, Country, Email, Scanned At,
   Raw QR Data.

All data lives only in the browser's IndexedDB **on that device** — nothing
is sent to imri2026.org or anywhere else. Data does not sync between devices;
each phone/tablet used at check-in builds its own local list and should
export its own CSV. Clearing Safari/Chrome site data for imri2026.org, or
uninstalling the home-screen app, deletes the scanned list, so export before
doing either.

## Regenerating icons

```bash
pip install pillow
python3 generate_icons.py
```

## Compatibility notes

- vCard parsing and CSV escaping were unit-tested against the exact vCard
  format produced by the companion `generate_badges.py` script (in the
  `imri2026-badge` repo), including commas/semicolons in affiliation and
  country fields.
- If a scanned QR code isn't a vCard, its raw text is still saved (Name/
  Affiliation/Country/Email blank, Raw QR Data filled in) so nothing is lost.
