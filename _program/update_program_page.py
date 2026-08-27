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

Each `session` row becomes its own HTML table: the session name and
moderators are merged into the table's own <caption> header, followed by
a Start/End/Presentation body listing its invited_talk/oral/keynote
children (omitted for sessions with none, e.g. the poster block). Other
rows (break, special, social) render as standalone single-row 'note'
tables between sections.
"""

import csv
import html
import re
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
---"""

TENTATIVE_NOTE = """\
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


def load_posters(path):
    path = Path(path)
    if not path.exists():
        return []
    return load_csv(path)


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
    if s == 'invited':   return ' (Invited)'
    if s in ('tba', 'tbd'): return ' (TBD)'
    return ''


def esc_html(s):
    """Escape for raw-HTML output (kramdown passes HTML blocks through untouched)."""
    return html.escape(s or '', quote=False)


def slugify(text):
    slug = re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')
    return slug or 'session'

# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def speaker_line(row, escape_fn):
    speaker = escape_fn(row.get('speaker', '') or '')
    affil   = escape_fn(row.get('affiliation', '') or '')
    city    = escape_fn(row.get('city', '') or '')
    country = escape_fn(row.get('country', '') or '')
    status  = row.get('status', '') or ''
    if not speaker:
        return None
    spk = speaker
    if affil:
        spk += f', {affil}'
    location = ', '.join(filter(None, [city, country]))
    if location:
        spk += f', {location}'
    spk += status_text(status)
    return spk


def render_session_child_row(row, notes_rows):
    """One <tr> of a session's #/Start/End/Presentation body."""
    num   = row.get('number', '') or ''
    num   = esc_html(f'O-{num}' if num else '')
    title = esc_html(row.get('title', '') or '')
    notes = esc_html(row.get('notes', '') or '')
    s = esc_html(fmt_12h(row.get('start', '') or ''))
    e = esc_html(fmt_12h(row.get('end',   '') or ''))

    parts = [f'<strong>{title}</strong>']

    spk = speaker_line(row, esc_html)
    if spk:
        parts.append(f'<em>{spk}</em>')

    if notes:
        parts.append(f'<em>{notes}</em>')

    for nr in notes_rows:
        nt = esc_html(nr.get('title', '') or '')
        nn = esc_html(nr.get('notes', '') or '')
        line = '. '.join(filter(None, [nt, nn]))
        if line:
            parts.append(f'<em>{line}</em>')

    cell = '<br>'.join(parts)
    return f'<tr><td>{num}</td><td>{s}</td><td>{e}</td><td>{cell}</td></tr>'


def render_day_heading(day_num, date):
    """A 'Day N: <date>' bar, styled like a session caption but orange."""
    label = esc_html(f'Day {day_num}: {fmt_day_label(date)}')
    return (
        '<table class="program-day-table">\n'
        f'<caption><span class="day-name">{label}</span></caption>\n'
        '</table>'
    )


def render_session_table(session_row, session_notes_rows, children, anchor_id):
    """A whole session: name + moderators merged into the table's own
    <caption> header, followed by its Start/End/Presentation body (omitted
    for sessions with no invited_talk/oral children, e.g. the poster block)."""
    title = esc_html(session_row.get('title', '') or '')
    mods  = esc_html(session_row.get('speaker', '') or '')
    notes = esc_html(session_row.get('notes', '') or '')

    lines = [f'<table class="program-session-table" id="{anchor_id}">', '<caption>']
    lines.append(f'<span class="session-name">{title}</span>')
    if mods:
        lines.append(f'<span class="session-moderators">{mods}</span>')
    if notes:
        lines.append(f'<span class="session-notes">{notes}</span>')
    for nr in session_notes_rows:
        nt = esc_html(nr.get('title', '') or '')
        nn = esc_html(nr.get('notes', '') or '')
        line = '. '.join(filter(None, [nt, nn]))
        if line:
            lines.append(f'<span class="session-notes">{line}</span>')
    lines.append('</caption>')

    if children:
        lines.append('<thead><tr><th>#</th><th>Start</th><th>End</th><th>Presentation</th></tr></thead>')
        lines.append('<tbody>')
        for child_row, child_notes in children:
            lines.append(render_session_child_row(child_row, child_notes))
        lines.append('</tbody>')

    lines.append('</table>')
    return '\n'.join(lines)


def render_standalone(row, notes_rows, out):
    """A break/special/social row: a single-row orange 'note' table."""
    title = escape(row.get('title', '') or '')
    notes = escape(row.get('notes', '') or '')
    s = fmt_12h(row.get('start', '') or '')
    e = fmt_12h(row.get('end',   '') or '')

    parts = [f'**{title}**']

    spk = speaker_line(row, escape)
    if spk:
        parts.append(f'*{spk}*')

    if notes:
        parts.append(f'*{notes}*')

    for nr in notes_rows:
        nt = escape(nr.get('title', '') or '')
        nn = escape(nr.get('notes', '') or '')
        line = '. '.join(filter(None, [nt, nn]))
        if line:
            parts.append(f'*{line}*')

    item_md = '<br>'.join(parts)

    out.append('')
    out.append('| Start | End | Item |')
    out.append('|-------|-----|------|')
    out.append(f'| {s} | {e} | {item_md} |')
    out.append('{: .program-note-table}')


