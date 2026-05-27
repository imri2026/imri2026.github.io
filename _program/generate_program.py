#!/usr/bin/env python3
"""
generate_program.py — Build the iMRI 2026 program schedule PDF from a CSV.

Usage:
    python generate_program.py [program.csv] [output.pdf]

Defaults:
    input:  program.csv  (same directory as this script)
    output: iMRI2026-program.pdf  (same directory)

CSV columns:
    date        YYYY-MM-DD
    start       HH:MM (24-hour), empty for notes/placeholder rows
    end         HH:MM (24-hour), empty for notes rows and Adjourn
    type        break | session | invited_talk | keynote | special | social | notes
    title       Primary text shown in the schedule row
    speaker     Presenter name(s)  [optional]
    affiliation Speaker affiliation  [optional]
    status      confirmed | invited | tba  [optional]
    notes       Free-form description printed below the title  [optional]

Dependencies:
    pip install reportlab pillow
"""

import csv
import sys
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
pt = 1.0  # reportlab's internal unit is points
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Table, TableStyle, Paragraph, Spacer, Image, KeepTogether,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ---------------------------------------------------------------------------
# Brand colours (matched to the draft booklet)
# ---------------------------------------------------------------------------
C_DARK   = HexColor('#1F4E79')   # dark navy — header box, col-header bg, accent strip
C_LIGHT  = HexColor('#BDD7EE')   # light steel blue — day-header row bg
C_GOLD   = HexColor('#E8A020')   # gold — thin accent strip, "15th"
C_GRAY_L = HexColor('#F2F2F2')   # light grey — break rows
C_GRAY   = HexColor('#555555')   # body/note text
C_WHITE  = white
C_BLACK  = black

# ---------------------------------------------------------------------------
# Page geometry
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = LETTER          # 8.5 × 11 in
M_LEFT  = 0.55 * inch
M_RIGHT = 0.55 * inch
M_TOP   = 1.05 * inch            # space reserved for the header
M_BOT   = 0.50 * inch

CONTENT_W = PAGE_W - M_LEFT - M_RIGHT

# Schedule table column widths
_W_GOLD  = 5 * pt               # thin gold accent strip
_W_BLUE  = 14 * pt              # dark blue accent strip
_W_START = 36 * pt              # "Start" time
_W_END   = 36 * pt              # "End" time
_W_TITLE = CONTENT_W - _W_GOLD - _W_BLUE - _W_START - _W_END
COL_WIDTHS = [_W_GOLD, _W_BLUE, _W_START, _W_END, _W_TITLE]

SCRIPT_DIR = Path(__file__).parent
SITE_DIR   = SCRIPT_DIR.parent
LOGO_PATH  = str(SITE_DIR / 'images' / 'imri-logo.png')

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
def _S(name, **kw):
    defaults = dict(fontName='Helvetica', fontSize=9, leading=12, textColor=C_BLACK)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

S = {
    'day_hdr':    _S('day_hdr',  fontName='Helvetica-Bold',   fontSize=9,  textColor=C_BLACK),
    'col_hdr':    _S('col_hdr',  fontName='Helvetica-Bold',   fontSize=9,  textColor=C_WHITE),
    'time':       _S('time',     fontName='Helvetica',        fontSize=9,  textColor=C_BLACK),
    'break_t':    _S('break_t',  fontName='Helvetica-Bold',   fontSize=9,  textColor=C_BLACK),
    'session_t':  _S('session_t',fontName='Helvetica-Bold',   fontSize=10, leading=13, textColor=C_BLACK),
    'talk_t':     _S('talk_t',   fontName='Helvetica-Bold',   fontSize=9,  textColor=C_BLACK),
    'speaker':    _S('speaker',  fontName='Helvetica',        fontSize=8.5,leading=11, textColor=C_BLACK),
    'note':       _S('note',     fontName='Helvetica',        fontSize=8.5,leading=11, textColor=C_GRAY),
    'special_t':  _S('special_t',fontName='Helvetica-Bold',   fontSize=9,  textColor=C_BLACK),
    'social_t':   _S('social_t', fontName='Helvetica-Bold',   fontSize=9,  textColor=C_BLACK),
}

def P(text, style):
    return Paragraph(text or '', S[style])

# ---------------------------------------------------------------------------
# Header / footer painted on every page
# ---------------------------------------------------------------------------
HEADER_H = 0.80 * inch

