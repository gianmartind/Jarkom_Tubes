import socket, threading

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket, playerNo):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = clientAddress
        self.player = playerNo
        self.symbol = ''
        if self.player == 1:
            self.symbol = 'X'
        elif self.player == 2:
            self.symbol = 'O'
        print ("New connection added: ", self.caddress)

    def run(self):
        global text
        global clients
        global status
        global tiles
        global current_player
        global isStarted

        print ("Connection from : ", self.caddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        self.csocket.send(bytes('player_{}'.format(self.player), 'UTF-8'))

        for c in clients.keys():
            clients[c].sendStatus()

        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            print ("from player {}:".format(self.player), msg)
            if isStarted:
                if current_player == self.player:
                    pos = msg.split()
                    tiles[int(pos[0])][int(pos[1])] = str(self.symbol)
                    #text = text + " (from {no}: {msg})".format(no=self.player, msg = msg)
                    for c in clients.keys():
                        clients[c].sendBoard()
                    
                    if check_win() == 1:
                        for c in clients.keys():
                            clients[c].sendMessage('player 1 win')
                        isStarted = False
                    elif check_win() == 2:
                        for c in clients.keys():
                            clients[c].sendMessage('player 2 win')
                        isStarted = False
                    elif check_win() == 0:
                        for c in clients.keys():
                            clients[c].sendMessage('draw')
                        isStarted = False

                    if current_player == 1:
                        current_player = 2
                    else:
                        current_player = 1
                else:
                    self.sendMessage('not your turn!')
            else:
                self.sendMessage('game not started!')
        self.csocket.close()
        print ("Client at ", self.caddress , " disconnected...")

    def sendStatus(self):
        global status
        self.csocket.send(bytes('s_{}'.format(status),'UTF-8'))

    def sendMessage(self, text):
        self.csocket.send(bytes('m_{}'.format(text),'UTF-8'))
    
    def sendBoard(self):
        global tiles
        board = str(tiles[0][0] + '|' + tiles[0][1] + '|' + tiles[0][2] + '|' +
                    tiles[1][0] + '|' + tiles[1][1] + '|' + tiles[1][2] + '|' +
                    tiles[2][0] + '|' + tiles[2][1] + '|' + tiles[2][2] + '|')
        print(board)
        self.csocket.send(bytes('b_{}'.format(board), 'UTF-8'))


LOCALHOST = "localhost"
PORT = 35421
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for player...")

status = "waiting for player..."
player_no = 1
clients = dict()

current_player = 1
isStarted = False
roundN = 1

tiles = list()
def init_tiles():
    global tiles
    tiles = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
  
def playGame():
    global isStarted
    init_tiles()
    isStarted = True

def check_win():
    i = 0
    while i < 3:
        if(tiles[i][0]==tiles[i][1]==tiles[i][2]=='X' or tiles[0][i]==tiles[1][i]==tiles[2][i]=='X'):
                return 1
        if(tiles[i][0]==tiles[i][1]==tiles[i][2]=='O' or tiles[0][i]==tiles[1][i]==tiles[2][i]=='O'):
                return 2
        i = i + 1
    if(tiles[0][0]==tiles[0][1]==tiles[0][2]==tiles[1][0]==tiles[1][1]==tiles[1][2]==tiles[2][0]==tiles[2][1]==tiles[2][2]=="X" or 
        tiles[0][0]==tiles[0][1]==tiles[0][2]==tiles[1][0]==tiles[1][1]==tiles[1][2]==tiles[2][0]==tiles[2][1]==tiles[2][2]=="O"):
        return 0
        
    elif(tiles[0][0]==tiles[1][1]==tiles[2][2]=='X' or tiles[0][2]==tiles[1][1]==tiles[2][0]=='X'):
        return 1
        
    elif(tiles[0][0]==tiles[1][1]==tiles[2][2]=='O' or tiles[0][2]==tiles[1][1]==tiles[2][0]=='O'):
        return 2
    
    return -1

while player_no <= 2:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    clients[player_no] = ClientThread(clientAddress, clientsock, player_no)
    clients[player_no].start()
    player_no = player_no + 1

playGame()
status = "player-found_{r}_{s}".format(r=roundN, s=1)

