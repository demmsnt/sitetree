#!/usr/bin/python
# -*- coding: UTF-8 -*-
import __main__
import tornado.web
import tornado.ioloop
import tornado.web
import os.path
from tornado.options import define, options


class Application(tornado.web.Application):
    def __init__(self, CONSTS, handlers):
        handlers = handlers[:]
        settings = dict(
            cookie_secret=CONSTS.get("SECRET", "TzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=" + __main__.__file__),
            login_url="/login",
            template_path=os.path.join(os.path.dirname(__main__.__file__), CONSTS.get("templates", "templates")),
            static_path=os.path.join(os.path.dirname(__main__.__file__), CONSTS.get("static", "static")),
            xsrf_cookies=CONSTS.get('XSRF', True),
            autoescape="xhtml_escape",
            debug=CONSTS.get('DEBUG', False)
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main(app_class, CONSTS, handlers):
    define("port", default=CONSTS['PORT'], help="run on the given port", type=int)
    tornado.options.parse_command_line()
    app = app_class(CONSTS, handlers)
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