def _draw_header(canvas, doc):
    c = canvas
    c.saveState()

    y_base = PAGE_H - HEADER_H + 4 * pt
    logo_h = 30 * pt
    logo_w = 75 * pt

    # iMRI logo
    try:
        c.drawImage(LOGO_PATH, M_LEFT, y_base,
                    width=logo_w, height=logo_h,
                    preserveAspectRatio=True, anchor='sw', mask='auto')
    except Exception:
        # Fallback text if image not found
        c.setFont('Helvetica-Bold', 16)
        c.setFillColor(C_DARK)
        c.drawString(M_LEFT, y_base + 8 * pt, 'iMRI')

    # Dark blue title box
    box_x = M_LEFT + logo_w + 6 * pt
    box_w = CONTENT_W - logo_w - 6 * pt
    c.setFillColor(C_DARK)
    c.rect(box_x, y_base, box_w, logo_h, fill=1, stroke=0)

    # "15th" in gold
    c.setFillColor(C_GOLD)
    c.setFont('Helvetica-Bold', 17)
    c.drawString(box_x + 8 * pt, y_base + 11 * pt, '15')
    c.setFont('Helvetica-Bold', 10)
    c.drawString(box_x + 29 * pt, y_base + 20 * pt, 'th')

    # "Interventional MRI Symposium"
    c.setFillColor(C_WHITE)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(box_x + 44 * pt, y_base + 14 * pt, 'Interventional MRI Symposium')

    # Sub-line: date + location
    c.setFont('Helvetica', 9)
    c.drawString(box_x + 44 * pt, y_base + 4 * pt, 'October 8–9, 2026, Boston MA')

    # Thin gold rule below header
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(1.5)
    c.line(M_LEFT, y_base - 5 * pt, PAGE_W - M_RIGHT, y_base - 5 * pt)

    # Page number
    c.setFillColor(C_GRAY)
    c.setFont('Helvetica', 9)
    c.drawCentredString(PAGE_W / 2, M_BOT * 0.45, f'– {doc.page} –')

    c.restoreState()


# ---------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------
def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return [{k: v.strip() for k, v in row.items()}
                for row in csv.DictReader(f)]


def fmt_date(date_str):
    """'2026-10-08' → 'THURSDAY, OCTOBER 8, 2026'"""
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d')
        return d.strftime('%A, %B %-d, %Y').upper()
    except ValueError:
        return date_str.upper()


# ---------------------------------------------------------------------------
# Build the schedule table
# ---------------------------------------------------------------------------

def _status_tag(status):
    s = (status or '').lower()
    if s == 'confirmed':
        return ' (<b>Confirmed</b>)'
    if s == 'invited':
        return ' (<b>Invited</b>)'
    if s in ('tba', 'tbd'):
        return ' (<b>TBD</b>)'
    return ''


def _title_cell(row):
    """Return a list of Paragraphs for the Title column."""
    rtype   = (row.get('type', '') or '').lower()
    title   = row.get('title', '') or ''
    speaker = row.get('speaker', '') or ''
    affil   = row.get('affiliation', '') or ''
    status  = row.get('status', '') or ''
    notes   = row.get('notes', '') or ''

    parts = []
    tag = _status_tag(status)

    if rtype == 'break':
        parts.append(P(f'<b>{title}</b>', 'break_t'))

    elif rtype == 'session':
        parts.append(P(f'<b>{title}</b>', 'session_t'))

    elif rtype in ('invited_talk', 'keynote'):
        parts.append(P(f'<b>{title}</b>', 'talk_t'))
        if speaker:
            spk_line = speaker
            if affil:
                spk_line += f', {affil}'
            spk_line += tag
            parts.append(P(spk_line, 'speaker'))

    elif rtype == 'special':
        parts.append(P(f'<b>{title}</b>', 'special_t'))
        if speaker:
            parts.append(P(speaker, 'speaker'))

    elif rtype == 'social':
        parts.append(P(f'<b>{title}</b>', 'social_t'))

    elif rtype == 'notes':
        parts.append(P(title, 'note'))

    else:
        parts.append(P(title, 'talk_t'))

    if notes:
        parts.append(P(notes, 'note'))

    return parts if parts else [P('', 'note')]


