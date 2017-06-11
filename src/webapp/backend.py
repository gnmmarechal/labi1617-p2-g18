import cherrypy
import json
import urllib.request
import sqlite3 as sql
import time
from PIL import Image
import effects
import meme
import os
import glob
from misc_module import remove_extension as rem_ext
from random import choice
from string import ascii_lowercase


class This(object):
    port = 10018  # The port the application is to use
    xcoa = False  # True if running on the xcoa server, False if running on a local machine
    debug = True  # True if in development. Enables extra methods

    class Database(object):
        path = "proj2.db"

# Dict with the this app's configuration:

cherrypy.config.update({"server.socket_port": This.port, })
cherrypy.config.update({"tools.staticdir.root" : True, "tools.staticdir.root" : os.getcwd(),})
baseDir = os.path.dirname(os.path.abspath(__file__))
config = {
  "/":     { "tools.staticdir.root": baseDir },
  "/js":   { "tools.staticdir.on": True,
             "tools.staticdir.dir": "js" },
  "/css":  { "tools.staticdir.on": True,
             "tools.staticdir.dir": "css" },
  "/html": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "html" },
  "/uploads": {"tools.staticdir.dir": True,
               "tools.staticdir.dir": "uploads"},
}


class AppAPI(object):
    def __init__(self):
        pass

    def rm_all(self, path):
        r = glob.glob(path)
        for i in r:
            os.remove(i)

    def get_username(self):
        cherrypy.response.headers['Content-Type'] = 'text/html'
        if This.xcoa:
            return cherrypy.request.headers.get("X-Remote-User")
        return "random-%s@localpc.com" % ''.join(choice(ascii_lowercase) for i in range(5))

    def get_img_id(self):
        cherrypy.response.headers['Content-Type'] = 'text/html'
        length = 10
        id = ""
        while True:
            id = ''.join(choice(ascii_lowercase) for i in range(length))
            # CHECK IF IT EXISTS IN MY DATABASE
            conn = sql.connect("proj2.db")
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS images (id TEXT PRIMARY KEY, type TEXT, author TEXT, timestamp INTEGER, upvotes INTEGER, downvotes INTEGER);""")
            c.execute("""SELECT * FROM images WHERE id="%s"; """ % id)
            conn.commit()
            exist = c.fetchone()
            c.close()
            if exist is None:
                break
            # CHECK IF IT EXISTS IN THEIR DATABASE
            # all = self.listAll()

        return id

    def db(self, database, sql_commands):
        try:
            result = database.execute(sql_commands)
            return result
        except Exception as e:
            print("ERROR: " + str(e))
            return -1
        return -2

    @cherrypy.expose
    def kill(self):
        cherrypy.response.headers['Content-Type'] = 'text/html'
        if This.debug:
            cherrypy.engine.exit()
            return "Killed server."
        else:
            return "Not in debug mode."

    @cherrypy.expose
    def clean(self):
        cherrypy.response.headers['Content-Type'] = 'text/html'
        if This.debug:
            os.remove("proj2.db")
            self.rm_all("temp/*")
            self.rm_all("temp2/*")
            self.rm_all("uploads/*")
            return "Cleaned"
        else:
            return "Not in debug mode."

    @cherrypy.expose
    def vote(self, id=None, vote=None):
        uid = self.get_username()
        cherrypy.response.headers['Content-Type'] = 'text/html'
        # Add check for existence of image here
        if str(vote) != "-1" and str(vote) != "1":
            return """<a href="vote?id=%s&vote=1">Upvote</a><br><a href="vote?id=%s&vote=-1">Downvote</a>""" % (id, id)

        # Update table with vote value
        conn = sql.connect("proj2.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS votes ( collective_id TEXT); """)
        c.execute("""CREATE TABLE IF NOT EXISTS images (id TEXT PRIMARY KEY, type TEXT, author TEXT, timestamp INTEGER, upvotes INTEGER, downvotes INTEGER);""")

        c.execute("""SELECT * FROM images WHERE id="%s"; """ % id)
        conn.commit()
        exist = c.fetchone()
        c.execute("""SELECT * FROM votes WHERE (collective_id="%s"); """ % (uid + "!!!" + id))
        conn.commit()
        exist1 = c.fetchone()
        if (exist is not None) and (exist1 is None):
            c.execute("""INSERT INTO votes VALUES ( "%s");""" % (uid + "!!!" + id))
            if str(vote) == "1":
                c.execute("""UPDATE images SET upvotes=upvotes+1 WHERE id="%s"; """ % id)
            else:
                c.execute("""UPDATE images SET downvotes=downvotes+1 WHERE id="%s"; """ % id)
        conn.commit()
        return """<meta http-equiv="refresh" content="0; url=../gallery" />"""

    @cherrypy.expose
    def list(self):
        cherrypy.response.headers['Content-Type'] = 'text/html'
        conn = sql.connect("proj2.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS votes ( collective_id TEXT); """)
        c.execute("""CREATE TABLE IF NOT EXISTS images (id TEXT PRIMARY KEY, type TEXT, author TEXT, timestamp INTEGER, upvotes INTEGER, downvotes INTEGER);""")
        c.execute("""SELECT * FROM images;""")
        conn.commit()
        json_as_dict = []
        for row in c:
            json_elem_as_dict = {
                "id": row[0],
                "votes_up": row[4],
                "votes_down": row[5],
                "category": row[1],
                "author": row[2]
            }
            json_as_dict.append(json_elem_as_dict)
        c.close()
        return json.dumps(json_as_dict)

    @cherrypy.expose
    def get(self, id="teast"):
        conn = sql.connect("proj2.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS images (id TEXT PRIMARY KEY, type TEXT, author TEXT, timestamp INTEGER, upvotes INTEGER, downvotes INTEGER);""")
        c.execute("""SELECT * FROM images WHERE id="%s"; """ % id)
        conn.commit()
        exist = c.fetchone()
        c.close()
        cherrypy.response.headers['Content-Type'] = "image/png"
        if exist is None:
            return open("404.png", "rb").read()
        else:
            return open("uploads/" + id + ".png", "rb").read()

    @cherrypy.expose
    def listAll(self):
        cherrypy.response.headers['Content-Type'] = 'text/html'
        # Get all online apps, then request /api/list from each of them and store that.
        apps_port = urllib.request.urlopen("http://xcoa.av.it.pt/labi1617-p2-list").read().decode("utf-8")[1:-1].split(",")
        dict_response = {}
        for port in apps_port:
            og_port = port
            port = int(port)
            server = "http://127.0.0.1:" + str(port) + "/api/list"
            if not This.xcoa:
                if port < 10010:
                    port -= 10000
                else:
                    port = int(str(port)[3:])
                server = "http://xcoa.av.it.pt/labi1617-p2-g" + str(port) + "/api/list"
            try:
                dict_response[og_port] = urllib.request.urlopen(server).read().decode("utf-8")
            except Exception as e:
                print("URL: " + server + " PORT:" + og_port + "ERROR: " + str(e))
        if not This.xcoa:  # If the computer is not xcoa, obtain the information for it and add it to the dictionary.
            dict_response[str(This.port)] = str(self.list())

        return json.dumps(dict_response)

    @cherrypy.expose
    def put(self, image, type, args):  # args --> effect!,!text!,!textup por exemplo
        cherrypy.response.headers['Content-Type'] = 'text/html'
        if not type == "MEME" and type == "EFFECT" and type == "PHOTO":
            return -1
        image_id = self.get_img_id()
        author = self.get_username()
        timestamp = int(time.time())
        fo = open("temp/" + image.filename, "wb")
        while True:
            data = image.file.read(8192)
            if not data:
                break
            fo.write(data)
        fo.close()
        #method = getattr(effects, args)
        #res = effects.effect_image("temp/" + image.filename, method)
        #return
        im = Image.open("temp/" + image.filename)
        im.thumbnail((640,480))
        im.save("temp2/" + str(image_id) + ".png")
        os.remove("temp/" + image.filename)
        #sql_query2 = "INSERT INTO images VALUES ("str(image_id) + "\", \"" + str(type) + "\", \"" + str(author) + "\", " + str(timestamp) + "," + str(0) + "," + str(0) + ");"
        # Database stuff
        conn = sql.connect("proj2.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS images (id TEXT PRIMARY KEY, type TEXT, author TEXT, timestamp INTEGER, upvotes INTEGER, downvotes INTEGER);""")
        c.execute("""INSERT INTO images VALUES ("%s", "%s", "%s", %s, 0, 0);""" % (str(image_id), str(type), str(author), str(timestamp)))
        conn.commit()

        c.close()
        arg_complete = args.split("&,&")
        for arg in arg_complete:
            am = arg.split("!,!")
            ef_name = am[0]
            if type == "EFFECT":
                method = getattr(effects, ef_name)
                effects.effect_image("temp2/" + str(image_id) + ".png", method)
            elif type == "MEME":
                if am[0] == "add_text":
                    if am[1] == "True":
                        am[1] = True
                    elif am[1] == "False":
                        am[1] = False
                method = getattr(meme, ef_name)

                meme.meme_image("temp2/" + str(image_id) + ".png", method, tuple(am[1:]))

        Image.open("temp2/" + str(image_id) + ".png").save("uploads/" + str(image_id) + ".png")
        os.remove("temp2/" + str(image_id) + ".png")
        return """<meta http-equiv="refresh" content="0; url=../gallery" />"""



