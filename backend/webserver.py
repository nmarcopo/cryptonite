#!/usr/bin/env python3.6
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# final project
# webserver.py

import cherrypy, asyncio, time
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

class Server:
    def __init__(self):
        # Initialize api files
        self.udb = _user_database("user_pwd.db", "user_wallet.db")
        self.crypto = _crypto_api()

    def start_service(self):
        # Create dispatcher and connect controller
        dispatcher = cherrypy.dispatch.RoutesDispatcher()
        # database files
        uController = UserController(self.udb)
        cController = CryptoController(self.crypto)
        rController = ResetController(self.udb, self.crypto)
        # User db controller
        dispatcher.connect('user_get_wallet', '/users/:user', controller=uController,
                            action = 'GET_WALLET', conditions=dict(method=['GET'])
                    )
        dispatcher.connect('user_changeID', '/users/change/', controller=uController,
                            action = 'PUT_CHANGE', conditions=dict(method=['PUT'])
                    )
        dispatcher.connect('user_check_pwd', '/users/', controller=uController,
                            action = 'PUT_PWD', conditions=dict(method=['PUT'])
                    )
        dispatcher.connect('make_new_id', '/users/', controller=uController,
                            action = 'POST_ID', conditions=dict(method=['POST'])
                    )
        dispatcher.connect('change_pwd', '/users/:user', controller=uController,
                            action = 'PUT', conditions=dict(method=['PUT'])
                    )
        dispatcher.connect('add_asset', '/users/:user', controller=uController,
                            action = 'POST', conditions=dict(method=['POST'])
                    )
        dispatcher.connect('delete_user', '/users/change/:user', controller=uController,
                            action = 'PUT_DELETE', conditions=dict(method=['PUT'])
                    )
        dispatcher.connect('delete_item', '/users/change/:user', controller=uController,
                            action = 'POST_DELETE', conditions=dict(method=['POST'])
                    )
        # Crypto api controller
        dispatcher.connect('get_hottest', '/crypto/', controller=cController,
                            action = 'POST_TOPN', conditions=dict(method=['POST'])
                    )
        dispatcher.connect('get_price', '/crypto/', controller=cController,
                            action = 'PUT', conditions=dict(method=['PUT'])
                    )
        dispatcher.connect('get_hotcold5', '/crypto/:temp', controller=cController,
                            action = 'GET_TEMP', conditions=dict(method=['GET'])
                    )
        dispatcher.connect('what_if', '/crypto/whatif/', controller=cController,
                            action = 'PUT_WHATIF', conditions=dict(method=['PUT'])
                    )
        # Reset controller
        dispatcher.connect('reset', '/reset/', controller=rController,
                            action = 'GET', conditions=dict(method=['GET'])
                    )

        # Options requests for dispatcher
        dispatcher.connect('user_options', '/users/:user', controller=optionsController,
                            action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                    )
        dispatcher.connect('users_all', '/users/', controller=optionsController,
                            action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                    )
        dispatcher.connect('users_change', '/users/change/', controller=optionsController,
                            action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                    ) 
        dispatcher.connect('users_delete', '/users/change/:user', controller=optionsController,
                            action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                    ) 
        dispatcher.connect('crypto_hot_cold', '/crypto/', controller=optionsController,
                            action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                    )
        dispatcher.connect('crypto_whatif', '/crypto/whatif/', controller=optionsController,
                            action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                    )
        dispatcher.connect('user_reset', '/reset/', controller=optionsController,
                            action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                    )

    
        # Configuration for the server
        conf = { 
                'global' : {
                        'server.socket_host': 'marcopo.li',
                        'server.socket_port': 52109,
                        'server.ssl_module':'builtin',
                        'server.ssl_certificate':'fullchain.pem',
                        'server.ssl_private_key':'privkey.pem',
                    },
                '/' : { 'request.dispatch': dispatcher,
                        'tools.CORS.on': True,
                    } 
               }

        # Update config
        cherrypy.config.update(conf)
        app = cherrypy.tree.mount(None, config=conf)
        cherrypy.quickstart(app)
    
    # function to fetch historic crypto data every 150 seconds
    def fetch_hist_data(self):
        print("Fetching historical data... ", end="")
        print(time.ctime()) 
        self.crypto.fetch_hist_data()
        print("Fetched! ", end="")
        print(time.ctime()) 

    # function to fetch crypto price data every 8 seconds
    def fetch_price_data(self):
        print("Fetching price data... ", end="")
        print(time.ctime()) 
        self.crypto.fetch_price_data()
        print("Fetched! ", end="")
        print(time.ctime()) 

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    server = Server()
    # Initial caching
    server.fetch_hist_data()
    server.fetch_price_data()
    # Cache data
    bg_hist = cherrypy.process.plugins.BackgroundTask(150, server.fetch_hist_data)
    bg_price = cherrypy.process.plugins.BackgroundTask(8, server.fetch_price_data)
    bg_hist.start()
    bg_price.start()
    server.start_service()