def build_schedule_table(csv_rows):
    """Return a reportlab Table representing the full schedule."""
    data = []
    cmds = []
    cur_date = None

    def ri():
        return len(data)

    for row in csv_rows:
        date  = row.get('date', '') or ''
        rtype = (row.get('type', '') or '').lower()
        start = row.get('start', '') or ''
        end   = row.get('end', '') or ''

        # --- Day header + column header when date changes ----------------
        if date and date != cur_date:
            cur_date = date
            r = ri()
            data.append(['', '', Paragraph(fmt_date(date), S['day_hdr']), '', ''])
            cmds += [
                ('SPAN',       (2, r), (4, r)),
                ('BACKGROUND', (0, r), (0, r), C_GOLD),
                ('BACKGROUND', (1, r), (1, r), C_DARK),
                ('BACKGROUND', (2, r), (4, r), C_LIGHT),
                ('TOPPADDING',    (0, r), (-1, r), 4),
                ('BOTTOMPADDING', (0, r), (-1, r), 4),
                ('LEFTPADDING',   (2, r), (2, r),  6),
            ]

            r = ri()
            data.append(['', '',
                         P('Start', 'col_hdr'),
                         P('End',   'col_hdr'),
                         P('Title', 'col_hdr')])
            cmds += [
                ('BACKGROUND', (0, r), (-1, r), C_DARK),
                ('BACKGROUND', (0, r), (0,  r), C_GOLD),
                ('TOPPADDING',    (0, r), (-1, r), 3),
                ('BOTTOMPADDING', (0, r), (-1, r), 3),
                ('LEFTPADDING',   (2, r), (-1, r), 6),
            ]

        # --- Content row -------------------------------------------------
        r = ri()
        title_content = _title_cell(row)
        data.append(['', '',
                     P(start, 'time'),
                     P(end,   'time'),
                     title_content])

        cmds += [
            ('BACKGROUND', (0, r), (0, r), C_GOLD),
            ('BACKGROUND', (1, r), (1, r), C_DARK),
            ('VALIGN',     (0, r), (-1, r), 'TOP'),
            ('TOPPADDING',    (2, r), (-1, r), 4),
            ('BOTTOMPADDING', (2, r), (-1, r), 5),
            ('LEFTPADDING',   (2, r), (3,  r), 6),
            ('LEFTPADDING',   (4, r), (4,  r), 4),
            ('RIGHTPADDING',  (4, r), (4,  r), 6),
        ]

        if rtype == 'break':
            cmds.append(('BACKGROUND', (2, r), (4, r), C_GRAY_L))
        elif rtype == 'notes':
            cmds += [
                ('TOPPADDING',    (2, r), (-1, r), 2),
                ('BOTTOMPADDING', (2, r), (-1, r), 3),
            ]

    # Global table style
    cmds += [
        ('FONT',       (0, 0), (-1, -1), 'Helvetica', 9),
        ('ROWBACKGROUNDS', (2, 0), (4, -1), [C_WHITE, C_WHITE]),  # default white
        ('LINEBELOW',  (0, -1), (-1, -1), 0.5, C_GRAY),
    ]

    tbl = Table(data, colWidths=COL_WIDTHS, repeatRows=0)
    tbl.setStyle(TableStyle(cmds))
    return tbl


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def generate(csv_path, pdf_path):
    csv_rows = load_csv(csv_path)

    doc = BaseDocTemplate(
        pdf_path,
        pagesize=LETTER,
        leftMargin=M_LEFT,
        rightMargin=M_RIGHT,
        topMargin=M_TOP,
        bottomMargin=M_BOT,
        title='iMRI 2026 Program',
        author='15th Interventional MRI Symposium',
    )

    frame = Frame(M_LEFT, M_BOT, CONTENT_W, PAGE_H - M_TOP - M_BOT,
                  leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)

    doc.addPageTemplates([
        PageTemplate(id='schedule', frames=[frame], onPage=_draw_header)
    ])

    tbl = build_schedule_table(csv_rows)
    doc.build([tbl])
    print(f'Generated: {pdf_path}')


if __name__ == '__main__':
    args = sys.argv[1:]
    csv_in  = args[0] if len(args) > 0 else str(SCRIPT_DIR / 'program.csv')
    pdf_out = args[1] if len(args) > 1 else str(SCRIPT_DIR / 'iMRI2026-program.pdf')
    generate(csv_in, pdf_out)
