import socket
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from caesar import CaesarCipher

class CaesarHandler(SimpleHTTPRequestHandler):
  def do_GET(self):
    if self.path == '/caesar/encrypt':
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      self.wfile.write("")
      return
    elif self.path == '/caesar/decrypt':
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write()
      return
    else:
      self.send_response(400)
      return
      #return SimpleHTTPRequestHandler.do_GET(self)
