#!/usr/bin/env python3.6
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# final project
# webserver.py

import cherrypy
from _user_database import _user_database
from _crypto_api import _crypto_api
from users import UserController
from crypto import CryptoController

def start_service():
    # Create dispatcher and connect controller
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    udb = _user_database()
    crypto = _crypto_api
    uController = UserController(udb)
    cController = CryptoController(crypto)
    # User db controller
    dispatcher.connect('user_get_wallet', '/users/:uid', controller=uController,
                        action = 'GET_WALLET', conditions=dict(method=['GET'])
                )
    dispatcher.connect('user_changeID', '/users/', controller=uController,
                        action = 'DELETE', conditions=dict(method=['DELETE'])
                )
    dispatcher.connect('user_check_pwd', '/users/', controller=uController,
                        action = 'PUT', conditions=dict(method=['PUT'])
                )
    dispatcher.connect('make_new_id', '/users/', controller=uController,
                        action = 'POST', conditions=dict(method=['POST'])
                )
    dispatcher.connect('change_pwd', '/users/:uid', controller=uController,
                        action = 'PUT', conditions=dict(method=['PUT'])
                )
    dispatcher.connect('add_asset', '/users/:uid', controller=uController,
                        action = 'POST', conditions=dict(method=['POST'])
                )
    dispatcher.connect('delete_user', '/users/:uid', controller=uController,
                        action = 'DELETE', conditions=dict(method=['DELETE'])
                )

    dispatcher.connect('get_hottest', '/crypto/', controller=cController,
                        action = 'GET', conditions=dict(method=['GET'])
                )
    dispatcher.connect('what_if', '/crypto/:days', controller=cController,
                        action = 'GET', conditions=dict(method=['GET'])
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
