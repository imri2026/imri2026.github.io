(function () {
  const els = {
    exportBtn: document.getElementById("exportBtn"),
    clearBtn: document.getElementById("clearBtn"),
    countLabel: document.getElementById("countLabel"),
    toggleScanBtn: document.getElementById("toggleScanBtn"),
    flipCamBtn: document.getElementById("flipCamBtn"),
    cameraError: document.getElementById("cameraError"),
    scanOverlayMsg: document.getElementById("scanOverlayMsg"),
    toast: document.getElementById("toast"),
    emptyState: document.getElementById("emptyState"),
    scanTable: document.getElementById("scanTable"),
    scanTableBody: document.getElementById("scanTableBody"),
    iosInstallTip: document.getElementById("iosInstallTip"),
  };

  let html5QrCode = null;
  let isScanning = false;
  let facingMode = "environment";
  let toastTimer = null;
  let scanLockUntil = 0;
  const SCAN_LOCK_MS = 2000;

  // ---------- Toast ----------
  function showToast(message, kind) {
    clearTimeout(toastTimer);
    els.toast.textContent = message;
    els.toast.className = "toast" + (kind ? " " + kind : "");
    els.toast.hidden = false;
    toastTimer = setTimeout(() => {
      els.toast.hidden = true;
    }, 2600);
  }

  // ---------- Rendering ----------
  function formatTime(ts) {
    try {
      return new Date(ts).toLocaleString(undefined, {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return "";
    }
  }

  function rowHTML(record) {
    const displayName = record.name || (record.type === "text" ? "(non-vCard QR)" : "(unnamed)");
    return `
      <tr data-id="${record.id}">
        <td class="wrap-cell">${escapeHTML(displayName)}</td>
        <td class="wrap-cell">${escapeHTML(record.affiliation || "")}</td>
        <td>${escapeHTML(record.country || "")}</td>
        <td class="wrap-cell">${escapeHTML(record.email || "")}</td>
        <td>${formatTime(record.scannedAt)}</td>
        <td><button class="row-delete" title="Remove" data-id="${record.id}">✕</button></td>
      </tr>`;
  }

  function escapeHTML(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  let cachedRecords = [];

  async function refreshList() {
    cachedRecords = await ScanDB.getAllScans();
    cachedRecords.sort((a, b) => (b.scannedAt || 0) - (a.scannedAt || 0));

    els.countLabel.textContent = `${cachedRecords.length} scanned`;
    els.exportBtn.disabled = cachedRecords.length === 0;
    els.clearBtn.disabled = cachedRecords.length === 0;

    if (cachedRecords.length === 0) {
      els.emptyState.hidden = false;
      els.scanTable.hidden = true;
      return;
    }
    els.emptyState.hidden = true;
    els.scanTable.hidden = false;
    els.scanTableBody.innerHTML = cachedRecords.map(rowHTML).join("");
  }

  els.scanTableBody.addEventListener("click", async (e) => {
    const btn = e.target.closest(".row-delete");
    if (!btn) return;
    const id = Number(btn.dataset.id);
    const record = cachedRecords.find((r) => r.id === id);
    const label = (record && (record.name || record.email)) || "this attendee";
    if (!confirm(`Remove ${label} from the scanned list?`)) return;
    await ScanDB.deleteScan(id);
    await refreshList();
  });

  els.clearBtn.addEventListener("click", async () => {
    if (cachedRecords.length === 0) return;
    if (!confirm(`Remove all ${cachedRecords.length} scanned attendees? This can't be undone.`)) return;
    await ScanDB.clearAll();
    await refreshList();
    showToast("All scans cleared");
  });

  els.exportBtn.addEventListener("click", async () => {
    if (cachedRecords.length === 0) return;
    els.exportBtn.disabled = true;
    try {
      const result = await CSVUtil.exportCSV(cachedRecords);
      if (result.method !== "cancelled") showToast("CSV exported");
    } catch (err) {
      console.error(err);
      showToast("Export failed: " + err.message, "error");
    } finally {
      els.exportBtn.disabled = cachedRecords.length === 0;
    }
  });

  // ---------- Scanning ----------
  function dedupeKeyFor(parsed) {
    if (parsed.email) return "email:" + parsed.email.trim().toLowerCase();
    return "raw:" + parsed.raw.trim();
  }

  async function onScanSuccess(decodedText) {
    const now = Date.now();
    if (now < scanLockUntil) return;
    scanLockUntil = now + SCAN_LOCK_MS;

    const parsed = VCardUtil.parseScannedText(decodedText);
    const dedupeKey = dedupeKeyFor(parsed);

    try {
      const existing = await ScanDB.findByDedupeKey(dedupeKey);
      if (existing) {
        showToast(`Already scanned: ${existing.name || existing.email || "this code"}`, "warn");
        return;
      }
      const record = {
        ...parsed,
        dedupeKey,
        scannedAt: now,
      };
      await ScanDB.addScan(record);
      await refreshList();
      showToast(`✓ Added ${record.name || record.email || "attendee"}`);
      if (navigator.vibrate) navigator.vibrate(80);
    } catch (err) {
      console.error(err);
      showToast("Couldn't save scan: " + err.message, "error");
    }
  }

  function onScanFailure() {
    // Called continuously while no QR is in frame; intentionally silent.
  }

  async function startScanning() {
    els.cameraError.hidden = true;
    if (!html5QrCode) {
      html5QrCode = new Html5Qrcode("reader", { verbose: false });
    }
    const config = { fps: 10, qrbox: { width: 250, height: 250 }, aspectRatio: 1.0 };
    try {
      await html5QrCode.start({ facingMode }, config, onScanSuccess, onScanFailure);
      isScanning = true;
      els.toggleScanBtn.textContent = "Stop Scanning";
      els.flipCamBtn.hidden = false;
      els.scanOverlayMsg.hidden = true;
    } catch (err) {
      console.error(err);
      isScanning = false;
      els.toggleScanBtn.textContent = "Start Scanning";
      els.cameraError.hidden = false;
      els.cameraError.textContent = describeCameraError(err);
    }
  }

  async function stopScanning() {
    if (html5QrCode && isScanning) {
      try {
        await html5QrCode.stop();
        html5QrCode.clear();
      } catch (err) {
        console.warn("stop() error", err);
      }
    }
    isScanning = false;
    els.toggleScanBtn.textContent = "Start Scanning";
    els.flipCamBtn.hidden = true;
  }

  function describeCameraError(err) {
    const name = err && (err.name || "");
    if (name === "NotAllowedError" || /permission/i.test(String(err))) {
      return "Camera permission denied. Enable camera access for this site in your browser settings, then try again.";
    }
    if (name === "NotFoundError") {
      return "No camera found on this device.";
    }
    if (location.protocol !== "https:" && location.hostname !== "localhost") {
      return "Camera access requires HTTPS. Open this app over a secure (https://) URL.";
    }
    return "Couldn't start the camera: " + (err && err.message ? err.message : String(err));
  }

  els.toggleScanBtn.addEventListener("click", () => {
    if (isScanning) stopScanning();
    else startScanning();
  });

  els.flipCamBtn.addEventListener("click", async () => {
    facingMode = facingMode === "environment" ? "user" : "environment";
    await stopScanning();
    await startScanning();
  });

  // ---------- iOS "Add to Home Screen" tip ----------
  function maybeShowInstallTip() {
    const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
    const isStandalone = window.matchMedia("(display-mode: standalone)").matches || navigator.standalone;
    if (isIOS && !isStandalone) {
      els.iosInstallTip.hidden = false;
    }
  }

  // ---------- Service worker ----------
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("sw.js").catch((err) => console.warn("SW registration failed", err));
    });
  }

  // ---------- Init ----------
  refreshList();
  maybeShowInstallTip();
})();
