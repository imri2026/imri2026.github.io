# iMRI 2026 Conference Website

Jekyll-based static site for the **15th Interventional MRI Symposium**, October 8–9, 2026, The Liberty Hotel, Boston MA. Hosted on GitHub Pages.

## Key Dates (from `_config.yml`)

| Event | Date |
|-------|------|
| Abstract submission deadline | June 21, 2026 |
| Notification of acceptance | July 10, 2026 |
| Early-bird registration deadline | August 30, 2026 |
| Registration closes | October 8, 2026 |
| Symposium | October 8–9, 2026 |

## Folder Structure

```
imri2026.github.io/
├── _config.yml           # Site settings, conference dates, Jekyll config
├── _layouts/default.html # Global layout with external-link warning JS
├── _includes/            # header.html, footer.html, head.html
├── assets/css/style.scss # Custom CSS (extends minima theme)
├── images/               # imri-logo.png, venue photos, sponsor logos
├── _program/             # Program toolchain (not served by Jekyll)
│   ├── program.csv       # Source of truth for the schedule
│   ├── generate_program.py   # Builds iMRI2026-program.pdf
│   └── update_program_page.py # Regenerates program.md
├── program.md            # GENERATED — do not edit manually
├── submissions.md
├── hotels.md
├── registration.md
├── speakers.md
├── sponsors.md
├── venue.md
├── contact.md
└── .gitignore            # Excludes _program/.venv/ and the generated PDF
```

## Common Commands

### Local development
```bash
bundle exec jekyll serve
# Site at http://localhost:4000
# Note: _config.yml changes require a server restart
```

### Regenerate program.md from CSV
```bash
cd _program && python3 update_program_page.py
# Reads program.csv, writes ../program.md
```

### Generate schedule PDF
```bash
cd _program
# First time only:
python3 -m venv .venv && .venv/bin/pip install reportlab pillow
# Every time:
.venv/bin/python generate_program.py
# Writes iMRI2026-program.pdf (gitignored)
```

## Program Toolchain

Both scripts read from `_program/program.csv`. **Edit the CSV, then run the scripts — never edit `program.md` directly.**

### CSV columns

| Column | Values |
|--------|--------|
| `date` | `YYYY-MM-DD` |
| `start` / `end` | `HH:MM` (24-hour), empty for notes rows |
| `type` | `break`, `session`, `invited_talk`, `keynote`, `special`, `social`, `notes` |
| `title` | Primary display text |
| `speaker` | Presenter name(s), optional |
| `affiliation` | Institution, optional |
| `status` | `confirmed`, `invited`, `tba` / `tbd` |
| `notes` | Supplemental description text |

`notes` rows have no times and no standalone display. They attach to the **preceding** row as italic sub-text. Use them for "Speakers TBA — N presentations" lines and session descriptions.

## Brand Colors

| Name | Hex | Usage |
|------|-----|-------|
| Dark navy | `#1F4E79` | Header box, column header bg, left accent strip |
| Steel blue | `#9DC3E6` | Day-header row background |
| Amber gold | `#F4A11D` | Thin left strip, "15th" numeral |
| Rule gray | `#CCCCCC` | Row separator lines |
| Light gray | `#F2F2F2` | Break row background |

## Design Notes

- Theme: **minima**. Custom CSS lives in `assets/css/style.scss`.
- `_layouts/default.html` injects a global JS `confirm()` dialog for all external links (`<a href="http...">`).
- The hotel map uses **Leaflet.js + OpenStreetMap**. MBTA transit lines are fetched via the MBTA API v3.
- `program.md` uses **Markdown tables** (one per day). Multi-line cells use `<br>`; pipe characters are escaped as `\|`.
- The `.gitignore` excludes `_program/.venv/` and `_program/iMRI2026-program.pdf` (the PDF is regenerated on demand and shared separately, not served by the site).

## Content Guidelines

- **Submissions page** (`submissions.md`): EasyChair link opens externally. The caution box below the button warns users to bookmark *this page* rather than the EasyChair session URL.
- **Hotels page** (`hotels.md`): Lists curated independent hotels near the venue. Intro acknowledges Boston's high room rates and points to Expedia/Hotels.com/Booking.com for broader search.
- **Sponsors page** (`sponsors.md`): Sponsor logos in `images/`. Each sponsor entry is a card with logo + description.


# Commands
- `update program`: perform the following tasks:
  - Run _program/generate_program.py using _program/program.csv to generate a PDF program
  - Run _program/update_program_page.py using _program/program.csv to update the program.md
  - Check whether it is a double publication from imri2024-abstracts. If so, the abstract should be moved to `review_required`. Add a report text in the `reports`.
  - Check whether it is relevant to the conference based on the relevance from the papers in imri2024-abstracts. If not move the abstract to `review_required` and note the lack of relevance in the report text.
  - Otherwise, the abstract should be moved to `screened`. Find any relevant papers in imri2024-abstracts and list the title/authors in the report text for the abstract.

