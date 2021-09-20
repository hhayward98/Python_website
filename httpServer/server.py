import os 
import shutil
from http import HTTPStatus 
from http.server import SimpleHTTPRequestHandler, HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class HTTPRequest_handler(SimpleHTTPRequestHandler):

	version = "My_HTTP_Server"
	path_prefix = "Files"

	def __init__(self, *args, directory=None, **kwargs):
		if directory is None:
			directory = os.getcwd()
		self.directory = directory
		super().__init__(*args,**kwargs)


	def Get_req(self):

		# prints client address to server when request is made
		print(self.client_address)

		# pasrse the url sent from client before path is changed
		parsed = urlparse(self.path)

		# converts the parsed query into a Dict.
		parsedqs = parse_qs(parsed.query)

		# sends the dict to function. 
		self.pasere_Query(parsedqs)

		# updates the path to path of server files.
		self.path = self.path_prefix + self.path

		

		# sending files to client 
		try:
			# opening the server file requested from client.
			f = open(self.path, 'rb')
			# send ok status to server
			self.send_response(HTTPStatus.OK)

			self.end_headers()
			# copys file contents and writes them to client. 
			shutil.copyfileobj(f, self.wfile)
			f.close()
		except OSError:
			self.send_response(HTTPStatus.NOT_FOUND)
			self.end_headers()



	def pasere_Query(self):
		pass 



def run_server(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
	server_address = ('', 8000)
	http_object = server_class(server_address, handler_class)
	http_object.serve_forever()

if __name__ == "__main__":
	run_server(HTTPServer, HTTPRequest_handler)