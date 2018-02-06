package lionpals;

import java.io.IOException;

public class LionPals {

    public static void main(String[] args) {
        try {
            web.Launcher.startServer();
        }
        catch(IOException e) {
            System.out.println("Server did not start");
        }
    }
    
}
