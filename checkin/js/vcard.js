/**
 * Minimal vCard (2.1/3.0/4.0) parser, good enough for badge QR payloads.
 * Not a full spec implementation, but handles line folding, escaped
 * separators, and the property groups we care about (FN, N, ORG, ADR, EMAIL).
 */
(function (global) {
  function unfold(text) {
    // Continuation lines start with a space or tab (RFC 6350 line folding).
    return text.replace(/\r\n/g, "\n").replace(/\n[ \t]/g, "");
  }

  function unescapeValue(v) {
    let out = "";
    for (let i = 0; i < v.length; i++) {
      if (v[i] === "\\" && i + 1 < v.length) {
        const next = v[i + 1];
        if (next === "n" || next === "N") { out += "\n"; i++; continue; }
        if (next === "," || next === ";" || next === "\\") { out += next; i++; continue; }
        out += next; i++; continue;
      }
      out += v[i];
    }
    return out;
  }

  function splitUnescaped(v, delimiter) {
    const parts = [];
    let cur = "";
    for (let i = 0; i < v.length; i++) {
      if (v[i] === "\\" && i + 1 < v.length) {
        cur += v[i] + v[i + 1];
        i++;
        continue;
      }
      if (v[i] === delimiter) {
        parts.push(cur);
        cur = "";
      } else {
        cur += v[i];
      }
    }
    parts.push(cur);
    return parts;
  }

  function parseLine(line) {
    const colonIdx = line.indexOf(":");
    if (colonIdx === -1) return null;
    const propPart = line.slice(0, colonIdx);
    const value = line.slice(colonIdx + 1);
    const [name, ...params] = propPart.split(";");
    return { name: name.trim().toUpperCase(), params, value };
  }

  function isVCardText(text) {
    return /BEGIN:VCARD/i.test(text || "");
  }

  function parseVCard(text) {
    if (!isVCardText(text)) return null;

    const lines = unfold(text.trim()).split("\n").map((l) => l.trim()).filter(Boolean);
    const result = { fn: "", org: "", email: "", country: "", n: "", tel: "" };

    for (const rawLine of lines) {
      if (/^BEGIN:VCARD$/i.test(rawLine) || /^END:VCARD$/i.test(rawLine) || /^VERSION:/i.test(rawLine)) {
        continue;
      }
      const parsed = parseLine(rawLine);
      if (!parsed) continue;
      const { name, value } = parsed;

      switch (name) {
        case "FN":
          result.fn = unescapeValue(value);
          break;
        case "N":
          result.n = unescapeValue(value);
          break;
        case "ORG":
          result.org = splitUnescaped(value, ";").map(unescapeValue).filter(Boolean).join(", ");
          break;
        case "EMAIL":
          if (!result.email) result.email = unescapeValue(value);
          break;
        case "TEL":
          if (!result.tel) result.tel = unescapeValue(value);
          break;
        case "ADR": {
          // ADR components: PO Box;Extended;Street;Locality;Region;PostalCode;Country
          const parts = splitUnescaped(value, ";").map(unescapeValue);
          const country = parts[6] || "";
          if (country) result.country = country;
          break;
        }
        default:
          break;
      }
    }

    if (!result.fn && result.n) {
      // N format: Last;First;Middle;Prefix;Suffix
      const parts = splitUnescaped(result.n, ";").map(unescapeValue);
      result.fn = [parts[3], parts[1], parts[2], parts[0]].filter(Boolean).join(" ").trim();
    }

    return result;
  }

  /**
   * Parse whatever text came out of the QR code. Returns a normalized
   * record; falls back to storing the raw text if it isn't a vCard.
   */
  function parseScannedText(text) {
    const vcard = parseVCard(text);
    if (vcard) {
      return {
        type: "vcard",
        name: vcard.fn || "",
        affiliation: vcard.org || "",
        country: vcard.country || "",
        email: vcard.email || "",
        raw: text,
      };
    }
    return {
      type: "text",
      name: "",
      affiliation: "",
      country: "",
      email: "",
      raw: text,
    };
  }

  global.VCardUtil = { parseVCard, parseScannedText, isVCardText };
})(window);
