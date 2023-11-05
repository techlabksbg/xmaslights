import http.server
import threading
import urllib.parse
import json
import re
import os

class httpServer():


    class MyHandler(http.server.SimpleHTTPRequestHandler):

        def processQuery(self):
            pairs = urllib.parse.parse_qs(self.path.split("?")[1])
            print(pairs)
            for key in pairs.keys():
                self.config.parsePair(key, pairs[key][0]) # Only take the first param (might be defined multiple times)
            res = json.dumps(self.config.config)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(res, 'UTF-8'))

        def serveFile(self):

            def sanitizePath(path):
                path = re.sub('\.\.+', '', path)  # Remove every occurence of two or more consecutive dots
                path = re.sub('//+', '/', path)  # Replace multiple consecutive slashes by a single slash
                path = re.sub('^/', '', path)   # Remove leading slash 
                if path=="":
                    path="index.html"
                path = "web/"+path
                if not (os.path.exists(path) and os.path.isfile(path)):
                    path = "web/index.html"
                return path


            path = sanitizePath(self.path)

            print(f"Serving {path}")
            t = {'tml':'text/html', '.js':'text/javascript', 'css':'text/css', 'png':'image/png', "ico":"image/icon"}
            ext = path[-3:]
            if not ext in t:
                print(f"WARNING: Unknown extension {ext}")
                path = "web/index.html"
                ext = "tml"

            self.send_response(200)
            self.send_header('Content-type', t[path[-3:]])
            self.end_headers()

            # Binary files
            if ext in ["png", "ico"]: 
                with open(path, "rb") as fb:
                    self.wfile.write(fb.read())
            else: # Text files
                with open(path, "r") as f:
                    self.wfile.write(bytes(f.read(), "UTF-8"))


        def do_GET(self):
            print(f"GET {self.path}")
            if '?' in self.path:
                self.processQuery()
            else:
                self.serveFile()

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
