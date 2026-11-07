# Ethiopia Economic Atlas — 2026 Research Edition

A static, Hostinger-ready, interactive geospatial research website generated from the user's actual version 46 Ethiopia Economic Atlas HTML data (1,198 source records).

## Deploy on Hostinger Web Hosting

1. Download the `ethiopia_atlas_hostinger_site.zip` archive.
2. In Hostinger hPanel, open your website's File Manager and enter `public_html` (or the correct document root for your domain/subdomain).
3. Upload the ZIP and extract it *inside the document root*. Ensure `index.html`, `styles.css`, `app.js`, and `atlas-data.json` are directly in that folder (not nested under an extra directory).
4. Visit the domain with HTTPS. Do not open `index.html` directly from your computer as `file://` blocks the local JSON fetch in most browsers.
5. Replace the founder biography placeholder in `index.html`, and review source permissions and records before public release.

## Live updates vs published data

- The atlas data is a *frozen November 2026 research snapshot*, not continuously refreshed.
- The national indicators use the latest **published World Bank observation** obtained from https://api.worldbank.org/v2/country/ETH/indicator/{code}?format=json and show the observation year. These are *not real-time figures*.
- The age composition doughnut updates from the World Bank if all age groups share a reference year.
- The UN Comtrade top export destination panel is **on-demand** and only renders rankings when a sufficient set of publicly returned records is available. Public preview data may be partial, blocked by browser CORS, or rate-limited; it then shows a source link. For production-grade reliable trade rankings, add a server-side proxy and cache using a Comtrade API subscription, and validate coverage before ranking.
- During network/API failure, statistics show N/A instead of invented values.

## Map

Leaflet 1.9.4 and leaflet.markercluster on actual OpenStreetMap tiles. Many atlas coordinates are regional or city-level placeholders; **do not present them as precise facility locations**. Map marker popups explicitly disclose this. OSM public tiles are reasonable for an initial modest-traffic demonstration subject to their tile usage policy; arrange a dedicated tile provider for significant usage. https://operations.osmfoundation.org/policies/tiles/

## Limitations and development improvements

- This prototype is not yet a tested high-traffic production application, nor a claim to comprehensive or verified business records.
- Exporter rank previews can be incomplete; never turn incomplete previews into definitive rankings.
- Consider a paid MapTiler/Mapbox dark basemap and color-coded map layers in the next version.
- Use a backend caching service if you need resilience or predictable refresh timing for economic APIs.
- Add static sector journeys only where relationships are evidenced, and a contact/corrections form with spam protection if useful.
- Review original data providers' redistribution licenses before offering downloadable `atlas-data.json` to visitors. Remove the download button if rights are unclear.

## File structure

- `index.html` - all website sections and semantic HTML
- `styles.css` - responsive design, dark/futuristic design system
- `app.js` - Leaflet map, dynamic atlas filters, World Bank indicators, trade previews, region comparisons
- `atlas-data.json` - existing atlas records from v46 HTML map

No credentials, paid APIs, databases, or build steps required for the baseline website.
