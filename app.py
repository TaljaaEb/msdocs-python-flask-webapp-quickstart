# a_sql_monitor.py
#from http.server import BaseHTTPRequestHandler, HTTPServer
#
## --- DATA ---
#transactions = [
#    "101 18V Cordless Drill 2 89.99",
#    "102 6-inch Wood Clamp 4 12.50",
#    "103 Carpenter's Hammer 1 19.99"
#]
#
#class Handler(BaseHTTPRequestHandler):
#    def do_GET(self):
#        if self.path == "/transactions":
#            self.send_response(200)
#            self.send_header("Content-type", "text/plain")
#            self.end_headers()
#            for t in transactions:
#                self.wfile.write(f"<item>{t}</item>\n".encode())
#        else:
#            self.send_response(404)
#            self.end_headers()
#            self.wfile.write(b"Not Found")
#
#def run(server_class=HTTPServer, handler_class=Handler, host="0.0.0.0", port=8000):
#    server_address = (host, port)
#    httpd = server_class(server_address, handler_class)
#    print(f"[A] Serving transactions at http://{host}:{port}/transactions")
#    httpd.serve_forever()
#
#if __name__ == "__main__":
#    run()
import os
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, Response

app = Flask(__name__)

# --- DATA ---
transactions = [
    "101 18V Cordless Drill 2 89.99",
    "102 6-inch Wood Clamp 4 12.50",
    "103 Carpenter's Hammer 1 19.99"
]

# --- ROUTES ---

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
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

@app.route('/transactions', methods=['GET'])
def get_transactions():
    # Serve transactions in simple XML-like format (similar to original)
    print("Request for transactions list received")
    output = "".join(f"<item>{t}</item>\n" for t in transactions)
    return Response(output, mimetype="text/plain")


if __name__ == '__main__':
    # Flask defaults to 127.0.0.1:5000, override for external binding if needed
    #app.run(host="0.0.0.0", port=5000)
    app.run()

