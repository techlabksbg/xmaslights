import http.server
import threading
import urllib.parse
import json

class httpServer():


    class MyHandler(http.server.SimpleHTTPRequestHandler):
        config = None
        def do_GET(self):
            res = "No params..."
            if '?' in self.path:
                pairs = urllib.parse.parse_qs(self.path.split("?")[1])
                print(pairs)
                for key in pairs.keys():
                    self.config[key] = pairs[key][0]  # Only take the first param (might be defined multiple times)
                self.config['configChanged']=True
                res = json.dumps(self.config)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(res, 'UTF-8'))
            

    def __init__(self, config):
        PORT = 15878
        httpServer.MyHandler.config = config
        def runhttpServer():
            with http.server.ThreadingHTTPServer(("", PORT), httpServer.MyHandler) as httpd:
                print("serving http at port", PORT)
                httpd.serve_forever()
        
        t = threading.Thread(target=runhttpServer)
        t.daemon = True  # Shutdown if main thread terminates
        t.start()
