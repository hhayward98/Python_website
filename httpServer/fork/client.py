import os
import requests
from urllib.parse import urlparse, parse_qs
import json




from requests.api import request


HEADER_SIZE = 64
FORMAT = "utf-8"
PORT = 8080
SERVER =  "127.0.0.1" #Gets local ip
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "NOT CONNECTED"



NAME = input("Enter Name: ")

def main():
    exitCommand = False
    while exitCommand is not True:

        print("welcome to RO-SHAM-BO")
        print("The game is best 2 out of 3")
        print("options include 'rock', 'paper', 'scissors' ")
        choice = input("1 -- Join Game\n 2 -- Game Score\n 3 -- Throw a Play\n 4 -- Play Result\n 5 -- Reset Game\n 6 -- Quit\n")

        if (int(choice) == 1):
            Name = NAME
            r = requests.post(f'http://localhost:8000/new', data=Name)
        elif (int(choice) == 2):
            r = requests.get('http://localhost:8000/gamescore')
            print('Reply status code %s\nContent:\n%s\n\n' % (r.status_code, r.text))
        elif (int(choice) == 3):
            # name = NAME
            count = 0
            while count != 1:
                throw = input("Rock, Paper or Scissors? ")
                if throw == "Rock":
                    count = count + 1
                    
                elif throw == "Paper":
                    count = count + 1
                    
                elif throw == "Scissors":
                    count = count + 1
                    
                else:
                    print("Error, input was not a valid answer\n")

            r = requests.post(f'http://localhost:8000/{NAME}/throw', data=throw)
            print('Reply status code %s\nContent:\n%s\n\n' % (r.status_code, r.text))
        elif (int(choice) == 4):
            r = requests.get('http://localhost:8000/turnresult')
            print('Reply status code %s\nContent:\n%s\n\n' % (r.status_code, r.text))
        elif (int(choice) == 5):
            r = requests.post('http://localhost:8000/reset', data="reset")
        elif (int(choice) == 6): 
            exitCommand = False
        else:
            print("Please enter an option from the menu.")

main()


