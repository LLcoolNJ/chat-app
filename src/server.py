import socket, select

class Server:
    """
        Server class
        ------------
        
        It is server class of chat application which accept connections from multiple
        clients. It asynchronously receives the message from all client and broadcast 
        it to all the other clients
    """
    CONNECTION_LIST = []
    BUFFER = 4096
    PORT = 50007
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clients = {}
    #constructor of the class
    def __init__(self, password):
        self.password = password
    #Broadcast message to all users
    def brodcastMsg(self, sender, msg):
        """
            It sends the messsage to all the clients which are presently connected 
            to the server. It search all live users in CONNECTION_LIST and sends the message.
        """
        for sock in self.CONNECTION_LIST:
            if sock != self.server_socket and sock != sender:
                try:
                    sock.send(msg)
                except:
                    sock.close()
                    self.CONNECTION_LIST.remove(sock)
    #Server initialiser
    def startServer(self):
        """
            It start the server and asynchronously listen to all connections (CONNECTION_LIST ).
            It receive the message and sends to all the available users by calling 
            brodcastMsg function.
        """
        self.server_socket.bind(('127.0.0.1', self.PORT))
        self.server_socket.listen(10)
        self.CONNECTION_LIST.append(self.server_socket)
        print 'Server is running'
        while True:
            try:
                rSocket, wSocket, eSocket = select.select(self.CONNECTION_LIST,[], [])
                
                for s in rSocket:
                    if s == self.server_socket:
                        sockfd, addr = self.server_socket.accept()
                        password = sockfd.recv(self.BUFFER)
                        if password.strip() != self.password:
                            sockfd.close()
                            continue
                        self.CONNECTION_LIST.append(sockfd)
                        handle = sockfd.recv(self.BUFFER)
                        if handle in self.clients.values():
                            sockfd.send('0')
                            sockfd.close()
                            self.CONNECTION_LIST.remove(sockfd)
                            continue
                        sockfd.send('1')
                        self.clients[sockfd] = handle
                        print 'Client (%s, %s, %s) connected' % (addr[0], addr[1], self.clients[sockfd]) 
                        self.brodcastMsg(sockfd, "\n[%s] entered room\n" % self.clients[sockfd])
                    else:
                        try:
                            msg = s.recv(self.BUFFER)
                            if msg:
                                self.brodcastMsg(s, '[' + self.clients[s] + ']' + msg)
                        except:
                            self.brodcastMsg(s, "\n[%s] exited room" % self.clients[s])
                            print "Client (%s, %s, %s) is offline" % (addr[0], addr[1], self.clients[s]) 
                            s.close()
                            self.CONNECTION_LIST.remove(s)
                            continue
            except KeyboardInterrupt:
                exit(1)
if __name__ == '__main__':
    print "usage server.py Server-Password"
    server = Server('123')
    server.startServer()