"""
A Flask web app that scrapes http://quotes.toscrape.com using Scrapy and Twisted.
To run this app, run it directly:
    python flask_twisted.py
Alternatively, use Twisted's `twist` executable. This assumes you're in the directory where the
source files are located:
    PYTHONPATH=$(pwd) twist web --wsgi flask_twisted.app --port tcp:9000:interface=0.0.0.0
"""


import json

from flask import Flask

app = Flask('Fraped')

if __name__ == '__main__':
    from sys import stdout

    from twisted.logger import globalLogBeginner, textFileLogObserver
    from twisted.web import server, wsgi
    from twisted.internet import endpoints, reactor

    # start the logger
    globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    # start the WSGI server
    root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    factory = server.Site(root_resource)
    http_server = endpoints.TCP4ServerEndpoint(reactor, 9000)
    http_server.listen(factory)

    # start event loop
reactor.run()
