from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        with open("events.jsonl", "a", encoding="utf-8") as f:
            f.write(body + "\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()