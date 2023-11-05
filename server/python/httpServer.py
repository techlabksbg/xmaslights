import http.server
import http.cookies
import threading
import urllib.parse
import json
import re
import os
import uuid
import time

class httpServer():

    class Session:
        def __init__(self):
            self.ping()

        def ping(self):
            self.lastRequest = time.time()
        
        def age(self):
            return time.time()-self.lastRequest
    
    class Sessions:
        def __init__(self):
            self.sessions={}
        
        def start(self, request):
            cookies = {}
            cookies_string = request.headers.get('Cookie')
            if cookies_string:
                cookies = http.cookies.Cookie.SimpleCookie()
                cookies.load(cookies_string)
            if 'xmascookie' in cookies:
                sessionid = cookies['xmascookie'].value
                if sessionid in self.sessions:
                    self.sessions[sessionid].ping()
                    return self.sessions[sessionid]
            sessionid = str(uuid.uuid4)
            cookies = http.cookies.Cookie.SimpleCookie()
            cookies['xmascookie'] = sessionid 
            for morsel in cookies.values():
                request.send_header("Set-Cookie", morsel.OutputString())
            self.sessions[sessionid] = httpServer.Session() 


    class MyHandler(http.server.SimpleHTTPRequestHandler):

        def __init__(self):
            self.sessions=httpServer.Sessions()

        def startSession(self):
            self.session = self.sessions.start(self)

        def processQuery(self):
            pairs = urllib.parse.parse_qs(self.path.split("?")[1])
            print(pairs)
            for key in pairs.keys():
                self.config.parsePair(key, pairs[key][0], self.session.age()) # Only take the first param (might be defined multiple times)
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
            self.startSession()
            if '?' in self.path:
                self.processQuery()
            else:
                self.serveFile()
            self.session.ping()

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
