#!/usr/bin/env python3
"""
Simple HTTP server for Trinexial Technologies Mock Aptitude Test
Handles test submission and email sending
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
from email_service import send_test_scorecard

class TrinexialTestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve static files"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('index.html', 'text/html')
        elif self.path == '/styles.css':
            self.serve_file('styles.css', 'text/css')
        elif self.path == '/app.js':
            self.serve_file('app.js', 'application/javascript')
        else:
            self.send_error(404, "File not found")
    
    def do_POST(self):
        """Handle test submission"""
        if self.path == '/submit-test':
            self.handle_test_submission()
        else:
            self.send_error(404, "Endpoint not found")
    
    def serve_file(self, filename, content_type):
        """Serve static file"""
        try:
            with open(filename, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")
    
    def handle_test_submission(self):
        """Handle test submission and send email"""
        try:
            # Get content length
            content_length = int(self.headers['Content-Length'])
            
            # Read POST data
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract user and score data
            user_data = {
                'name': data.get('name', ''),
                'email': data.get('email', ''),
                'roll': data.get('roll', '')
            }
            
            score_data = {
                'score': data.get('score', 0),
                'total': data.get('total', 0),
                'answers': data.get('answers', []),
                'questions': data.get('questions', []),
                'violations': data.get('violations', 0)
            }
            
            # Send email in background thread
            email_thread = threading.Thread(
                target=self.send_email_async,
                args=(user_data, score_data)
            )
            email_thread.daemon = True
            email_thread.start()
            
            # Send response
            response = {
                'success': True,
                'message': 'Test submitted successfully. Scorecard will be sent to your email shortly.',
                'email_sent': True
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            print(f"Error handling test submission: {str(e)}")
            
            response = {
                'success': False,
                'message': f'Error processing submission: {str(e)}',
                'email_sent': False
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def send_email_async(self, user_data, score_data):
        """Send email asynchronously"""
        try:
            success = send_test_scorecard(user_data, score_data)
            if success:
                print(f"Scorecard email sent to {user_data.get('email')}")
            else:
                print(f"Failed to send email to {user_data.get('email')}")
        except Exception as e:
            print(f"Email sending error: {str(e)}")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8000):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, TrinexialTestHandler)
    
    print(f"Trinexial Technologies Mock Test Server")
    print(f"Server running on http://localhost:{port}")
    print(f"Make sure to set GMAIL_APP_PASSWORD environment variable for email functionality")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8000.")
    
    run_server(port)
