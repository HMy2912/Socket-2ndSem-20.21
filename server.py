import socket
import requests
import json
import os
import threading
import hashlib
# from getTeamList import Dict_fromAPI
HEADER = 64
PORT = 5050
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
RECEIVED_MESSAGE = 'RECEIVED\n'
clients, names = [], []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDRESS)
except socket.error as e:
    print(str(e))

file = open('key_value_api.json', 'r')
KeyValueJson = json.loads(file.read())
file.close()


def sendCommand(conn):
    conn.send(RECEIVED_MESSAGE.encode(FORMAT))


def startChat():
    print("SERVER now is on " + SERVER)

    server.listen()

    while True:
        try:
            conn, addr = server.accept()
            # sendCommand(conn)
            thread = threading.Thread(target=handle, args=(conn, addr))
            thread.start()
            print(f"ACTIVE CONNECTIONS: {threading.activeCount()-1}")
        except:
            print("Send Error...")


def nameByID(ID_Match):
    linkRequests = "http://livescore-api.com/api-client/scores/live.json?key=KEY&secret=VALUE"
    linkRequests = linkRequests.replace('KEY', KeyValueJson['key'])
    linkRequests = linkRequests.replace('VALUE', KeyValueJson['value'])
    try:
        apiRequest = requests.get(linkRequests)
        ScoreData = json.loads(apiRequest.content)
        for obj in ScoreData['data']['match']:
            if obj['id'] == ID_Match:
                return 'Home Team: ' + obj['home_name'] + '\n' + 'Away Team: ' + obj['id']['away_name'] + '\n'
    except Exception as e:
        print(f"Error... {e}")
        return []
    return []


def LiveScoreMessage(conn):
    linkRequests = "http://livescore-api.com/api-client/scores/live.json?key=KEY&secret=VALUE"
    linkRequests = linkRequests.replace('KEY', KeyValueJson['key'])
    linkRequests = linkRequests.replace('VALUE', KeyValueJson['value'])
    try:
        apiRequest = requests.get(linkRequests)
        ScoreData = json.loads(apiRequest.content)
        for obj in ScoreData['data']['match']:
            conn.send("{:<8} {:<17} {:<25} {:<10} {:<25} \n".format(
                obj['id'], obj['status'], obj['home_name'], obj['score'], obj['away_name']).encode(FORMAT))
    except Exception as e:
        print(f"Error... {e}")
        conn.send("Unable to show LIVE SCORE.\n".encode(FORMAT))


def searchByID_Match(conn, message):
    # https://livescore-api.com/api-client/matches/stats.json?match_id=172252&key=lQNUCP8IbJHbBeIe&secret=1l6a2MSLYLk0ry8MpWG1MPKYzr9aGRpH
    linkRequests = "https://livescore-api.com/api-client/matches/stats.json?match_id=MATCH_ID&key=KEY&secret=VALUE"
    linkRequests = linkRequests.replace('KEY', KeyValueJson['key'])
    linkRequests = linkRequests.replace('VALUE', KeyValueJson['value'])
    linkRequests = linkRequests.replace('MATCH_ID', message)
    try:
        apiRequest = requests.get(linkRequests)
        ScoreData = json.loads(apiRequest.content)
        M_send = 'Yellow cards: ' + ScoreData['data']['yellow_cards'] + '\n' + 'Red cards: ' + ScoreData['data']['red_cards'] + '\n' + 'Subtitutions: ' + ScoreData['data']['subtitutions'] + '\n' + 'Corner kicks: ' + ScoreData['data']['corners'] + '\n' + \
            'Number of players injured: ' + ScoreData['data']['treatments'] + '\n' + 'Attacks: ' + ScoreData['data']['attacks'] + '\n' + \
            'Dangerous attacks: ' + ScoreData['data']['dangerous_attacks'] + '\n' + \
            'Penalties: ' + \
            ScoreData['data']['penalties'] + '\n' + nameByID(message)
        conn.send(M_send.encode(FORMAT))
    except Exception as e:
        print(f"Error... {e}")
        conn.send("Unable to show ID in details.\n".encode(FORMAT))


def handle(conn, addr):
    print(f"NEW CONNECTION: {addr}")
    while True:
        # recieve message
        message = conn.recv(1024).decode(FORMAT)
        print(message)
        if message == DISCONNECT_MESSAGE:
            print(f"{DISCONNECT_MESSAGE}, {addr}")
            break
        elif message == 'LOG IN SUCCESSFULLY':
            conn.send("Welcome!!\n".encode(FORMAT))
        elif message == 'LIVE SCORE':
            LiveScoreMessage(conn)
        elif message.isnumeric():
            searchByID_Match(conn, message)
        else:
            try:
                conn.send(RECEIVED_MESSAGE.encode(FORMAT))
            except:
                print("ERROR")
                while not connected:
                    try:
                        conn.connect(addr)
                        connected = True
                    except socket.error as e:
                        print(e)
                break

    conn.close()


startChat()
