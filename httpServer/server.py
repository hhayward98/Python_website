import os 
import shutil
from http import HTTPStatus 
from http.server import SimpleHTTPRequestHandler, HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import time
from socketserver import ThreadingMixIn

class ThredingHTTPServer(ThreadingMixIn, HTTPServer):
	pass



class HTTPRequest_handler(SimpleHTTPRequestHandler):

	version = "My_HTTP_Server"
	path_prefix = "Files"

	player1 = 'l'
	player2 = 'l'
	count = 0


	def __init__(self, *args, directory=None, **kwargs):
		if directory is None:
			directory = os.getcwd()
		self.directory = directory

		super().__init__(*args,**kwargs)





	def do_GET(self):

		# prints client address to server when request is made
		print(self.client_address)


		# while self.count != 2:
		# 	print("Waiting on player2 to join....")
		# 	time.sleep(5)

		# while self.count != 2:


		# 	if len(self.player1) > 2:
		# 		if self.count != 1:
		# 			self.count + 1
		# 		print("Waiting on player2 to join....")
		# 		time.sleep(5)
		# 		self.do_GET()

		# 	if len(self.player2) > 2:
		# 		if self.count != 2:
		# 			self.count + 1
		# 		print("both players have connected")

		# 	self.Set_players(self.client_address)

		self.Set_players(self.client_address)

		print(self.player1)

		# create function for 2 players.


		# pasrse the url sent from client before path is changed
		parsed = urlparse(self.path)
		print(parsed.query)



		self.pasere_Query(parsed.query)
		
		self.path = parsed.path
		print(self.path)


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

		self.Report()



	# this function writes the query sent from client to a file. 
	def pasere_Query(self,queryDict):
		ans = queryDict
		f =open("Files/ans.txt", "w")
		f.write(ans)
		f.close()


	# this function reads the query that was written to the file. 
	def Report(self):
		buffer_size = 10
		print(self.path)
		Aws_path = self.path_prefix + '/ans.txt'
		f = open(Aws_path, 'r')
		ans = f.read(buffer_size)
		print(ans)


		
	def Set_players(self,client_info):
		IP = client_info[0]

		if len(self.player1) > 2:
			
			return 0

		if len(self.player1) < 2:
			self.player1 = IP
			print("Player1 is: " + IP)
		elif len(self.player1) > 1:
			self.player2 = IP
			print("Player2 is: " + IP)



def run_server(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
	server_address = ('', 8000)
	Http_object1 = ThredingHTTPServer(server_address, handler_class)
	Http_object1.serve_forever()
	# http_object = server_class(server_address, handler_class)
	# http_object.serve_forever()


if __name__ == "__main__":
	run_server(HTTPServer, HTTPRequest_handler)