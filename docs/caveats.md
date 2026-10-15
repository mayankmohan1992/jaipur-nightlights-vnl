# Caveats

## 1. The licence

The deck's original brief said the EOG data were **public domain**. That is wrong.
EOG's product page states the VIIRS night-time lights are available under
**Creative Commons Attribution 4.0 International (CC-BY 4.0)** and asks that
product generation be credited to the **Earth Observation Group, Payne Institute
for Public Policy, Colorado School of Mines**. The deck carries that credit on its
first and last slides. **Any reuse must carry the attribution too**, along with the
Elvidge et al. citations EOG lists (doi:10.3390/rs13050922).

## 2. Saturation — the caveat that argues against the headline

**Jaipur is already one of India's brightest cities.** VIIRS saturates over very
bright cores, and — more importantly — a city that is already bright simply cannot
double its relative radiance the way a dark district can. **The +113 % headline
therefore understates Jaipur's change, not the reverse.**

India's own night-lights atlas names Rajasthan's most-prominent change districts as
**Sikar, Bharatpur, Karauli and Jhunjhunu — not Jaipur.** The deck states this on
its method slide and again on its honesty slide rather than letting the headline
imply Jaipur leads. This is a property of the measurement, not a shortcoming of the
arithmetic.

## 3. Two series that must never be mixed

| | covers | ends |
|---|---|---|
| Annual composite | full calendar years | **2025** |
| Jan–Aug monthly mean | the same 8 months each year | **2026** |

Their percentages differ (+68 % vs +113 %) for two reasons: the annual series
stops a year earlier, and the full-year mean is higher than the Jan–Aug mean in
every year, so the same absolute growth is a smaller proportion of it.

**Never** compare a partial 2026 against a full 2025. The deck's only 2025→2026
comparison is Jan–Aug against Jan–Aug.

## 4. The record starts in 2013

There is no 2012 image in this product for this area. The annual series is
**13 years**. A "since 1992" line would require DMSP-OLS, which is **a different
instrument with a different calibration** — the two are not spliced anywhere in
this deck.

## 5. Radiance is light, not land use

A bright pixel may be a streetlight, a lit highway, an industrial yard or a
floodlit empty plot. The "lit fraction" counts pixels above the 1.6
nW·cm⁻²·sr⁻¹ threshold — it is a **lit-footprint proxy**, and the deck calls it
"lit", never "built-up".

## 6. Mean, not median or maximum

Both statistics use the `average` band and an `ee.Reducer.mean()`. A mean is
sensitive to outliers — one very bright site shifts a zone's figure. The
distributions are not published here; the honest reading is that these are means
computed exactly as stated, and no claim is made about how the light is spread
within a zone.

## 7. The threshold is a convention, not a fact

**1.6 nW·cm⁻²·sr⁻¹** is NRSC/ISRO's background-noise threshold, adopted so the
figure is comparable with published Indian work. A different threshold gives a
different lit fraction. The radiance mean does not depend on the threshold at all.

## 8. The map renders are for comparison, not for measurement

Every panel uses one fixed colour scale (`min 0, max 60`). The brightest cores are
at the top of that scale and are **clipped in colour** — which is what makes the
14 frames comparable, but also means you must not read an absolute radiance value
off a map. The numbers come from the CSVs.

## 9. The monthly product has variants

The 2026 figure uses `NOAA/VIIRS/DNB/MONTHLY_V1/**VCMCFG**` — the cloud-masked
monthly composite. A stray-light-corrected sibling variant exists whose values
differ, so **the variant choice matters**; this repository states the one used.
Averaging eight monthly composites also means a heavily clouded month contributes
a noisier scene, though over an eight-month mean the effect is small.

## 10. Datasets are versioned

The annual series merges `ANNUAL_V21` (to 2021) and `ANNUAL_V22` (2022 onward).
A future `V23` — or a reprocessing of V21/V22 — would move these numbers. The two
CSVs are committed with their SHA-256 in [`figures.md`](figures.md) so the values
used here are pinned.

## 11. Reproducing it needs a Google account

Earth Engine requires registration and a Cloud project (`EE_PROJECT`). This is a
one-time human step; see [`data-sources.md`](data-sources.md#environments). No
raster is downloaded — the statistics are computed server-side, which also means
results depend on Earth Engine's current build of the collection.
