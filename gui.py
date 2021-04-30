from tkinter import *
from tkinter import messagebox
import random as r
import socket
import threading

def tombol(frame):         
    b=Button(frame,padx=1,bg="pale turquoise",width=3,text="   ",font=('arial',70,'bold'),relief="sunken",bd=10)
    return b
'''
def mengganti_operand():             
    global a
    for i in ['O','X']:
        if not(i==a):
            a=i
            break
'''
'''        
def check():
    i = 0
    while i < 3:
            if(b[i][0]["text"]==b[i][1]["text"]==b[i][2]["text"]==a or b[0][i]["text"]==b[1][i]["text"]==b[2][i]["text"]==a):
                    messagebox.showinfo("Selamat, pemain","'"+a+"' menang!")
                    permainan_kembali_dari_awal()
            i = i + 1
    if(b[0][0]["state"]==b[0][1]["state"]==b[0][2]["state"]==b[1][0]["state"]==b[1][1]["state"]==b[1][2]["state"]==b[2][0]["state"]==b[2][1]["state"]==b[2][2]["state"]==DISABLED):
        messagebox.showinfo("Permainan telah berakhir dan hasilnya seri!")
        permainan_kembali_dari_awal()
    elif(b[0][0]["text"]==b[1][1]["text"]==b[2][2]["text"]==a or b[0][2]["text"]==b[1][1]["text"]==b[2][0]["text"]==a):
        messagebox.showinfo("Selamat, pemain","'"+a+"' menang!")
        permainan_kembali_dari_awal()   
'''            
def masukkan_pilihan(row,col):
    global client
        #b[row][col].config(text=a,state=DISABLED,disabledforeground=colour[a])
        #check()
        #mengganti_operand()
        #label.config(text="Sekarang giliran "+a)
    client.sendall(bytes(str(row) + ' ' + str(col),'UTF-8'))

def set_board(board_tiles):
    global b
    print(board_tiles)
    i = 0
    row = 0
    while row < len(b):
        col = 0
        while col < len(b[row]):
            b[row][col].config(text=board_tiles[i], disabledforeground=colour[board_tiles[i]])
            col = col + 1
            i = i + 1
        row = row + 1


'''       
def permainan_kembali_dari_awal():                
    global a
    i = 0
    while i < 3:
        j = 0
        while j < 3:
                b[i][j]["text"]=" "
                b[i][j]["state"]=NORMAL
                j = j + 1
        i = i + 1
    a=r.choice(['O','X'])
'''
#GUI comp
root=Tk()                  
root.title("Game TicTacToe")   
a=r.choice(['O','X'])       
colour={'O':"purple",'X':"medium blue", ' ':"black"}
b=[[],[],[]]
for i in range(3):
        for j in range(3):
                b[i].append(tombol(root))
                b[i][j].config(command= lambda row=i,col=j:masukkan_pilihan(row,col))
                b[i][j].grid(row=i,column=j)
label=Label(text="",font=('arial',25,'bold'))
label.grid(row=3,column=0,columnspan=3)
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
    global label
    while True:
        in_data = client.recv(1024)
        inp = in_data.decode()
        if inp.startswith('s_'):
            status = inp.split('_')[1]
            label.config(text=status)
        elif inp.startswith('b_'):
            board = inp.split('_')[1]
            print(board)
            board_tiles = board.split('|')
            print(board_tiles)
            set_board(board_tiles)
        elif inp.startswith('m_'):
            msg = inp.split('_')[1]
            messagebox.showinfo(msg)
    #print("From Server :" ,in_data.decode())

threading.Thread(target=receiver).start()

root.mainloop()
