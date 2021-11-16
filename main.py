import wifi, time, ds18x20, onewire, socket, ntptime, config
from machine import Pin, I2C

IRQ = Pin(12, Pin.IN)

IIC = I2C(scl = Pin(5), sda = Pin(4), freq = 100000)
OW = onewire.OneWire(Pin(0))
DS = ds18x20.DS18X20(OW)

def debug(*data):
    if config.LOG: print(data)


def request_handler(query):

    ''' Function processing request and generate answer or execute commands'''

    if query == '/commands':
        vals = (b'ВЫКЛ.', b'ВКЛ.')
        ch_val = [b'', b'', b'', b'', b'', b'', b'', b'']
        debug('Requested list of commands.')
        response = openfile('commands.json', 'rb')
        state = int.from_bytes(IIC.readfrom(33, 1), 'big')
        for i in range(0, len(ch_val)):
            val = state >> i & 1
            ch_val[i] = vals[val]
        response = response % tuple(ch_val)
        return response

    ch_list = ('/0', '/1', '/2', '/3', '/4', '/5', '/6', '/7')
    if query in ch_list:
        response = openfile('complete.json', 'rb')
        mask = 1 << ch_list.index(query)
        switch(mask)
        debug("INFO: Execute succesfull.")
        response = response % query.encode()
        return response
    
    debug('ERROR: Execution error.')
    response = openfile('error.json', 'rb')
    response = response % query.encode()
    return response
    
    
def openfile(filename, mode):
    if filename:
        f = open(filename, mode)
        data = f.read()
        f.close()
        return data
    else: debug('ERROR: File doesn\'t exist.')

def writefile(filename, data):
    f = open(filename, 'w')
    f.write(data)
    f.close()
    
def irq_handler(p):
    mask = 255 - int.from_bytes(IIC.readfrom(32, 1), 'big')
    switch(mask)
    
def switch(mask):
    val = int.from_bytes(IIC.readfrom(33, 1), 'big')
    val = bytes([val ^ mask])
    IIC.writeto(33, val)
        
def http_server():
    HEADER = b'HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n'
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    resp = openfile('commands.json', 'rb')
    while True:
        if not wifi.status(): wifi.start()
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        client_stream = client_sock.makefile("rwb")
        req = client_stream.readline()
        req = str(req).split(' ')[1]
        debug("Client address:", client_addr)
        debug("Client socket:", client_sock)
        debug("Request:")
        debug(req)

        client_stream.write(HEADER)
        while True:
            header = client_stream.readline()
            if header == b"" or header == b"\r\n":
                break
            debug(header)
            

        resp = request_handler(req)
        client_stream.write(resp)
        client_stream.close()




















































































































def main():
    IIC.writeto(33, b'\x00')
    IRQ.irq(trigger = Pin.IRQ_FALLING, handler = irq_handler)
    wifi.start()
    http_server()


main()
