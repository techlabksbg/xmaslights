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
        def __init__(self, sessionid):
            self.sessionid= sessionid
            self.new = True
            self.ping()

        def ping(self):
            self.lastRequest = time.time()
        
        def age(self):
            return time.time()-self.lastRequest

        def setCookie(self, handler):
            self.new = False
            cookies = http.cookies.SimpleCookie()
            cookies['xmascookie'] = self.sessionid
            for morsel in cookies.values():
                morsel['max-age']=180  # Delete cookie after 3 minutes
                handler.send_header("Set-Cookie", morsel.OutputString())

    
    class Sessions:
        def __init__(self):
            self.sessions={}
        
        def start(self, request):
            self.purge()  # Remove old sessions
            cookies = {}
            cookies_string = request.headers.get('Cookie')
            #print(f"cookies_string: {cookies_string}")
            if cookies_string:
                cookies = http.cookies.SimpleCookie()
                cookies.load(cookies_string)
            # print(f"cookies = {cookies}")
            if 'xmascookie' in cookies:
                sessionid = cookies['xmascookie'].value
                #print(f"We have a xmascookie with value {sessionid}")
                if sessionid in self.sessions:
                    #print(f"And already stored this session with age {self.sessions[sessionid].age()}")
                    return self.sessions[sessionid]
            sessionid = str(uuid.uuid4())
            #print(self.sessions)
            self.sessions[sessionid] = httpServer.Session(sessionid)
            # print(f"Generated new sessionid {sessionid}")
            return self.sessions[sessionid]

        # Delete old sessions
        def purge(self):
            self.sessions = {k:v for k,v in self.sessions.items() if v.age()<180}  # Only keep cookies younger than 3 minutes

        def remove(self, session):
            if session.sessionid in self.sessions:
                del self.sessions[session.sessionid]

    class MyHandler(http.server.SimpleHTTPRequestHandler):

        def startSession(self):
            self.session = self.sessions.start(self)

        def processQuery(self):
            pairs = urllib.parse.parse_qs(self.path.split("?")[1])
            measuring = ('led' in pairs and 'prg' in pairs and pairs['prg'][0] == "SingleLED")
            if (not self.session.new) or measuring: # No valid cookie? No dough! (Except for measuring)
                for key in pairs.keys():
                    self.config.parsePair(key, pairs[key][0], 9999 if measuring else self.session.age()) # Only take the first param (might be defined multiple times)
            else:
                pass
                #print("still a new session: "+self.session.sessionid)
            res = self.config.toJSON()
            self.send_response(200)
            if (not measuring):
                self.session.setCookie(self)
            else: # remove session when measuring
                self.sessions.remove(self.session)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(res, 'UTF-8'))

        def serveFile(self):

            def sanitizePath(path):
                path = re.sub('\.\.+', '', path)  # Remove every occurence of two or more consecutive dots
                path = re.sub('//+', '/', path)  # Replace multiple consecutive slashes by a single slash
                path = re.sub('^/', '', path)   # Remove leading slash
                allowed = self.ipAllowed()
                if not allowed and path=="index.html":
                    path = "outside.html"
                if path=="":
                    if allowed:
                        path="index.html"
                    else:
                        path="outside.html"
                path = "web/"+path
                if not (os.path.exists(path) and os.path.isfile(path)):
                    if allowed:
                        path = "web/index.html"
                    else:
                        path = "web/outside.html"
                return path


            path = sanitizePath(self.path)

            #print(f"Serving {path}")
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

        def ipAllowed(self):
            if 'X-Forwarded-For' in self.headers:
                ip = self.headers['X-Forwarded-For'].split(",")[0]
                return ("141.195.93." in ip or "83.150.5." in ip or "192.168.1." in ip)
            return True

        def permissionDenied(self):
            self.send_response(403)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Nope, not from this network, sorry. Really sorry. Terribly sorry even :-(")


        def do_GET(self):
            self.startSession()
            if '?' in self.path:
                if self.ipAllowed():
                    self.processQuery()
                    self.config.lastHttpRequest = time.time()
                else:
                    self.permissionDenied()
            else:
                self.serveFile()
            self.session.ping()  # Store last access time

    def __init__(self, config):
        PORT = 15878
        httpServer.MyHandler.config = config
        httpServer.MyHandler.sessions = httpServer.Sessions()
        def runhttpServer():
            with http.server.ThreadingHTTPServer(("", PORT), httpServer.MyHandler) as httpd:
                #print("serving http at port", PORT)
                httpd.serve_forever()
        
        self.thread = threading.Thread(target=runhttpServer)
        self.thread.daemon = True  # Shutdown if main thread terminates
        self.thread.start()
