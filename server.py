import socket
from _thread import *
import sys
from game import Game
import pickle

server = "127.0.0.1" # Change this
port = 5555

# Setting up a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port)) 
except socket.error as e:
    str(e)

s.listen()
print("Server Started,Waiting on connection")

connected = set() # Store the ip addresses of the connected clients
games = {} # Storing the game. gameId will be the key and the games object will be the value
idCount = 0 # Keep track of the current ID/ How many people are connected to the server at once

# Threaded function(runs independently in the while loop, meaning that the program doesn't w8 for it to finish execution)
# Multi-Threading
# You don't have to wait for the function to finish executing before establishing another connection
# Meaning that this function runs for every connection, if 100 clients are connected this function is executed 100 times
def threaded_client(conn, p, gameId): 
    global idCount # Global to keep track of the number of games
    conn.send(str.encode(str(p)))
    reply = ""

    while True:
        try:
            # Three options: GET, RESET, MOVE
            data = conn.recv(4096).decode()# The more clients the bigger the number should be

            if gameId in games: # If one of the clients dissconnects, this deletes the game
                game = games[gameId]

                if not data: 
                    break
                else:
                    # Check options
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply)) 
            else:
                break
        except:
            break
    print("Connection Lost!")
    try:
        del games[gameId]
        print("Closing... ", gameId)
    except:
        pass
    idCount -=1 # After ending the game/ losing connection to client
    conn.close()
    

    # conn.send(pickle.dumps(players[player]))
    # reply = ""
    # while True:
    #     try:
    #         #The ammount of information you're trying to recieve
    #         #The larger the number/size the longer it takes to recieve information
    #         data = pickle.loads(conn.recv(2048))
    #         players[player] = data
    #         # from "45, 33" -> (45,33)
    #         #decoding recieved information
    #         # reply = data.decode("utf-8")
    #         if not data:
    #             #If the client doesn't send information it dissconnects
    #             #Meaning the client dissconnected or left the session
    #             print("Disconnected")
    #             break
    #         else:
    #             # Determining which player is sending
    #             if player == 1:
    #                 reply = players[0]
    #             else:
    #                 reply = players[1]
    #             print("Recieved: ", data)
    #             print("Sending: ", reply)

    #         conn.sendall(pickle.dumps(reply))
        
    #     except:
    #         break

    # print("Lost connection")
    # conn.close()

# currentPlayer = 0


# Create new games based on new people joining or delete games when people leave.
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2 # Since each player joining increments idCount then if 10 players join there will be 10 games, that's why this is devided by 2, to keep track of number of games
    if idCount % 2 == 1: # Determines if the player connectin is player 1 or 2, meaning that if the number of players is odd it creates a new game
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else: # 3 people already exists and a fourth has connected this adds the fourth player
        games[gameId].ready = True # Starts the game
        p = 1 


    start_new_thread(threaded_client, (conn, p, gameId)) # Runs independent to the while loop. Meaning that each session opened this function is run