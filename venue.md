---
layout: page
title: Venue & Travel Information
permalink: /venue/
---

## Symposium Venue

### The Liberty Hotel

- **Address**: 215 Charles St, Boston, MA 02114
- **Tel**: +1 617-224-4000
- [Hotel website](https://www.marriott.com/en-us/hotels/boslc-the-liberty-a-luxury-collection-hotel-boston/overview/)

### About The Venue
**The 15th Interventional MRI Symposium (iMRI)** will be held at The Liberty Hotel in Downtown Boston. Located in Beacon Hill, a historic district known for its picturesque residential streets and landmarks such as the Massachusetts State House and Boston Common, the hotel sits adjacent to the main campus of Massachusetts General Hospital. With excellent access from Boston Logan Airport, South Station, Interstate 90/93, and US Route 1, it's an ideal location for this international medical conference.

The Liberty Hotel is also renowned for its unique history and stunning architecture. Originally built as the Charles Street Jail in 1851, it housed notable inmates including Malcolm X and former Boston Mayor James Michael Curley. After closing as a jail in 1990, the building was transformed into a luxury hotel in 2007. The property beautifully preserves many original architectural features, offering guests an inspiring experience and providing a unique setting for conferences like iMRI.

### Hotel Reservation

A special room rate will be available for registered attendees. We will communicate the details directly to those who register. Please note that the availability of rooms with the special rate is limited.

## Suggested Hotels

The conference venue is steps from the **Charles/MGH station** on the MBTA Red Line. The hotels below are along the Red Line and Green Line corridors with good transit access to the venue. October is peak season in Boston — we recommend booking early.

| Hotel | Location | Nearest T Stop | Route to Charles/MGH |
|-------|----------|----------------|----------------------|
| [Holiday Inn Express & Suites Boston-Cambridge](https://www.ihg.com/holidayinnexpress/hotels/us/en/cambridge/boscb/hoteldetail) | Cambridge | Lechmere (Green Line, 5 min walk) | Green Line → Park Street → Red Line, ~20 min |
| [Porter Square Hotel](https://www.theportersquarehotel.com) | Cambridge | Porter Square (Red Line, at hotel) | Direct Red Line, ~15 min, no transfer |
| [Hotel Ivy Boston Common](https://www.hotelivyboston.com) | Theatre District | Boylston (Green Line, 1 block) | Green Line → Park Street → Red Line, ~15 min |
| [Hampton Inn Boston/Cambridge](https://www.hilton.com/en/hotels/boscahx-hampton-boston-cambridge/) | Cambridge | Lechmere (Green Line, 5 min walk) | Green Line → Park Street → Red Line, ~20 min |
| [Eurostars The Boxer](https://www.eurostarshotels.us/eurostars-the-boxer.html) | West End | North Station (Green Line, 2 min walk) | Green Line → Park Street → Red Line, ~20 min |
| [YOTEL Boston](https://www.yotel.com/en/hotels/yotel-boston) | Seaport | Courthouse (Silver Line, 5 min walk) | Silver Line → South Station → Red Line, ~25 min |
| [The Midtown Hotel MOD Collection by Sonesta](https://www.midtownhotel.com) | Back Bay | Symphony (Green Line E, 5 min walk) | Green Line → Park Street → Red Line, ~25 min |
| [Hampton Inn Boston/Braintree](https://www.hilton.com/en/hotels/bosbrhx-hampton-boston-braintree/) | Braintree | Braintree (Red Line, shuttle) | Direct Red Line, ~35 min, no transfer |
| [La Quinta Inn & Suites Boston/Somerville](https://www.wyndhamhotels.com/laquinta/somerville-massachusetts/la-quinta-boston-somerville/overview) | Somerville | Sullivan Square (Orange Line, 10 min walk) | Orange Line → Downtown Crossing → Red Line, ~30 min |

> **Note:** A limited number of rooms at The Liberty Hotel will be available at a special conference rate for registered attendees. Details will be communicated after registration.
>
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
  pin(42.3694, -71.0800, hotelStyle, 'Holiday Inn Express &amp; Suites Boston-Cambridge', 'Lechmere (Green Line, 5 min walk)');
  pin(42.3880, -71.1191, hotelStyle, 'Porter Square Hotel', 'Porter Square (Red Line, at hotel)');
  pin(42.3521, -71.0634, hotelStyle, 'Hotel Ivy Boston Common', 'Boylston (Green Line, 1 block)');
  pin(42.3706, -71.0762, hotelStyle, 'Hampton Inn Boston/Cambridge', 'Lechmere (Green Line, 5 min walk)');
  pin(42.3641, -71.0593, hotelStyle, 'Eurostars The Boxer', 'North Station (Green Line, 2 min walk)');
  pin(42.3490, -71.0445, hotelStyle, 'YOTEL Boston', 'Courthouse (Silver Line, 5 min walk)');
  pin(42.3441, -71.0869, hotelStyle, 'The Midtown Hotel MOD Collection by Sonesta', 'Symphony (Green Line E, 5 min walk)');
  pin(42.2073, -71.0012, hotelStyle, 'Hampton Inn Boston/Braintree', 'Braintree (Red Line terminal, shuttle)');
  pin(42.3857, -71.0990, hotelStyle, 'La Quinta Inn &amp; Suites Boston/Somerville', 'Sullivan Square (Orange Line, 10 min walk)');

  var group = new L.featureGroup(markers);
  map.fitBounds(group.getBounds().pad(0.12));

  var legend = L.control({ position: 'bottomright' });
  legend.onAdd = function () {
    var div = L.DomUtil.create('div');
    div.style.cssText = 'background:white;padding:8px 12px;border-radius:4px;border:1px solid #ccc;font-size:13px;line-height:2;';
    div.innerHTML =
      '<svg width="12" height="12" style="vertical-align:middle"><circle cx="6" cy="6" r="6" fill="#c0392b"/></svg> Conference Venue<br>' +
      '<svg width="12" height="12" style="vertical-align:middle"><circle cx="6" cy="6" r="6" fill="#2471a3"/></svg> Suggested Hotel';
    return div;
  };
  legend.addTo(map);
})();
</script>

## Visa Information

International attendees may require a visa to enter the United States. We recommend checking the [U.S. Department of State website](https://travel.state.gov/content/travel/en/us-visas.html) for visa requirements based on your country of citizenship.

Upon registration, we can provide a letter of invitation to assist with your visa application. Please contact us at [{{ site.email }}](mailto:{{ site.email }}) with your registration confirmation and passport details.

## Local Attractions

Boston offers numerous historical and cultural attractions for visitors:

- Museums
  - [Museum of Fine Arts Boston](https://www.mfa.org)
  - [Isabella Stewart Gardner Museum](https://www.gardnermuseum.org)
  - [Institute of Contemporary Art / Boston](https://www.icaboston.org)
  - [Museum of Science](https://www.mos.org)
  - [USS Constitution Museum](https://ussconstitutionmuseum.org)
  - [Harvard Museum of Natural History](https://www.hmnh.harvard.edu)
  - [MIT Museum](https://mitmuseum.mit.edu)
  - [Museum of Medical History and Innovation](https://www.massgeneral.org/museum)
  - [Boston Tea Party Ships & Museum](https://www.bostonteapartyship.com)
- Music
  - [Boston Symphony Orchestra](https://www.bso.org)
  - [Boston Ballet](https://www.bostonballet.org/)
  
- Sports
  - [Fenway Park](https://www.mlb.com/redsox/ballpark)
  - [TD Garden](https://www.tdgarden.com)
- Walking
  - [Freedom Trail](https://www.thefreedomtrail.org)
  - [Boston Common and Public Garden](https://www.boston.gov/parks/public-garden)
  - [Charles River](https://www.mass.gov/locations/charles-river-reservation)
  - [Quincy Market](https://www.quincy-market.com)
- Campuses
  - [Harvard University](https://www.harvard.edu)
  - [Massachusetts Institute of Technology](https://www.mit.edu)


