package tile;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import javax.imageio.ImageIO;
import java.awt.Graphics2D;
import main.GamePanel;
public class TileManager {
    GamePanel gp;
    Tile[] tile;
    int mapTileNum[][];
    // Image file for each tile id 1..55, in id order (id 1 = first entry), matching
    // the old Path_1.png..Path_55.png order but with the new descriptive file names.
    String[] pathImage = {
        "path_corner_grass_southeast",       // 1
        "path_edge_grass_south",             // 2
        "path_corner_grass_southwest",       // 3
        "path_edge_grass_east",              // 4
        "path_isolated_grass",               // 5
        "path_edge_grass_west",              // 6
        "path_corner_grass_northeast",       // 7
        "path_edge_grass_north",             // 8
        "path_corner_grass_northwest",       // 9
        "path_half_grass_northwest",         // 10
        "path_corners_grass_northwest_northeast", // 11
        "path_half_grass_northeast",         // 12
        "path_corners_grass_northwest_southwest", // 13
        "path_plain_1",                      // 14
        "path_corners_grass_northeast_southeast", // 15
        "path_half_grass_southwest",         // 16
        "path_corners_grass_southwest_southeast", // 17
        "path_half_grass_southeast",         // 18
        "path_half_grass_northwest_2",       // 19
        "path_edge_grass_north_2",           // 20
        "path_half_grass_northeast_2",       // 21
        "path_edge_grass_west_2",            // 22
        "path_plain_2",                      // 23
        "path_edge_grass_east_2",            // 24
        "path_half_grass_southwest_2",       // 25
        "path_edge_grass_south_2",           // 26
        "path_half_grass_southeast_2",       // 27
        "path_half_grass_northwest_3",       // 28
        "path_edge_grass_north_3",           // 29
        "path_half_grass_northeast_3",       // 30
        "path_edge_grass_west_3",            // 31
        "path_corners_grass_all",            // 32
        "path_edge_grass_east_3",            // 33
        "path_half_grass_southwest_3",       // 34
        "path_edge_grass_south_3",           // 35
        "path_half_grass_southeast_3",       // 36
        "path_three_grass_north_west_east",  // 37
        "path_band_grass_west_east",         // 38
        "path_three_grass_south_west_east",  // 39
        "path_three_grass_north_south_west", // 40
        "path_band_grass_north_south",       // 41
        "path_three_grass_north_south_east", // 42
        "path_grass_only",                   // 43
        "path_edge_grass_north_4",           // 44
        "path_edge_grass_north_5",           // 45
        "path_edge_grass_south_4",           // 46
        "path_edge_grass_south_5",           // 47
        "path_half_grass_northwest_4",       // 48
        "path_band_grass_north_south_2",     // 49
        "path_half_grass_northeast_4",       // 50
        "path_band_grass_west_east_2",       // 51
        "path_band_grass_west_east_3",       // 52
        "path_half_grass_southwest_4",       // 53
        "path_band_grass_north_south_3",     // 54
        "path_half_grass_southeast_4",       // 55
    };
    public TileManager(GamePanel gp) {
            this.gp = gp;

            tile = new Tile[57];
            this.mapTileNum = new int[gp.maxScreenRow][gp.maxScreenCol];
            getTileImage();
            loadMap();

    
    }
    public void loadMap() {
        try {
            InputStream is = getClass().getResourceAsStream("/maps/map1.txt");
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            for (int i = 0; i < gp.maxScreenRow; ++i) {
                String line = br.readLine();
                String[] nums = line.split(" ");
                for (int j =0 ; j < gp.maxScreenCol ; ++j) {
                    mapTileNum[i][j] = Integer.parseInt(nums[j]);
                }
            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void getTileImage() {
        try {
            tile[0] = new Tile();
            tile[0].image = ImageIO.read(getClass().getResourceAsStream("/tiles/PNG/Tiles/Grass/Grass.png"));
            
            for (int i = 1 ; i < 56; ++i) {
                tile[i] = new Tile();
                tile[i].image = ImageIO.read(getClass().getResourceAsStream("/tiles/PNG/Tiles/Path/" + pathImage[i - 1] + ".png"));
            }
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
    public void draw(Graphics2D g2) {
        int m =  gp.maxScreenRow;
        int n = gp.maxScreenCol;
        for (int i = 0 ; i < m;++i) {       
            for (int j = 0 ; j < n ; ++j) {
                g2.drawImage(tile[mapTileNum[j][i]].image,  i * gp.tileSize, j* gp.tileSize,  gp.tileSize, gp.tileSize, null);
        
            }
        }
    }

}