POSTER_SESSION_SLUG = 'poster-session'


def render_poster_section(posters):
    """A 'Poster Session' banner plus one table per topic, listing every
    poster's number, title, and presenter (all posters share the single
    Day 1 poster time slot, so no per-poster times are shown)."""
    categories = []
    by_category = {}
    for row in posters:
        cat = row.get('category', '') or 'Other'
        if cat not in by_category:
            by_category[cat] = []
            categories.append(cat)
        by_category[cat].append(row)

    lines = ['', (
        f'<table class="program-day-table" id="{POSTER_SESSION_SLUG}">\n'
        '<caption><span class="day-name">Poster Session</span></caption>\n'
        '</table>'
    )]
    lines.append('')
    lines.append(
        f'All {len(posters)} poster-assigned abstracts are presented in the area adjacent to the '
        'main conference room during Session III — Poster Presentations '
        '(1:00 PM – 2:30 PM, October 8, 2026), grouped below by topic.'
    )

    for cat in categories:
        group = by_category[cat]
        lines.append('')
        lines.append(f'### {escape(cat)} ({len(group)})')
        lines.append('')
        lines.append('| # | Title | Presenter |')
        lines.append('|---|-------|-----------|')
        for row in group:
            num     = row.get('number', '') or ''
            num     = escape(f'P-{num}' if num else '')
            title   = escape(row.get('title', '') or '')
            author  = escape(row.get('author', '') or '')
            inst    = escape(row.get('institution', '') or '')
            city    = escape(row.get('city', '') or '')
            country = escape(row.get('country', '') or '')

            presenter = author
            location = ', '.join(filter(None, [inst, city, country]))
            if location:
                presenter += f', {location}'
            lines.append(f'| {num} | {title} | {presenter} |')
        lines.append('{: .program-poster-table}')

    return lines


def render_toc(groups):
    """A 'Sessions Overview' box linking to every session/section, grouped."""
    lines = [
        '<div class="program-toc">',
        '<div class="program-toc-title">Sessions Overview</div>',
        '<div class="program-toc-hint">(Click a session title to jump to the session details)</div>',
    ]
    for group_label, sessions in groups:
        lines.append(f'<div class="program-toc-day">{esc_html(group_label)}</div>')
        lines.append('<ul>')
        for title, slug in sessions:
            lines.append(f'<li><a href="#{slug}">{esc_html(title)}</a></li>')
        lines.append('</ul>')
    lines.append('</div>')
    return '\n'.join(lines)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

CHILD_TYPES = ('invited_talk', 'oral', 'keynote')


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

    body = []
    toc_days = []

    for day_num, date in enumerate(day_order, 1):
        day_rows = days[date]
        toc_sessions = []

        body.append('')
        body.append(render_day_heading(day_num, date))

        current_session  = None  # (session_row, session_notes_rows) for the open session
        session_children = []    # accumulated invited_talk/oral rows for the open session
        pending_notes    = []    # notes rows attached to whatever comes next

        def flush_session():
            nonlocal current_session
            if current_session is not None:
                sess_row, sess_notes = current_session
                title = sess_row.get('title', '') or ''
                slug = slugify(f'day{day_num}-{title}')
                toc_sessions.append((title, slug))
                body.append('')
                body.append(render_session_table(sess_row, sess_notes, session_children, slug))
            current_session = None
            session_children.clear()

        for row in day_rows:
            rtype = (row.get('type', '') or '').lower()

            if rtype == 'notes':
                pending_notes.append(row)
                continue

            if rtype in CHILD_TYPES:
                session_children.append((row, pending_notes))
            elif rtype == 'session':
                flush_session()
                current_session = (row, pending_notes)
            else:
                flush_session()
                render_standalone(row, pending_notes, body)

            pending_notes = []

        flush_session()
        toc_days.append((f'Day {day_num}: {fmt_day_label(date)}', toc_sessions))

    posters = load_posters(Path(csv_path).parent / 'posters.csv')
    if posters:
        body += render_poster_section(posters)
        toc_days.append(('Posters', [('Poster Session', POSTER_SESSION_SLUG)]))

    out = [FRONT_MATTER, '', render_toc(toc_days), '', TENTATIVE_NOTE] + body
    out.append('')

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'Updated: {md_path}')


if __name__ == '__main__':
    args   = sys.argv[1:]
    csv_in = args[0] if len(args) > 0 else str(SCRIPT_DIR / 'program.csv')
    md_out = args[1] if len(args) > 1 else str(SITE_DIR / 'program.md')
    generate(csv_in, md_out)
