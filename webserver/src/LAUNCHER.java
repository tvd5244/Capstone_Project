
import java.io.IOException;
import java.net.InetSocketAddress;
import com.sun.net.httpserver.HttpServer;
import java.io.File;

public class LAUNCHER {
	
	public static void main(String[] args) 
		throws IOException {
		HttpServer server = HttpServer.create(new InetSocketAddress(80), 0);
		StaticPage login = new StaticPage(new File("web/login.html"));
		
		server.createContext("/", login);
		server.createContext("/index", login);
		server.createContext("/login", login);
		server.createContext("/signup", new StaticPage(new File("web/signup.html")));
		server.createContext("/friends", new StaticPage(new File("web/friends.html")));
		server.createContext("/recommendations", new StaticPage(new File("web/recommendations.html")));
		server.start();
	}
}
