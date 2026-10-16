"""Tiny demo API used to showcase the CI/CD pipeline."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            body, code = {"status": "ok"}, 200
        elif self.path == "/":
            body, code = {"app": "demo-api", "env": os.getenv("APP_ENV", "local")}, 200
        else:
            body, code = {"error": "not found"}, 404
        payload = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
