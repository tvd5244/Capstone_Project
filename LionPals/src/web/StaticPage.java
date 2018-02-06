package web;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;

public class StaticPage 
	implements HttpHandler {
	File file;
	
	public StaticPage(File file) {
		this.file = file;
	}
	
	public void handle(HttpExchange req) 
		throws IOException, 
		FileNotFoundException {
		FileInputStream in = new FileInputStream(file);
		PrintStream out = new PrintStream(req.getResponseBody());
		byte[] bytes = new byte[(int)file.length()];
		
		req.sendResponseHeaders(200, bytes.length);
		in.read(bytes, 0, bytes.length);
		out.write(bytes, 0, bytes.length);
		out.close();
		in.close();
	}
}
