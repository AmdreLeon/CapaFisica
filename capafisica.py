import random as rd
import os

class System():
    def __init__(self):
        self.network = Network()
        self.subnetworks = []
        self.globaltime = 0
        self.signal_time = 10
        
    def create_hub(self,command):
        sn = SubNetwork([],len(self.subnetworks))
        hub_ = Hub(command[3],int(command[4]),sn)
        sn.devices_list.append(hub_)
        hub_.my_subnetwork = sn
        self.network.add_vertex(hub_)
        self.subnetworks.append(sn)
        return hub_
        
    def create_host(self,command):
        sn = SubNetwork([],len(self.subnetworks))
        computer_ = Computer(command[3],int(command[0]),sn)
        sn.devices_list.append(computer_)
        computer_.my_subnetwork = sn
        self.network.add_vertex(computer_)
        self.subnetworks.append(sn)
        return computer_
        
    def connect(self,command):
        a = None
        b = None
        for i in self.network.get_vertex)l():
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
            self.network.add_edge(a,b,(b.ports[port2],a.ports[port1]),(a.ports[port1],b.ports[port2]))
            DFS(self)  
            for sn in self.subnetworks:
                sn.update()
        
    def disconnect(self,command):
        a = None
        for i in self.network.get_vertex)l():
            for p in range(0,len(i.ports)):
                if i.ports[p] == command[2] and i.connected[p]:
                    a = i
                    i.connected[p] = 0
                    break
        for b in self.network.vertex_list[a].connected_to:
            if b[1] == command[2]:
                self.network.vertex_list[a].connected_to[b].id.connected[int(b[0][len(b[0])-1])-1] = 0
                self.network.del_edge(a,self.network.vertex_list[a].connected_to[b].id,b,(command[2],b[0]))
                break
        DFS(self)
        for sn in self.subnetworks:
            sn.update()
        
    def send(self,command):
        for i in self.network.get_vertex)l():
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
        self.signal_time = int(file.readline().split()[1])
        current = 0
        keep = 1
        while(len(commands) or keep):
            keep = 0 
            while(len(commands) and int(commands[current][0]) == self.globaltime):
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

            for pc_hub in self.network.get_vertex)l():
                if len(commands) == 0:
                    if type(pc_hub) is Computer:
                        if len(pc_hub.process) >= 1:
                            keep = 1

                if self.globaltime % self.signal_time == 0:
                    pc_hub.print_status(self.globaltime)
                pc_hub.update(self.signal_time)
            for sn in self.subnetworks:
                sn.update()
            self.globaltime +=1
        
        for i in self.network.get_vertex)l():
            i.my_file.close()

class Computer():
    def __init__(self,name,time,my_subnetwork):
        self.name = name
        self.status = "receiving"
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

    def update(self,sgntime):
        if self.status == "sending" and self.my_subnetwork.pc is self:
            a = int((self.process_pointer-1) / sgntime)
            self.my_subnetwork.status = self.process[0][a]
            if (self.process_pointer / sgntime) == len(self.process[0]):
                self.process.pop(0)
                self.procces_pointer = 0
                self.status = "receiving"
                self.my_subnetwork.pc = None
            else:
                self.process_pointer += 1 
        else:
            self.status = "receiving"

        if len(self.process) == 0:
            self.ready = 0
        else:
            self.ready = 1
        return
    
    def print_status(self,globaltime):
        self.my_file.write(str(globaltime) + " " +  str(self.ports[0]) + " " + self.status + " " + self.my_subnetwork.status+'\n')

class Cable():
    def __init__(self,port1,port2):
        self.port1 = port1
        self.port2 = port2
        self.status = "null"
                
class Hub():
    def __init__(self,name,c_ports,my_subnetwork):
        self.name = name 
        self.c_ports = c_ports
        self.computers_list = []
        self.ports = [name + "_" + str(i) for i in range(1, c_ports + 1)]
        self.connected = [0 for i in range(0,c_ports)]
        self.status = "receiving"
        self.my_subnetwork = my_subnetwork
        self.my_file = open("./output/"+name+".txt","w")
        
    def print_status(self, globaltime):
        for port in range(0,self.c_ports):
            if self.connected[port]:
                self.my_file.write(str(globaltime) + " " +  str(self.ports[port]) + " " + self.status + " " + self.my_subnetwork.status+'\n')  

    def update (self,sgntime):
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
            if type(comp) is Computer:
                comp.sending()
    
    def update(self):
        for c in self.devices_list:
            c.my_subnetwork = self
        if self.pc is None:
            for device in self.devices_list:
                if type(device) is Computer and device.ready:
                    self.pc = device
                    self.pc.status = "sending"
                    return
            self.status = "null"
                    
class Device():
    def __init__(self,clave):
        self.id = clave
        self.connected_to = {}
        self.visited = 0

    def add_neighbour(self,vecino,port):
        self.connected_to[port] = vecino

    def delete_neighbour(self,port):
        del self.connected_to[port]
    
    def __str__(self):
        return str(self.id) + ' connected to: ' + str([x.id for x in self.connected_to])

    def get_connections(self):
        return self.connected_to.values()

    def get_id(self):
        return self.id
   
class Network:
    def __init__(self):
        self.vertex_list = {}
        self.num_vertex = 0

    def add_vertex(self,clave):
        self.num_vertex = self.num_vertex + 1
        new_vertex = Device(clave)
        self.vertex_list[clave] = new_vertex
        return new_vertex

    # def obtenerVertice(self,n):
    #     if n in self.vertex_list:
    #         return self.vertex_list[n]
    #     else:
    #         return None

    def __contains__(self,n):
        return n in self.vertex_list

    def add_edge(self,from_,to,port1,port2):
        """
        if from_ not in self.vertex_list:
            nv = self.add_vertex(from)
        if to not in self.vertex_list:
            nv = self.add_vertex(to)
        """
        self.vertex_list[from_].add_neighbour(self.vertex_list[to], port1)
        self.vertex_list[to].add_neighbour(self.vertex_list[from_], port2)
        
    def del_edge(self,from_,to,port1,port2):
        self.vertex_list[from_].delete_neighbour(port1)
        self.vertex_list[to].delete_neighbour(port2)
        
    def get_vertex(self):
        return self.vertex_list.keys()

    def __iter__(self):
        return iter(self.vertex_list.values())
 
def DFS(system):
    system.subnetworks = []
    cc = 0
    for vertex in system.network.get_vertex)l():
        if not system.network.vertex_list[vertex].visited:
            system.subnetworks.append(SubNetwork(DFS_VISIT(system.network,vertex,[]),cc))
            vertex.subnetwork = system.subnetworks[cc]
            cc+=1
    for vertex in system.network.vertex_list:
        system.network.vertex_list[vertex].visited = 0
    return system.subnetworks
     
def DFS_VISIT(graph, source,path = []):
    (graph.vertex_list[source]).visited = 1
    if source not in path:
        path.append(source)
        if source not in graph:
        # leaf node, backtrack
            return path
        for neighbour in graph.vertex_list[source].get_connections():
            if neighbour not in path:
                path = DFS_VISIT(graph, neighbour.id, path)
    return path

# def randomGraph(graph):
#     my_list = [graph.add_vertex(rd.randint(0,100)) for i in range(0,50)]
#     for j in my_list:
#         o = rd.randint(0,1)
#         if o:
#             graph.add_edge(j.id,my_list[rd.randint(0,49)].id)
            
S = System()
S.run()