# tools/

Helper scripts + reference for the tile set and the generated world.
**Nothing under `src/` was modified** - the Java snippets you need are further down,
copy/paste them yourself.

| file | what it is |
| --- | --- |
| `generate_world.py` | builds `assets/maps/world0.txt` + `assets/maps/tileset0.txt` |
| `world0_preview.png` | the generated world rendered at 32 px per tile - check the map without launching the game |
| `tiles_backup_pre_rename.tar.gz` | `assets/tiles/PNG` exactly as it was **before** the rename - your rollback |

## Tile ids

`assets/maps/tileset0.txt` holds one image path per line and **the line number is
the tile id** used inside `world0.txt`:

* `0` -> `Grass.png`, plain grass. Everything that is not ground is this tile.
* `1` .. `55` -> the path tiles. This is **exactly the old `Path_1.png` ... `Path_55.png`
  order**, so every id already used in `map1.txt` still means the same picture it
  always did, and `map1.txt` renders exactly as before.
* `56` .. `92` -> the 37 `Objects/` props (cave, house, rocks, lanterns, ...).

Paths are classpath relative (no leading `/`), because Gradle maps `assets/` to the
resource root: `getResourceAsStream("/" + line)`.

## The rename that was done

`Path/Path_1.png` ... `Path_55.png` became `path_<shape>_grass_<sides>[_variant].png`:

| old | new | the picture |
| --- | --- | --- |
| `Path_2.png` | `path_edge_grass_south.png` | grass band along the **south** edge |
| `Path_8.png` | `path_edge_grass_north.png` | grass band along the north edge |
| `Path_10.png` | `path_half_grass_northwest.png` | grass in the **northwest corner only** |
| `Path_32.png` | `path_corners_grass_all.png` | grass in all four corners |
| `Path_41.png` | `path_band_grass_north_south.png` | grass top + bottom, ground strip in the middle |
| `Path_37.png` | `path_three_grass_north_west_east.png` | ground only on the south side (a corridor opening south) |
| `Path_43.png` | `path_grass_only.png` | the odd one out, all grass |

Names say where the **grass** is (the green band you see around the ground), which is
the opposite of "where the path is", so read them carefully.
The extra hand drawn duplicates are `_2`, `_3`, `_4`, `_5`.

The full 55 line mapping *is* `tileset0.txt` read in order, so the old names are no
longer needed for anything. `Objects/*.png` became `obj_<name>.png`
(`obj_rock_1.png`, `obj_house.png`, ...) and are lines 56+ of `tileset0.txt`.

Rollback if you ever want the old names back:

```bash
tar -xzf tools/tiles_backup_pre_rename.tar.gz -C assets/tiles/
```

## Regenerating / editing the world

```bash
python3 tools/generate_world.py            # run from the repo root
```

It always rewrites both files and then self-checks, refusing to finish if something
is wrong. Output looks like:

```
wrote assets/maps/tileset0.txt (93 tiles, ids 0..92)
ground: 523 cells, 523 reachable
wrote assets/maps/world0.txt (50x50)
distinct tiles used: 79 of 93
ids never used by this map: [5, 10, 11, ...]
```

* `523 cells, 523 reachable` - every ground tile can be walked to from every other
  one, so you cannot accidentally strand a road.
* `ids never used` - harmless. `5` (isolated 1 tile island), `43` (all grass, which
  is just tile 0) and a few `_2`/`_3` variants that the variant picker did not roll
  for this particular layout.

To change the map, edit the two lists near the bottom of `generate_world.py`:

* `ROADS` - `(col0, row0, col1, row1)` rectangles, inclusive. Overlapping rectangles
  merge, and a 1 tile wide rectangle gives you a narrow trail.
* `OBJECTS` - `(row, col, "obj_name")`. Props must sit on grass or the script
  complains; the name is the file name without `.png`.

The script autotiles everything: for each ground cell it looks at its 8 neighbours
(outside the map counts as grass) and picks the matching edge / corner / band /
three-way / isolated tile, then picks one of that role's variants with a
`(row*7 + col*13) % variants` hash so the result is different all over the map but
identical on every run.

## Java changes you need to make

### A. DONE - the tile image paths are already updated

`TileManager` now carries a `String[] pathImage` table (55 entries, ids 1..55 = the old
`Path_1..Path_55`, in the order listed above) and `getTileImage()` builds

```java
"/tiles/PNG/Tiles/Path/" + pathImage[i - 1] + ".png"
```

`tile[0]` is still `/tiles/PNG/Tiles/Grass/Grass.png` (that file kept its name).
Nothing else changed: same array size, same `i = 1 ; i < 56` loop, same `catch (IOException)`.

The table must stay in `tileset0.txt` order - the id number *is* the line number, so
reordering it silently changes what every existing map draws.

Verified after the edit: sources compile, all 55 paths resolve through
`getResourceAsStream` + `ImageIO.read`, and the game launches and renders `map1.txt`
exactly as it did before the rename.

### A2. Only needed for the 50x50 `world0.txt` (tile ids 56..92)

`map1.txt` uses ids 0..55 only, which `tile = new Tile[57]` already covers. `world0.txt`
also uses the 37 object tiles (ids 56..92), so for that map you have to grow the array:

```java
tile = new Tile[93];   // 93 = number of lines in assets/maps/tileset0.txt
```

and you can then drop the `pathImage` table and replace the whole body of
`getTileImage()` with the id-table reader:

```java
    public void getTileImage() {
        try {
            // tileset0.txt: one image path per line, line number == tile id
            InputStream is = getClass().getResourceAsStream("/maps/tileset0.txt");
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            String line;
            int i = 0;
            while ((line = br.readLine()) != null && i < tile.length) {
                line = line.trim();
                if (line.isEmpty()) {
                    continue;
                }
                tile[i] = new Tile();
                tile[i].image = ImageIO.read(getClass().getResourceAsStream("/" + line));
                if (tile[i].image == null) {
                    System.out.println("could not load tile " + i + ": " + line);
                }
                ++i;
            }
            br.close();
        }
        catch (Exception e) {   // not just IOException: read(null) throws otherwise
            e.printStackTrace();
        }
    }
```

That alone makes the game run again, still showing your old 15x15 `map1.txt`,
because the ids kept their meaning. It also fixes the `tile[0]` NPE for good, since
every id the map uses now has an image.

### B. Optional - actually use the 50x50 `world0.txt`

`world0.txt` is 3200x3200 px, so it needs a camera. Four small edits:

`GamePanel` - add the world size next to `maxScreenCol`/`maxScreenRow`
(keep those two at 15, they are the visible window):

```java
    public final int maxWorldCol = 50;
    public final int maxWorldRow = 50;
    public final int worldWidth = tileSize * maxWorldCol;    // 3200
    public final int worldHeight = tileSize * maxWorldRow;   // 3200
    public int cameraX, cameraY;
```

`GamePanel.update()` - follow the player with the camera:

```java
    public void update() {
        player.update();
        cameraX = player.x - screenWidth / 2;
        cameraY = player.y - screenHeight / 2;
        cameraX = Math.max(0, Math.min(cameraX, worldWidth - screenWidth));
        cameraY = Math.max(0, Math.min(cameraY, worldHeight - screenHeight));
    }
```

`TileManager` - size the array from the world and read the new file:

```java
        this.mapTileNum = new int[gp.maxWorldRow][gp.maxWorldCol];   // was maxScreenRow/Col
```

```java
    public void loadMap() {
        try {
            InputStream is = getClass().getResourceAsStream("/maps/world0.txt");
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            for (int i = 0; i < gp.maxWorldRow; ++i) {
                String line = br.readLine();
                String[] nums = line.split(" ");
                for (int j = 0; j < gp.maxWorldCol; ++j) {
                    mapTileNum[i][j] = Integer.parseInt(nums[j]);
                }
            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
```

`TileManager.draw()` - draw only the cells inside the camera window, and draw the
props (`id >= 56`) at their own shape standing on the bottom of the cell instead of
squashing them into a square. Add `import java.awt.image.BufferedImage;` at the top.

```java
    public void draw(Graphics2D g2) {
        int startCol = Math.max(0, gp.cameraX / gp.tileSize);
        int startRow = Math.max(0, gp.cameraY / gp.tileSize);
        for (int row = startRow; row <= startRow + gp.maxScreenRow; ++row) {
            for (int col = startCol; col <= startCol + gp.maxScreenCol; ++col) {
                if (row < 0 || col < 0 || row >= gp.maxWorldRow || col >= gp.maxWorldCol) {
                    continue;
                }
                int id = mapTileNum[row][col];
                BufferedImage img = tile[id].image;
                int x = col * gp.tileSize - gp.cameraX;
                int y = row * gp.tileSize - gp.cameraY;
                if (id <= 55) {
                    g2.drawImage(img, x, y, gp.tileSize, gp.tileSize, null);   // ground
                } else {
                    int h = img.getHeight() * gp.tileSize / img.getWidth();    // prop
                    g2.drawImage(img, x, y + gp.tileSize - h, gp.tileSize, h, null);
                }
            }
        }
    }
```

`Player` - clamp to the world instead of the screen, and subtract the camera when
drawing:

```java
            y = Math.max(0, y - speed);                                // up
            y = Math.min(gp.worldHeight - gp.tileSize, y + speed);     // down
            x = Math.max(0, x - speed);                                // left
            x = Math.min(gp.worldWidth - gp.tileSize, x + speed);      // right
```

```java
        g2.drawImage(image, x - gp.cameraX, y - gp.cameraY, gp.tileSize, gp.tileSize, null);
```

## Things I noticed but did not change

* `Player.update()` uses `else if`, so holding two keys only moves in one direction.
  Replacing the three `else if` with `if` gives diagonal movement.
* The props are part of the tile layer, so the player is always drawn on top of trees
  and rocks. Proper occlusion needs a separate object layer drawn after the player.
* Tile images are 64 px wide but 47..79 px tall (`Grass.png` is 64x47) while
  `tileSize` is 64. Stretching them into 64x64 tiles seamlessly because every cell
  gets the same treatment, but the green bands change thickness slightly where two
  differently sized tiles meet. Normalising every PNG to 64x64 (keeping the art
  bottom aligned) would reproduce the artist's original alignment exactly.
* `map1.txt` is still your hand made 15x15 map and is untouched. Its ids were not
  re-organised, so nothing about it changed.


