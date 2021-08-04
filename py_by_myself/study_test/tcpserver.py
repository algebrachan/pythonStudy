from socket import *
from datetime import datetime
from socketserver import (TCPServer as TCP,StreamRequestHandler as SRH)


HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)

# tcpSerSock = socket(AF_INET,SOCK_STREAM)
# tcpSerSock.bind(ADDR)
# tcpSerSock.listen(5)

# while True:
#     print('waiting for connection...')
#     tcpCliSock,addr = tcpSerSock.accept()
#     print('...connect from:',addr)
    
#     while True:
#         data = tcpCliSock.recv(BUFSIZ).decode('utf-8')
#         data = f'{data}-{datetime.now()}'
#         if not data:
#             break
#         tcpCliSock.send(data.encode('utf-8'))
        
#     tcpCliSock.close()
# tcpSerSock.close()


class MyRequestHandler(SRH):
  def handle(self):
    print('...connect from:',self.client_address)
    self.data = self.request.recv(BUFSIZ).strip()
    self.request.sendall(f'{self.data}:{datetime.now()}'.encode('utf-8'))

tcpServ = TCP(ADDR,MyRequestHandler)
print('waiting for connection...')
tcpServ.serve_forever()