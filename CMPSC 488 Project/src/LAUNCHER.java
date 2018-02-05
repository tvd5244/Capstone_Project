
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.IOException;
import java.net.InetSocketAddress;
import com.sun.net.httpserver.HttpServer;
import java.io.PrintStream;
import java.io.UnsupportedEncodingException;

public class LAUNCHER {
	
	public static void main(String[] args) 
		throws IOException {
		HttpServer server = HttpServer.create(new InetSocketAddress(80), 0);
		server.createContext("/", new HttpHandler() {
			public void handle(HttpExchange req) 
				throws IOException {
				PrintStream out = new PrintStream(req.getResponseBody());
				
				String res = "<html>"
				+ "<body>"
				+ "<p>Hello World!</p>"
				+ "</body>"
				+ "</html>";
				
				req.sendResponseHeaders(200, res.getBytes("UTF-8").length);
				out.print(res);
				
				out.close();
			}
		});
		server.start();
	}
}
