# LinkedIn post series on Jaipur — research & plan

Status: **plan only, no deck built.** Everything below marked ✅ was verified live during
this research (probe output saved under `research/`); ❓ marks an assumption or something
still to be confirmed; 🔒 marks a source that needs an account or a manual step.

Scope: a series of short LinkedIn decks (≤10 slides each), one aspect of Jaipur per post.
Post 1 is **"Nightlights over the Jaipur MDP — how the city's glow has grown over the
years."**

---

## 0. Headline result

There **is** a public, un-gated, official Indian night-time-lights product covering
Jaipur, and it has a real time series — but its shape is not what I expected:

| what | verdict |
|---|---|
| Bhuvan NGMaps portal serves Night-Time Lights | ❌ **No** — no `night`/`ntl`/`viirs` string anywhere in its code |
| Bhuvan WMS serves an NTL layer | ✅ **Yes** — `ntl:BhuvanNTL` on `vec3wms`, ✳️ **13 annual epochs 2012–2024**, clipping to any bbox works |
| NTL **radiance values** from Bhuvan WMS | ❌ **No** — it returns rendered imagery; GetFeatureInfo gives RGBA, not radiance |
| NTL **statistics** from Bhuvan | ✅ **Yes**, but **state-level only** (Rajasthan ✅, Jaipur district ❌) |
| District-level NTL statistics | ❌ **No** — `getStats.php` ignores a district parameter and returns `[]` |
| NOAA/EOG VIIRS VNL + DMSP-OLS | 🔒 **Yes but login-gated** (free account; redirects to an OpenID login) |
| NASA Black Marble | 🔒 Earthdata/LAADS login; used by NRSC's own atlas as the input |
| Official published method + noise threshold | ✅ In the NRSC NTL Atlas (downloaded, 86 pp) |

**The single most useful discovery:** the state-level series the portal publishes is
**byte-for-byte reproducible and independently cross-validated** — the portal's 2021
value implies +22.0% for 2012→2021, the NRSC Atlas says "approx. 22%"; the portal implies
−10.2% for 2020 vs 2019, the Atlas says "10% decrease"; portal +7.9% for 2021 vs 2020,
Atlas "8% increase". Three independent agreements. That lets post 1 lead with an official
number that can be defended.

**The honesty problem post 1 must confront:** NRSC's own atlas names the Rajasthan
districts with the *most prominent* NTL change — **Sikar, Bharatpur, Karauli, Jhunjhunu**
— and **Jaipur is not among them.** The likely reason is saturation (Jaipur already
starts bright). The post is much stronger if it says that out loud than if it implies
Jaipur is the growth champion.

---

## 1. Bhuvan NGMaps — what it actually is ✅

`https://bhuvan.nrsc.gov.in/ngmaps` is a **Next.js app** (turbopack chunks). I pulled all
20 JS chunks (5.4 MB; kept packed as `research/chunks.tgz`) and searched them.

- **No night-lights content at all.** Searching all 20 chunks (re-verified from the
  packed copy, case-insensitive) the precise evidence is:
  - **`NTL` case-sensitive: 0 occurrences.** `VIIRS`: 0. `DMSP`: 0. `black marble`: 0.
    `luminos`: 0.
  - `night`: 2 hits, both the CSS colour name **`midnightblue`**.
  - `ntl`: 424 hits, all substrings of unrelated JS identifiers — `addEventListener`
    (157), `removeEventListener` (87), `currentLevel` (45), `pointLocation` (15), and so on.
  So a naive case-insensitive grep *looks* like it finds NTL hundreds of times; none of it
  is the product.
- Its API surface is elsewhere: `apiscience/latest_updates` ✅ 200 (returns **HTML**, not
  JSON, despite `content-type: application/json`), `apiscience/getKYRInfo` needs params,
  `apitheme/` and `apiscience/` are **404** (the strings exist in the bundle but the bare
  paths do not resolve).
