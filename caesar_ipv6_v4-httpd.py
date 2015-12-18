import socket
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from caesar import CaesarCipher

class CaesarHandler(SimpleHTTPRequestHandler):
  def do_GET(self):
    # import pdb; pdb.set_trace()
    if self.path == '/caesar/encrypt':
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write("{}")
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

class HTTPServerV6(HTTPServer):
  address_family = socket.AF_INET6

class HTTPServerV4(HTTPServer):
  address_family = socket.AF_INET

if __name__ == '__main__':
  serverV6 = HTTPServerV6(('::', 8000), CaesarHandler)
  serverV4 = HTTPServerV4(("0.0.0.0", 8001), CaesarHandler)
  
  # cool kids provide v6
  serverV6.serve_forever()
  serverV4.serve_forever()