#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import sys
import codecs
import html
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from http.server import HTTPServer, CGIHTTPRequestHandler
server_address = ("", 8000)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()