- Map layers it uses: `vec1wms` `india3`, `cadastral:cadastral_india`, `nb24wms`.
- Also present: `tileserver2`, `tileserver2_api`, `titlier/tiles/WebMercatorQuad/`,
  `predict/get`, `ras2hotspot`, `searchnext`, `districtweights`.

**Conclusion: NGMaps is a general basemap/thematic portal and is not the NTL source.**
The NTL product lives on a separate sub-site (§3).

## 2. The WMS services — what each actually carries ✅

GetCapabilities was fetched from each endpoint named in the brief and saved to
`research/cap_*.xml`:

| endpoint | HTTP | size | layers | NTL layer? |
|---|---|---|---|---|
| `bhuvan-vec1.nrsc.gov.in/bhuvan/gwc/service/wms` | 200 | 2.70 MB | 5,136 | no (`*_ntl` names are admin boundaries: `india_state_bound_lebel_new_ntl`, `admin_group_ntl`, `STATE_BDY_UPD_ForNTL`) |
| `bhuvan.nrsc.gov.in/vec1wms/gwc/service/wms` | 200 | 2.70 MB | 5,136 | same as vec1 (mirror) |
| `bhuvan.nrsc.gov.in/vec3wms/wms/` | 200 | 4.35 MB | 7,151 | ✅ **`ntl:BhuvanNTL`** |
| `bhuvan-vec2.nrsc.gov.in/bhuvan/wbis/wms` | 200 | 240 KB | 29 | no |
| `bhuvan.nrsc.gov.in/nb24wms/gwc/service/wms` | **400** | 419 B | — | no (the URL from the brief rejects GetCapabilities) |

A trap worth recording: the `*_ntl` layer names on vec1 are **not** night lights — the
suffix is internal ("for NTL") on state/admin boundary layers. Only `ntl:BhuvanNTL`
carries lights.

### 2.1 `ntl:BhuvanNTL` — verified behaviour ✅

From the capabilities:

```
Name      ntl:BhuvanNTL
Title     BhuvanNTL
Abstract  "A sample style for rasters"          <- GeoServer default; no product metadata
SRS       EPSG:4326
BBox      68.108, 6.683 -> 97.413, 37.075      <- all India
Style     raster  ("A boring default style")    <- no labelled legend
Dimension (none declared)
```

Verified by request, not by metadata:

- **GetMap works, clipped to any bbox** — a Jaipur-MDP request returns a real RGBA PNG.
  Exact template that I used (reproduce verbatim):

  ```
  https://bhuvan.nrsc.gov.in/vec3wms/wms
    ?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap
    &LAYERS=ntl:BhuvanNTL&STYLES=raster&SRS=EPSG:4326
    &BBOX=75.3676,26.5834,76.0968,27.2764      # Jaipur MDP
    &WIDTH=800&HEIGHT=760&FORMAT=image/png&TRANSPARENT=true
    &TIME=2024-01-01
  ```
  → 200, `image/png`, 48,685 bytes, 800×760 RGBA.

- **A genuine time series.** Different `TIME` values return genuinely different pixels
  (pixel md5 differs per year), and the differences are a clean monotonic trend, not noise.

- **The time axis is exactly 13 annual epochs, 1 January only.** I enumerated 1998–2027:
  2012 ✅ through 2024 ✅, everything else rejected. Non-epoch dates are *not* silently
  ignored — the service returns a WMS exception, which pins it down:

  ```
  <ServiceException code="InvalidDimensionValue" locator="time">
     Could not find a match for 'time' value: '2024-06-01'
  </ServiceException>
  ```
  So: `2012-01-01 … 2024-01-01`, **annual, 13 epochs, no monthlies.** (2011 → invalid;
  2025 → invalid; `2024-01-02` → invalid.) No `TIME` at all returns the 2024 epoch.

