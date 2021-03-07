def run():
    file = open("script.txt","r")
    return parser(file)

def create_hub(command):
    print(command[2:])
    pass
def create_host(command):
    print(command[2:])
    pass  
def connect(command):
    print(command[2:])
    pass  
def send(command):
    pass    
def disconnect(command):
    pass  

def parser(file):
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

