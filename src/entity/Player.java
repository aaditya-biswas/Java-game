package entity;

import main.GamePanel;
import main.KeyHandler;
public class Player extends Entity {
    GamePanel gp;
    KeyHandler keyH;

    public Player(GamePanel gp , KeyHandler keyH) {
        this.gp = gp;
        this.keyH = keyH;
    }
    
    public void setDefaultValues() {
        x = 100;
        y = 100;
        speed = 4;

    }
    public void update() {
        // Update the player position 
        if (keyH.upPressed == true) {
            y = Math.max(0, y - speed);
        }
        else if (keyH.downPressed == true) {
            y = Math.min(gp.screenHeight, y  + speed);
        }
        else if (keyH.leftPressed == true) {
            x = Math.max(0 , x - speed);
        }
        else if (keyH.rightPressed == true) {
            x = Math.min(gp.screenWidth , x + speed);
        } 
    }

}
