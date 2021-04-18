import components as cm

def dfs(source, sgtime, gltime):
    a = dfs_visit(source,[],0)
    if not a[1]:
        for elmnt in a[0]:
            if a[0].index(elmnt) == 0:
                elmnt.id.update_sending(sgtime)
                continue
            if type(elmnt.id) is cm.SwitchPort:
                elmnt.id.update(elmnt.id,sgtime,source.id.sending)
            else:
                elmnt.id.update(gltime,sgtime,source.id.sending)
    for elmnt in a[0]:
        if type(elmnt.id) is cm.Switch:
            elmnt.id.active_ports = []
    return a[1]

def dfs_visit(source, path,collision):
    if collision == 1:
        return
    path.append(source) 
    for d in source.connected_to:
        device = source.connected_to[d]
        if device in path:
            return
        if type(device.id) is cm.Switch:
            for p in device.id.ports_:
                if p in path:
                    break
                if p.id.port == d[0]:
                    device.id.active_ports.append(p)
                    path.append(p)
        elif device.id.receiving == 'null':
            dfs_visit(device,path,0)
        else:
            collision=1
            break
    return path,collision

def hexa_bin(number,h_b):
    if h_b == "h":
        hexa_dec = hex(int(number, 2))[2:]
        return str(hexa_dec)
    elif h_b == "b":
        binary = bin(int(number, 16))[2:]
        if len(binary) % 4 != 0:
            binary = '0'*(4-(len(binary) % 4)) + binary
        return str(binary)
    
def complete(binary, l):
    if len(binary) != l:
        binary = '0'* (l - len(binary))+ binary
    return binary
    