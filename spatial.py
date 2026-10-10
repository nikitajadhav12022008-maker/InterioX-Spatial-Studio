"""Server-side spatial logic — mirrors the browser (oriented-rectangle SAT).

Layout JSON: {"rooms": {roomId: {"width", "depth", "items": [{"uid","catalogId","x","y","rotation"}]}}}
The catalog dict below is a minimal subset; in production read dims from the
catalog_items table.
"""
import math

DIMS = {  # catalogId: (w, d, obstacle)
    "sofa-scandi": (210, 90, True), "tv-console": (160, 40, True),
    "coffee-table-round": (90, 90, True), "bed-queen-scandi": (160, 200, True),
    "wardrobe": (120, 60, True), "nightstand": (45, 40, True),
}


def corners(it, dims=DIMS):
    w, d, _ = dims.get(it["catalogId"], (50, 50, True))
    rad = math.radians(it.get("rotation", 0))
    c, s = math.cos(rad), math.sin(rad)
    pts = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
    return [(it["x"] + x * c - y * s, it["y"] + x * s + y * c) for x, y in pts]


def _axes(poly):
    out = []
    for i in range(2):
        (x1, y1), (x2, y2) = poly[i], poly[i + 1]
        ex, ey = x2 - x1, y2 - y1
        n = math.hypot(ex, ey) or 1
        out.append((-ey / n, ex / n))
    return out


def overlap(a, b) -> bool:
    for ax, ay in _axes(a) + _axes(b):
        pa = [x * ax + y * ay for x, y in a]
        pb = [x * ax + y * ay for x, y in b]
        if max(pa) < min(pb) or max(pb) < min(pa):
            return False
    return True


def find_collisions(layout: dict) -> dict:
    result = {}
    for room_id, room in layout.get("rooms", {}).items():
        items = [i for i in room["items"] if DIMS.get(i["catalogId"], (0, 0, True))[2]]
        hits = set()
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if overlap(corners(items[i]), corners(items[j])):
                    hits.update([items[i]["uid"], items[j]["uid"]])
        result[room_id] = sorted(hits)
    return result


def audit_house(layout: dict) -> dict:
    """Simplified: reports collision-free rooms. Extend with door/window/TV/lux rules."""
    collisions = find_collisions(layout)
    scores = {rid: (100 if not hits else 50) for rid, hits in collisions.items()}
    overall = round(sum(scores.values()) / len(scores)) if scores else 100
    return {"roomScores": scores, "overall": overall}
