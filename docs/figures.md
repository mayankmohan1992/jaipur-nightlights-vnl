# Jaipur's glow, 2013–2026 — figure provenance

Every number that appears on a slide in this deck, and the table or arithmetic it
came from. The deck itself is `jaipur-nightlights-linkedin.pdf` (10 slides, one per
page) with one PNG per slide in `slides/`.

## Source

- **Instrument**: VIIRS Day/Night Band, NASA/NOAA Suomi-NPP.
- **Product generation**: Earth Observation Group (EOG), Payne Institute for Public
  Policy, Colorado School of Mines.
- **Data products**, accessed through Google Earth Engine:
  - Annual composites **`NOAA/VIIRS/DNB/ANNUAL_V21`** (2013–2021) and
    **`ANNUAL_V22`** (2022–2025) — the annual series.
  - Monthly composites **`NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG`** aggregated to
    January–August for 2026 — the like-for-like current-year figure.
- **Spatial resolution**: ~464 m (15 arc-seconds).
- **Statistic**: **normalised Sum of Lights** — total radiance divided by area, in
  **nW·cm⁻²·sr⁻¹**. Being a mean, it cannot be inflated by area.
- **Lit threshold**: **1.6 nW·cm⁻²·sr⁻¹**, the background-noise
  threshold used in India's own night-lights atlas (NRSC/ISRO).
- **Area of interest**: the Jaipur Development Authority Master Development Plan
  2025 boundary, split into its **17** named planning zones.

### Licence and credit, stated precisely

