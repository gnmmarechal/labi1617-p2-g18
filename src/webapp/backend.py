import cherrypy
import json
import urllib.request
import sqlite3 as sql
import time
from PIL import Image
import effects
from meme import *
import os
from misc_module import remove_extension as rem_ext

class This(object):
    port = 10018  # The port the application is to use
    xcoa = False  # True if running on the xcoa server, False if running on a local machine
    debug = True  # True if in development. Enables extra methods

    class Database(object):
        path = "proj2.db"

cherrypy.config.update({"server.socket_port": This.port, })


class AppAPI(object):
    def __init__(self):
        pass

    def get_username(self):
        return cherrypy.request.headers.get("X-Remote-User")

    def create_img_id(self):
        return "test"

    def db(self, database_path, sql_commands):
        try:
            database = sql.connect(database_path)
            result = database.execute(sql_commands)
            database.close()
            return result
        except Exception as e:
            print("ERROR: " + str(e))
            return -1
        return -2

    @cherrypy.expose
    def kill(self):
        if This.debug:
            cherrypy.engine.exit()
            return "Killed server."
        else:
            return "Not in debug mode."

    @cherrypy.expose
    def vote(self, id=None, uid=None, vote=None):
        # Add check for existence of image here
        if str(vote) != "-1" and str(vote) != "1":
            return "{ 'msg': 'WRONG VOTE', 'code': '1', 'vote':" + str(vote) + ", 'status': 'ERROR'}"

        # Update table with vote value
        return "The user " + str(uid) + " voted " + str(vote)

    @cherrypy.expose
    def list(self):
        return "[]"

    @cherrypy.expose
    def listAll(self):
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
            dict_response[str(This.port)] = str(list())
        json_response = json.dumps(dict_response)

        return json_response

    @cherrypy.expose
    def put(self, image, type, args):  # args --> effect!,!text!,!textup por exemplo
        if not type == "MEME" and type == "EFFECT" and type == "PHOTO":
            return -1
        image_id = create_img_id()
        author = get_username()
        timestamp = time.time()
        fo = open("temp/" + image.filename, "wb")
        while True:
            data = image.file.read(8192)
            if not data:
                break
            fo.write(data)
        fo.close()
        im = Image.open("temp/" + image.filename)
        im.save("uploads/" + image_id + ".png")
        os.remove("temp/" + image.filename)

        db(This.Database.path, "CREATE TABLE IF NOT EXISTS images (id TEXT, type TEXT, author TEXT, timestamp INTEGER, upvotes INTEGER, downvotes INTEGER")
        db(This.Database.path, "INSERT INTO images VALUES (" + image_id + ", " + type + ", " + author + ", " + timestamp + ")")
        arg_complete = args.split("&,&")
        for arg in arg_complete:
            am = arg.split("!,!")
            ef_name = am[0]
            if type == "EFFECT":
                method = getattr(effects, ef_name)
                res = effects.effect_image("temp/" + image_id + ".png", method)
            return 0


class Root(object):
    api = AppAPI()

    @cherrypy.expose
    def index(self):
        return "<HTML html> <HEAD><TITLE>P2 Labi</TITLE></HEAD><BODY><H1>Hello World</H1></BODY></HTML>"


cherrypy.quickstart(Root())