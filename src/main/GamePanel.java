package main;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import javax.swing.JPanel;
import javax.swing.plaf.DimensionUIResource;
import entity.Player;

public class GamePanel extends JPanel implements Runnable {
    // SCREEN SETTINGS 
    final int originalTileSize = 16; // 16 * 16 Tile Default size of player character
    // Since modern computers have large 
    final int scale = 3;
    final int FPS = 60;
    final int tileSize = originalTileSize * scale; // Final tile size
    final int maxScreenCol = 16;
    final int maxScreenRow = 18;
    public final int screenWidth = tileSize * maxScreenCol;
    public final int screenHeight = tileSize * maxScreenRow;
    // Set the default position 
    int playerX = 100;
    int playerY = 100;
    int playerSpeed = 4;

    
    Thread gameThread; // Helps in repeating a task
    KeyHandler keyH = new KeyHandler();
    Player player = new Player(this,this.keyH);
    
    public GamePanel() {
        this.setPreferredSize(new DimensionUIResource(screenWidth, screenHeight));
        this.setBackground(Color.BLACK);
        this.addKeyListener(keyH);
        // Game Panel can be focused to receive key input 
        this.setFocusable(true);
        // Improves the game's performance 
        this.setDoubleBuffered(true);
    }

    public void startGameThread() {
        // Initializes this panel runs in separate to the program
        gameThread = new Thread(this);
        gameThread.start();
    }
    // public void run() {
    //     // When we start the thread it calls the run method
    //     // Now we create a game loop here 
    //     double drawInterval = 1e9 / FPS;
    //     double nextDrawTime = System.nanoTime() + drawInterval;
    //     while (gameThread != null ) {
    //         // Update the information such as char positions 

    //         // Draw the screen with the updated information
    //         update();
    //         // Calling this calls paintComponent
    //         repaint();
    //         try {
    //             double remainingTime = nextDrawTime - System.nanoTime();
    //             remainingTime /= 1e6;
    //             Thread.sleep(Math.max(1l*0,(long) (remainingTime)));
    //             nextDrawTime += drawInterval;
    //         }
    //         catch (InterruptedException e) {
    //             e.printStackTrace();
    //         }
            
    //     }

    // }
    @Override 
    public void run() {
        double drawInterval =  1000000000/FPS;
        double delta = 0;
        long lastTime = System.nanoTime();
        long currentTime;
        long timer = 0;
        int drawCount  = 0; 
        
        while (gameThread != null ){
            currentTime = System.nanoTime();
            delta += (currentTime - lastTime ) / drawInterval;
            timer += (currentTime - lastTime);
            lastTime = currentTime ;
            if (delta >= 1) {
                update();
                repaint();
                delta--;
                drawCount++;
            }
            if (timer >= 1000000000) {
                System.out.println("FPS " + drawCount );
                drawCount = 0;
                timer = 0;
            }
        } 
    }
    public void update() {
        player.update();
    }
        // Builtin method: Standard method for painting components on Jpanel
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        // Conversion to 2D graphics for better control
        // Polymorphism
        Graphics2D g2 = (Graphics2D) g; 
        // Sets a color for drawing objects
        g2.setColor(Color.WHITE);
        
        g2.fillRect(playerX, playerY, tileSize,  tileSize);
        // Dispose of graphics Component
        
        g2.dispose();
    }
}
