class cable():
    def __init__(self,port1,port2):
        self.port1 = port1
        self.port2 = port2
        self.status = "null"
        
class cumputer():
    def __init__(self,name):
        self.name = name
        self.status = "receving"
        
        
class hub():
    def __init__(self,name,c_ports):
        self.name = name 
        self.c_ports = c_ports
        self.computers_list = []

def connect(port1,port2):
    if (type(port1) is hub):
        pass


a = hub("andres",1)

print(type(a))