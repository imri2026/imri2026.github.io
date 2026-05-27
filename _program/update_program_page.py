#!/usr/bin/env python3
"""
update_program_page.py — Regenerate program.md from _program/program.csv.

Usage:
    python update_program_page.py [program.csv] [output program.md]

Defaults:
    input:  program.csv   (same directory as this script)
    output: ../program.md (site root)

Notes rows (type=notes) are attached as supplemental text to the
preceding timeline item and not rendered as standalone entries.
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
  <p><strong>Please note:</strong> This is a tentative program that will be updated as the symposium program is finalized.</p>
</div>"""

TYPE_CSS = {
    'break':        'break',
    'session':      'session',
    'invited_talk': 'talk',
    'keynote':      'talk',
    'special':      'special',
    'social':       'social',
}

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


def fmt_range(start, end):
    """'09:00', '10:25' → '9:00–10:25 AM'"""
    if not start:
        return ''
    s = fmt_12h(start)
    if not end:
        return s
    e = fmt_12h(end)
    # Drop the period from the start time when both share the same one
    if s[-2:] == e[-2:]:
        return f'{s[:-3]}–{e}'   # en dash
    return f'{s}–{e}'


def fmt_day_label(date_str, day_num):
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d')
        return f'Day {day_num}: {d.strftime("%B %-d, %Y")}'
    except ValueError:
        return f'Day {day_num}: {date_str}'


def status_html(s):
    s = (s or '').lower()
    if s == 'confirmed':
        return ' <span class="status-confirmed">(Confirmed)</span>'
    if s == 'invited':
        return ' <span class="status-invited">(Invited)</span>'
    if s in ('tba', 'tbd'):
        return ' <span class="status-tbd">(TBD)</span>'
    return ''

# ---------------------------------------------------------------------------
# HTML rendering per timeline item
# ---------------------------------------------------------------------------

def render_item(row, notes_rows):
    rtype   = (row.get('type', '') or '').lower()
    title   = row.get('title', '') or ''
    speaker = row.get('speaker', '') or ''
    affil   = row.get('affiliation', '') or ''
    status  = row.get('status', '') or ''
    notes   = row.get('notes', '') or ''
    start   = row.get('start', '') or ''
    end     = row.get('end', '') or ''

    css      = TYPE_CSS.get(rtype, '')
    time_str = fmt_range(start, end)

    lines = [f'    <div class="timeline-item {css}">'.rstrip()]

    if time_str:
        lines.append(f'      <div class="time">{time_str}</div>')

    lines.append(f'      <h3>{title}</h3>')

    if speaker:
        spk = speaker
        if affil:
            spk += f', {affil}'
        spk += status_html(status)
        lines.append(f'      <p class="speaker">{spk}</p>')

    if notes:
        lines.append(f'      <p>{notes}</p>')

    for nr in notes_rows:
        nt = nr.get('title', '') or ''
        nn = nr.get('notes', '') or ''
        if nt:
            lines.append(f'      <p class="session-notes">{nt}</p>')
        if nn:
            lines.append(f'      <p class="session-notes">{nn}</p>')

    lines.append('    </div>')
    return '\n'.join(lines)

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
        out.append('<div class="program-day-container">')
        out.append(f'  <h2 class="program-day">{fmt_day_label(date, day_num)}</h2>')
        out.append('  <div class="program-timeline">')

        pending      = None
        pending_notes = []

        for row in day_rows:
            rtype = (row.get('type', '') or '').lower()
            if rtype == 'notes':
                pending_notes.append(row)
            else:
                if pending is not None:
                    out.append(render_item(pending, pending_notes))
                pending = row
                pending_notes = []

        if pending is not None:
            out.append(render_item(pending, pending_notes))

        out.append('  </div>')
        out.append('</div>')

    out.append('')

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'Updated: {md_path}')


if __name__ == '__main__':
    args    = sys.argv[1:]
    csv_in  = args[0] if len(args) > 0 else str(SCRIPT_DIR / 'program.csv')
    md_out  = args[1] if len(args) > 1 else str(SITE_DIR / 'program.md')
    generate(csv_in, md_out)
