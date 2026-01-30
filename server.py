#!/usr/bin/env python3
"""
OpenHamClock Development Server

A simple HTTP server for OpenHamClock with API proxy capabilities.
This allows the application to fetch live data from external sources
without CORS issues.

Usage:
    python3 server.py [port]
    
    Default port: 8080
    Open http://localhost:8080 in your browser

Requirements:
    Python 3.7+
    requests library (optional, for API proxy)
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
import sys
import os
from datetime import datetime

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

# API endpoints for live data
API_ENDPOINTS = {
    'solarflux': 'https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-flux.json',
    'kindex': 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json',
    'xray': 'https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json',
    'sunspots': 'https://services.swpc.noaa.gov/json/solar-cycle/sunspots.json',
    'pota': 'https://api.pota.app/spot/activator',
    'bands': 'https://www.hamqsl.com/solarxml.php',  # HamQSL solar data
}

class OpenHamClockHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler with API proxy support."""
    
    def do_GET(self):
        # Handle API proxy requests
        if self.path.startswith('/api/'):
            self.handle_api()
        else:
            # Serve static files
            super().do_GET()
    
    def handle_api(self):
        """Proxy API requests to avoid CORS issues."""
        endpoint = self.path.replace('/api/', '').split('?')[0]
        
        if endpoint not in API_ENDPOINTS:
            self.send_error(404, f"Unknown API endpoint: {endpoint}")
            return
        
        try:
            url = API_ENDPOINTS[endpoint]
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching: {url}")
            
            # Make the request
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'OpenHamClock/1.0'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read()
                content_type = response.headers.get('Content-Type', 'application/json')
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'max-age=60')
                self.end_headers()
                self.wfile.write(data)
                
        except urllib.error.URLError as e:
            print(f"[ERROR] Failed to fetch {endpoint}: {e}")
            self.send_error(502, f"Failed to fetch data: {e}")
        except Exception as e:
            print(f"[ERROR] {e}")
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        """Custom logging format."""
        if args[0].startswith('GET /api/'):
            return  # Already logged in handle_api
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def main():
    # Change to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=" * 50)
    print("  OpenHamClock Development Server")
    print("=" * 50)
    print()
    print(f"  Serving from: {script_dir}")
    print(f"  URL: http://localhost:{PORT}")
    print(f"  Press Ctrl+C to stop")
    print()
    print("  Available API endpoints:")
    for name, url in API_ENDPOINTS.items():
        print(f"    /api/{name}")
    print()
    print("=" * 50)
    print()
    
    with socketserver.TCPServer(("", PORT), OpenHamClockHandler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()
