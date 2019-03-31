from http.server import HTTPServer, BaseHTTPRequestHandler
import gpiozero
import sys

# Pin where our relay is connected to
RELAY_PIN = 18
relay = gpiozero.OutputDevice(RELAY_PIN, active_high=True, initial_value=False)

class RequestHandler(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write(b'ON' if relay.value == 1 else b'OFF')
    
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_body = self.rfile.read(content_length)

        if post_body == b'ON':
            relay.on()
        elif post_body == b'OFF':
            relay.off()

        self._set_response()

try:
    port = int(sys.argv[1])
    print("Listening on port " + str(port))
    server = HTTPServer(("", port), RequestHandler)
    server.serve_forever()
except (ValueError, IndexError):
    print("Usage: python3 " + sys.argv[0] + " <port>")
except KeyboardInterrupt:
    print("Bye")
