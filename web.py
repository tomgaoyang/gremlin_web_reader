#!/usr/bin/env python
# Start importing gremlin library
from __future__  import print_function  # Python 2/3 compatibility
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

"""
Very simple HTTP server in python (Updated for Python 3.7)
Usage:
    ./dummy-web-server.py -h
    ./dummy-web-server.py -l localhost -p 8000
Send a GET request:
    curl http://localhost:8000
Send a HEAD request:
    curl -I http://localhost:8000
Send a POST request:
    curl -d "foo=bar&bin=baz" http://localhost:8000
"""
import argparse
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

graph = Graph()


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f'<html><body><h1>{message}</h1></body></html>'
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("hi!"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        # self.wfile.write(self._html("POST!"))
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)
        print(str(self.path).encode().decode("utf-8"))
        print(str(self.headers))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        # self._set_response()

        # Start opening connections
        remoteConn = DriverRemoteConnection('wss://neptunedbcluster-duhtid8h5yms.cluster-cqhaxlvmnnup.ap-northeast-2.neptune.amazonaws.com:8182/gremlin','g')
        g = graph.traversal().withRemote(remoteConn)

        if str(self.path).encode().decode("utf-8") == '/risk':
            print("RISK!")
            print(post_data)
            print("query data = ")
            print(g.E().hasLabel('risk').outV().hasLabel('user').has('name', 'lily').toList())
            if g.E().hasLabel('risk').outV().hasLabel('user').has('name', 'lily').toList()[0] is not None:
                result = 1
            else:
                result = 0
        elif str(self.path).encode().decode("utf-8") == '/gender':
            print("Gender!")
            result = 'M'
        else:
            print("path has no match")
            result = '"path has no match"'
        json_string = json.dumps('{' + str(result) + '}' )
        self.wfile.write(json_string.encode())
        # self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
