package main;
import javax.swing.JFrame;

public class Main{
    public static void main(String[] args){
        JFrame window = new JFrame();
        // 
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setResizable(false);

        window.setTitle("2D Adventure");
        GamePanel gamePanel = new GamePanel();
        window.add(gamePanel);
        // Causes window to fit it 's subcomponents i.e GamePanel
        window.pack();

        // Window will be displayed at the center of the screen

        window.setLocationRelativeTo(null);
        // We are able to see the window
        window.setVisible(true);
        gamePanel.requestFocusInWindow();
        gamePanel.startGameThread();        
    }
}