- **It is a classified colour map, not a radiance ramp.** The Jaipur render uses discrete
  fills — `#47475F` (dominant, low class), `#F5EBA6`, `#FF0000` (high class), plus a long
  anti-aliased tail (299–364 distinct colours). Class shares over the MDP move
  monotonically 2013→2024 (high-class share 3.11% → 6.67%), which is a real signal.

- **GetFeatureInfo returns RGBA, not radiance** — `RED_BAND 255, GREEN_BAND 0, BLUE_BAND 0,
  ALPHA_BAND 255`, i.e. the *painted colour*. Identical for 2012/2018/2024 at the same
  point because that point is in the top class every year. **The WMS is a visualisation
  service; you cannot recover physical radiance from it.**

- **The advertised WCS is dead.** DescribeLayer points at
  `https://bhuvan.nrsc.gov.in/bhuvan/wcs?` for `ntl:BhuvanNTL`; a DescribeCoverage request
  returns a **404 HTML page**. So no coverage/axis metadata is obtainable that way.

- **No legend.** GetLegendGraphic returns a 20×20 px ramp swatch (337 bytes, 52 colours) —
  an unlabelled colour sample, not a class legend. **The mapping from colour to radiance
  class is undocumented**, which is why §5 recommends not quoting class-area deltas as
  radiance growth.

**Assumed/unknown:** whether the class palette is identical across all 13 years. The
colour sets differ slightly year to year (299→364 distinct values, consistent with
anti-aliasing), and `#F5EBAC` disappears after 2020 — that *may* be a legend change or
may be a class emptying out. ❓ **Treat cross-year colour-class comparison as unproven
until the legend is confirmed.** This is the main caveat on post 1.

## 3. The Bhuvan NTL portal and its APIs ✅ — the real find

The sub-site is `https://bhuvan-app1.nrsc.gov.in/bhuvan_ntl/` (a React/Leaflet app). I
captured its network calls in a real browser (`research/probe_page.js`) and read its
bundle. **All endpoints below are public — no login, no key** ✅:

| endpoint | returns |
|---|---|
| `/bhuvanNTL/get_ntl_years.php` | `[2012,…,2024]` — ✅ matches the WMS epoch list exactly |
| `/bhuvanNTL/getStates.php` | 37 states/UTs |
| `/bhuvanNTL/getDistricts.php?statename=RAJASTHAN` | 33 districts incl. `JAIPUR` |
| `/bhuvanNTL/getStats.php?state=RAJASTHAN` | **13-value yearly series** (see below) |
| `/bhuvanNTL/getIndiaStats.php` | the same series for every state |
| `/bhuvanNTL/district_centroid.php?district=JAIPUR` | `{"centroid_lon":"75.7243097053951","centroid_lat":"26.9804512550603"}` |
| `/bhuvanNTL/state_centroid.php?state=RAJASTHAN` | state centroid |
| `/bhuvanNTL/geometryDistrict.php?state=RAJASTHAN` | ⚠️ returns an **empty** FeatureCollection |

**District statistics do not exist.** `getStats.php` takes only `state=`.
`district=JAIPUR` → `[]`. Districts are used only to recentre the map. So the portal gives
Jaipur a **map** but not a **number**.

### 3.1 The metric, and its unit — quoted from the portal's own code ✅

The chart's y-axis label, read out of `main.js`, is verbatim:

```
Cumulative Radiance/Area(nW.cm⁻².sr⁻¹km⁻²)
```

and the series is named **"Cumulative NTL Radiance"**, computed as
`sum of NTL radiance for region / total area of region`. NRSC's Atlas describes the same
quantity as the **normalised Sum of Lights (SoL)**. I use "normalised Sum of Lights (SoL)"
with the portal's unit string quoted as-is (note the portal writes `km⁻²`, not `km²`).

### 3.2 The Rajasthan series, and the cross-validation ✅

`GET /bhuvanNTL/getStats.php?state=RAJASTHAN` (saved to
`research/bhuvan_ntl_api/getStats.php_state_RAJASTHAN.json`):

