import socket
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from urlparse import urlparse, parse_qs

from caesar import CaesarCipher

class CaesarHandler(SimpleHTTPRequestHandler):
  def do_GET(self):
    url = urlparse(self.path)
    caesar = CaesarCipher()
    message_dict = parse_qs(url.query)
    try:
      message = message_dict.get("message").pop()
    except:
      message = ''
    try:
      shift = message_dict.get("shift").pop()
    except:
      shift = 3
    # import pdb; pdb.set_trace()
    if url.path == '/caesar/encrypt':
      encrypted = caesar.encrypt(message, shift)
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write("{'encrypted': '%s', 'shift': %i}" % (encrypted, shift))
      return
    if url.path == '/caesar/decrypt':
      decrypted = caesar.decrypt(message, shift)
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