class Root(object):
    api = AppAPI()

    @cherrypy.expose
    def index(self):
        cherrypy.response.headers['Content-Type'] = 'text/html'
        # return "<HTML html> <HEAD><TITLE>P2 Labi</TITLE></HEAD><BODY><H1>Hello World</H1></BODY></HTML>"
        return open("html/index.html").read()

    @cherrypy.expose
    def gallery(self):
        partA = """<!doctype html><html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Proj2-Galeria</title><meta name="viewport" content="initial-scale=1, maximum scale=1, user-scalable=no, minimal-ui"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black"><link rel="stylesheet" href="css/ratchet.css"><link rel="stylesheet" href="css/ratchet-theme-android.css"><link rel="stylesheet" href="css/app.css"><script src="js/jquery-2.2.3.min.js"></script><script src="js/ratchet.js"></script></head><body><header class="bar bar-nav"> <button class="btn btn-link btn-nav pull-right" style="pointer-events: none"> <b>Gallery</b> <span class="icon icon-pages"></span> </button> <form action="index"> <button class="btn btn-link btn-nav pull-left"> <span class="icon icon-home"></span> Home </button> <h1 class="title" style="text-align:center"><b>&nbsp;Projeto 2</b></h1> </form> </header><div class="content" ><!--<input type="button" name="" id="" value="Back"></input>-->"""
        partC = """	</div></body></html>"""
        picture_list = json.loads(self.api.list())
        # a = """<img src="api/get?id=%s" >""" % picture_list[0]["id"]
        reply = partA
        for picture in picture_list:
            reply += """<div style="text-align:center"><img src="api/get?id=%s"><br><a href="api/vote?id=%s&vote=1" class="button">   +  (%s) </a><a href="api/vote?id=%s&vote=-1" class="button">   -  (%s) </a><br><br></div>""" % (str(picture["id"]),str(picture["id"]), str(picture["votes_up"]),str(picture["id"]),str(picture["votes_down"]))
        reply += partC
        return reply


cherrypy.quickstart(Root(), "/", config)
