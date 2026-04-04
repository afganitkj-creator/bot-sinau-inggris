from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
        
    def log_message(self, format, *args):
        # Disable logging for each request to keep logs clean
        pass

def run_server():
    # Render uses the PORT environment variable
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

def keep_alive():
    # Start the server in a separate thread so it doesn't block the bot
    t = Thread(target=run_server)
    t.daemon = True
    t.start()
