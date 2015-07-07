import socket, select, sys, logging, time

class Server:
    """
        Server class
        ------------
        
        It is server class of chat application which accept connections from multiple
        clients. It asynchronously receives the message from all client and broadcast 
        it to all the other clients
    """
    CONNECTIONS = []
    BUFFER = 4096
    PORT = 50007
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clients = {}
    #constructor of the class
    def __init__(self, password):
        fl = time.strftime("%d %b %Y %H-%M-%S") + '.log'
        logging.basicConfig(filename = fl, level = logging.DEBUG)
        self.password = password
    #Broadcast message to all users
    def brodcastMsg(self, sender, msg):
        """
            It sends the messsage to all the clients which are presently connected 
            to the server. It search all live users in CONNECTIONS and sends the message.
        """
        for sock in self.CONNECTIONS:
            if sock != self.server_socket and sock != sender:
                try:
                    sock.send(msg)
                except:
                    sock.close()
                    self.CONNECTIONS.remove(sock)
    #Server initialiser
    def startServer(self):
        """
            It start the server and asynchronously listen to all connections (CONNECTIONS ).
            It receive the message and sends to all the available users by calling 
            brodcastMsg function.
        """
        logging.info('Server is running')
        self.server_socket.bind(('127.0.0.1', self.PORT))
        self.server_socket.listen(10)
        self.CONNECTIONS.append(self.server_socket)
        print 'Server is running'
        while True:
            try:
                rSocket, wSocket, eSocket = select.select(self.CONNECTIONS,[], [])
                
                for s in rSocket:
                    if s == self.server_socket:
                        sockfd, addr = self.server_socket.accept()
                        password = sockfd.recv(self.BUFFER)
                        if password.strip() != self.password:
                            sockfd.close()
                            continue
                        self.CONNECTIONS.append(sockfd)
                        handle = sockfd.recv(self.BUFFER)
                        if handle in self.clients.values():
                            sockfd.send('0')
                            sockfd.close()
                            self.CONNECTIONS.remove(sockfd)
                            continue
                        sockfd.send('1')
                        self.clients[sockfd] = handle
                        logging.info('Client (%s, %s, %s) connected' % (addr[0], addr[1], self.clients[sockfd]))
                        print 'Client (%s, %s, %s) connected' % (addr[0], addr[1], self.clients[sockfd]) 
                        logging.info("[%s] entered room" % self.clients[sockfd])
                        self.brodcastMsg(sockfd, "[%s] entered room\n" % self.clients[sockfd])
                    else:
                        try:
                            msg = s.recv(self.BUFFER)
                            if msg:
                                logging.info('<' + self.clients[s] + '>:' + msg.strip())
                                self.brodcastMsg(s, '<' + self.clients[s] + '>:' + msg)
                        except:
                            logging.info("[%s] exited room" % self.clients[s])
                            self.brodcastMsg(s, "[%s] exited room\n" % self.clients[s])
                            logging.info("Client (%s, %s, %s) is offline" % (addr[0], addr[1], self.clients[s]))
                            print "Client (%s, %s, %s) is offline" % (addr[0], addr[1], self.clients[s]) 
                            self.clients.pop(s)
                            s.close()
                            self.CONNECTIONS.remove(s)
                            continue
            except KeyboardInterrupt:
                logging.info('Got Interrupt clossing server')
                exit(1)
if __name__ == '__main__':
    try:
        if sys.argv[1] == '-h' or sys.argv[1] == '--h' or sys.argv[1] == '-help': 
            print "usage server.py [Server-Password | -h | --h | -help]"
        else:
            passw = sys.argv[1]
            server = Server(passw)
            server.startServer()
    except IndexError:
        print 'Invalid input format'
        print "usage server.py [Server-Password | -h | --h | -help]"