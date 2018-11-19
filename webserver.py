#!/usr/bin/env python3.6
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# final project
# webserver.py

import cherrypy
from _user_database import _user_database
from users import UserController

def start_service():
    # Create dispatcher and connect controller
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    udb = _user_database()
    uController = UserController(udb)
    # User db controller
    dispatcher.connect('user_get_wallet', '/users/:uid', controller=uController,
                        action = 'GET_WALLET', conditions=dict(method=['GET'])
                )
    dispatcher.connect('user_changeID', '/users/', controller=uController,
                        action = 'DELETE', conditions=dict(method=['DELETE'])
                )
    dispatcher.connect('user_check_pwd', '/users/:uid', controller=uController,
                        action = 'PUT', conditions=dict(method=['PUT'])
                )
    
    # Configuration for the server
    conf = { 
            'global' : {
                    'server.socket_host': 'student04.cse.nd.edu',
                    'server.socket_port': 52109, 
                },
            '/' : { 'request.dispatch': dispatcher } 
           }

    # Update config
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

if __name__ == '__main__':
    start_service()
