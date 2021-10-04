import os
import requests
import json

FORMAT = "utf-8"
PORT = 8080
SERVER =  "127.0.0.1" #Gets local ip





NAME = ''


def main():
    exitCommand = True
    endGame = True
    print("welcome to RO-SHAM-BO")
    NAME = input("\nPlease enter your name: ")

    payload = {"name" : NAME}
    r = requests.post(f'http://localhost:8000/new', json=json.dumps(payload))
    print(f"\n {r.text} \n")

    while exitCommand :


        # choice = input("\n1 -- Game Score\n2 -- Throw a Play\n3 -- Play Result\n4 -- Reset Game\n5 -- Quit\n")
        print("Enter an option to continue!\n")
        choice_game = input("\n1 -- Play game\n2 -- Quit\n")

        if (int(choice_game) == 1):
            while endGame :

                choice = input("\n1 -- Game Score\n2 -- Throw a Play\n3 -- Reset Game\n4 -- Quit\n")

                if (int(choice) == 1):
                    r = requests.get('http://localhost:8000/gamescore')
                    print(f"\n {r.text} \n")
                elif (int(choice) == 2):
                    throw = input("\nRock, Paper or Scissors? ")

                    if throw.lower() == "rock" or throw.lower() == "paper" or throw.lower() == "scissors":
                        if (throw.lower() == "rock"):
                            throw = str(0)
                        elif(throw.lower() == "paper"):
                            throw = str(-1)
                        elif(throw.lower() == "scissors"):
                            throw = str(1)

                        payload = {"throw" : throw}
                        r = requests.post(f'http://localhost:8000/throw/{NAME}', json=json.dumps(payload))
                        if (r.status_code == requests.codes.conflict):
                            print(f"\nStatus Code: {r.status_code} -- You played a duplicate throw.\n")
                        else:
                            print(f"\nStatus Code: {r.status_code} -- {r.text} \n")
                    else:
                        print('\nPlease enter Rock, Paper or Scissors.')

                    print("\nRuning game")
                    print("\nDetermining results\n")

                    r = requests.get('http://localhost:8000/playresult')
                    print(f"\nStatus Code: {r.status_code} --  {r.text} \n")

                elif (int(choice) == 3):
                    payload = {"reset" : 'True'}
                    r = requests.post(f'http://localhost:8000/reset/{NAME}', json=json.dumps(payload))
                    print(f"\nStatus Code: {r.status_code} -- {r.text} \n")

                elif (int(choice) == 4):
                    print("\nExiting Game")
                    endGame = False
                else:
                    print("\nPlease enter an option from the menu.\n")
        elif (int(choice_game) == 2): 
            r = requests.post(f'http://localhost:8000/exit/{NAME}', json=json.dumps(payload))
            print("\nThanks for playing!")
            exitCommand = False
        else:
            print("\nPlease enter an option from the menu.\n")

main()

