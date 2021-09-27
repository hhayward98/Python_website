import os
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, HTTPServer, BaseHTTPRequestHandler
import json
import socket

FORMAT = "utf-8"
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname()) #Gets local ip

# POST /games/new

# Protocall

# POST /new: <NAME>
# -> 200: Joined Game | Two Players Have Joined

# POST <NAME>/throw: <rock|paper|scissors>
# -> 200: waiting for other player, you can't throw a play | Throw recorded

# GET /gamescore
# -> 200: score | game lost | game won

# GET /turnresult/
# -> 200: won with <your throw> to <opponents throw> | lost with <your throw> to <opponents throw>

# POST /<NAME>/reset/
# -> 200: You have requested to reset | you already requested to reset | Game has reset




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
        self.path = self.path_prefix + self.path

        path = self.path.split("/")
        
        if (path[1] == 'gamescore'):
            try:
                response = self.getScore()
            
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write((response).encode())
            except OSError:
                self.send_response(HTTPStatus.NOT_FOUND)
                self.end_headers()
        elif (path[1] == 'playresult'):
            try:
                response = self.playResult()
            
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write((response).encode())
    
            except OSError:
                self.send_response(HTTPStatus.NOT_FOUND)
                self.end_headers()


    def do_POST(self):

        length = int(self.headers['Content-length'])
        content = self.rfile.read(length).decode(FORMAT)
        content = json.loads(content)
        content = eval(content)

        path = self.path.split("/")

        if (path[1] == 'new' ):
            joinStatus = self.setPlayers(content, self.client_address)
            # here we response to wait for other player or start game
            if (joinStatus):
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(("You have joined the game!").encode())

                startGame()
            else:
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(("Sorry Two Players have joined already").encode())
            

        elif (path[1] == 'throw'):
            throwStatus = self.processThrow(content, path)
            result = self.playResult()

            if (throwStatus != 0):
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write((f"{throwStatus}\n{result}").encode())
            else:
                self.send_response(HTTPStatus.CONFLICT)
                self.end_headers()


        elif (path[1] == 'reset'):
            resetStatus = self.reset(content, path)
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write((resetStatus).encode())


    def setPlayers(self, content, client_address):

        client = { "ip" : client_address[0],"port" : client_address[1], "score": "0", 'reset': "False", "throw": ""}
        client.update(content)
        print(client)
        if (os.path.exists("www/player1.json") and os.path.exists("www/player2.json")):
            return False
        elif (os.path.exists("www/player1.json")):
            f = open(f"www/player2.json", "w")
            f.write(json.dumps(client))
            f.close()
            return True
        else:
            f = open(f"www/player1.json", "w")
            f.write(json.dumps(client))
            f.close()
            return True

    def processThrow(self, content, path):
        pf1 = open("www/player1.json" , 'r+')
        playerData1 = json.load(pf1)
        if (os.path.exists("www/player2.json")):
           pf2 = open("www/player2.json" , 'r+')
           playerData2 = json.load(pf2)

        if (playerData1['throw'] == content["throw"]):
            return 0
        
        elif (playerData1['name'] == path[2]):
                playerData1.update(content)
                self.writeToFile(pf1, playerData1)
                return "Throw was recorded."
        elif (playerData2['throw'] == content["throw"]):
            return 0
        elif (playerData2['name'] == path[2]):
                playerData2.update(content)
                self.writeToFile(pf2, playerData2)
                return "Throw was recorded."
        else:
            return 0


    def reset(self, content, path):
        pf1 = open("www/player1.json" , 'r+')
        playerData1 = json.load(pf1)
        if (os.path.exists("www/player2.json")):
           pf2 = open("www/player2.json" , 'r+')
           playerData2 = json.load(pf2)

        if ((playerData1["reset"] == "True" and playerData2["reset"] == "True") or (playerData1["reset"] == "True" and playerData2['name'] == path[2]) or (playerData2["reset"] == "True" and playerData1['name'] == path[2])):

            #os.remove("www/player2.json")
            #os.remove("www/player1.json")
            playerData1["throw"] = ''
            playerData2["throw"] = ''
            playerData1["reset"] = 'False'
            playerData2["reset"] = 'False'
            playerData1["score"] = '0'
            playerData2["score"] = '0'
            self.writeToFile(pf1, playerData1)
            self.writeToFile(pf2, playerData2)

            return "Game as been reset."
        else:
            if (playerData1['name'] == path[2] and playerData1['reset'] == "False"):
                playerData1.update(content)
                self.writeToFile(pf1, playerData1)
                return "Waiting for other player to request a reset."
            elif (playerData2['name'] == path[2] and playerData2['reset'] == "False"):
                playerData2.update(content)
                self.writeToFile(pf2, playerData2)
                return "Waiting for other player to request a reset."
            else:
                return "You have already requested to reset."

    def playResult(self):
        if (os.path.exists("www/player1.json") and os.path.exists("www/player2.json")):
            pf1 = open("www/player1.json" , 'r+')
            playerData1 = json.load(pf1)
            pf2 = open("www/player2.json" , 'r+')
            playerData2 = json.load(pf2)

            if(playerData1["throw"] != '' and playerData2["throw"] != ''):
                throw1 = int(playerData1["throw"])
                throw2 = int(playerData2["throw"])
                score = self.compareThrows(throw1, throw2)
                playerData1["throw"] = ''
                playerData2["throw"] = ''

                if (score == 2):
                    return "You both tied."
                elif (score == throw1):
                    scoreValue = int(playerData1["score"])
                    scoreValue += 1
                    playerData1.update({'score': str(scoreValue)})
                    self.writeToFile(pf1, playerData1)
                    self.writeToFile(pf2, playerData2)
                    return f"Player {playerData1['name']} won that turn." 
                else:
                    scoreValue = int(playerData2["score"])
                    scoreValue += 1
                    playerData2.update({'score': str(scoreValue)})
                    self.writeToFile(pf2, playerData2)
                    self.writeToFile(pf1, playerData1)
                    return f"Player {playerData2['name']} won that turn."

            else: return "Still waiting on other player throw"
        else:
            return "Still waiting on other player to join."

    def getScore(self):
        if (os.path.exists("www/player1.json") and os.path.exists("www/player2.json")):
            pf1 = open("www/player1.json" , 'r+')
            playerData1 = json.load(pf1)
            pf2 = open("www/player2.json" , 'r+')
            playerData2 = json.load(pf2)
            return f"Score is: {playerData1['name']} with {playerData1['score']} wins too {playerData2['name']} with {playerData2['score']} wins."
        else:
            return "Score issn't avalible until both players have joined."

    def compareThrows(self, p1Throw, p2Throw):   
        tie = 2
        if (p1Throw != p2Throw):
            if (abs(p1Throw) == abs(p2Throw)):
                tie = max(p1Throw, p2Throw)
            else:
                tie = min(p1Throw, p2Throw)
        return tie
    

    def writeToFile(self, file, payload):
        file.seek(0)
        file.write(json.dumps(payload))
        file.truncate()
        file.close()


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    PORT = 8000
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Running on port {PORT}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run(HTTPServer, MyHTTPRequestHandler)