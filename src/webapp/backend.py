import cherrypy

cherrypy.config.update({"server.socket_port": 10018, })


class AppAPI(object):
    def __init__(self):
        pass

    @cherrypy.expose
    def vote(self, id=None, uid=None, vote=None):
        return "The user " + str(uid) + " voted " + str(vote)

    @cherrypy.expose
    def list(self):
        return
    @cherrypy.expose
    def listAll(self):
        return



class Root(object):
    api = AppAPI()

    @cherrypy.expose
    def index(self):
        return "<HTML html> <HEAD><TITLE>P2 Labi</TITLE></HEAD><BODY><H1>Hello World</H1></BODY></HTML>"


cherrypy.quickstart(Root())
