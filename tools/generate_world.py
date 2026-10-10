#!/usr/bin/env python3
"""Builds the tile index and the 50x50 world map for the Java game.

Outputs (both under assets/maps/):
  * tileset0.txt - one tile image per line.  The line number is the tile id
                   that is stored inside world0.txt, so line 0 is tile 0.
  * world0.txt   - 50 lines of 50 space separated tile ids.

The world is stored as a "road mask" and every road cell is then turned into
the correct ground tile by looking at its eight neighbours (autotiling), so
the grass edges and corners line up instead of just stamping one tile
everywhere.

Usage (from the project root):
    python3 tools/generate_world.py
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = os.path.join(ROOT, "assets", "maps")

W = H = 50  # world size in tiles

GRASS = "tiles/PNG/Tiles/Grass/Grass.png"

# ---------------------------------------------------------------------------
# Canonical tile order.  The id of a tile is its position in this list, so the
# (now descriptive) file names must never be re-ordered without regenerating
# the maps.  Id 0 is the plain grass tile, ids 1..55 are the ground/path
# pieces (the old Path_1..Path_55 order) and ids 56+ are the objects.
# ---------------------------------------------------------------------------
PATH_TILES = [
    "path_corner_grass_southeast",            # 1
    "path_edge_grass_south",                  # 2
    "path_corner_grass_southwest",            # 3
    "path_edge_grass_east",                   # 4
    "path_isolated_grass",                    # 5
    "path_edge_grass_west",                   # 6
    "path_corner_grass_northeast",            # 7
    "path_edge_grass_north",                  # 8
    "path_corner_grass_northwest",            # 9
    "path_half_grass_northwest",              # 10
    "path_corners_grass_northwest_northeast",  # 11
    "path_half_grass_northeast",              # 12
    "path_corners_grass_northwest_southwest",  # 13
    "path_plain_1",                           # 14
    "path_corners_grass_northeast_southeast",  # 15
    "path_half_grass_southwest",              # 16
    "path_corners_grass_southwest_southeast",  # 17
    "path_half_grass_southeast",              # 18
    "path_half_grass_northwest_2",            # 19
    "path_edge_grass_north_2",                # 20
    "path_half_grass_northeast_2",            # 21
    "path_edge_grass_west_2",                 # 22
    "path_plain_2",                           # 23
    "path_edge_grass_east_2",                 # 24
    "path_half_grass_southwest_2",            # 25
    "path_edge_grass_south_2",                # 26
    "path_half_grass_southeast_2",            # 27
    "path_half_grass_northwest_3",            # 28
    "path_edge_grass_north_3",                # 29
    "path_half_grass_northeast_3",            # 30
    "path_edge_grass_west_3",                 # 31
    "path_corners_grass_all",                 # 32
    "path_edge_grass_east_3",                 # 33
    "path_half_grass_southwest_3",            # 34
    "path_edge_grass_south_3",                # 35
    "path_half_grass_southeast_3",            # 36
    "path_three_grass_north_west_east",       # 37
    "path_band_grass_west_east",              # 38
    "path_three_grass_south_west_east",       # 39
    "path_three_grass_north_south_west",      # 40
    "path_band_grass_north_south",            # 41
    "path_three_grass_north_south_east",      # 42
    "path_grass_only",                        # 43
    "path_edge_grass_north_4",                # 44
    "path_edge_grass_north_5",                # 45
    "path_edge_grass_south_4",                # 46
    "path_edge_grass_south_5",                # 47
    "path_half_grass_northwest_4",            # 48
    "path_band_grass_north_south_2",          # 49
    "path_half_grass_northeast_4",            # 50
    "path_band_grass_west_east_2",            # 51
    "path_band_grass_west_east_3",            # 52
    "path_half_grass_southwest_4",            # 53
    "path_band_grass_north_south_3",          # 54
    "path_half_grass_southeast_4",            # 55
]

OBJECT_TILES = [
    "obj_animal_skeleton",
    "obj_boulder_1",
    "obj_boulder_2",
    "obj_boulder_3",
    "obj_broken_boat",
    "obj_bushes_1",
    "obj_bushes_2",
    "obj_bushes_3",
    "obj_cave_entrance",
    "obj_danger_sign",
    "obj_flag",
    "obj_house",
    "obj_lantern",
    "obj_leaf_water_1",
    "obj_leaf_water_2",
    "obj_leaf_water_3",
    "obj_rafflesia",
    "obj_rock_1",
    "obj_rock_2",
    "obj_rock_3",
    "obj_rock_4",
    "obj_rock_5",
    "obj_shrub_swamp_1",
    "obj_shrub_swamp_2",
    "obj_shrub_swamp_3",
    "obj_sticks_1",
    "obj_sticks_2",
    "obj_sticks_3",
    "obj_sticks_4",
    "obj_sticks_5",
    "obj_tree_tower_short",
    "obj_tree_tower_tall",
    "obj_water_plant_1",
    "obj_water_plant_2",
    "obj_water_plant_3",
    "obj_wooden_floor_horizontal",
    "obj_wooden_floor_vertical",
]

# id lookup: "path_edge_grass_north" -> 8, "obj_rock_1" -> 73, ...
ID = {GRASS: 0}
for _i, _name in enumerate(PATH_TILES):
    ID["tiles/PNG/Tiles/Path/%s.png" % _name] = _i + 1
for _i, _name in enumerate(OBJECT_TILES):
    ID["tiles/PNG/Tiles/Objects/%s.png" % _name] = len(PATH_TILES) + 1 + _i

TILE_COUNT = 1 + len(PATH_TILES) + len(OBJECT_TILES)


def tid(name):
    """Tile id of a ground/object tile given its short (file) name."""
    if name.startswith("obj_"):
        return ID["tiles/PNG/Tiles/Objects/%s.png" % name]
    return ID["tiles/PNG/Tiles/Path/%s.png" % name]


# Several tiles are hand drawn variants of the same role. Picking between them
# with a position hash keeps big open areas from looking copy pasted.
VARIANTS = {
    "edge_n": ["path_edge_grass_north", "path_edge_grass_north_2",
               "path_edge_grass_north_3", "path_edge_grass_north_4",
               "path_edge_grass_north_5"],
    "edge_s": ["path_edge_grass_south", "path_edge_grass_south_2",
               "path_edge_grass_south_3", "path_edge_grass_south_4",
               "path_edge_grass_south_5"],
    "edge_e": ["path_edge_grass_east", "path_edge_grass_east_2",
               "path_edge_grass_east_3"],
    "edge_w": ["path_edge_grass_west", "path_edge_grass_west_2",
               "path_edge_grass_west_3"],
    "half_nw": ["path_half_grass_northwest", "path_half_grass_northwest_2",
                "path_half_grass_northwest_3", "path_half_grass_northwest_4"],
    "half_ne": ["path_half_grass_northeast", "path_half_grass_northeast_2",
                "path_half_grass_northeast_3", "path_half_grass_northeast_4"],
    "half_sw": ["path_half_grass_southwest", "path_half_grass_southwest_2",
                "path_half_grass_southwest_3", "path_half_grass_southwest_4"],
    "half_se": ["path_half_grass_southeast", "path_half_grass_southeast_2",
                "path_half_grass_southeast_3", "path_half_grass_southeast_4"],
    "band_ns": ["path_band_grass_north_south", "path_band_grass_north_south_2",
                "path_band_grass_north_south_3"],
    "band_we": ["path_band_grass_west_east", "path_band_grass_west_east_2",
                "path_band_grass_west_east_3"],
    "plain": ["path_plain_1", "path_plain_2"],
}

# roles that only have a single hand drawn tile
FIXED = {
    "corner_se": "path_corner_grass_southeast",
    "corner_sw": "path_corner_grass_southwest",
    "corner_ne": "path_corner_grass_northeast",
    "corner_nw": "path_corner_grass_northwest",
    "corners_nw_ne": "path_corners_grass_northwest_northeast",
    "corners_nw_sw": "path_corners_grass_northwest_southwest",
    "corners_ne_se": "path_corners_grass_northeast_southeast",
    "corners_sw_se": "path_corners_grass_southwest_southeast",
    "corners_all": "path_corners_grass_all",
    "three_nwe": "path_three_grass_north_west_east",
    "three_swe": "path_three_grass_south_west_east",
    "three_nsw": "path_three_grass_north_south_west",
    "three_nse": "path_three_grass_north_south_east",
    "isolated": "path_isolated_grass",
    "grass_only": "path_grass_only",
}


def autotile(road, r, c):
    """Pick the ground tile for road cell (r, c) from its eight neighbours."""

    def grass(rr, cc):
        if rr < 0 or cc < 0 or rr >= H or cc >= W:
            return True  # outside the map behaves like grass
        return not road[rr][cc]

    n, s = grass(r - 1, c), grass(r + 1, c)
    e, w = grass(r, c + 1), grass(r, c - 1)

    def pick(role):
        names = VARIANTS.get(role)
        if names is None:
            return tid(FIXED[role])
        # deterministic "random" variant, so the map is reproducible
        return tid(names[(r * 7 + c * 13) % len(names)])

    if not (n or s or e or w):
        # road on all four sides: only the diagonals can break the tile up
        nw, ne = grass(r - 1, c - 1), grass(r - 1, c + 1)
        sw, se = grass(r + 1, c - 1), grass(r + 1, c + 1)
        if nw and ne and sw and se:
            return pick("corners_all")
        if nw and ne:
            return pick("corners_nw_ne")
        if nw and sw:
            return pick("corners_nw_sw")
        if ne and se:
            return pick("corners_ne_se")
        if sw and se:
            return pick("corners_sw_se")
        if nw:
            return pick("corner_nw")
        if ne:
            return pick("corner_ne")
        if sw:
            return pick("corner_sw")
        if se:
            return pick("corner_se")
        return pick("plain")
    if n and not (s or e or w):
        return pick("edge_n")
    if s and not (n or e or w):
        return pick("edge_s")
    if e and not (n or s or w):
        return pick("edge_e")
    if w and not (n or s or e):
        return pick("edge_w")
    if n and w and not (s or e):
        return pick("half_nw")
    if n and e and not (s or w):
        return pick("half_ne")
    if s and w and not (n or e):
        return pick("half_sw")
    if s and e and not (n or w):
        return pick("half_se")
    if n and s and not (e or w):
        return pick("band_ns")
    if e and w and not (n or s):
        return pick("band_we")
    if n and e and w and not s:
        return pick("three_nwe")
    if s and e and w and not n:
        return pick("three_swe")
    if n and s and w and not e:
        return pick("three_nsw")
    if n and s and e and not w:
        return pick("three_nse")
    return pick("isolated")


# ---------------------------------------------------------------------------
# The world itself.  The ground is described as a union of rectangles so the
# layout stays easy to edit.  (col0, row0, col1, row1) are inclusive.
# ---------------------------------------------------------------------------
ROADS = [
    (10, 5, 12, 45),    # north/south main road
    (5, 22, 45, 24),    # east/west main road
    (8, 19, 14, 27),    # plaza around the crossing of the two main roads
    (12, 6, 32, 8),     # northern arm
    (30, 8, 32, 22),    # links the northern arm down to the main road
    (12, 36, 40, 38),   # southern arm
    (38, 24, 40, 36),   # links the main road to the southern arm
    (4, 30, 10, 32),    # western branch
    (13, 13, 26, 13),   # narrow trail east of the main road (1 tile wide)
    (4, 33, 4, 40),     # narrow trail south of the western branch
    (44, 25, 44, 30),   # narrow trail south of the eastern road
]

# Objects: (row, col, tile name).  Props are meant to stand on grass, so they
# are kept off the ground cells - one placed on a road hides the road.
OBJECTS = [
    (4, 20, "obj_cave_entrance"),   # the northern arm leads into the cave
    (5, 33, "obj_danger_sign"),
    (4, 8, "obj_tree_tower_tall"),
    (4, 14, "obj_tree_tower_short"),
    (28, 6, "obj_house"),
    (28, 5, "obj_wooden_floor_vertical"),
    (29, 6, "obj_wooden_floor_horizontal"),
    (29, 7, "obj_wooden_floor_horizontal"),
    (10, 9, "obj_lantern"),
    (16, 13, "obj_lantern"),
    (18, 9, "obj_lantern"),
    (33, 9, "obj_lantern"),
    (43, 13, "obj_lantern"),
    (20, 6, "obj_flag"),
    (14, 28, "obj_rafflesia"),
    (40, 25, "obj_rafflesia"),
    (9, 6, "obj_rock_1"),
    (11, 42, "obj_rock_2"),
    (33, 20, "obj_rock_3"),
    (43, 28, "obj_rock_4"),
    (17, 43, "obj_rock_5"),
    (3, 35, "obj_boulder_1"),
    (46, 20, "obj_boulder_2"),
    (26, 3, "obj_boulder_3"),
    (9, 16, "obj_bushes_1"),
    (21, 42, "obj_bushes_2"),
    (39, 16, "obj_bushes_3"),
    (16, 35, "obj_shrub_swamp_1"),
    (32, 44, "obj_shrub_swamp_2"),
    (41, 5, "obj_shrub_swamp_3"),
    (10, 24, "obj_sticks_1"),
    (17, 3, "obj_sticks_2"),
    (34, 34, "obj_sticks_3"),
    (45, 43, "obj_sticks_4"),
    (13, 47, "obj_sticks_5"),
    (35, 45, "obj_animal_skeleton"),
    (13, 27, "obj_broken_boat"),
    (6, 38, "obj_water_plant_1"),
    (41, 3, "obj_water_plant_2"),
    (18, 45, "obj_water_plant_3"),
    (4, 3, "obj_leaf_water_1"),
    (29, 43, "obj_leaf_water_2"),
    (47, 13, "obj_leaf_water_3"),
]


def write_tileset():
    """assets/maps/tileset0.txt - line number == tile id used in world0.txt."""
    lines = [GRASS]
    for name in PATH_TILES:
        lines.append("tiles/PNG/Tiles/Path/%s.png" % name)
    for name in OBJECT_TILES:
        lines.append("tiles/PNG/Tiles/Objects/%s.png" % name)
    path = os.path.join(MAPS, "tileset0.txt")
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote %s (%d tiles, ids 0..%d)" % (path, len(lines), len(lines) - 1))


def build_road_mask():
    road = [[False] * W for _ in range(H)]
    for (c0, r0, c1, r1) in ROADS:
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                road[r][c] = True
    return road


def report_connectivity(road):
    """Sanity check: all ground should be reachable from any ground cell."""
    cells = [(r, c) for r in range(H) for c in range(W) if road[r][c]]
    if not cells:
        return False
    seen = {cells[0]}
    stack = [cells[0]]
    while stack:
        r, c = stack.pop()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < H and 0 <= cc < W and road[rr][cc] and (rr, cc) not in seen:
                seen.add((rr, cc))
                stack.append((rr, cc))
    orphans = [p for p in cells if p not in seen]
    print("ground: %d cells, %d reachable%s"
          % (len(cells), len(seen),
             "" if not orphans else " - ORPHANED: %s" % orphans[:10]))
    return not orphans


def main():
    write_tileset()
    road = build_road_mask()
    connected = report_connectivity(road)

    grid = [[0] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            if road[r][c]:
                grid[r][c] = autotile(road, r, c)

    conflicts = []
    for (r, c, name) in OBJECTS:
        if road[r][c]:
            conflicts.append("%s at row %d col %d is on a road tile"
                             % (name, r, c))
        grid[r][c] = tid(name)

    # self check: nothing outside the tile set, none of the images missing
    for r in range(H):
        for c in range(W):
            if not 0 <= grid[r][c] < TILE_COUNT:
                raise SystemExit("bad tile id %d at row %d col %d"
                                 % (grid[r][c], r, c))

    path = os.path.join(MAPS, "world0.txt")
    with open(path, "w") as fh:
        for r in range(H):
            fh.write(" ".join(str(grid[r][c]) for c in range(W)) + "\n")

    used = set(v for row in grid for v in row)
    unused = [i for i in range(TILE_COUNT) if i not in used]
    print("wrote %s (%dx%d)" % (path, W, H))
    print("distinct tiles used: %d of %d" % (len(used), TILE_COUNT))
    if unused:
        print("ids never used by this map: %s" % unused)

    if conflicts:
        for line in conflicts:
            print("WARNING: " + line)
        raise SystemExit("fix the object placements above and re-run")
    if not connected:
        raise SystemExit("the ground is not fully connected - fix ROADS")


if __name__ == "__main__":
    main()
