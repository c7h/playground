import socket
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from urlparse import urlparse, parse_qs

from caesar import CaesarCipher

class CaesarHandler(SimpleHTTPRequestHandler):
  caesar = CaesarCipher()

  def parse_args(self, path):
    url = urlparse(path)
    message_dict = parse_qs(url.query)
    try:
      message = message_dict.get("message").pop()
    except:
      message = ''
    try:
      shift = int(message_dict.get("shift").pop())
    except:
      shift = 3
    return (url.path, message, shift)

  def do_GET(self):
    path, message, shift = self.parse_args(self.path)
    # import pdb; pdb.set_trace()
    if path == '/caesar/encrypt':
      encrypted = self.caesar.encrypt(message, shift)
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write("{'encrypted': '%s', 'shift': %i}" % (encrypted, shift))
      return
    if path == '/caesar/decrypt':
      decrypted = self.caesar.decrypt(message, shift)
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write("{'decrypted': '%s', 'shift': %i}" % (decrypted, shift))
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