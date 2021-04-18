import functions as fn

class Computer():
    def __init__(self, name, time):
        self.name = name
        self.mac_address = None
        self.sending = "null"
        self.receiving = "null"
        self.time = time
        self.ports = [name + "_1"]
        self.process = []
        self.process_pointer = 0
        self.frame_pointer = time
        self.current = ''
        self.connected = [0]
        self.data_receiving = ''
        self.frame_receiving = 0
        self.ready = 0
        self.t_sends = 0
        self.frames = {}
        self.my_file = open("./output/"+name+".txt", "w")
        self.my_frame_file = open("./output/"+name+"_data.txt", "w")

    def update(self, global_time, sgtime, value):
        self.receiving = value
        if self.frame_pointer == 1:
            self.data_receiving += value
            self.frame_pointer = sgtime
            hexa = fn.hexa_bin(self.data_receiving, "h")
            
            if (len(self.data_receiving) == 16) and self.frame_receiving == 0:
                if hexa == self.mac_address or hexa == 'ffff':
                    self.frame_receiving = 1
                    self.data_receiving = ''
            elif self.frame_receiving:
                if len(self.data_receiving) >= 16:
                    if(len(self.data_receiving)==16):
                        self.frames[hexa] = ["",0]
                        self.current = hexa
                    self.frames[self.current][0] = self.data_receiving
                    self.frames[self.current][1] = global_time
                    len_frame_current = len(self.frames[self.current][0])
                    if len_frame_current > 32:
                        l = self.frames[self.current][0][16:24]
                        len_frame = int(l, 2)*8
                        len_data = len(self.frames[self.current][0][32:])
                        if (len_frame == len_data):
                            self.frame_receiving = 0
                            self.data_receiving = ''
                            self.print_data(self.current)
                            del self.frames[self.current]
        else:
            self.frame_pointer -= 1
        
    def print_data(self,source):
        self.my_frame_file.write(str(self.frames[source][1]) + " " + str(source) + " " + fn.hexa_bin(self.frames[source][0],'h') + '\n')
        
    def update_sending(self, sgntime):
        a = int((self.process_pointer-1) / sgntime)
        self.sending = self.process[0][a]
        if (self.process_pointer / sgntime) == len(self.process[0]):
            self.process.pop(0)
            self.process_pointer = 0
        else:
            self.process_pointer += 1

        if len(self.process) == 0:
            self.ready = 0
        else:
            self.ready = 1
        return

    def print_status(self, globaltime):
        self.my_file.write(str(globaltime) + " " + str(self.ports[0]) + " sending " + self.sending+ ' -- '  + "receiving " + self.receiving + '\n')

class Hub():
    def __init__(self, name, c_ports):
        self.name = name
        self.c_ports = c_ports
        self.computers_list = []
        self.ports = [name + "_" + str(i) for i in range(1, c_ports + 1)]
        self.connected = [0 for i in range(0, c_ports)]
        self.status = "receiving"
        self.receiving = "null"
        self.my_file = open("./output/"+name+".txt", "w")

    def print_status(self, globaltime):
        for port in range(0, self.c_ports):
            if self.connected[port]:
                self.my_file.write(str(globaltime) + " " + str(self.ports[port]) + " " + self.status + " " + self.receiving + '\n')

    def update(self, globalti, sgntime, value):
        self.receiving = str(value)
    
class Switch():
    def __init__(self, name, c_ports,sgtime):
        self.name = name
        self.c_ports = c_ports
        self.ports = [name + "_" + str(i) for i in range(1, c_ports + 1)]
        self.ports_ = [Device(SwitchPort(self,name,sgtime)) for name in self.ports]
        self.connected = [0 for i in range(0, c_ports)]
        self.receiving = 'null'
        self.active_ports = []
        self.process = []
        
    def update_sending(self):
        for pro in range(len(self.process)):
            if self.process[pro] != 0: 
                mac = self.process[pro][0][:16]
                for port in self.ports_:
                    if self.process[pro][1] != port.id.port:
                        if mac == '1111111111111111' or mac in port.id.mac_table:
                            port.id.process.append(self.process[pro][0])
                            port.id.ready = 1
                self.process[pro] = 0
                        
class SwitchPort():
    def __init__(self,switch, port, time):
        self.port = port
        self.mac_table = []
        self.sending = 'null'
        self.send = 0
        self.process = []
        self.process_pointer = 0
        self.current = ''
        self.connected = 0
        self.data_receiving = ''
        self.frame_receiving = 0
        self.ready = 0
        self.my_switch = switch
        self.frame_pointer = time

    def update(self, switch, sgtime, value):
        self.receiving = value
        if self.frame_pointer == 1:
            self.data_receiving += value
            self.frame_pointer = sgtime
            if len(self.data_receiving) >= 48:
                l = self.data_receiving[32:40]
                len_frame = int(l, 2)*8
                len_data = len(self.data_receiving[48:])
                if (len_frame == len_data):
                    mac = self.data_receiving[16:32]
                    if not (mac in self.mac_table):
                        self.mac_table.append(mac)
                    self.my_switch.process.append([self.data_receiving , self.port])
                    self.data_receiving = ''
                    self.frame_receiving = 0
                elif len(self.data_receiving) > 2088:
                    self.data_receiving = ''
                    self.frame_receiving = 0
        else:
            self.frame_pointer -= 1
            
    def update_sending(self, sgntime):
        self.send = 1
        a = int((self.process_pointer-1) / sgntime)
        self.sending = self.process[0][a]
        if (self.process_pointer / sgntime) == len(self.process[0]):
            self.process.pop(0)
            self.process_pointer = 0
        else:
            self.process_pointer += 1
        if len(self.process) == 0:
            self.ready = 0
        else:
            self.ready = 1
        return
            
class Device():
    def __init__(self, clave):
        self.id = clave
        self.connected_to = {}
        self.visited = 0

    def add_neighbour(self, vecino, port):
        self.connected_to[port] = vecino
        if type(self.id) is Switch:
            for p in self.id.ports_:
                if p.id.port == port[1]:
                    p.connected_to[port]=vecino

    def delete_neighbour(self, port):
        del self.connected_to[port]
        if type(self.id) is Switch:
            for p in self.id.ports_:
                if p.id.port == port[1]:
                    del p.connected_to[port]

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

    def add_vertex(self, clave):
        self.num_vertex = self.num_vertex + 1
        new_vertex = Device(clave)
        self.vertex_list[clave] = new_vertex
        return new_vertex

    def __contains__(self, n):
        return n in self.vertex_list

    def add_edge(self, from_, to, port1, port2):
        self.vertex_list[from_].add_neighbour(self.vertex_list[to], port1)
        self.vertex_list[to].add_neighbour(self.vertex_list[from_], port2)

    def del_edge(self, from_, to, port1, port2):
        self.vertex_list[from_].delete_neighbour(port1)
        self.vertex_list[to].delete_neighbour(port2)

    def get_vertex(self):
        return self.vertex_list.keys()

    def __iter__(self):
        return iter(self.vertex_list.values())
