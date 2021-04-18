import components as cm
from components import Hub, Network, Computer, Switch
from functions import dfs, hexa_bin, complete
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
        hub_ = cm.Hub(command[3], int(command[4]))
        self.hubs.append(self.network.add_vertex(hub_))
        return hub_

    def create_switch(self,command):
        switch_ = cm.Switch(command[3], int(command[4]),self.signal_time)
        self.switches.append(self.network.add_vertex(switch_))
        return switch_
    
    def create_host(self, command):
        computer_ = cm.Computer(command[3], self.signal_time)
        self.hosts.append(self.network.add_vertex(computer_))
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

    def send(self, command):
        for i in self.network.get_vertex():
            if i.name == command[2]:
                pc_current = i
                break
        mac_dir = '1111111111111111'
        mac_ori = hexa_bin(pc_current.mac_address,'b')
        data = complete(command[3],(8 - len(command[3])%8)+len(command[3]))
        data_vol = complete(hexa_bin(str(int(len(data)/8)),'b'),8)
        error = '00000000'
        pc_current.process.append(mac_dir+mac_ori+data_vol+error+data)
        pc_current.ready = 1
        return pc_current

    def send_frame(self,command):
        for i in self.network.get_vertex():
            if i.name == command[2]:
                pc_current = i
        mac_dir = complete(hexa_bin(command[3],'b'),16)
        mac_ori = complete(hexa_bin(command[4][0:4],'b'), 16)
        data_vol = complete(hexa_bin(command[4][4:6],'b'),8)
        error = complete(hexa_bin(command[4][6:8],'b'),8)
        data = complete(hexa_bin(command[4][8:],'b'),int(data_vol,2)*8)
        pc_current.process.append(mac_dir+mac_ori+data_vol+error+data)
        pc_current.ready = 1
        return pc_current
    
    def mac(self, command):
        for pc in self.network.get_vertex():
            if type(pc) is cm.Computer:
                if pc.name == command[2]:
                    pc.mac_address = (command[3]).lower()
    
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
            
            for pc in [i for i in self.hosts]:
                if len(commands) == 0:
                    if len(pc.id.process) > 0:
                        keep = 1

                if pc.id.ready and not dfs(pc, self.signal_time, self.globaltime):
                    temp = self.hosts.index(pc)
                    self.hosts.pop(temp)
                    self.hosts.insert(0,pc)

            for sw in self.switches:
                if len(commands) == 0:
                    for port in sw.id.ports_:
                        if port.id.ready:
                            keep = 1
                
                sw.id.update_sending()            
                for port in sw.id.ports_: 
                    if port.id.ready:
                        dfs(port, self.signal_time, self.globaltime) 
                
            if self.globaltime % self.signal_time == 0:
                for components in self.network.get_vertex():
                    if not type(components) is Switch:
                        components.print_status(self.globaltime)

            for item in self.network.get_vertex():
                if type(item) is Computer or type(item) is Hub:
                    item.sending = 'null'
                    item.receiving = 'null'
                else:
                    for ports in item.ports_:
                        ports.send = 0
                    
            self.globaltime += 1

        for i in self.network.get_vertex():
            if type(i) is Switch:
                continue
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
        except:
            print('An exception occurred')
    
if __name__ == "__main__":
    S = System()
    if len(sys.argv) > 1:
        S.run(sys.argv[1])
    else:
        S.run()
