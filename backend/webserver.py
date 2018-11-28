#!/usr/bin/env python3.6
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# final project
# webserver.py

import cherrypy, asyncio
from _user_database import _user_database
from _crypto_api import _crypto_api
from users import UserController
from crypto import CryptoController
from reset import ResetController

class optionsController:
    def OPTIONS(self, *args, **kargs):
        return ""

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "*"

def start_service():
    # Create dispatcher and connect controller
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    udb = _user_database()
    crypto = _crypto_api()
    uController = UserController(udb)
    cController = CryptoController(crypto)
    rController = ResetController(udb, crypto)
    # User db controller
    dispatcher.connect('user_get_wallet', '/users/:uid', controller=uController,
                        action = 'GET_WALLET', conditions=dict(method=['GET'])
                )
    dispatcher.connect('user_changeID', '/users/', controller=uController,
                        action = 'DELETE', conditions=dict(method=['DELETE'])
                )
    dispatcher.connect('user_check_pwd', '/users/', controller=uController,
                        action = 'PUT_PWD', conditions=dict(method=['PUT'])
                )
    dispatcher.connect('make_new_id', '/users/', controller=uController,
                        action = 'POST_ID', conditions=dict(method=['POST'])
                )
    dispatcher.connect('change_pwd', '/users/:uid', controller=uController,
                        action = 'PUT', conditions=dict(method=['PUT'])
                )
    dispatcher.connect('add_asset', '/users/:uid', controller=uController,
                        action = 'POST', conditions=dict(method=['POST'])
                )
    dispatcher.connect('delete_user', '/users/:uid', controller=uController,
                        action = 'DELETE_ID', conditions=dict(method=['DELETE'])
                )
    # Crypto api controller
    dispatcher.connect('get_hottest', '/crypto/', controller=cController,
                        action = 'PUT_TOPN', conditions=dict(method=['PUT'])
                )
    dispatcher.connect('what_if', '/crypto/:days', controller=cController,
                        action = 'PUT', conditions=dict(method=['PUT'])
                )
    # Reset controller
    dispatcher.connect('reset', '/reset/', controller=rController,
                        action = 'GET', conditions=dict(method=['GET'])
                )

    # Options requests for dispatcher
    dispatcher.connect('user_options', '/users/:uid', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                )
    dispatcher.connect('users_all', '/users/', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                )
    dispatcher.connect('crypto_hot_cold', '/crypto/', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                )
    dispatcher.connect('crypto_whatif', '/crypto/:days', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                )
    dispatcher.connect('user_reset', '/reset/', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                )

    
    # Configuration for the server
    conf = { 
            'global' : {
                    'server.socket_host': 'student04.cse.nd.edu',
                    'server.socket_port': 52107, 
                },
            '/' : { 'request.dispatch': dispatcher,
                    'tools.CORS.on': True,
                  } 
           }

    # Update config
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    start_service()
    #loop = asyncio.get_event_loop()
    #asyncio.set_event_loop(asyncio.new_event_loop())
