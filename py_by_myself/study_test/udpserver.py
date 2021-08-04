from socket import *
from datetime import datetime

HOST = '127.0.0.1'
PORT = 21568
BUFSIZ = 1024
ADDR = (HOST,PORT)

udpSerSock = socket(AF_INET,SOCK_DGRAM)
udpSerSock.bind(ADDR)
print('waiting for message...')

while True:
  data,addr = udpSerSock.recvfrom(BUFSIZ)
  data = data.decode('utf-8')
  data = f'{data}:{datetime.now()}'
  udpSerSock.sendto(data.encode('utf-8'),addr)
  print('...received from and returned to:',addr)

udpSerSock.close()