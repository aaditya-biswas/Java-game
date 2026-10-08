
package main;
import javax.swing.JFrame;

public class Main{
    public static void main(String[] args){
        JFrame window = new JFrame();
        // 
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setResizable(false);

        window.setTitle("2D Adventure");
        // Window will be displayed at the center of the screen
        window.setLocationRelativeTo(null);
        // We are able to see the window
        window.setVisible(true);
    }
}