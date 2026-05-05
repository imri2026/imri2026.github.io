---
layout: page
title: Alternative Hotel Options
permalink: /hotels/
---

We assembled a list of affordable hotel options. The conference venue is steps from the **Charles/MGH station** on the MBTA Red Line, and the hotels on this list are accessible from the venue by walk or using the public transit. October is peak season in Boston — we recommend booking early.

> **Disclaimer:** The hotels listed below are suggestions for your convenience only and are not affiliated with, endorsed by, or sponsored by the 15th Interventional MRI Symposium or its organizers.

| Hotel | Location | Nearest T Stop | Route to Charles/MGH |
|-------|----------|----------------|----------------------|
| [Wyndham Boston Beacon Hill](https://www.wyndhamhotels.com/wyndham/boston-massachusetts/wyndham-boston-beacon-hill/overview) | Beacon Hill | Charles/MGH (Red Line, at hotel) | Walk directly, ~3 min |
| [Omni Parker House](https://www.omnihotels.com/hotels/boston-parker-house) | Downtown | Park Street (Red Line, 3 min walk) | Red Line → Charles/MGH, ~10 min |
| [The Godfrey Hotel](https://www.godfreyhotelboston.com) | Downtown | Downtown Crossing (Red Line, 2 min walk) | Red Line → Charles/MGH, ~12 min |
| [Porter Square Hotel](https://www.theportersquarehotel.com) | Cambridge | Porter Square (Red Line, at hotel) | Direct Red Line, ~15 min, no transfer |
| [Hotel Ivy Boston Common](https://www.hotelivyboston.com) | Theatre District | Boylston (Green Line, 1 block) | Green Line → Park Street → Red Line, ~15 min |
| [Holiday Inn Express & Suites Boston-Cambridge](https://www.ihg.com/holidayinnexpress/hotels/us/en/cambridge/boscb/hoteldetail) | Cambridge | Lechmere (Green Line, 5 min walk) | Green Line → Park Street → Red Line, ~20 min |
| [Hampton Inn Boston/Cambridge](https://www.hilton.com/en/hotels/boscahx-hampton-boston-cambridge/) | Cambridge | Lechmere (Green Line, 5 min walk) | Green Line → Park Street → Red Line, ~20 min |
| [Eurostars The Boxer](https://www.eurostarshotels.us/eurostars-the-boxer.html) | West End | North Station (Green Line, 2 min walk) | Green Line → Park Street → Red Line, ~20 min |
| [citizenM Boston North Station](https://www.citizenm.com/hotels/united-states/boston/boston-north-station-hotel/) | West End | North Station (Green Line, 2 min walk) | Green Line → Park Street → Red Line, ~20 min |
| [YOTEL Boston](https://www.yotel.com/en/hotels/yotel-boston) | Seaport | Courthouse (Silver Line, 5 min walk) | Silver Line → South Station → Red Line, ~25 min |
| [The Midtown Hotel MOD Collection by Sonesta](https://www.midtownhotel.com) | Back Bay | Symphony (Green Line E, 5 min walk) | Green Line → Park Street → Red Line, ~25 min |
| [La Quinta Inn & Suites Boston/Somerville](https://www.wyndhamhotels.com/laquinta/somerville-massachusetts/la-quinta-boston-somerville/overview) | Somerville | Sullivan Square (Orange Line, 10 min walk) | Orange Line → Downtown Crossing → Red Line, ~30 min |

> We recommend checking booking sites such as [Expedia](https://www.expedia.com), [Hotels.com](https://www.hotels.com), or [Booking.com](https://www.booking.com) for availability and current rates.

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<div id="hotel-map" style="height: 500px; width: 100%; margin: 1.5em 0; border-radius: 4px; border: 1px solid #ddd;"></div>
<script>
(function () {
  var map = L.map('hotel-map');
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18
  }).addTo(map);

  var venueStyle = { radius: 11, fillColor: '#c0392b', color: '#fff', weight: 2.5, opacity: 1, fillOpacity: 0.95 };
  var hotelStyle = { radius: 8,  fillColor: '#2471a3', color: '#fff', weight: 2,   opacity: 1, fillOpacity: 0.9  };

  var markers = [];

  function pin(lat, lng, style, title, detail) {
    var m = L.circleMarker([lat, lng], style).addTo(map)
      .bindPopup('<strong>' + title + '</strong><br><small>' + detail + '</small>');
    markers.push(m);
  }

  pin(42.3614, -71.0681, venueStyle, '&#9733; The Liberty Hotel (Conference Venue)', '215 Charles St, Boston — Charles/MGH (Red Line)');
  pin(42.3625, -71.0706, hotelStyle, 'Wyndham Boston Beacon Hill', 'Charles/MGH (Red Line, at hotel) — walk directly, ~3 min');
  pin(42.3574, -71.0601, hotelStyle, 'Omni Parker House', 'Park Street (Red Line, 3 min walk) — ~10 min to Charles/MGH');
  pin(42.3551, -71.0613, hotelStyle, 'The Godfrey Hotel', 'Downtown Crossing (Red Line, 2 min walk) — ~12 min to Charles/MGH');
  pin(42.3664, -71.0621, hotelStyle, 'citizenM Boston North Station', 'North Station (Green Line, 2 min walk) — ~20 min to Charles/MGH');
  pin(42.3694, -71.0800, hotelStyle, 'Holiday Inn Express &amp; Suites Boston-Cambridge', 'Lechmere (Green Line, 5 min walk)');
  pin(42.3880, -71.1191, hotelStyle, 'Porter Square Hotel', 'Porter Square (Red Line, at hotel)');
  pin(42.3521, -71.0634, hotelStyle, 'Hotel Ivy Boston Common', 'Boylston (Green Line, 1 block)');
  pin(42.3706, -71.0762, hotelStyle, 'Hampton Inn Boston/Cambridge', 'Lechmere (Green Line, 5 min walk)');
  pin(42.3641, -71.0593, hotelStyle, 'Eurostars The Boxer', 'North Station (Green Line, 2 min walk)');
  pin(42.3490, -71.0445, hotelStyle, 'YOTEL Boston', 'Courthouse (Silver Line, 5 min walk)');
  pin(42.3441, -71.0869, hotelStyle, 'The Midtown Hotel MOD Collection by Sonesta', 'Symphony (Green Line E, 5 min walk)');
  pin(42.3857, -71.0990, hotelStyle, 'La Quinta Inn &amp; Suites Boston/Somerville', 'Sullivan Square (Orange Line, 10 min walk)');

  var group = new L.featureGroup(markers);
  map.fitBounds(group.getBounds().pad(0.12));

  function decodePolyline(str) {
    var index = 0, lat = 0, lng = 0, result = [];
    while (index < str.length) {
      var b, shift = 0, res = 0;
      do { b = str.charCodeAt(index++) - 63; res |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
      lat += (res & 1) ? ~(res >> 1) : (res >> 1);
      shift = res = 0;
      do { b = str.charCodeAt(index++) - 63; res |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
      lng += (res & 1) ? ~(res >> 1) : (res >> 1);
      result.push([lat / 1e5, lng / 1e5]);
    }
    return result;
  }

  function addMBTALine(routeIds, color, idPattern) {
    var re = new RegExp(idPattern);
    return fetch('https://api-v3.mbta.com/shapes?filter%5Broute%5D=' + routeIds)
      .then(function(r) { return r.json(); })
      .then(function(data) {
        data.data.filter(function(s) { return re.test(s.id); })
          .forEach(function(shape) {
            L.polyline(decodePolyline(shape.attributes.polyline), {
              color: color, weight: 3, opacity: 0.7, interactive: false
            }).addTo(map);
          });
      })
      .catch(function() { console.warn('Could not load MBTA line:', routeIds); });
  }

  Promise.all([
    addMBTALine('Red', '#DA291C', '^canonical-933_'),
    addMBTALine('Green-B,Green-C,Green-D,Green-E', '#00843D', '^canonical-'),
    addMBTALine('Orange', '#ED8B00', '^canonical-')
  ]).then(function() {
    markers.forEach(function(m) { m.bringToFront(); });
  });

  var legend = L.control({ position: 'bottomright' });
  legend.onAdd = function () {
    var div = L.DomUtil.create('div');
    div.style.cssText = 'background:white;padding:8px 12px;border-radius:4px;border:1px solid #ccc;font-size:13px;line-height:2;';
    div.innerHTML =
      '<svg width="12" height="12" style="vertical-align:middle"><circle cx="6" cy="6" r="6" fill="#c0392b"/></svg> Conference Venue<br>' +
      '<svg width="12" height="12" style="vertical-align:middle"><circle cx="6" cy="6" r="6" fill="#2471a3"/></svg> Suggested Hotel<br>' +
      '<svg width="24" height="12" style="vertical-align:middle"><line x1="0" y1="6" x2="24" y2="6" stroke="#DA291C" stroke-width="3"/></svg> Red Line<br>' +
      '<svg width="24" height="12" style="vertical-align:middle"><line x1="0" y1="6" x2="24" y2="6" stroke="#00843D" stroke-width="3"/></svg> Green Line<br>' +
      '<svg width="24" height="12" style="vertical-align:middle"><line x1="0" y1="6" x2="24" y2="6" stroke="#ED8B00" stroke-width="3"/></svg> Orange Line';
    return div;
  };
  legend.addTo(map);
})();
</script>
