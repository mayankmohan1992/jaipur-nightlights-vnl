# Method — how every figure is calculated

Everything here is computed by [`../scripts/gee_nightlights.py`](../scripts/gee_nightlights.py)
and can be re-derived from [`../data/`](../data/) with a spreadsheet.

---

## 1. The pipeline

For each year and each region (the 17 zones, and the MDP as a whole):

```python
img = collection.filterDate(f"{y}-01-01", f"{y+1}-01-01").first()   # annual composite
lit = img.gte(1.6).rename("lit")                                    # boolean band
stacked = img.addBands(lit)
zres = stacked.reduceRegions(collection=zones, reducer=ee.Reducer.mean(), scale=463.83)
mres = stacked.reduceRegion(reducer=ee.Reducer.mean(), geometry=mdp,
                            scale=463.83, maxPixels=1e10, bestEffort=True)
```

Three points worth noting:

- **`scale=463.83`** is the product's native pixel size. Reducing at a coarser
  scale would blur zone edges; at a finer one Earth Engine would resample data
  that does not exist.
- **`bestEffort=True`** on the MDP-wide reduction: the MDP is larger than the
  default pixel budget, and without it the call errors rather than returning.
- **The same mask is used for every year** — the zone features never change — so a
  year-on-year difference is a difference in light, not in framing.

## 2. Why there are two series

An annual composite for 2026 **cannot exist** — the year is not finished. So the
deck carries two series and never mixes them:

| Series | Source | Years | Used for |
|---|---|---|---|
| **Annual** | `ANNUAL_V21` + `ANNUAL_V22`, band `average` | 2013–**2025** | the +68 % figure, the 13-year trend, the CAGR |
| **Like-for-like Jan–Aug** | `MONTHLY_V1/VCMCFG`, band `avg_rad`, `filterDate(y-01-01, y-09-01)` | 2013–**2026** | the +113 % headline, the 2026 figure |

The Jan–Aug series takes the **same eight months in every year**, which is what
makes 2026 comparable to 2013. The deck **never** compares a partial 2026 against
a full 2025; the only 2025→2026 comparison is Jan–Aug against Jan–Aug.

The two series give different percentages for the same question, and both are
printed:

| | 2013 | end | change |
|---|---:|---:|---:|
| Annual | 4.529 | 7.623 (2025) | **+68.3 %** |
| Jan–Aug | 3.496 | 7.436 (2026) | **+112.7 %** |

They differ for two honest reasons: the annual series **stops at 2025**, and the
two windows have **different baselines** (the full-year mean is higher than the
Jan–Aug mean in every year).

## 3. Every derived figure, with its arithmetic

| Figure on the deck | How it is computed | Value |
|---|---|---|
| **+113 %** (hero) | 7.436 ÷ 3.496 − 1 (Jan–Aug, 2013→2026) | +112.7 % |
| **+68 % on the annual record** | 7.623 ÷ 4.529 − 1 (annual, 2013→2025) | +68.3 % |
| **9.5 %/yr since 2021** | (7.623 ÷ 5.310)^(1/4) − 1 (annual, 2021→2025) | +9.49 %/yr |
| **~1 %/yr, 2013–2020** | (4.869 ÷ 4.529)^(1/7) − 1 (annual) | +1.03 %/yr |
| **2026 +11.2 %** | 7.436 ÷ 6.685 − 1 (Jan–Aug, 2025→2026) | +11.2 % |
| **0.55 → 0.86 lit** | annual `mdp_lit_fraction`, 2013 → 2025 | 0.550 → 0.860 |
| **Fastest zone, +260 %** | ZDP-15: 2.51 ÷ 0.70 − 1 (Jan–Aug, 2013→2026) | +260.1 % |

### Worked example — the hero number

```
2013 Jan–Aug MDP mean radiance   3.49606586…  nW·cm⁻²·sr⁻¹
2026 Jan–Aug MDP mean radiance   7.43609985…  nW·cm⁻²·sr⁻¹

7.43609985 / 3.49606586 = 2.1270…
2.1270 − 1 = 1.1270  ->  +112.7 %   (rounded once, at the end)
```

## 4. The precision gotcha that bit us

On the first verification pass three figures disagreed with the brief:

| figure | computed | brief | cause |
|---|---:|---:|---|
| 2021→2025 CAGR | 9.4 %/yr | 9.5 %/yr | input pre-rounded to 2 dp |
| ZDP-15 growth | 258.6 % | 260 % | input pre-rounded to 2 dp |
| ZDP-16 growth | 211.2 % | 212 % | input pre-rounded to 2 dp |

**Rounding an input shifts a ratio.** ZDP-15's growth is 258.6 % from 2-dp inputs
and 259.7 % from the raw ones. The rule adopted: **carry full precision everywhere
and round only the outputs**, once, at the end. After that all figures agree.

## 5. The maps

[`../scripts/make_maps.py`](../scripts/make_maps.py) renders one PNG per year with
`ee.Image.getThumbURL` (no Drive, no export tasks):

- each image is **clipped to the MDP geometry**, so all 14 frames share one mask;
  the transparent background is identical year to year, which is what makes the
  sequence slide a comparison of light rather than of framing;
- one fixed colour ramp and one fixed scale (`min 0, max 60`) for every year —
  every panel uses the same scale, so brightness is comparable across the row;
- 2026 is the Jan–Aug monthly mean, matching the series it belongs to.

## 6. What is *not* computed

- **No built-up area.** Radiance is light, not land use. The lit fraction counts
  *pixels above a noise threshold*, which is a proxy for lit footprint — the deck
  calls it "lit", never "built-up".
- **No district comparison.** The deck does not rank Jaipur against other
  districts from this data; it quotes India's atlas for that claim and attributes it.
- **No pre-2013 line.** DMSP-OLS is a different instrument and is not spliced in.
- **No interpolation.** Missing years are missing; nothing is filled.
