from tkinter import *
from tkinter import messagebox
import random as r
import socket
import threading

def tombol(frame):         
    b=Button(frame,padx=1,bg="pale turquoise",width=3,text="   ",font=('arial',40,'bold'),relief="sunken",bd=10)
    return b
        
def masukkan_pilihan(row,col):
    global client
    client.sendall(bytes(str(row) + ' ' + str(col),'UTF-8'))

def set_board(board_tiles):
    global b
    print(board_tiles)
    i = 0
    row = 0
    while row < len(b):
        col = 0
        while col < len(b[row]):
            if board_tiles[i] != ' ':
                b[row][col].config(text=board_tiles[i], disabledforeground=colour[board_tiles[i]], state=DISABLED)
            else:
                b[row][col].config(text=board_tiles[i], disabledforeground=colour[board_tiles[i]])
            col = col + 1
            i = i + 1
        row = row + 1

#GUI comp
root=Tk()                  
root.title("TicTacToe")   
a=r.choice(['O','X'])       
colour={'O':"purple",'X':"medium blue", ' ':"black"}
b=[[],[],[]]
for i in range(3):
        for j in range(3):
                b[i].append(tombol(root))
                b[i][j].config(command= lambda row=i,col=j:masukkan_pilihan(row,col))
                b[i][j].grid(row=i,column=j)

#label untuk keterangan player
player=Label(text="",font=('arial',10,'bold'))
player.grid(row=3,column=0,columnspan=1)
#label untuk ronde
roundN=Label(text="Round: 1/5", font=('arial',10,'bold'))
roundN.grid(row=3,column=1,columnspan=1)
#label untuk score
score=Label(text="Player 1: 4 | Player 2: 1", font=('arial',8,'bold'))
score.grid(row=3,column=2,columnspan=1)
root.resizable(False, False)

#client
SERVER = "localhost"
PORT = 35421
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

player_no = 0

player_data = client.recv(1024).decode()
if player_data.startswith("player"):
  player_no = player_data.split('_')[1]
  print("You're player {}".format(player_no))

def receiver():
    global client
    global player
    global roundN
    while True:
        in_data = client.recv(1024)
        inp = in_data.decode()
        if inp.startswith('s_'):
            status = inp.split('_')[1]
            if status == 'player-found':
                player.config(text="Player {}".format(player_no))
            else:
                player.config(text=status)
            roundnum = inp.split('_')[2]
            player.config(text="Round {}/5".format(roundnum))
        elif inp.startswith('b_'):
            board = inp.split('_')[1]
            print(board)
            board_tiles = board.split('|')
            print(board_tiles)
            set_board(board_tiles)
        elif inp.startswith('m_'):
            msg = inp.split('_')[1]
            messagebox.showinfo(title="Message", message=msg.upper())
    #print("From Server :" ,in_data.decode())

threading.Thread(target=receiver).start()

root.mainloop()
