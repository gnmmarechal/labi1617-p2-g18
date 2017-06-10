import cherrypy
import json
import socket
import net_funcs
import urllib.request
import ast


class This(object):
    port = 10018
    xcoa = False

cherrypy.config.update({"server.socket_port": This.port, })


class AppAPI(object):
    def __init__(self):
        pass

    def get_username(self):
        return cherrypy.request.headers.get("X-Remote-User")

    @cherrypy.expose
    def vote(self, id=None, uid=None, vote=None):
        # Add check for existence of image here
        if str(vote) != "-1" and str(vote) != "1":
            return "{ 'msg': 'WRONG VOTE', 'code': '1', 'vote':" + str(vote) + "}"

        # Update table with vote value
        return "The user " + str(uid) + " voted " + str(vote)

    @cherrypy.expose
    def list(self):
        return

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
        json_response = json.dumps(dict_response)

        return json_response

    @cherrypy.expose
    def put(self):
        return


class Root(object):
    api = AppAPI()

    @cherrypy.expose
    def index(self):
        return "<HTML html> <HEAD><TITLE>P2 Labi</TITLE></HEAD><BODY><H1>Hello World</H1></BODY></HTML>"


cherrypy.quickstart(Root())
