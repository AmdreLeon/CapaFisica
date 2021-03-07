class parser():

    def run(self):
        file = open("script.txt","r")
        return parser(file)

    def parser(self,file):
        def create_hub(self,command):
            return(command[2:])
            
        def create_host(self,command):
            print(command[2:])
            # make_create_host(t, elm1, elm2)
            pass  
        def connect(self,command):
            print(command[2:])
            pass  
        def send(self,command):
            pass    
        def disconnect(self,command):
            pass  
        commands = []
        current = 0
        while True:
            line = file.readline()
            if not line: break
            commands.append(line.split())
            if commands[current][1] == "create":
                if commands[current][2] == "hub":
                    create_hub(commands[current])
                else: 
                    create_host(commands[current])
            elif commands[current][1] == "connect":
                connect(commands[current])
            elif commands[current][1] == "send":
                send(commands[current])
            else:
                disconnect(commands[current])
            current += 1
        return commands


class cable():
    def __init__(self,port1,port2):
        self.port1 = port1
        self.port2 = port2
        self.status = "null"
        
class cumputer():
    def __init__(self,name):
        self.name = name
        
        
class hub():
    def __init__(self,name,c_ports):
        self.name = name 
        self.c_ports = c_ports