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
             tile[0].image = ImageIO.read(getClass().getResourceAsStream("/tiles/PNG/Tiles/Grass/Grass.png"));
            
            for (int i = 1 ; i < 56; ++i) {
                tile[i].image = ImageIO.read(getClass().getResourceAsStream("/tiles/PNG/Tiles/Path/Path_" + i + ".png"));
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
