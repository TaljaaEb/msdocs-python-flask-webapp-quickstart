# merged_app.py

import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from flask import Flask, redirect, render_template, request, send_from_directory, url_for

# --- DATA ---
transactions = [
    "101 18V Cordless Drill 2 89.99",
    "102 6-inch Wood Clamp 4 12.50",
    "103 Carpenter's Hammer 1 19.99"
]

# -------------------------
# Legacy HTTPServer Handler
# -------------------------
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/transactions":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            for t in transactions:
                self.wfile.write(f"<item>{t}</item>\n".encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

def run_http_server(host="0.0.0.0", port=8081):
    server_address = (host, port)
    httpd = HTTPServer(server_address, Handler)
    print(f"[A] Legacy server at http://{host}:{port}/transactions")
    httpd.serve_forever()

# -------------------------
# Flask App
# -------------------------
app = Flask(__name__)

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')
    if name:
        print(f'Request for hello page received with name={name}')
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name -- redirecting')
        return redirect(url_for('index'))

# -------------------------
# Flask transactions route
# -------------------------
@app.route('/transactions', methods=['GET'])
def get_transactions():
    global Handler  # <-- equivalent to exposing legacy do_GET
    return "\n".join(f"<item>{t}</item>" for t in transactions)

# -------------------------
# Runner
# -------------------------
if __name__ == '__main__':
    # Start legacy HTTP server in background thread
    t = threading.Thread(target=run_http_server, daemon=True)
    t.start()

    # Start Flask server
    print("[B] Flask server at http://127.0.0.1:5000/")
    #app.run(host="0.0.0.0", port=5000)
    app.run()
