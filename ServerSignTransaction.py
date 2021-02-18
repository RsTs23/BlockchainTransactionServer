from io import BytesIO
import socketserver
import http.server
import requests
from requests.api import request
from thor_devkit import cry, transaction
import json 

class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
 def _set_headers(self):
         # self.send_header('Content-type', 'text/plain')
        self.end_headers()

 def do_GET(self):
        self._set_headers()
        f = open("index.html", "r")
        self.wfile.write(f.read())

 def do_HEAD(self):
        self._set_headers()

 def do_POST(self):
        #self._set_headers()
        print ("in post method")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        jsonData = json.loads(self.data_string)
       

        if jsonData["paid"] == "true": 
                # Construct an unsigned transaction.
                tx = transaction.Transaction(jsonData["tx"])
                priv_2 = bytes.fromhex('***')
                dh = tx.get_signing_hash(jsonData["address"]) # Gas Payer hash to be signed.
                serversig = cry.secp256k1.sign(dh, priv_2)  
                self.send_response(200)
                print(serversig)
                self.wfile.write(serversig)
                 
        else:      
                self.send_response(401)

        self.end_headers()
        return 


PORT = 8000
handler_object = MyHttpRequestHandler

my_server = socketserver.TCPServer(("", PORT), handler_object)
print("serving at port", PORT)

# Star the server
my_server.serve_forever()
       



 



