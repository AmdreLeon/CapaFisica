import components as cm
import random as rd
import os
import shutil as sh
import sys


class System():
    def __init__(self):
        self.network = cm.Network()
        self.subnetworks = []
        self.hosts = []
        self.hubs = []
        self.switches = []
        self.globaltime = 0
        self.signal_time = 10

    def create_hub(self, command):
        sn = cm.SubNetwork([], len(self.subnetworks))
        hub_ = cm.Hub(command[3], int(command[4]), sn)
        sn.devices_list.append(hub_)
        hub_.my_subnetwork = sn
        self.network.add_vertex(hub_)
        self.subnetworks.append(sn)
        self.hubs.append(hub_)
        return hub_
    
    def create_switch(self,command):
        sn = cm.SubNetwork([], len(self.subnetworks))
        switch_ = cm.Switch(command[3], int(command[4]), sn)
        sn.devices_list.append(switch_)
        switch_.my_subnetwork = sn
        self.network.add_vertex(switch_)
        self.subnetworks.append(sn)
        self.switches.append(switch_)
        return switch_
    
    def create_host(self, command):
        sn = cm.SubNetwork([], len(self.subnetworks))
        computer_ = cm.Computer(command[3], int(command[0]), sn)
        sn.devices_list.append(computer_)
        computer_.my_subnetwork = sn
        self.network.add_vertex(computer_)
        self.subnetworks.append(sn)
        self.hosts.append(computer_)
        return computer_

    def connect(self, command):
        a = None
        b = None
        for i in self.network.get_vertex():
            for p in range(0, len(i.ports)):
                if i.ports[p] == command[2] and not i.connected[p]:
                    a = i
                    i.connected[p] = 1
                    port1 = p
                elif i.ports[p] == command[3] and not i.connected[p]:
                    b = i
                    i.connected[p] = 1
                    port2 = p
        if a and b:
            self.network.add_edge(
                a, b, (b.ports[port2], a.ports[port1]), (a.ports[port1], b.ports[port2]))
            DFS(self)
            for sn in self.subnetworks:
                sn.update()

    def disconnect(self, command):
        a = None
        for i in self.network.get_vertex():
            for p in range(0, len(i.ports)):
                if i.ports[p] == command[2] and i.connected[p]:
                    a = i
                    i.connected[p] = 0
                    break
        for b in self.network.vertex_list[a].connected_to:
            if b[1] == command[2]:
                self.network.vertex_list[a].connected_to[b].id.connected[int(
                    b[0][len(b[0])-1])-1] = 0
                self.network.del_edge(
                    a, self.network.vertex_list[a].connected_to[b].id, b, (command[2], b[0]))
                break
        DFS(self)
        for sn in self.subnetworks:
            sn.update()

    def send(self, command):
        for i in self.network.get_vertex():
            if i.name == command[2]:
                pc_current = i
        pc_current.process.append(command[3])
        pc_current.ready = 1
        return pc_current

    def send_frame(self,command):
        for i in self.network.get_vertex():
            if i.name == command[2]:
                pc_current = i
        pc_current.process.append(command[3])
        pc_current.ready = 1
        return pc_current
    
    def mac(self, command):
        for pc in self.network.get_vertex():
            if type(pc) is cm.Computer:
                if pc.name == command[2]:
                    pc.mac_address = command[3]
    
    def parser(self, file):
        commands = []
        while True:
            line = file.readline()
            if not line:
                break
            commands.append(line.split())
        return commands

    def run(self, script='script.txt'):
        self.remove_txt()
        file = open(script, "r")
        commands = self.parser(file)
        file.close()
        file = open("config.txt", "r")
        self.signal_time = int(file.readline().split()[1])
        file.close()
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
                        elif commands[current][2] == "switch":
                            self.create_switch(commands[current])
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
                    elif commands[current][1] == "send_frame":
                        self.send_frame(commands[current])
                        commands.pop(current)
                    elif commands[current][1] == "mac":
                        self.mac(commands[current])
                        commands.pop(current)
                    else:
                        self.disconnect(commands[current])
                        commands.pop(current)
            for pc_hub in self.network.get_vertex():
                if len(commands) == 0:
                    if type(pc_hub) is cm.Computer:
                        if len(pc_hub.process) >= 1:
                            keep = 1

                if self.globaltime % self.signal_time == 0:
                    pc_hub.print_status(self.globaltime)
                pc_hub.update(self.signal_time)
            for sn in self.subnetworks:
                sn.update()
            self.globaltime += 1

        for i in self.network.get_vertex():
            i.my_file.close()
            if type(i) is cm.Computer:
                i.my_frame_file.close()

    def remove_txt(self):
        try:
            os.chdir(os.path.join('.', 'output'))
            for filename in os.listdir():
                if filename.endswith('.txt'):
                    os.unlink(filename)
            os.chdir('..')
            # print(os.getcwd())
        except:
            print('An exception occurred')


def DFS(system):
    system.subnetworks = []
    cc = 0
    for vertex in system.network.get_vertex():
        if not system.network.vertex_list[vertex].visited:
            system.subnetworks.append(cm.SubNetwork(
                DFS_VISIT(system.network, vertex, []), cc))
            vertex.subnetwork = system.subnetworks[cc]
            cc += 1
    for vertex in system.network.vertex_list:
        system.network.vertex_list[vertex].visited = 0
    return system.subnetworks


def DFS_VISIT(graph, source, path=[]):
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

def hexa_bin(number,h_b):
    if h_b == "b":
        hexa_dec = hex(int(number, 2))[2:]
        return str(hexa_dec)
    elif h_b == "h":
        binary = bin(int(number, 16))[2:]
        return str(binary)

if __name__ == "__main__":
    S = System()
    if len(sys.argv) > 1:
        S.run(sys.argv[1])
    else:
        S.run()
