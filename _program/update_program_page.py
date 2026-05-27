#!/usr/bin/env python3
"""
update_program_page.py — Regenerate program.md from _program/program.csv.

Usage:
    python update_program_page.py [program.csv] [output program.md]

Defaults:
    input:  program.csv   (same directory as this script)
    output: ../program.md (site root)

Notes rows (type=notes) are folded into the preceding row's title cell
as supplemental italic sub-text rather than rendered as separate rows.
"""

import csv
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SITE_DIR   = SCRIPT_DIR.parent

FRONT_MATTER = """\
---
layout: page
title: Symposium Program
permalink: /program/
---

<div class="content-card">
  <p><strong>Please note:</strong> This is a tentative program. The times, speakers, and titles are subject to change.</p>
</div>"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return [{k: v.strip() for k, v in row.items()}
                for row in csv.DictReader(f)]


def fmt_12h(t):
    """'14:30' → '2:30 PM'"""
    if not t:
        return ''
    try:
        h, m = map(int, t.split(':'))
    except ValueError:
        return t
    period = 'AM' if h < 12 else 'PM'
    h12 = h % 12 or 12
    return f'{h12}:{m:02d} {period}'


def fmt_day_label(date_str):
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d')
        return d.strftime('%B %-d, %Y')
    except ValueError:
        return date_str


def escape(s):
    """Escape pipe characters so they don't break Markdown table cells."""
    return (s or '').replace('|', '\\|')


def status_text(s):
    s = (s or '').lower()
    if s == 'confirmed': return ' (Confirmed)'
    if s == 'invited':   return ' (Invited)'
    if s in ('tba', 'tbd'): return ' (TBD)'
    return ''

# ---------------------------------------------------------------------------
# Markdown row rendering
# ---------------------------------------------------------------------------

def render_row(row, notes_rows):
    rtype   = (row.get('type', '') or '').lower()
    title   = escape(row.get('title',       '') or '')
    speaker = escape(row.get('speaker',     '') or '')
    affil   = escape(row.get('affiliation', '') or '')
    status  = row.get('status', '') or ''
    notes   = escape(row.get('notes',       '') or '')
    start   = row.get('start', '') or ''
    end     = row.get('end',   '') or ''

    s = fmt_12h(start)
    e = fmt_12h(end)

    # Title cell: bold title, optional italic speaker + notes lines
    parts = [f'**{title}**']

    if speaker:
        spk = speaker
        if affil:
            spk += f', {affil}'
        spk += status_text(status)
        parts.append(f'*{spk}*')

    if notes:
        parts.append(f'*{notes}*')

    for nr in notes_rows:
        nt = escape(nr.get('title', '') or '')
        nn = escape(nr.get('notes', '') or '')
        line = '. '.join(filter(None, [nt, nn]))
        if line:
            parts.append(f'*{line}*')

    title_md = '<br>'.join(parts)
    return f'| {s} | {e} | {title_md} |'

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate(csv_path, md_path):
    rows = load_csv(csv_path)

    # Group by date, preserving order
    days = {}
    day_order = []
    for row in rows:
        date = row.get('date', '') or ''
        if date not in days:
            days[date] = []
            day_order.append(date)
        days[date].append(row)

    out = [FRONT_MATTER]

    for day_num, date in enumerate(day_order, 1):
        day_rows = days[date]

        out.append('')
        out.append(f'## Day {day_num}: {fmt_day_label(date)}')
        out.append('')
        out.append('| Start | End | Session |')
        out.append('|-------|-----|---------|')

        pending       = None
        pending_notes = []

        for row in day_rows:
            rtype = (row.get('type', '') or '').lower()
            if rtype == 'notes':
                pending_notes.append(row)
            else:
                if pending is not None:
                    out.append(render_row(pending, pending_notes))
                pending = row
                pending_notes = []

        if pending is not None:
            out.append(render_row(pending, pending_notes))

    out.append('')

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'Updated: {md_path}')


if __name__ == '__main__':
    args   = sys.argv[1:]
    csv_in = args[0] if len(args) > 0 else str(SCRIPT_DIR / 'program.csv')
    md_out = args[1] if len(args) > 1 else str(SITE_DIR / 'program.md')
    generate(csv_in, md_out)