The brief for this deck described the EOG data as public domain. **EOG's own product
page states otherwise**: *"Many of the VIIRS Nighttime Lights data are available
under Creative Commons Attribution 4.0 International license"*, and asks that the
product generation be credited to the Earth Observation Group, Payne Institute for
Public Policy. The deck therefore carries an attribution line on its first and last
slides rather than a public-domain assertion, and the credit names the Payne
Institute. No licence text is printed on a slide; the accurate position is recorded
here so it cannot be lost. If the deck is republished anywhere the EOG terms (and
the Elvidge et al. citations listed on EOG's page) should be reproduced with it.

## Verification (the brief's cross-check, performed)

Every headline figure was **recomputed from the two CSVs** before use and compared
against the figures stated in the brief:

- **27 checks agree, 0 disagree.**

  No discrepancy remains. **Three did appear on the first pass** and are worth
  recording, because the cause was a method error rather than a data error:

  - `2021→2025 CAGR` came out 9.4%/yr against the brief's 9.5%/yr
  - `ZDP-15` 14-year growth came out 258.6% against the brief's 260%
  - `ZDP-16` came out 211.2% against the brief's 212%

  All three were caused by **rounding each input to 2 dp before computing a
  percentage**. Rounding an input shifts a ratio: ZDP-15's growth is 258.6% from
  rounded inputs and 259.7% from the raw ones. The fix was to keep full precision
  throughout and round **only the outputs**, after which all three agree exactly.
  Every figure on the slides is computed that way.

## Method notes that apply to the whole deck

- **Two series, deliberately.** The annual composite for a year that is not finished
  cannot exist, so 2026 appears only as a **January–August** mean, compared against
  the same eight months in every earlier year. The annual series therefore ends at
  2025 and the like-for-like series at 2026. This deck never compares a partial 2026
  against a full 2025.
- **The record starts in 2013.** There is no 2012 image in this product for this
  area, so the annual series is **13 years** (2013–2025).
- **Zero-based axes.** Every value axis on every chart starts at zero. A truncated
  axis would flatter a +68% change into something it is not.
- **The maps share one clip mask.** The MDP-clipped radiance maps carry an identical
  alpha mask in every year (50.3% transparent, 37.5% opaque, 12.2% anti-aliased),
  so a year-to-year difference on the sequence slide is a change in light, not in
  framing. The transparent background is also why each map is placed on a dark
  panel: composited directly on the ivory slide, the bright core washed out.
- **Saturation is real and is stated, not buried.** Jaipur is already among India's
  brightest cities, so its relative growth is structurally low. India's own
  night-lights atlas names Rajasthan's most-prominent change districts as **Sikar,
  Bharatpur, Karauli and Jhunjhunu — not Jaipur**. Slide 09 says so plainly.

## Input files, pinned

| file | sha256 |
|---|---|
| `ntl_zone_year.csv` | `ec43fe560a30accc8b14c2488e367c9006ed30e52e1e0bb2b8a85ff933e4f7f7` |
| `ntl_zone_ytd.csv` | `3d659d6ad8d94bc78b597f95676aec9ccb76e06650d629aa3d0da7c813c876a1` |
| `_raw_evidence.json` | `6e0221d0b1556800e2c1a4e409ed2fdd5b9c4ba6dcda166056ce58db5b14bda8` |

`ntl_zone_year.csv` carries the annual series per zone plus the MDP-wide mean and lit
fraction; `ntl_zone_ytd.csv` carries the like-for-like January–August series for the
same zones. `_raw_evidence.json` holds the unaggregated values behind both. Nothing
on a slide comes from anywhere else.

---

## Figures, slide by slide

### Slide 01 — Cover

| figure on the slide | value | where it comes from |
|---|---|---|
| +113% (hero) | +112.7% | like-for-like Jan–Aug 2026 ÷ 2013 − 1 |
| 3.50 → 7.44 | 3.50 → 7.44 | `ntl_zone_ytd.csv`, MDP-wide `mdp_mean_radiance`, 2013 and 2026 |
| +68% on the annual record | +68.3% | annual 2025 ÷ 2013 − 1 (`ntl_zone_year.csv`) |
| 9.5%/yr since 2021 | 9.5%/yr | (2025 ÷ 2021)^(1/4) − 1 on the annual series |
| 0.55 → 0.86 of the MDP lit | 0.55 → 0.86 | annual `mdp_lit_fraction`, 2013 and 2025 |

* The hero number is the like-for-like one because that is the figure that includes
* 2026. “More than doubled” is true of it (+112.7%); the annual record alone
* is +68.3%, and is labelled as such on the slide so the two cannot be conflated.

### Slide 02 — Method & source

| figure on the slide | value | where it comes from |
|---|---|---|
| 17 planning zones | 17 | distinct zone labels in both CSVs |
| 1.6 threshold | 1.6 nW·cm⁻²·sr⁻¹ | background-noise threshold, NRSC/ISRO night-lights atlas method |
| 13 years | 2013–2025 | the years present in `ntl_zone_year.csv` |
| 2026 = January–August | 8 months | the window in `ntl_zone_ytd.csv` for 2026 |
| 27 of 27 figures reproduce | 27 / 27 | this document's verification section |

* The method slide also carries the saturation caveat, because a reader who stops
* after slide 02 should already know that a bright city's relative growth is small.

### Slide 03 — Then & now (2013 vs 2026 maps)

| figure on the slide | value | where it comes from |
|---|---|---|
| 3.50 → 7.44 | 3.50 → 7.44 | as slide 01 |
| +113% | +112.7% | as slide 01 |
| 0.55 → 0.86 lit | 0.55 → 0.86 | as slide 01 |
| map panels | ntl_2013.png, ntl_2026_jan_aug.png | MDP-clipped radiance maps supplied with the pack, unmodified |

* Both panels are the same eight-month window on the same colour scale, so the
* difference between them is the change and nothing else.

### Slide 04 — The sequence (2013 / 2017 / 2021 / 2025)

| figure on the slide | value | where it comes from |
|---|---|---|
| map panels | ntl_2013, ntl_2017, ntl_2021, ntl_2025 | annual-composite radiance maps supplied with the pack, unmodified |

* Every panel shares the clip mask verified above, so the four frames register
* pixel-for-pixel.

### Slide 05 — The annual trend

| figure on the slide | value | where it comes from |
|---|---|---|
| 2013 4.53 / 2025 7.62 | 4.53 / 7.62 | annual MDP-wide `mdp_mean_radiance` |
| +68% | +68.3% | 2025 ÷ 2013 − 1 |
| 1.0%/yr (2013–2020) | 1.0%/yr | (2020 ÷ 2013)^(1/7) − 1 |
| 9.5%/yr (2021–2025) | 9.5%/yr | (2025 ÷ 2021)^(1/4) − 1 |
| −2.8% (2020 vs 2019) | -2.8% | annual 2020 ÷ 2019 − 1 |

* The 4.4%/yr figure for the whole 2013–2025 span is in the deck copy, not the
* chart: it is (2025 ÷ 2013)^(1/12) − 1 and it hides the break, which is the point
* the slide makes.

### Slide 06 — Like-for-like January–August

| figure on the slide | value | where it comes from |
|---|---|---|
| 3.50 → 7.44 | 3.50 → 7.44 | `ntl_zone_ytd.csv` |
| +113% | +112.7% | 2026 ÷ 2013 − 1 on the Jan–Aug window |
| +11.2% (2026 vs 2025) | +11.2% | Jan–Aug 2026 ÷ 2025 − 1 |
| 8.9%/yr since 2021 | 8.9%/yr | (2026 ÷ 2021)^(1/5) − 1 on the same window |

* 2026 is drawn as a hollow, dashed-approach point because it is eight months, not
* a year.

### Slide 07 — Lit area

| figure on the slide | value | where it comes from |
|---|---|---|
| 0.55 → 0.86 | 0.55 → 0.86 | annual MDP-wide `mdp_lit_fraction`, 2013 and 2025 |
| 5 brightest zones fully lit in 2013 | yes | annual `lit_fraction` for the five brightest zones in 2013, all ≥ 0.995 |
| least-lit zone ZDP-15 | 0.04 → 0.59 | annual `lit_fraction` for the lowest zone in 2013, and the same zone in 2025 |
| 12 → 17 zones above half lit | 12 → 17 | count of zones with `lit_fraction` ≥ 0.5, 2013 and 2026 |

* The “growth moved to the periphery” claim is arithmetic, not interpretation:
* the brightest zones had no lit-area headroom left in 2013, so any increase in lit
* area is necessarily outside them.

### Slide 08 — By zone — brightest and fastest-growing

| figure on the slide | value | where it comes from |
|---|---|---|
| the eight brightest zones | ZDP-03 35.9, ZDP-04 32.2, ZDP_02 32.1, ZDP-05 28.5, ZDP-01 27.8, ZDP-10 18.9, ZDP-06 17.3, ZDP-08 14.3 | `mean_radiance_jan_aug`, 2026 |
| MDP-wide average | 7.44 | `mdp_mean_radiance`, Jan–Aug 2026 |
| the eight fastest-growing zones | ZDP-15 +260%, ZDP-10 +259%, ZDP-08 +253%, ZDP-09 +237%, ZDP-16 +212%, ZDP-12 +140%, ZDP-14 +134%, ZDP-07 +130% | Jan–Aug 2026 ÷ 2013 − 1, per zone |
| only 2 of 8 appear on both lists | ZDP-08, ZDP-10 | intersection of the two displayed top-8 sets |

* **This figure was wrong on the first pass** and the copy was corrected. The deck
* originally said *“not one appears on both lists”*, which is true at a depth of
* five but false at the depth of eight that the charts actually draw — ZDP-08 and
* ZDP-10 are in both. The overlap is now computed at the displayed depth, asserted
* in `facts.py`, and the copy states it.

### Slide 09 — Honesty — saturation

| figure on the slide | value | where it comes from |
|---|---|---|
| brightest ÷ dimmest zone | 16× | Jan–Aug 2026: ZDP-03 35.9 vs ZDP-11A 2.2 |
| brightest zone growth | +48% | ZDP-03, Jan–Aug 2013 → 2026 |
| fastest zone growth | +260% | ZDP-15, same window |
| named change districts | Sikar, Bharatpur, Karauli, Jhunjhunu | NRSC/ISRO night-lights atlas (published), not computed here |

* The atlas district names are quoted from the published ISRO atlas, which is a
* secondary source for this deck and is labelled as such on the slide.

### Slide 10 — Takeaways

| figure on the slide | value | where it comes from |
|---|---|---|
| 1.0%/yr → 9.5%/yr | 1.0% → 9.5% | as slide 05 |
| +11.2% (2026 vs 2025) | +11.2% | as slide 06 |
| 0.55 → 0.86 | 0.55 → 0.86 | as slide 07 |
| ZDP-15 at +260% | 260% | fastest-growing zone, Jan–Aug 2013 → 2026 |
| about 48% in the brightest zone | 48% | ZDP-03, same window |
| “under a fifth of that” | 18% | brightest zone's growth as a fraction of the fastest zone's |

* The closing ratio was also corrected: an earlier draft said “roughly a third”,
* which the data does not support (48% ÷ 260% = 18%). The value is now computed in
* the build rather than written by hand.

---

## Reproducing this deck

Nothing is fetched and nothing is downloaded at build time: the charts are
hand-rolled SVG from the Python standard library, the maps are embedded as data
URIs, and no font is downloaded (Inter and Noto Serif are used from the system).

    python3 facts.py         # re-derive and check every figure -> facts.json
    bash build_charts.sh     # charts/*.svg, laid out against measured text widths
    python3 build_deck.py    # deck.html, self-contained
    python3 make_sources.py  # this document
    node render.js           # PDF + one PNG per slide + the layout audit
    node ../tools/verify_chart_marks.js deck.html   # no text touches a mark

The last of those is the series legibility rule: **no text may overlap a chart
mark — bar, line, point, area, axis or gridline — nor another piece of text**
(docs/linkedin-series/DESIGN.md §1). It is checked by measuring painted geometry
from the rendered deck, not by eye, and this deck reports **zero** violations
across its 7 charts.
`render.js` checks, and fails the build on: the slide count, that every slide is
exactly 1080×1350 with nothing overflowing or colliding, that every radiance map
panel carries an embedded image, that the source line appears on the first and last
slides only, that no logo element exists, and that the console is silent. It also
reports the vertical balance of each slide, which is what caught three slides that
were technically correct but left a third of the page empty.

