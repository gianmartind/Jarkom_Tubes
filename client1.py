import socket
import threading
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

  while True:
    in_data = client.recv(1024)
    print("From Server :" ,in_data.decode())

threading.Thread(target=receiver).start()
while True:
  out_data = input()
  client.sendall(bytes(out_data,'UTF-8'))
  if out_data=='bye':
    break
client.close()
