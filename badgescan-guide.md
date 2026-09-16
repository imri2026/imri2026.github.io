---
layout: page
title: Badge Scanner Guide
permalink: /badgescan-guide/
---

Badge Scanner is a free tool for scanning the QR code printed on every attendee badge at the 15th Interventional MRI Symposium. It works right in your phone's browser — no app store, no account, no setup.

<div class="hero-buttons">
<a href="/badgescan/" class="btn">Open Badge Scanner</a>
</div>

- [What It Does](#what-it-does)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [How to Scan](#how-to-scan)
- [Exporting Your Scans](#exporting-your-scans)
- [Privacy & Data](#privacy--data)
- [Troubleshooting](#troubleshooting)

## What It Does

Badge Scanner was created to streamline how vendors obtain attendee contact information at the symposium — legally and with the attendee's explicit consent. Choosing to have your badge scanned is an in-person opt-in, so vendors only collect contacts who chose to share their information with them.

Each attendee badge has a QR code containing that person's name, affiliation, country, and email address. Badge Scanner uses your phone's camera to read the code, saves the information to a running list on your phone, and lets you export that list as a CSV file (opens in Excel, Google Sheets, Numbers, etc.) whenever you're ready.

It's useful for exhibitors collecting leads at their table, and for staff checking in attendees at registration.

## Getting Started

Open **[imri2026.org/badgescan](/badgescan/)** in your phone's browser. For the best experience, add it to your home screen so it launches full-screen like a regular app:

**iPhone (Safari)**
1. Tap the **•••** (more) button next to the address bar — on newer iOS this sits at the bottom of the screen, not in a top toolbar. (If you see a **Share** icon directly instead, tap that.)
2. Tap **Share**, then **Add to Home Screen**.

**Android (Chrome)**
1. Tap the **⋮** menu in the top right.
2. Tap **Add to Home screen** (or **Install app**).

The first time you tap "Start Scanning," your browser will ask for camera permission — allow it.

## Testing

Before you start collecting real contacts, try scanning this sample QR code to see how it works. It's a fictional badge for "Magnetic R. Imaging" of "iMRI Symposium":

<div style="text-align:center;">
<img src="/images/badgescan-example-qr.png" alt="Example badge QR code for testing Badge Scanner" style="max-width:260px; width:100%; height:auto;">
</div>

Once you're comfortable with how a scan looks and behaves, tap the **✕** next to this test entry to remove it before you start scanning real badges.

## How to Scan

1. Tap **Start Scanning** and point the camera at the QR code on the top right of the badge.
2. A confirmation appears and the attendee is added to the list below. Scanning the same badge again shows "Already scanned" instead of adding a duplicate.
3. Tap **Flip Camera** if you need to switch between front and back cameras.
4. Tap the **✕** next to any row to remove it, or **Clear all** to start over — both ask you to confirm first.

## Exporting Your Scans

Tap **Export CSV**. On iPhone/Android this opens the native share sheet, so you can save it to Files, send it by AirDrop, email it to yourself, etc. The CSV includes Name, Affiliation, Country, Email, Scan Time, and the raw QR data for each attendee.

Do this before you're done for the day — see the privacy note below.

## Privacy & Data

Everything is stored locally on your device (in the browser, not on any server) — nothing is uploaded anywhere. This also means:

- Your scanned list **only exists on the phone you scanned with**. It doesn't sync between devices, and multiple people scanning at once each build their own separate list.
- Export the CSV before you clear your browser data for this site, or uninstall it from your home screen, since either one deletes the local list for good.
- As with any badge scan, please only scan a badge with that attendee's knowledge.

## Troubleshooting

- **Camera permission denied**: check your browser's site settings for imri2026.org and allow camera access, then reload the page.
- **Camera won't start / blank preview**: make sure no other app or browser tab is currently using the camera, then try again.
- **QR code won't scan**: hold the phone steady, make sure the badge is well-lit, and get close enough that the code fills a good part of the frame.

Questions? Reach out to [{{ site.email }}](mailto:{{ site.email }}).