| year | Rajasthan | India |
|---|---|---|
| 2012 | 12.42 | 17.52 |
| 2013 | 14.27 | 18.84 |
| 2014 | 16.13 | 20.02 |
| 2015 | 16.52 | 20.68 |
| 2016 | 16.48 | 21.52 |
| 2017 | 14.83 | 22.37 |
| 2018 | 15.57 | 23.49 |
| 2019 | 15.64 | 24.07 |
| 2020 | 14.04 | 22.96 |
| 2021 | 15.15 | 25.08 |
| 2022 | 18.59 | 30.74 |
| 2023 | 21.23 | 35.85 |
| 2024 | 29.20 | 47.34 |

Derived (computed, not asserted):

- Rajasthan **2012 → 2024: +135.1%** (CAGR 7.4%/yr); India **+170.2%**
- Rajasthan **2019 → 2024: +86.7%** (CAGR 13.3%/yr) — a sharp post-2021 acceleration
- **2024 alone: +37.5%** over 2023 — one year responsible for a large share of the decade
- A **dip in 2020** (−10.2% vs 2019) and a flat 2016–2020 plateau
- Rajasthan's share of the India total **falls 70.9% → 61.7%**, i.e. the rest of India is
  brightening faster than Rajasthan

**Cross-check against the published NRSC Atlas ✅ — three independent agreements:**

| interval | portal series implies | Atlas text says |
|---|---|---|
| 2012 → 2021 | **+22.0%** | "Approx. 22% increase observed from 2012 to 2021" |
| 2020 vs 2019 | **−10.2%** | "10% decrease observed in 2020 w.r.t 2019" |
| 2021 vs 2020 | **+7.9%** | "8% increase observed in 2021 w.r.t 2020" |

That is strong evidence the API's six-digit strings are real, correctly-scaled SoL values.

## 4. The official NRSC NTL Atlas ✅

Downloaded: `research/NTL_Atlas.pdf` — 12,296,000 bytes, 86 pages, "Decadal Change of
Night Time Light (NTL) over India from Space (2012 – 2021)", NRSC/ISRO.

