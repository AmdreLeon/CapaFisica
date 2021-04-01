class Computer():
    def __init__(self, name, time, my_subnetwork):
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
        self.my_file = open("./output/"+name+".txt", "w")

    def update(self, sgntime):
        if self.status == "sending" and self.my_subnetwork.pc is self:
            a = int((self.process_pointer-1) / sgntime)
            self.my_subnetwork.status = self.process[0][a]
            if (self.process_pointer / sgntime) == len(self.process[0]):
                self.process.pop(0)
                self.process_pointer = 0
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

    def print_status(self, globaltime):
        self.my_file.write(str(globaltime) + " " + str(
            self.ports[0]) + " " + self.status + " " + self.my_subnetwork.status+'\n')


class Cable():
    def __init__(self, port1, port2):
        self.port1 = port1
        self.port2 = port2
        self.status = "null"


class Hub():
    def __init__(self, name, c_ports, my_subnetwork):
        self.name = name
        self.c_ports = c_ports
        self.computers_list = []
        self.ports = [name + "_" + str(i) for i in range(1, c_ports + 1)]
        self.connected = [0 for i in range(0, c_ports)]
        self.status = "receiving"
        self.my_subnetwork = my_subnetwork
        self.my_file = open("./output/"+name+".txt", "w")

    def print_status(self, globaltime):
        for port in range(0, self.c_ports):
            if self.connected[port]:
                self.my_file.write(str(globaltime) + " " + str(
                    self.ports[port]) + " " + self.status + " " + self.my_subnetwork.status+'\n')

    def update(self, sgntime):
        return


class SubNetwork():
    def __init__(self, devices_list, cc):
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
    def __init__(self, clave):
        self.id = clave
        self.connected_to = {}
        self.visited = 0

    def add_neighbour(self, vecino, port):
        self.connected_to[port] = vecino

    def delete_neighbour(self, port):
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

    def add_vertex(self, clave):
        self.num_vertex = self.num_vertex + 1
        new_vertex = Device(clave)
        self.vertex_list[clave] = new_vertex
        return new_vertex

    # def obtenerVertice(self,n):
    #     if n in self.vertex_list:
    #         return self.vertex_list[n]
    #     else:
    #         return None

    def __contains__(self, n):
        return n in self.vertex_list

    def add_edge(self, from_, to, port1, port2):
        """
        if from_ not in self.vertex_list:
            nv = self.add_vertex(from)
        if to not in self.vertex_list:
            nv = self.add_vertex(to)
        """
        self.vertex_list[from_].add_neighbour(self.vertex_list[to], port1)
        self.vertex_list[to].add_neighbour(self.vertex_list[from_], port2)

    def del_edge(self, from_, to, port1, port2):
        self.vertex_list[from_].delete_neighbour(port1)
        self.vertex_list[to].delete_neighbour(port2)

    def get_vertex(self):
        return self.vertex_list.keys()

    def __iter__(self):
        return iter(self.vertex_list.values())
