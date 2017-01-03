#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Modified

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
from time import sleep

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/html", HtmlHandler),
            (r"/data", DataHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=options.debug,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class HtmlHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        HtmlHandler.clients.add(self)

    def on_close(self):
        HtmlHandler.clients.remove(self)

    def on_message(self, message):
        logging.info("got html message %r", message)

    @classmethod
    def send_updates(cls, html_file):
        logging.info("sending html to %d clients", len(cls.clients))
        for clients in cls.clients:
            try:
                clients.write_message(html_file.read())
            except:
                logging.error("Error sending html", exc_info=True)

class DataHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        DataHandler.clients.add(self)

    def on_close(self):
        DataHandler.clients.remove(self)

    def on_message(self, message):
        logging.info("got data message %r", message)

    @classmethod
    def send_updates(cls, data):
        logging.info("sending data to %d clients", len(cls.clients))
        for clients in cls.clients:
            try:
                clients.write_message(json.dumps(data))
            except:
                logging.error("Error sending data", exc_info=True)

i = 0

def cb():
    sleep(2)
    global i
    HtmlHandler.send_updates(file('templates/X01.html'))
    tornado.ioloop.IOLoop.current().add_callback(cb)
    i += 1

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().add_callback(cb)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