Method facts taken verbatim (these belong on the post's method slide):

- Input: **VIIRS/DNB**, **15 arc-second (~500 m)** spatial resolution, **daily / monthly /
  annual** composites, **from January 2012 onwards**.
- Annual composite used for the decadal study; period **2012–2021** in the Atlas
  (the portal and WMS now run to **2024** ✅ — so the API is *newer* than the atlas).
- Statistic: *"Annual normalized Sum Of Lights (SoL) is calculated by aggregating the
  total radiance divided by total geographic area at different administrative units."*
- **Noise threshold:** *"To avoid background noise, the NTL radiance < 1.6 nW.cm⁻².sr⁻¹
  [16 * scale factor (0.1)] are excluded while calculating statistics."* — this is the
  threshold to quote; it is not my invention.
- Data storage: *"Radiance value are unsigned 16 bits (i.e. 0-65535) with 0.1 scale
  factor."*
- Input product: **Black Marble VNP46A4 annual composite**, all-angle snow-free, with the
  quality flag; VNP46A2 geolocation uncertainty 50 m, radiance robustness
  ±0.1 nW.cm⁻².sr⁻¹.
- Rajasthan page (p. 49): *"Approx. 22% increase observed from 2012 to 2021 w.r.t. 2012,
  then 10% decrease observed in 2020 w.r.t 2019 and 8% increase observed in 2021 w.r.t
  2020."*
- Rajasthan "most prominent changes" districts (p. 50): **SIKAR, BHARATPUR, KARAULI,
  JHUNJHUNUN** — **Jaipur is not listed.**

## 5. The Jaipur-clipping question ✅

Already solved inside the repo — no new geometry work needed:

- `data/zones_data.js` (2.7 MB, 17 features, 119,296 coordinate pairs) gives the MDP
  extent directly. I computed it: **W 75.3676, S 26.5834, E 76.0968, N 27.2764**
  (~72 × 77 km), saved to `research/mdp_bbox.json`.
- Bhuvan's Jaipur district centroid is 75.7243, 26.9805 — comfortably inside that bbox ✅,
  so a bbox request and a centroid sanity check agree.
- For a *true* polygon clip (not a bbox), `data/mdp_data.js` (33 MB, the land-use union)
  or `data/zones_data.js` clipped to the 17 zones are both usable as a raster mask.

**Raster clipping tooling is the gap.** This machine has **no rasterio, no GDAL, no PIL,
no numpy** ✅ (checked). Available: `magick`/`convert` (ImageMagick), `ffmpeg`,
`rsvg-convert`, Node, and the vendored Chromium. See §8.

## 6. Authoritative NTL sources — access reality ✅🔒

| product | resolution | years | format | access | Jaipur subset |
|---|---|---|---|---|---|
| **Bhuvan `ntl:BhuvanNTL`** (WMS) | 15 arc-sec source, rendered | **2012–2024, annual (1 Jan), 13 epochs** | PNG (rendered, RGBA) | ✅ **open, no key, no login** | ✅ bbox clip, any size |
| **Bhuvan NTL stats** (portal API) | state aggregate | 2012–2024 | JSON | ✅ open | ❌ state only |
| **VIIRS VNL V2.1** (NOAA/EOG) | 15 arc-sec (~500 m) | annual 2012→present; monthly 2012→present | GeoTIFF (avg_rade9h, cf_cvg, cvg; nW·cm⁻²·sr⁻¹) | 🔒 **login-gated** — `eogdata.mines.edu/nighttime_light/annual/v21/` **302 → OpenID login** at `eogauth.mines.edu` | ✅ ideal, once registered |
| **DMSP-OLS V4** (NOAA/EOG) | 30 arc-sec (~1 km) | **1992–2013** | gzipped tar of GeoTIFF/`.dat` | 🔒 former NGDC direct links now **404**; EOG requires the same account | ✅ but coarse; pre-2012 history only |
| **Black Marble VNP46A2/A4** (NASA) | 15 arc-sec | VNP46A2 daily 2012→; VNP46A4 annual | HDF5 (tiles) | 🔒 Earthdata/LAADS login | ✅ needs HDF5 tooling |
| **NRSC NTL Atlas** | published maps/text | 2012–2021 | PDF | ✅ open (downloaded) | Rajasthan pages only |

Notes:
- **Licence:** EOG states most VIIRS Nighttime Lights data are **CC-BY 4.0** ("cite EOG as
  the data source"); attribution is required. Bhuvan/ISRO data carries NRSC attribution
  terms — ❓ the exact commercial-reuse wording for Bhuvan NTL should be confirmed on the
  Bhuvan data-policy page before a branded post; safe default is "Source: NRSC/ISRO Bhuvan".
- **DMSP-OLS is the only pre-2012 option** and is not comparable to VIIRS (different
  sensor, saturation, no on-board calibration) — NRSC's atlas says the same. ❓ Do **not**
  splice DMSP and VIIRS into one "since 1992" trend line without a calibration note.
- ✅ **There is no India-specific *raw-radiance* NTL product published openly.** What ISRO
  publishes openly is the state-level SoL series and rendered maps. That is enough for a
  credible post if the caveat is stated.

## 7. Post 1 — the method, concretely

**Angle.** "Jaipur's glow, 2012 → 2024" — the official Indian NTL series, clipped to the
Jaipur MDP, with the honest twist that Jaipur is already the bright one.

**Data path A (recommended for the headline number) — official statistics, no gating:**

1. `GET /bhuvanNTL/getStats.php?state=RAJASTHAN` → the 13-value SoL series (§3.2).
2. Recompute the growth figures in Python and confirm they match the Atlas's three stated
   deltas (§3.2). If they ever stop matching, say so on the method slide.
3. Report Rajasthan-level SoL as the quantitative anchor, clearly labelled *state*, with
   Jaipur called out as the dominant city inside it.

**Data path B (recommended for the maps) — the MDP-clipped renders:**

1. For each year in 2012…2024, `GetMap` `ntl:BhuvanNTL` with
   `BBOX=75.3676,26.5834,76.0968,27.2764` at `WIDTH=1000` (≈75 m/px — oversampled versus
   the ~500 m source; request at 2× and downsample, or just accept the smoothing) and a
   fixed PNG size so every year is pixel-registered.
2. Empirical pixel aggregate per year from the decoded PNGs (ImageMagick, since there is no
   PIL/numpy) — mean luminance and the share of "high class" pixels. **Report these as
   *relative* change only**, because the class→radiance legend is undocumented (§2.1).
3. Optional true clip: rasterise `zones_data.js` (17 zones) as an SVG mask, composite with
   ImageMagick, and recompute the same aggregates inside the MDP polygon only.

**Data path C (the upgrade, if the account step is acceptable) 🔒:**

Register a free EOG account, download **VNL V2.1 annual** for 2012–2023 and, if wanted,
VNP46A4. Then real radiance clipped to the MDP with the *official* 1.6 nW·cm⁻²·sr⁻¹
threshold, and — the real prize — **per-ZDP-zone SoL** using the 17 zones the repo already
has, which is what nobody else has published for Jaipur.

**Metrics to publish (in order of defensibility):**
1. ✅ Rajasthan SoL 2012→2024: **+135.1%** (official, cross-validated)
2. ✅ Rajasthan 2019→2024: **+86.7%**; 2024 vs 2023: **+37.5%**
3. ✅ The 2020 dip: **−10.2%**
4. ✅ Rajasthan's falling share of the India total (**70.9% → 61.7%**)
5. ✳️ MDP-clipped rendered change 2012→2024 (relative only, legend caveat stated)
6. ❓ Per-zone SoL for the 17 ZDP zones — needs path C, or an approximation via
   per-zone pixel aggregates from the renders (path B + mask)

**Images the post would show (≤10 slides):**

| # | image | source |
|---|---|---|
| 1 | Cover: "Jaipur's glow, 2012 → 2024" | designed |
| 2 | **Side-by-side MDP night renders, 2012 / 2018 / 2024** | GetMap, path B |
| 3 | 13-frame annual sequence of the MDP (small multiples) | GetMap, path B |
| 4 | **Rajasthan SoL line chart 2012–2024** with the 2020 dip annotated | getStats, path A |
| 5 | Same chart vs India, indexed to 2012 = 100 | getStats |
| 6 | The acceleration: 2012–19 vs 2019–24 CAGR bars (+7.4% vs +13.3%/yr) | computed |
| 7 | Rajasthan's share of the India total, falling | computed |
| 8 | "The growth is elsewhere": NRSC's own prominent-change districts for Rajasthan (Sikar, Bharatpur, Karauli, Jhunjhunu) — Jaipur's absence named honestly | Atlas p. 50 |
| 9 | Method & caveats: VIIRS/DNB 15 arc-sec, annual epochs, 1.6 nW·cm⁻²·sr⁻¹ threshold, legend undocumented, state-level statistics | Atlas + §2.1 |
| 10 | Takeaways | designed |

Slide 6–8 are what make this post more interesting than "lights went up".

## 8. Tooling reality on this machine ✅

- ❌ **No `rasterio`, `GDAL`, `PIL`, `numpy`.** Any plan that assumes `rasterio.mask` or
  `PIL.Image` will fail here.
- ✅ Available: `magick`/`convert` (ImageMagick — can crop, threshold, composite, and
  compute `%[fx:mean]`-style statistics per image), `ffmpeg`, `rsvg-convert`, Node,
  the vendored Chromium (`~/.cache/ms-playwright/chromium-1234/...`) with a working CDP
  harness (`research/probe_page.js`), and `pdftotext`/`pdfinfo`.
- Practical consequence: path B aggregates pixels via ImageMagick; a true polygon clip is
  done by compositing an SVG mask; a Jupyter/rasterio workflow would need an install
  (`pip install rasterio` pulls GDAL — ❓ flag before promising it).

## 9. Proposed series — 8 posts

Each ≤10 slides, same design system as the two existing decks (Pink City palette, rose
`#C1446A` / gold `#E0A34E` / indigo `#1F2A44` / ivory `#F5EDE4`, Noto Serif over Inter,
1080×1350). Two are already built and only need repackaging.

**Post 1 — Nightlights over the Jaipur MDP** *(this plan, §7)*
Data: Bhuvan NTL WMS + portal stats; optionally EOG VNL 🔒.
Charts: MDP renders 2012/2018/2024, Rajasthan SoL line, indexed vs India, CAGR bars,
prominent-districts honesty slide.

**Post 2 — What the MDP is actually used for**
✅ **Already built**: `docs/linkedin-series/land-use/` (12 slides, 17 named planning zones, land-use
mix). Repackage as the series' second post — zero new work.

**Post 3 — What Jaipur's property registrations are worth**
✅ **Already built**: `docs/linkedin-series/property-revenue/` (12 slides, IGRS monthly revenue
2021-04→2026-09). Repackage.

**Post 4 — Five lakh eighty thousand parcels: Jaipur's khasra fabric**
Data: ✅ repo `__KHASRA_PARTS` (598,716 BhuNaksha parcels, georeferenced) + `__KHASRA_INDEX`.
Method: parcel-size distribution, tehsil/village density, largest and smallest holdings.
Charts: parcel-count choropleth by tehsil, parcel-size histogram, top villages.
Angle: the grain of the city nobody sees — the cadastre.

**Post 5 — The RERA pipeline: what's being built, and where**
Data: ✅ repo `__RERA_ANALYSIS` (196 records since 2026-01, with zones/areas) and
`__RERA_LAUNCHES` (79 Group Housing pin centroids, 2026).
Method: units and saleable area by ZDP zone and quarter; promoter mix.
Charts: launches by quarter, units by zone, plot vs built-up area scatter.
Angle: is supply following the plan's zoning, or not?

**Post 6 — Where Jaipur is dense: wards, ULBs and the urban edge**
Data: ✅ repo `__WARDS_DATA` (345 wards / 8 ULBs) + MDP land use; ❓ population by ward
would need a census join (Census 2011 ward data is the only public option — flag the age).
Method: ward area, built-up share per ward, ward count per ULB.
Charts: ward density map, area-vs-built-share scatter.

**Post 7 — The planned road network**
Data: ✅ repo `__MDP_ROADS_DATA` (7,917 planned roads, width + type) and `__TEHSILS_DATA`.
Method: road length and width classes by zone; how much of the plan is road reserve.
Charts: road network map, km by width class, roads vs built-up area by zone.
Angle: the plan reserves more land for roads than for shops, schools and hospitals
combined — already verified in the land-use deck (17,331 ha of Road vs 11,476 + 10,518).

**Post 8 — What the e-auction market says about land prices**
Data: ✅ repo `__EAUCTION_PINS` (80 pins, achieved vs BSP, premium %, precision grade) and
`__SCHEMES_DATA` (2,575 schemes).
Method: premium-over-BSP distribution, unsold vs sold by scheme type (JDA/private/coop).
Charts: premium histogram, map of sold vs unsold, BSP vs achieved by year.
Angle: where the state's own land sales clear, and where they don't.

*(A 9th/10th could be: water bodies and green cover, and "how the city changed, year by
year" off the repo's `__TIMELINE` version store — the latter is only meaningful once a
layer has a second pull.)*

## 10. Files saved under `research/`

| file | what |
|---|---|
| `ngmaps.html` | NGMaps page source |
| `chunks.tgz`, `chunklist.txt` | all 20 NGMaps JS chunks (5.4 MB raw, 1.8 MB packed) — searched, no NTL |
| `cap_vec3wms.xml.gz`, `cap_vec1_bhuvan.xml.gz`, `cap_vec2_wbis.xml.gz` | WMS GetCapabilities (gzipped; raw XML was 2.6–4.2 MB each) |
| `ntl_getmap.png` | 800×760 Jaipur-MDP NTL render (2024 epoch) |
| `ntl_t*.png`, `ntl_probe/*.png` | per-year renders used for the time-series proof |
| `ntl_probe_summary.json` | per-year pixel md5 + high-class share |
| `apiscience_latest_updates.json` | NGMaps science endpoint (HTML, not JSON) |
| `bhuvan_ntl_api/*.json` | years / states / districts / stats / IndiaStats / centroids |
| `wcs_ntl.xml` | the 404 from the advertised WCS |
| `gfi.xml` | GetFeatureInfo output (RGBA only) |
| `legend.png` | unlabelled 20×20 legend swatch |
| `ntl_main_extract.md` | the NTL portal's API surface, call shapes and unit strings, extracted from its 3.0 MB bundle |
| `atlas_full.txt` | text extracted from the official NRSC atlas (86 pp) |
| `provenance.sha256` | sha256 of the two large originals that were trimmed |
| `mdp_bbox.json` | MDP bbox computed from `data/zones_data.js` |
| `probe_page.js` | CDP page/network prober used throughout |

Two large downloads were **trimmed after extraction rather than vendored**, so this
directory is 2.8 MB instead of 28 MB: the 12 MB ISRO atlas PDF (text kept in
`atlas_full.txt`, URL recorded in §4) is not re-hosted in git, and the minified JS
bundles are kept packed plus as readable extracts. `provenance.sha256` records the
sha256 of both originals so the evidence chain is intact either way.

## 11. Manual steps / accounts / open questions

🔒 **Needs a free account (not doable unattended):**
1. NOAA/EOG registration for VIIRS VNL V2.1 (and DMSP-OLS) — required before any real
   radiance download. Without it, post 1 must lean on the Bhuvan renders + Rajasthan SoL.
2. NASA Earthdata login for Black Marble VNP46A2/A4 (only if you want daily/monthly).

❓ **Open / to confirm before publishing:**
1. **The class legend of `ntl:BhuvanNTL`.** Unresolved; it decides whether path B can claim
   radiance growth or only relative change. Could be chased via the Bhuvan forum, a
   `GetMetadata`/SLD request, or by emailing NRSC.
2. **Whether the palette is stable across all 13 epochs** (§2.1) — the `#F5EBAC`
   disappearance after 2020 needs explaining before any colour-class delta is published.
3. **Bhuvan's NTL licence/reuse terms** for a branded post.
4. **Whether `getStats.php` has an undocumented district/bbox variant.** The bundle shows
   only `state=`; the app never asks for less. Low probability, high value.
5. **Saturation.** Jaipur is already among India's brightest urban areas, so its *relative*
   SoL growth should be structurally lower than a dark district's. The post should say this
   rather than let the reader infer Jaipur is lagging.
6. **Census population by ward** — only 2011 is public; ❓ flag the age if post 6 uses it.

## 12. Recommendation

Build post 1 from **path A + path B** now: it needs no account, every number is official,
and the state series is triple-validated against a published ISRO document. Lead with the
honest framing — *Jaipur is the bright one; Rajasthan's fastest glow-up is in the smaller
districts* — and put the legend/saturation caveats on the method slide.

Then take the EOG account (one manual step) and rebuild post 1 with real radiance and
**per-ZDP-zone SoL**, which is a genuinely novel cut: nobody has published night-lights
statistics for the 17 Jaipur planning zones.
