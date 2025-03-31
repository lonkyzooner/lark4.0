#!/usr/bin/env python3
"""
Simple HTTP server for LARK LiveKit implementation on UniHiker
"""
import http.server
import socketserver
import os
import argparse

# Default port
DEFAULT_PORT = 8080

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='LARK LiveKit server for UniHiker')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help=f'Port to listen on (default: {DEFAULT_PORT})')
    args = parser.parse_args()
    
    # Directory containing the HTML file
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Create custom handler with directory
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
        
        def end_headers(self):
            # Add CORS headers to allow accessing resources from any origin
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    # Create and start the server
    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        print(f"Starting LARK server at http://localhost:{args.port}")
        print(f"Serving files from: {directory}")
        print("Press Ctrl+C to stop")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    main()
