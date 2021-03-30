import random as rd
import os

class System():
    def __init__(self):
        self.network = Network()
        self.subnetworks = []
        self.globaltime = 0
        
    def create_hub(self,command):
        sn = SubNetwork([],len(self.subnetworks))
        hub_ = hub(command[3],int(command[4]),sn)
        sn.devices_list.append(hub_)
        hub_.my_subnetwork = sn
        self.network.agregarVertice(hub_)
        self.subnetworks.append(sn)
        return hub_
        
    def create_host(self,command):
        sn = SubNetwork([],len(self.subnetworks))
        computer_ = computer(command[3],int(command[0]),sn)
        sn.devices_list.append(computer_)
        computer_.my_subnetwork = sn
        self.network.agregarVertice(computer_)
        self.subnetworks.append(sn)
        return computer_
        
    def connect(self,command):
        a = None
        b = None
        for i in self.network.obtenerVertices():
            for p in range(0,len(i.ports)):
                if i.ports[p] == command[2] and not i.connected[p]:
                    a = i
                    i.connected[p] = 1
                    port1 = p
                elif i.ports[p] == command[3] and not i.connected[p]:
                    b = i
                    i.connected[p] = 1
                    port2 = p
        if a and b:
            self.network.agregarArista(a,b,(b.ports[port2],a.ports[port1]),(a.ports[port1],b.ports[port2]))
            DFS(self)  
            for sn in self.subnetworks:
                sn.update()
        
    def disconnect(self,command):
        a = None
        for i in self.network.obtenerVertices():
            for p in range(0,len(i.ports)):
                if i.ports[p] == command[2] and i.connected[p]:
                    a = i
                    i.connected[p] = 0
                    break
        for b in self.network.listaVertices[a].conectadoA:
            if b[1] == command[2]:
                self.network.listaVertices[a].conectadoA[b].id.connected[int(b[0][len(b[0])-1])-1] = 0
                self.network.eliminarArista(a,self.network.listaVertices[a].conectadoA[b].id,b,(command[2],b[0]))
                break
        DFS(self)
        for sn in self.subnetworks:
            sn.update()
        
    def send(self,command):
        for i in self.network.obtenerVertices():
            if i.name == command[2]:
                pc_current = i
        pc_current.process.append(command[3])  
        pc_current.ready = 1
        return pc_current
            
    def parser(self,file):
        commands = []
        while True:
            line = file.readline()
            if not line: break
            commands.append(line.split())    
        return commands
    
    def run(self):
        file = open("script.txt","r")
        commands = self.parser(file)
        file.close()
        file = open("config.txt","r")
        signal_time = int(file.readline().split()[1])
        current = 0
        keep = 1
        while(len(commands) or keep):
            keep = 0 
            if len(commands) and int(commands[current][0]) == self.globaltime:
                if commands[current][1] == "create":
                    if commands[current][2] == "hub":
                        self.create_hub(commands[current])
                        commands.pop(current)
                    else: 
                        self.create_host(commands[current])
                        commands.pop(current)
                elif commands[current][1] == "connect":
                    self.connect(commands[current])
                    commands.pop(current)
                elif commands[current][1] == "send":
                    self.send(commands[current])
                    commands.pop(current)
                else:
                    self.disconnect(commands[current])
                    commands.pop(current)
                    
            for pc_hub in self.network.obtenerVertices():
                if len(commands) == 0:
                    if type(pc_hub) is computer:
                        if len(pc_hub.process) >= 1:
                            keep = 1

                if self.globaltime % signal_time == 0:
                    pc_hub.print_status(self.globaltime)
                pc_hub.update()
            for sn in self.subnetworks:
                sn.update()
            self.globaltime +=1
        
        for i in self.network.obtenerVertices():
            i.my_file.close()
        
class computer():
    def __init__(self,name,time,my_subnetwork):
        self.name = name
        self.status = "receive"
        self.time = time
        self.ports = [name + "_1"]
        self.process = []
        self.process_pointer = 0
        self.current = 0
        self.connected = [0]
        self.my_subnetwork = my_subnetwork
        self.ready = 0
        self.t_sends = 0
        self.my_file = open("./output/"+name+".txt","w")
            
    # def sending(self,value):
    #     # if self.t_sends > 16:
    #     #     self.process.pop(0)
    #     # else:
    #     if self.my_subnetwork.status != "null" or self.my_subnetwork.pc is not self:
    #         # self.t_sends += 1
    #     else:
    #         self.my_subnetwork.status = self.process[self.current]

    def update(self):
        if self.status == "sending" and self.my_subnetwork.pc is self:
            self.my_subnetwork.status = self.process[0][self.process_pointer-1]
            if self.process_pointer == len(self.process[0]):
                self.process.pop(0)
                self.procces_pointer = 0
                self.status = "receive"
            else:
                self.process_pointer += 1 
        else:
            self.status = "receive"

        if len(self.process) == 0:
            self.ready = 0
        else:
            self.ready = 1
        return
    
    def print_status(self,globaltime):
        self.my_file.write(str(globaltime) + " " +  str(self.ports[0]) + " " + self.status + " " + self.my_subnetwork.status+'\n')

