# Jaipur night-lights, 2013–2026

How the *“Jaipur's glow has more than doubled since 2013”* deck was built: the
satellite product behind it, every computation, the two series that must never be
confused, and the caveats — including the one that argues *against* the headline.

**Instrument:** VIIRS Day/Night Band (NASA/NOAA Suomi-NPP).
**Product generation:** Earth Observation Group (EOG), Payne Institute for Public
Policy, Colorado School of Mines.
**Data access:** Google Earth Engine — *no raster downloads*; all zonal statistics
are computed server-side.
**Area of interest:** the Jaipur Development Authority **MDP 2025 boundary**, split
into its **17** named planning zones.

| | |
|---|---|
| [`deck/jaipur-nightlights-linkedin.pdf`](deck/) | the 10-slide deck (PDF; one PNG per slide in `deck/slides/`) |
| [`data/`](data/) | the two result tables and the raw GEE responses behind them |
| [`maps/`](maps/) | 14 MDP-clipped radiance renders (one per year, 2013–2025 + 2026 Jan–Aug) |
| [`scripts/`](scripts/) | the Earth Engine pipeline and the map renderer |
| [`docs/method.md`](docs/method.md) | every calculation, step by step |
| [`docs/data-sources.md`](docs/data-sources.md) | the datasets, the threshold, the licence |
| [`docs/caveats.md`](docs/caveats.md) | saturation, series splicing, and what the deck refuses to claim |
| [`docs/figures.md`](docs/figures.md) | every figure traced to its table, slide by slide |

---

## Headline figures

| | 2013 | latest | change |
|---|---:|---:|---:|
| Mean radiance over the MDP — **like-for-like Jan–Aug** | 3.50 | **7.44** (2026) | **+113 %** |
| Mean radiance over the MDP — **full calendar years** | 4.53 | **7.62** (2025) | **+68 %** |
| Share of the MDP above the 1.6 threshold (lit) | 0.55 | 0.86 (2025) | +56 % |

- **2013–2020: +1.0 %/yr** — essentially flat.
- **2021–2025: +9.5 %/yr** — a step change.
- **2026 Jan–Aug vs 2025 Jan–Aug: +11.2 %.**

The deck leads with the **like-for-like** figure (+113 %) because it is the only
one that includes 2026, and labels the annual figure (+68 %) separately so the two
cannot be conflated. See [`docs/method.md`](docs/method.md#why-there-are-two-series).

## The measure

**Normalised Sum of Lights** — the mean radiance over an area, in
**nW·cm⁻²·sr⁻¹**. Being a mean, it cannot be inflated by area, and it is the
statistic used by India's own night-lights atlas (NRSC/ISRO). The **lit**
statistic is the share of pixels at or above **1.6 nW·cm⁻²·sr⁻¹**, that atlas's
background-noise threshold.

## Reproduce it

```bash
pip install earthengine-api
earthengine authenticate
export EE_PROJECT=<your-google-cloud-project>
python3 scripts/gee_nightlights.py     # -> data/ntl_zone_year.csv, ntl_zone_ytd.csv, _raw_evidence.json
python3 scripts/make_maps.py           # -> maps/ntl_*.png
```

Both tables are committed, so every figure can be checked without any setup.

## The caveat the deck states about itself

**Jaipur is already one of India's brightest cities, so its *relative* growth is
structurally low** — a dark district can double its radiance far more easily. By
India's own night-lights atlas, the most prominent change districts in Rajasthan
are **Sikar, Bharatpur, Karauli and Jhunjhunu — not Jaipur**. The deck says this
plainly on its method slide and its honesty slide rather than letting a +113 %
headline imply otherwise.

## Attribution

EOG VIIRS night-time lights are licensed **CC-BY 4.0** and EOG asks that product
generation be credited to the Earth Observation Group, Payne Institute for Public
Policy, Colorado School of Mines (Elvidge et al. 2021,
doi:10.3390/rs13050922). That credit appears on the deck's first and last slides.
**The deck previously described the data as public domain — that was wrong and is
corrected here.** See [`docs/caveats.md`](docs/caveats.md#1-the-licence).

Code in `scripts/` is MIT — see [`LICENSE`](LICENSE).
