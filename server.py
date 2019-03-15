import socket
from _thread import *
import pickle
from game import Game

server = "192.168.10.170"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("waiting for a connection, server started")


connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == 'reset':
                        game.resetWent()
                    elif data != 'get':
                        game.play(p, data)
                reply = game
                conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break
    print("lost connection")
    try:
        del games[gameId]
        print("closing game: ", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount-1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print('creating a new game...')
    else:
        games[gameId].ready = True
        p = 1
    start_new_thread(threaded_client, (conn, p, gameId))

