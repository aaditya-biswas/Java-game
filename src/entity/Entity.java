package entity;

import java.awt.image.BufferedImage;

public class Entity {
    public  int x,y;
    public int speed;
    public final int imagesPerDirection = 2;
    public BufferedImage[] up , down , left ,right;
    public String direction;
    public int spriteCounter = 0;
    public int spriteNum = 1;
    Entity() {
        up = new BufferedImage[imagesPerDirection];
        down = new BufferedImage[imagesPerDirection];
        right = new BufferedImage[imagesPerDirection];
        left =  new BufferedImage[imagesPerDirection];        
    }

}