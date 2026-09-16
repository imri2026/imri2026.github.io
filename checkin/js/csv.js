/**
 * CSV building + export (download or native share sheet) for scan records.
 */
(function (global) {
  const HEADERS = ["Name", "Affiliation", "Country", "Email", "Scanned At", "Raw QR Data"];

  function csvField(value) {
    const s = value == null ? "" : String(value);
    if (/[",\n\r]/.test(s)) {
      return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
  }

  function toCSV(records) {
    const rows = [HEADERS.map(csvField).join(",")];
    for (const r of records) {
      rows.push(
        [
          r.name || "",
          r.affiliation || "",
          r.country || "",
          r.email || "",
          r.scannedAt ? new Date(r.scannedAt).toISOString() : "",
          r.raw || "",
        ]
          .map(csvField)
          .join(",")
      );
    }
    return rows.join("\r\n");
  }

  function filename() {
    const d = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    return `imri2026-checkin-${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}-${pad(
      d.getHours()
    )}${pad(d.getMinutes())}.csv`;
  }

  async function exportCSV(records) {
    const csv = "﻿" + toCSV(records); // BOM so Excel opens UTF-8 names correctly
    const name = filename();
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });

    // Prefer the native share sheet on mobile (works in installed/standalone
    // PWAs on iOS where plain downloads can silently fail).
    if (global.navigator?.canShare) {
      try {
        const file = new File([blob], name, { type: "text/csv" });
        if (navigator.canShare({ files: [file] })) {
          await navigator.share({ files: [file], title: name });
          return { method: "share" };
        }
      } catch (err) {
        if (err && err.name === "AbortError") return { method: "cancelled" };
        // fall through to download
      }
    }

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 4000);
    return { method: "download" };
  }

  global.CSVUtil = { toCSV, exportCSV };
})(window);
