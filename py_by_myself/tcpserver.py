from socket import *
from time import ctime

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print('waiting for connection...')
    tcpCliSock,addr = tcpSerSock.accept()
    print('...connect from:',addr)
    
    while True:
        data = tcpCliSock.recv(BUFSIZ)
        print(data)
        if not data:
            break
        tcpCliSock.send(data)
        
    tcpCliSock.close()
tcpSerSock.close()