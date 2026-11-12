"""Build a dot matrix world map (equirectangular) from Natural Earth 110m land (world-atlas TopoJSON, public domain data).
Usage: python3 -I mapdots.py land-110m.json out.json [step_deg]
"""
import json, sys
import numpy as np
topo = json.load(open(sys.argv[1]))
step = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
sx, sy = topo["transform"]["scale"]; tx, ty = topo["transform"]["translate"]
arcs = []
for a in topo["arcs"]:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
    arcs.append(pts)
def ring(idx):
    out = []
    for i in idx:
        pts = arcs[i] if i >= 0 else arcs[~i][::-1]
        out.extend(pts if not out else pts[1:])
    return np.array(out)
rings = []
for g in topo["objects"]["land"]["geometries"]:
    polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
    for poly in polys:
        for r in poly: rings.append(ring(r))
LAT0, LAT1 = 78.0, -56.0
lons = np.arange(-180 + step / 2, 180, step); lats = np.arange(LAT0 - step / 2, LAT1, -step)
LON, LAT = np.meshgrid(lons, lats); px, py = LON.ravel(), LAT.ravel()
inside = np.zeros(px.shape, bool)
for r in rings:
    x1, y1 = r[:-1, 0], r[:-1, 1]; x2, y2 = r[1:, 0], r[1:, 1]
    for a, b, c, d in zip(x1, y1, x2, y2):
        if b == d: continue
        cond = ((b > py) != (d > py))
        xint = a + (py - b) * (c - a) / (d - b)
        inside ^= cond & (px < xint)
cols, rows = len(lons), len(lats)
idx = np.nonzero(inside)[0]
dots = [[int(i % cols), int(i // cols)] for i in idx]
json.dump({"step": step, "lon0": -180, "lat0": LAT0, "cols": cols, "rows": rows, "dots": dots}, open(sys.argv[2], "w"))
print(f"grid {cols}x{rows}, land dots {len(dots)}")
