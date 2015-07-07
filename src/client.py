import socket, select, sys

class Client:
    """
        Client class
        ------------
        
        Client class of chat application. It connects to the server and it asynchronously
        listen from server and standard input and pass the message to the server.
    """
    name = None
    handle = None
    password = None
    host = None
    port = None
    BUFFER = 4096
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    #constructor
    def __init__(self, name, handle, password, host, port):
        self.name = name
        self.handle = handle
        self.password = password
        self.host = host
        self.port = port
    #Get Handle
    def getHandle(self):
        return self.handle
    #Get Name
    def getName(self):
        return self.name
    #Get Details
    def getDetails(self):
        return (self.name, self.handle, self.password)
    #Get Add
    def getAdd(self):
        return (self.host, self.port)
    #Basic prompt
    def prompt(self):
        sys.stdout.write('<You>:')
        sys.stdout.flush()
    #Connection initialiser
    def conServer(self):
        """
            It start the client and make a connection to the server.
            It asynchronously listen to server and standard input.
            If present message is from standard input then it sends the message 
            to the server which brodcast it to all other user.
            And if message is from server then it output it to screen.
        """
        CONNECTIONS = [sys.stdin, self.sock]
        try:
            self.sock.connect(self.getAdd())
            self.sock.send(self.password)
            self.sock.send(self.handle)
            x = self.sock.recv(self.BUFFER)
            if x == '0':
                print 'Handle not available'
                exit(1)
        except:
            print 'Unable to connect'
            exit(1)
        print 'Connected to host'
        self.prompt()
        while True:
            rSocket, wSocket, eSocket = select.select(CONNECTIONS,[], [])
            
            for s in rSocket:
                if s == self.sock:
                    msg = s.recv(self.BUFFER)
                    if not msg:
                        print '\nDisconnected'
                        sys.exit()
                    else:
                        print
                        sys.stdout.write(msg)
                        self.prompt()
                else:
                    msg = sys.stdin.readline()
                    self.sock.send(msg)
                    self.prompt()
                        
if __name__ == '__main__':
    try:
        if sys.argv[1] == '-h' or sys.argv[1] == '--h' or sys.argv[1] == '-help': 
            print "usage client.py [Clinet-Name Handle Server-Password Server-IP | -h | --h | -help]"
        else:
            client = Client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], 50007)
            client.conServer()
    except IndexError:
        print 'Invalid Input format'
        print "usage client.py [Clinet-Name Handle Server-Password Server-IP | -h | --h | -help]"
        exit(1)