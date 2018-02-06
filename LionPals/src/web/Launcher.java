package web;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.IOException;
import java.net.InetSocketAddress;
import com.sun.net.httpserver.HttpServer;
import java.io.File;
import java.util.Scanner;

public class Launcher {
	
	public static void startServer() 
		throws IOException {
		HttpServer server = HttpServer.create(new InetSocketAddress(80), 0);
		StaticPage login = new StaticPage(new File("web/pages/login.html"));
		
		server.createContext("/do_login", new HttpHandler() {
			public void handle(HttpExchange req) 
				throws IOException {
				Scanner in = new Scanner(req.getRequestBody());
				
				System.out.println("received login: ");
				
				while (in.hasNextLine()) {
					System.out.println(in.nextLine());
				}
				
				System.out.println("done.");
				
				login.handle(req);
			}
		});
		
		server.createContext("/", login);
		server.createContext("/index", login);
		server.createContext("/login", login);
		server.createContext("/signup", new StaticPage(new File("web/pages/signup.html")));
		server.createContext("/friends", new StaticPage(new File("web/pages/friends.html")));
		server.createContext("/recommendations", new StaticPage(new File("web/pages/recommendations.html")));
		server.start();
	}
}
