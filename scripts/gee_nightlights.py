#!/usr/bin/env python3
"""Nightlights over the Jaipur MDP — Google Earth Engine pipeline (path C).

Computes, for each year 2012–2024, the night-time-light statistics for the whole
Jaipur MDP and for each of its 17 ZDP planning zones, from the official VIIRS
annual product — no raster downloads (GEE does the zonal work server-side).

Dataset: NOAA/VIIRS/DNB/ANNUAL_V22 (VIIRS DNB annual composite, ~464 m,
2012–2024; band `average` in nanoWatts/sr/cm²; public domain — cite EOG /
Elvidge et al. 2021, doi:10.3390/rs13050922).

Method (NRSC NTL Atlas): normalised Sum of Lights = total radiance / area. We
report, per zone per year:
  mean_radiance   — the zone mean of `average` (nanoWatts/sr/cm²) = normalised SoL
  lit_fraction    — share of the zone's pixels with radiance >= 1.6 nW/sr/cm²
                    (the Atlas noise threshold), i.e. the built-up/lit footprint
  zone_area_ha    — the zone's geodesic area, for context

Prereq (manual, once):
  pip install --user --break-system-packages earthengine-api rasterio
  earthengine authenticate            # browser OAuth, or use a service account
  export EE_PROJECT=<your-gcp-project>   # the Cloud project enabled for EE

Run:
  python3 docs/linkedin-series/nightlights/gee_nightlights.py

Outputs (docs/linkedin-series/nightlights/):
  data/ntl_zone_year.csv    zone x year (17 x 13 rows) + MDP-wide rows
  maps/ntl_<year>.png       MDP-clipped annual radiance render (for the slides)
  data/_raw.json            the raw GEE responses (evidence)
"""
import csv
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))   # repo root
ZONES_JS = os.path.join(ROOT, "data", "zones_data.js")
OUT = os.path.join(HERE, "data")
MAPS = os.path.join(HERE, "maps")
YEARS = range(2013, 2026)
THRESHOLD = 1.6                                        # nW/sr/cm^2 (NRSC Atlas)
SCALE = 463.83                                         # m, V22 pixel size

try:
    import ee
except ImportError:
    sys.exit("earthengine-api not installed — pip install --user --break-system-packages earthengine-api")


def load_zones():
    """The 17 ZDP zones from the viewer's baked file (window.__ZONES_DATA)."""
    s = open(ZONES_JS, encoding="utf-8").read()
    d = json.loads(s[s.index("=") + 1:].rstrip().rstrip(";"))
    feats = d["features"] if isinstance(d, dict) else d
    for f in feats:
        f["properties"] = {"zone": (f.get("properties") or {}).get("ZONE") or "?"}
    return feats


def main():
    ee.Initialize(project=os.environ.get("EE_PROJECT") or None)
    feats = load_zones()
    fc = ee.FeatureCollection(feats)
    mdp = fc.geometry()
    coll = (ee.ImageCollection("NOAA/VIIRS/DNB/ANNUAL_V21")
            .merge(ee.ImageCollection("NOAA/VIIRS/DNB/ANNUAL_V22"))
            .select("average"))

    os.makedirs(OUT, exist_ok=True)
    os.makedirs(MAPS, exist_ok=True)
    rows, raw = [], {}

    for y in YEARS:
        img = coll.filterDate(f"{y}-01-01", f"{y+1}-01-01").first()
        if img is None:
            print(f"  {y}: no image in the collection")
            continue
        img = ee.Image(img)
        lit = img.gte(THRESHOLD).rename("lit")
        stacked = img.addBands(lit)

        # per-zone mean radiance and lit fraction (small: 17 features)
        zres = stacked.reduceRegions(collection=fc, reducer=ee.Reducer.mean(),
                                     scale=SCALE).getInfo()["features"]
        # MDP-wide
        mres = stacked.reduceRegion(reducer=ee.Reducer.mean(), geometry=mdp,
                                    scale=SCALE, maxPixels=1e10, bestEffort=True).getInfo()
        raw[str(y)] = {"zones": zres, "mdp": mres}

        for f in zres:
            p = f["properties"]
            rows.append({"zone": p.get("zone"), "year": y,
                         "mean_radiance": p.get("average"), "lit_fraction": p.get("lit"),
                         "mdp_mean_radiance": mres.get("average"),
                         "mdp_lit_fraction": mres.get("lit")})

        # small MDP-clipped map render for the slides (no Drive needed)
        try:
            bbox = mdp.bounds().getInfo()["coordinates"][0]
            xs = [c[0] for c in bbox]; ys = [c[1] for c in bbox]
            region = ",".join(str(v) for v in [min(xs), min(ys), max(xs), max(ys)])
            url = img.clip(mdp).getThumbURL({"min": 0, "max": 60, "dimensions": 900,
                                             "region": region, "format": "png"})
            urllib.request.urlretrieve(url, os.path.join(MAPS, f"ntl_{y}.png"))
        except Exception as e:                          # a map failure must not kill the table
            print(f"  {y}: map render skipped ({e})")

        print(f"  {y}: MDP mean={mres.get('average'):.3f} lit={mres.get('lit'):.3f}")

    # ── like-for-like January–August series, from the MONTHLY product ──
    # The annual composite ends at 2025; the monthly product runs to 2026-08, so
    # this gives a fair 2026 year-to-date (same Jan–Aug window every year).
    mon = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG").select("avg_rad")
    yrows = []
    for y in range(2013, 2027):
        img = mon.filterDate(f"{y}-01-01", f"{y}-09-01").mean()   # Jan..Aug
        lit = img.gte(THRESHOLD).rename("lit")
        stacked = img.addBands(lit)
        zres = stacked.reduceRegions(collection=fc, reducer=ee.Reducer.mean(),
                                     scale=SCALE).getInfo()["features"]
        mres = stacked.reduceRegion(reducer=ee.Reducer.mean(), geometry=mdp,
                                    scale=SCALE, maxPixels=1e10, bestEffort=True).getInfo()
        raw[f"ytd_{y}"] = {"zones": zres, "mdp": mres}
        for f in zres:
            p = f["properties"]
            yrows.append({"zone": p.get("zone"), "year": y,
                          "mean_radiance_jan_aug": p.get("avg_rad"),
                          "lit_fraction_jan_aug": p.get("lit"),
                          "mdp_mean_radiance": mres.get("avg_rad"),
                          "mdp_lit_fraction": mres.get("lit")})
        print(f"  Jan-Aug {y}: MDP mean={mres.get('avg_rad'):.3f}")

    with open(os.path.join(OUT, "ntl_zone_year.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["zone", "year", "mean_radiance", "lit_fraction",
                                           "mdp_mean_radiance", "mdp_lit_fraction"])
        w.writeheader(); w.writerows(rows)
    with open(os.path.join(OUT, "ntl_zone_ytd.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["zone", "year", "mean_radiance_jan_aug",
                                           "lit_fraction_jan_aug", "mdp_mean_radiance",
                                           "mdp_lit_fraction"])
        w.writeheader(); w.writerows(yrows)
    with open(os.path.join(OUT, "_raw.json"), "w", encoding="utf-8") as fh:
        json.dump(raw, fh)
    print(f"wrote {OUT}/ntl_zone_year.csv ({len(rows)} rows), "
          f"{OUT}/ntl_zone_ytd.csv ({len(yrows)} rows) and {MAPS}/ntl_*.png")


if __name__ == "__main__":
    main()
