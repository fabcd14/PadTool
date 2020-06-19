from plugins import templateATC

from urllib.parse import urlparse, parse_qs
from io import BytesIO
from threading import Thread

import html
import http.server
import json
import base64
import os
#import cgi
import glob
from misc import indexPage

class CustomServerHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_authHead(self):
        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Basic realm="PadTool Web Interface"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        key = self.server.get_auth_key()
        cfg = self.server.getCfg()

        if self.headers.get('Authorization') == None:
            self.do_authHead()

            response = {
                'success': False,
                'error': 'No auth header received'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif(self.headers.get('Authorization') == 'Basic ' + str(key)):
            query = urlparse(self.path).query
            try:
                if(self.path.startswith("/atc") and cfg.get('general', 'mode') == "server"):
                    self._set_headers()
                    try:
                        artist = ""
                        title = ""
                        cover = ""
                        getData = json.dumps(parse_qs(urlparse(self.path).query))
                        for k, v in json.loads(getData).items():
                            val = ""
                            if(isinstance(v, list)):
                                val = str(v[0])
                            else:
                                val = str(v)

                            if(k == "artist"):
                                artist = val
                            elif(k == "title"):
                                title = val
                            elif(k == "cover"):
                                cover = val
                        
                        templateATC.generate(cfg, mode="server", artistFromServer=artist, titleFromServer=title, coverFromServer=cover)

                        response = {
                            'success': True,
                            'artist': artist,
                            'title': title,
                            'cover': cover
                        }
                        self.wfile.write(bytes(json.dumps(response), 'utf-8'))
                    except Exception as ex:
                        response = {
                            'success': False,
                            'error': "Missing one of 'artist' or 'title' tags",
                            'details': str(ex)
                        }
                        self.wfile.write(bytes(json.dumps(response), 'utf-8'))
                elif(self.path.startswith("/config")):
                    self._set_headers()
                    d = dict()
                    
                    for sect in cfg.sections():
                        d2 = dict()
                        for k,v in cfg.items(sect):
                            d2.update({k:v},)
                        d.update({sect:d2})
                    self.wfile.write(bytes(json.dumps(d), 'utf-8'))
                elif(self.path.startswith("/slide/sls")):
                    self._set_headers()
                    outFolder = cfg.get('general', 'outFolder')
                    listFilesDabCtlSls = [os.path.basename(x) for x in glob.glob(outFolder + '/*.jpg')]
                    self.wfile.write(bytes(json.dumps(listFilesDabCtlSls), 'utf-8'))
                elif(self.path.startswith("/slide/dls")):
                    self._set_headers()
                    dictDls = dict()
                    try:
                        outFile = cfg.get('dls', 'outFile')
                        f = open(outFile, "r")
                        lastLine = f.readlines()[-1]
                        baseFileName = os.path.basename(cfg.get('dls', 'outFile'))
                        f.close()
                        dictDls.update({baseFileName:lastLine})
                        self.wfile.write(bytes(json.dumps(dictDls), 'utf-8'))
                    except:
                        if(cfg.get('general', 'mode') == "dabctl"):
                            outFolder = "/tmp/PadTool-" + str(os.getpid())
                        else:
                            outFolder = cfg.get('general', 'outFolder')
                        listFilesDabCtlDls = [os.path.basename(x) for x in glob.glob(outFolder + '/*.txt')]
                        for curFile in listFilesDabCtlDls:
                            f = open(outFolder + "/" + curFile, "r")
                            lastLine = f.readlines()[-1]
                            dictDls.update({curFile:lastLine})
                            f.close()
                        self.wfile.write(bytes(json.dumps(dictDls), 'utf-8'))
                elif(self.path.startswith("/slide/")):
                    path = self.path.replace("/slide/", "")
                    if(cfg.get('general', 'mode') == "dabctl"):
                        pathToImg = "/tmp/PadTool-" + str(os.getpid()) + "/" + path
                    else:
                        pathToImg = cfg.get('general', 'outFolder') + "/" + path
                    try:
                        pathToImg = pathToImg.split("?")[0]
                    except:
                        pass
                    f = open(pathToImg, 'rb')
                    self.send_response(200)
                    self.send_header("Content-type", "image/jpg")
                    self.send_header("Content-length", os.stat(pathToImg).st_size)
                    self.end_headers() 
                    self.wfile.write(f.read())
                    f.close()
                elif(self.path == "/"):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    idxP = indexPage.generate()
                    idxP = idxP.replace("$radioName", cfg.get('general', 'radioName'))
                    idxP = idxP.replace("$slogan", cfg.get('general', 'slogan'))
                    self.wfile.write(bytes(idxP, 'utf-8'))
                else:
                    raise Exception("Identifier not recognized")

            except Exception as ex:
                response = {
                    'success': False,
                    'error': 'Bad Query',
                    'details': str(ex)
                }
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            self.do_authHead()

            response = {
                'success': False,
                'error': 'Invalid credentials'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_POST(self):
        key = self.server.get_auth_key()
        cfg = self.server.getCfg()

        if self.headers.get('Authorization') == None:
            self.do_authHead()

            response = {
                'success': False,
                'error': 'No auth header received'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif(self.headers.get('Authorization') == 'Basic ' + str(key)):
            try:
                if(self.path.startswith("/azuracast") and cfg.get('general', 'mode') == "server"):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                    post_data = self.rfile.read(content_length) # <--- Gets the data itself
                    jsonF = json.loads(post_data)
                    artist = jsonF['now_playing']['song']['artist']
                    title = jsonF['now_playing']['song']['title']
                    cover = jsonF['now_playing']['song']['art']

                    artist, title = templateATC.generate(cfg, mode="server", artistFromServer=artist, titleFromServer=title, coverFromServer=cover)
                    response = {
                        'success': True,
                        'artist': artist,
                        'title': title,
                        'cover': cover
                    }
                    self.wfile.write(bytes(json.dumps(response), 'utf-8'))
                elif(cfg.get('general', 'mode') == "server"):
                    length = int(self.headers['Content-Length'])
                    post_data = parse_qs(self.rfile.read(length).decode('utf-8'))
                    post_data = json.dumps(post_data)
                
                    if(self.path.startswith("/atc")):
                        self._set_headers()
                        artist = ""
                        title = ""
                        cover = ""
                        d = json.loads(post_data)
                        for k,v in d.items():
                            val = ""
                            if(isinstance(v, list)):
                                val = v[0]
                            else:
                                val = v

                            if(k == "artist"):
                                artist = val
                            elif(k == "title"):
                                title = val
                            elif(k == "cover"):
                                cover = val

                        if(artist != "" and title != ""):
                            artist, title = templateATC.generate(cfg, mode="server", artistFromServer=artist, titleFromServer=title, coverFromServer=cover)
                            response = {
                                'success': True,
                                'artist': artist,
                                'title': title,
                                'cover': cover
                            }
                            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
                        else:
                            response = {
                                'success': False,
                                'error': "Missing one of 'artist' or 'title' tags",
                                'details': str(ex)
                            }
                            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
                    else:
                        raise Exception("Identifier not recognized")
                else:
                    raise Exception("Request received but actual mode is : " + cfg.get('general', 'mode'))
            except Exception as ex:
                response = {
                    'success': False,
                    'error': 'Bad Query',
                    'details': str(ex)
                }
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_PUT(self):
        self.do_POST()
    
    def log_message(self, format, *args):
        return


class CustomHTTPServer(http.server.HTTPServer):
    key = ''
    cfg = None

    def __init__(self, address, handlerClass=CustomServerHandler):
        super().__init__(address, handlerClass)

    def set_auth(self, username, password):
        self.key = base64.b64encode(
            bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key

    def getCfg(self):
        return self.cfg

    def setCfg(self, cfg):
        self.cfg = cfg

def launchWebServer(cfg, port, user, pwd):
    host = '0.0.0.0'
    server = CustomHTTPServer(('0.0.0.0', int(port)))
    server.set_auth(user, pwd)
    server.setCfg(cfg)
    server.serve_forever()

class Server(Thread):
    def __init__(self, cfg, port, user, pwd):
        Thread.__init__(self)
        self.cfg = cfg
        self.port = port
        self.user = user
        self.pwd = pwd

    def run(self):
        launchWebServer(self.cfg, self.port, self.user, self.pwd)