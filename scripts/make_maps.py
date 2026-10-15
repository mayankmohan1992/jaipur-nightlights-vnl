#!/usr/bin/env python3
"""Render the MDP-clipped nightlight maps for the deck (one PNG per year).

Uses ee.Image.getThumbURL (no Drive/export needed). Annual 2013-2025 from the
V21+V22 annual collections; 2026 is the Jan-Aug monthly mean (like the YTD series).
Colour ramp is the deck palette: black -> indigo -> rose -> gold -> ivory.
"""
import json
import os
import urllib.request

import ee

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
MAPS = os.path.join(HERE, "maps")
PALETTE = ["#0d0b12", "#1F2A44", "#6a2f57", "#C1446A", "#E0A34E", "#F5EDE4"]
VIS = {"min": 0, "max": 60, "palette": PALETTE, "dimensions": 900, "format": "png"}


def zones():
    s = open(os.path.join(ROOT, "data", "zones_data.js"), encoding="utf-8").read()
    feats = json.loads(s[s.index("=") + 1:].rstrip().rstrip(";"))["features"]
    return ee.FeatureCollection(feats)


def fetch(img, path):
    url = img.getThumbURL(VIS)
    with urllib.request.urlopen(url, timeout=120) as r:
        data = r.read()
    with open(path, "wb") as fh:
        fh.write(data)
    return len(data)


def main():
    ee.Initialize(project=os.environ.get("EE_PROJECT") or None)
    fc = zones()
    mdp = fc.geometry()
    os.makedirs(MAPS, exist_ok=True)
    annual = (ee.ImageCollection("NOAA/VIIRS/DNB/ANNUAL_V21")
              .merge(ee.ImageCollection("NOAA/VIIRS/DNB/ANNUAL_V22")).select("average"))
    for y in range(2013, 2026):
        img = ee.Image(annual.filterDate(f"{y}-01-01", f"{y+1}-01-01").first()).clip(mdp)
        n = fetch(img, os.path.join(MAPS, f"ntl_{y}.png"))
        print(f"  {y}: {n//1024} KB")
    # 2026 = Jan-Aug monthly mean
    mon = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG").select("avg_rad")
    img26 = mon.filterDate("2026-01-01", "2026-09-01").mean().clip(mdp)
    n = fetch(img26, os.path.join(MAPS, "ntl_2026_jan_aug.png"))
    print(f"  2026 Jan-Aug: {n//1024} KB")


if __name__ == "__main__":
    main()
