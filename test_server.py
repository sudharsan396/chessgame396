#!/usr/bin/env python3
"""
Simple HTTP server to test the chess web app locally
"""
import http.server
import socketserver
import os
from urllib.parse import unquote

class ChessWebHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for Pyodide
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # Handle requests
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

def run_server(port=8000):
    """Run the local web server"""
    os.chdir('web-app')

    with socketserver.TCPServer(("", port), ChessWebHandler) as httpd:
        print(f"Chess Web App Server running at http://localhost:{port}")
        print("Open your browser and navigate to the URL above")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()