# Copyright 2014 Alan Lee

import webapp2
import urllib2
import re
import logging

logging.getLogger().setLevel(logging.DEBUG)

class ProxyHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        # must call initialize when subclassing
        self.initialize(request, response)
        
        # TODO: Add host address used for remote query
        self.base = 'https://qrng.anu.edu.au'

    def remote_fetch(self, url, data = None):
        ''' fetch HTTP Response from remote host and create new response with CORS header '''

        try:
          logging.debug(url)
          result = urllib2.urlopen(url, data)
          response_text = result.read()

          content_type = result.info().get('content-type')
          # replace 'text/javascript' (obsoleted by RFC 4329) with 'application/json'
          if content_type == 'text/javascript':
              content_type = 'application/json'

          self.response.headers["Content-Type"] =  content_type
          self.response.headers.add_header("Access-Control-Allow-Origin", "*") # CORS header
          logging.debug(response_text)
          self.response.write(response_text)
        except urllib2.URLError, e:
          self.response.write(str(e.reason))


class DefaultHandler(ProxyHandler):
    def get(self, path_string):
        query_string = self.request.path_qs
        translated_url = self.base + query_string
        self.remote_fetch(translated_url)

    def post(self, path_string):
        query_string = self.request.path_qs
        translated_url = self.base + query_string
        payload = self.request.body
        self.remote_fetch(translated_url, payload)


app = webapp2.WSGIApplication([
    # TODO: modify URL filter to match the target query to prevent misuse
    (r'/(.*)', DefaultHandler)
], debug=True)

