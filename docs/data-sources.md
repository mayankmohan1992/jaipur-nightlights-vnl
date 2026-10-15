# Data sources

## The instrument and the product

| | |
|---|---|
| **Sensor** | VIIRS Day/Night Band (DNB), aboard NASA/NOAA **Suomi-NPP** |
| **Product maker** | Earth Observation Group (EOG), Payne Institute for Public Policy, Colorado School of Mines |
| **Nominal resolution** | ~15 arc-seconds — **~464 m** at Jaipur's latitude |
| **Unit** | nanoWatts · cm⁻² · sr⁻¹ (nW·cm⁻²·sr⁻¹) |
| **Access route** | **Google Earth Engine** (server-side zonal statistics; no raster downloads) |

VIIRS measures **radiance** — how much light is leaving the ground — not "built-up
area". A pixel can be bright for a streetlight, a lit highway or a factory yard.

## The three datasets used

| GEE asset | Role | Coverage used |
|---|---|---|
| `NOAA/VIIRS/DNB/ANNUAL_V21` | annual composite, band `average` | 2013 – 2021 |
| `NOAA/VIIRS/DNB/ANNUAL_V22` | annual composite, band `average` | 2022 – 2025 |
| `NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG` | monthly composite, band `avg_rad` | Jan–Aug 2013 – 2026 |

The two annual collections are **merged** (`ANNUAL_V21.merge(ANNUAL_V22)`) and the
`average` band is selected, so one code path serves 2013–2025.

**There is no 2012 image for this area in the product**, so the record starts in
2013 — 13 annual years. **The annual composite for 2026 cannot exist** (the year is
not finished), which is why 2026 appears only in the Jan–Aug series.

## The two statistics

### Mean radiance = normalised Sum of Lights

```
mean_radiance(zone, year) = Σ radiance of the zone's pixels ÷ number of pixels
```

That is a plain `ee.Reducer.mean()` over the zone at the product's native scale
(`scale=463.83` m). Dividing by area is what makes it a **normalised** Sum of
Lights, and being a mean it cannot be inflated by a larger zone.

### Lit fraction

```
lit = image.gte(1.6)                              # a boolean band
lit_fraction(zone, year) = mean(lit) over the zone
```

**1.6 nW·cm⁻²·sr⁻¹** is the background-noise threshold used by India's own
night-lights atlas (NRSC/ISRO) — i.e. everything below it is treated as unlit
ground, not as faint development. Using the atlas's own threshold means the
figure is comparable with published Indian work rather than being our invention.

## The area of interest

The 17 **ZDP planning zones** of the **JDA Master Development Plan 2025**, taken
from the viewer's baked `zones_data.js` (`window.__ZONES_DATA`, produced by the
same JDA land-use layer documented in the companion land-use repository). Each
zone is reduced independently, and the MDP as a whole is reduced separately with
`reduceRegion(..., maxPixels=1e10, bestEffort=True)`.

## Licence and credit — corrected

The deck's original brief called the EOG data **public domain**. EOG's own product
page says otherwise:

> *"Many of the VIIRS Nighttime Lights data are available under Creative Commons
> Attribution 4.0 International license"* — and asks that product generation be
> credited to the Earth Observation Group, Payne Institute for Public Policy.

So the data are **CC-BY 4.0**: free to use, **attribution required**. The deck
carries the credit on its first and last slides. The citations EOG lists
(Elvidge et al. 2021, doi:10.3390/rs13050922) should travel with any reuse.

DMSP-OLS, the older night-lights series (1992–2013), is **a different instrument
with a different calibration** and is deliberately not used or spliced here.

## Environments

| Requirement | Note |
|---|---|
| `earthengine-api` | `pip install earthengine-api` |
| Earth Engine access | register at <https://console.cloud.google.com/earth-engine> and note the **project id** |
| Authenticate | `earthengine authenticate` (interactive), or a service-account JSON |
| Set the project | `export EE_PROJECT=<project id>` — `ee.Initialize(project=…)` needs it |
| `make_maps.py` | uses `ee.Image.getThumbURL` — no Drive or export task needed |

No raster files are downloaded at any point; the only network calls are to the
Earth Engine API and to the thumbnail URLs it returns.
