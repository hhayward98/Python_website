import os
import shutil
from urllib.parse import urlparse, parse_qs, urlencode
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, HTTPServer, BaseHTTPRequestHandler

from urllib.parse import urlparse, parse_qs

import json
import socket
import threading



HEADER_SIZE = 64
FORMAT = "utf-8"
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname()) #Gets local ip
ADDR = (SERVER, PORT)








def startGame():
    print("Game has started...")
    

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    """A custom HTTP Request Handler based on SimpleHTTPRequestHandler"""

    
    server_version = "My_HTTP_Server/"
    path_prefix = "www"
    
    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()  # start file path with the current directory
        self.directory = directory  # or with the directory passed in the argument
        super().__init__(*args, **kwargs)  # initialize the base handler



    def do_GET(self):
        """Serve a GET request."""
        

        print("Test1: Running Get request")
        # get info from the HTTP request
        # look at https://docs.python.org/3/library/http.server.html for other BaseHTTPRequestHandler instance variables

        #top level hash map to keep game state
        print(self.client_address)

        


    
        print(self.path)

        # update the path with the prefix of server files
        self.path = self.path_prefix + self.path

        path = self.path.split("/")
        print(path)

        
        if (path[1] == 'gamescore'):
            try:
                # f is the file being opened from folder www
                f = open(self.path, 'rb')
                self.send_response(HTTPStatus.OK)

                self.end_headers()
                # wfile writes contents of f to the client
                shutil.copyfileobj(f, self.wfile)

                f.close()
            except OSError:
                self.send_response(HTTPStatus.NOT_FOUND)
                self.end_headers()
        elif (path[1] == 'turnresult'):
            try:
                # f is the file being opened from folder www
                f = open(self.path, 'rb')
                self.send_response(HTTPStatus.OK)

                self.end_headers()
                # wfile writes contents of f to the client
                shutil.copyfileobj(f, self.wfile)

                f.close()
            except OSError:
                self.send_response(HTTPStatus.NOT_FOUND)
                self.end_headers()


    def do_POST(self):
        print("Test: Running Post")
        print(self.path)
        print(self.client_address)

        length = int(self.headers['Content-length'])

        content = self.rfile.read(length).decode(FORMAT)
        print(content)

        path = self.path.split("/")
        print(path)


        #pushing data to files via pickle may be the best bet

        if (path[1] == 'new'):
            # self.setPlayers(content, self.client_address)
            self.Set_player(content)
            startGame()

            # here we response to wait for other player or start game
            self.send_response(200, "OK")
            self.end_headers()
            
        elif (path[2] == 'throw'):

            if os.stat("www/player1.txt").st_size != 0:
                print("Test: open player1 file for throw")
                f = open("www/player1.txt", "r")
                p1Line = f.readlines()
                print(p1Line)
                if path[1] == p1Line[0]:
                    print("Testing: writing player1 throw to file\n")
                    player1 = 1
                    self.write_throw(content, player1)
                    self.send_response(200, "OK")
                    self.send_response(200, "OK")
                    self.end_headers()
                    
            if os.stat("www/player2.txt").st_size != 0:
                s = open("www/player2.txt", "r")
                p2Line = s.readlines()
                if path[1] == p2Line[0]:
                    print("Testing: writing player2 throw to file\n")
                    player2 = 2
                    self.write_throw(content, player2)
                    self.send_response(200, "OK")
                    self.end_headers()
                    

            else:
                print("error: failed at throw if stmt\n")



            if self.run_Game() == 1:
                self.reset_throws()
                print("game has ended\n")

            
        elif (path[1] == 'reset'):

            x = open("www/reset.txt", "r")
            reset_val = x.readlines()

            if int(reset_val[0]) == 2:
                self.reset_throws()
                self.reset_game()
                self.rest_palyers()



            # We will have to wait for both players to reset and communicate this
            # Could be done by just waiting for two different reset requests. (1 and 0)
            pass


        #self.wfile.write("POST request for {}".format(self.path).encode(FORMAT) )




    def write_throw(self,throw,player_num):
        if player_num == 1:
            f = open("www/player1_throw.txt", "w")
            f.write(throw)
            f.close()
        elif player_num == 2:
            f = open("www/player2_throw.txt", "w")
            f.write(throw)
            f.close()
        else:
            print("error could not print throw to file\n")



    def run_Game(self):

        if os.stat("www/player2_throw.txt").st_size != 0:
            if os.stat("www/player1_throw.txt").st_size != 0:
                print("Running game\n")
                self.game_results()
                return 1
        else:
            print("waiting on another player to join game\n")
            return 0



    def game_results(self):
        f = open("www/player1_throw.txt", "r+")
        s = open("www/player2_throw.txt", "r+")
        p1_throw = f.readlines()
        p2_throw = s.readlines()

        if p1_throw[0] == 'Rock':
            p1 = 1
        elif p1_throw[0] == 'Paper':
            p1 = 2
        elif p1_throw[0] == "Scissors":
            p1 = 3
        else:
            print("error with if stmt setting player1 throw ")

        if p2_throw[0] == "Rock":
            p2 = 1
        elif p2_throw[0] == "Paper":
            p2 = 2
        elif p2_throw[0] == "Scissors":
            p2 = 3
        else:
            print("error with if stmt setting player2 throw ")


        print("Test: player1 num: " + str(p1) + " Player2 num: " + str(p2))
        print(self.evaluate(p1,p2))
        print("Testing: evaluation was compleate\n")



        f.close()
        s.close()

    def evaluate(self, p1, p2):
        f = open("www/gamescore.txt", "r+")
        Lines = f.readlines()
        Player1_score = int(Lines[0])
        Player2_score = int(Lines[1])
        f.close()
        f = open("www/gamescore.txt", "w")
        victor = ''
        
        if p1 > p2:
            Player1_score = Player1_score + 1
            L = [str(Player1_score)+'\n', str(Player2_score)+'\n']
            f.writelines(L)
            victor = "player1 has won\n"
            f.close()
            return victor
        elif p1 < p2:
            Player2_score = Player2_score + 1
            L = [str(Player1_score)+'\n', str(Player2_score)+'\n']
            f.writelines(L)
            victor = "player2 has won\n"
            f.close()
            return victor
        elif p1 == p2:
            L = [str(Player1_score)+'\n', str(Player2_score)+'\n']
            f.writelines(L)
            victor = "The game was a draw\n"
            f.close()
            return victor
        else:
            print("error with writing game score to file\n")

        





    def serialize(self, content):
        return json.dumps(parse_qs(content))

    def Set_player(self,name):

        if os.stat("www/player1.txt").st_size == 0:
            f = open("www/player1.txt", "w")
            f.write(name)
            f.close()
        elif os.stat("www/player1.txt").st_size != 0:
            if os.stat("www/player2.txt").st_size == 0:
                f = open("www/player2.txt", "w")
                f.write(name)
                f.close()
        else:
            print("error: failed at Set_player\n")


    def rest_palyers(self):
        f = open("www/player1.txt", "w")
        s = open("www/player2.txt", "w")

        no_str = ''
        f.write(no_str)
        s.write(no_str)

        f.close()
        s.close()


    def reset_throws(self):
        f = open("www/player1_throw.txt", "w")
        s = open("www/player2_throw.txt", "w")

        no_str = ''
        f.write(no_str)
        s.write(no_str)

        f.close()
        s.close()

    def reset_game(self):
        f = open("www/gamescore.txt")
        L = [str(0)+'\n', str(0)+'\n']
        f.writelines(L)
        f.close()




    # def setPlayers(self, content, client_address):
    #     # to do ... save client address and entered name to a file to be accessed later.

    #     client = {"name": content, "ip" : client_address[0],"port" : client_address[1], "reset": False, "score": 0 }
    #     #print(client)
    #     f = open(f"www/players.json", "w")
    #     f.write(json.dumps(client))
    #     f.close()


    #     self.Report()


    # def Report(self):
    #     buffer_size = 10
    #     print(self.path)
    #     Aws_path = self.path_prefix + '/player1.txt'
    #     f = open(Aws_path, 'r')
    #     ans = f.read(buffer_size)
    #     print(ans)

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):

    PORT = 8000
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Running on port {PORT}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run(HTTPServer, MyHTTPRequestHandler)
