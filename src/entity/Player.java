package entity;

import java.awt.Color;
import java.awt.Graphics2D;
import java.io.IOException;
import javax.imageio.ImageIO;
import main.GamePanel;
import main.KeyHandler;
import java.awt.image.BufferedImage;

public class Player extends Entity {
    GamePanel gp;
    KeyHandler keyH;
    public String BASE = "/sprites/PNG/cardinal";

    public Player(GamePanel gp , KeyHandler keyH) {
        this.gp = gp;
        this.keyH = keyH;
        setDefaultValues();
        getPlayerImage();
        direction = "down";
    }
    
    public void setDefaultValues() {
        x = 100;
        y = 100;
        speed = 4;
    }

    public void getPlayerImage() {
        try {
            for (int i = 0 ; i < imagesPerDirection; ++i) {
                left[i] = ImageIO.read(getClass().getResourceAsStream(BASE + "/left/left_" + i + ".png"));
                down[i] = ImageIO.read(getClass().getResourceAsStream(BASE + "/down/down_" + i + ".png"));
                up[i] = ImageIO.read(getClass().getResourceAsStream(BASE + "/up/up_" + i + ".png"));
                right[i] = ImageIO.read(getClass().getResourceAsStream(BASE + "/right/right_" + i + ".png"));
            }
        } catch (IOException e ) {
            e.printStackTrace();
        }
    }
    public void update() {
        // Update the player position 
        if (!keyH.upPressed && !keyH.downPressed && !keyH.leftPressed && !keyH.rightPressed ) return;
        if (keyH.upPressed == true) {
            direction = "up";
            y = Math.max(-1, y - speed);

        }
        else if (keyH.downPressed == true) {
            direction = "down";
            y = Math.min(gp.screenHeight - gp.tileSize + 1 , y  + speed);
        }
        else if (keyH.leftPressed == true) {
            direction = "left";
            x = Math.max(-1 , x - speed);
        }
        else if (keyH.rightPressed == true) {
            direction = "right";
            x = Math.min(gp.screenWidth - gp.tileSize + 1 , x + speed);
        } 
        spriteCounter++;
        if (spriteCounter % 10 == 0) {
            if (spriteNum == 1) spriteNum = 2;
            else spriteNum = 1;
            spriteCounter = 0;
        }
    }

    public void draw(Graphics2D g2) {
        BufferedImage image = null;

        switch (direction) {
            case "up":
                if (spriteNum % 2 == 1) image = up[0];
                else image = up[1];
                break;
            case "down":
                if (spriteNum % 2 == 1) image = down[0];
                else image = down[1];
                break;
            case "left":
                if (spriteNum % 2 == 1) image = left[0];
                else image = left[1];
                break;
            case "right":
                if (spriteNum % 2 == 1) image = right[0];
                else image = right[1];
                break;
        }
        g2.drawImage(image,x,y,gp.tileSize  ,gp.tileSize  ,null);
        
    }

}