class cable():
    def __init__(self,port1,port2):
        self.port1 = port1
        self.port2 = port2
        self.status = "null"
                
class hub():
    def __init__(self,name,c_ports,my_subnetwork):
        self.name = name 
        self.c_ports = c_ports
        self.computers_list = []
        self.ports = [name + "_" + str(i) for i in range(1, c_ports + 1)]
        self.connected = [0 for i in range(0,c_ports)]
        self.status = "receive"
        self.my_subnetwork = my_subnetwork
        self.my_file = open("./output/"+name+".txt","x")
        
    def print_status(self, globaltime):
        for port in range(0,self.c_ports):
            if self.connected[port]:
                self.my_file.write(str(globaltime) + " " +  str(self.ports[0]) + " " + self.status + " " + self.my_subnetwork.status+'\n')  

    def update (self):
        return
       
                     
class SubNetwork():
    def __init__(self,devices_list,cc):
        self.devices_list = devices_list
        self.time = 0
        self.id = cc
        self.status = "null"
        self.pc = None
        
    def value(self):
        for comp in self.network:
            if type(comp) is computer:
                comp.sending()
    
    def update(self):
        for c in self.devices_list:
            c.my_subnetwork = self
        if self.pc is None:
            for device in self.devices_list:
                if type(device) is computer and device.ready:
                    self.pc = device
                    self.pc.status = "sending"
                    return
            self.status = "null"
                    

        
class Divice():
    def __init__(self,clave):
        self.id = clave
        self.conectadoA = {}
        self.visited = 0

    def agregarVecino(self,vecino,port):
        self.conectadoA[port] = vecino

    def eliminarVecino(self,port):
        del self.conectadoA[port]
    
    def __str__(self):
        return str(self.id) + ' conectadoA: ' + str([x.id for x in self.conectadoA])

    def obtenerConexiones(self):
        return self.conectadoA.values()

    def obtenerId(self):
        return self.id

    #def obtenerPonderacion(self,vecino):
    #    return self.conectadoA[vecino]
    
class Network:
    def __init__(self):
        self.listaVertices = {}
        self.numVertices = 0

    def agregarVertice(self,clave):
        self.numVertices = self.numVertices + 1
        nuevoVertice = Divice(clave)
        self.listaVertices[clave] = nuevoVertice
        return nuevoVertice

    def obtenerVertice(self,n):
        if n in self.listaVertices:
            return self.listaVertices[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.listaVertices

    def agregarArista(self,de,a,port1,port2):
        """
        if de not in self.listaVertices:
            nv = self.agregarVertice(de)
        if a not in self.listaVertices:
            nv = self.agregarVertice(a)
        """
        self.listaVertices[de].agregarVecino(self.listaVertices[a], port1)
        self.listaVertices[a].agregarVecino(self.listaVertices[de], port2)
        
    def eliminarArista(self,de,a,port1,port2):
        self.listaVertices[de].eliminarVecino(port1)
        self.listaVertices[a].eliminarVecino(port2)
        
    def obtenerVertices(self):
        return self.listaVertices.keys()

    def __iter__(self):
        return iter(self.listaVertices.values())
 
def DFS(system):
    system.subnetworks = []
    cc = 0
    for vertex in system.network.obtenerVertices():
        if not system.network.listaVertices[vertex].visited:
            system.subnetworks.append(SubNetwork(DFS_VISIT(system.network,vertex,[]),cc))
            vertex.subnetwork = system.subnetworks[cc]
            cc+=1
    for vertex in system.network.listaVertices:
        system.network.listaVertices[vertex].visited = 0
    return system.subnetworks
     
def DFS_VISIT(graph, source,path = []):
    (graph.listaVertices[source]).visited = 1
    if source not in path:
        path.append(source)
        if source not in graph:
        # leaf node, backtrack
            return path
        for neighbour in graph.listaVertices[source].obtenerConexiones():
            if neighbour not in path:
                path = DFS_VISIT(graph, neighbour.id, path)
    return path

def randomGraph(graph):
    lista = [graph.agregarVertice(rd.randint(0,100)) for i in range(0,50)]
    for j in lista:
        o = rd.randint(0,1)
        if o:
            graph.agregarArista(j.id,lista[rd.randint(0,49)].id)
            
S = System()
S.run()
print(1)
"""
a = Network()
randomGraph(a)
G = System()
G.network = a
ll = DFS(G)
for i in ll:
    print(i.network , i.id)
print(["hub"+"_"+str(i) for i in range(1,8)])
#a.agregarArista(22,1)
#print(DFS(a))
"""
