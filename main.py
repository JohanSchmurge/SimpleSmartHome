import wifi
import time
import ds18x20
import onewire
import socket
import ntptime
import config
from machine import Pin, I2C, Timer


IRQ = Pin(12, Pin.IN)
IIC = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
OW = onewire.OneWire(Pin(0))
DS = ds18x20.DS18X20(OW)
OUT = 0


def request_handler(query):

    ''' Function processing request and generate answer or execute commands'''

    if query == '/commands':
        vals = (b'ВЫКЛ.', b'ВКЛ.')
        ch_val = []
        response = openfile('commands.json', 'rb')
        state = int.from_bytes(IIC.readfrom(33, 1), 'big')
        ch_val = [vals[state >> i & 1] for i in range(8)]
        response = response % tuple(ch_val)
        return response

    ch_list = ('/0', '/1', '/2', '/3', '/4', '/5', '/6', '/7')
    if query in ch_list:
        response = openfile('complete.json', 'rb')
        mask = 1 << ch_list.index(query)
        switch(mask)
        response = response % query.encode()
        return response

    response = openfile('error.json', 'rb')
    response = response % query.encode()
    return response


def openfile(filename, mode):
        f = open(filename, mode)
        data = f.read()
        f.close()
        return data


def writefile(filename, data):
    f = open(filename, 'wb')
    f.write(data)
    f.close()


def irq_handler(p):
    mask = 255 - int.from_bytes(IIC.readfrom(32, 1), 'big')
    switch(mask)


def switch(mask):
    data = int.from_bytes(IIC.readfrom(33, 1), 'big')
    OUT = data ^ mask
    val = bytes([OUT])
    IIC.writeto(33, val)
    time.sleep_ms(10)
    IIC.writeto(33, val)


def http_server():
    print('Starting HTTP server.')
    HEADER = b'HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n'
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    resp = openfile('commands.json', 'rb')
    while True:
        res = s.accept()
        client_sock, client_addr = res
        client_stream = client_sock.makefile("rwb")
        req = client_stream.readline()
        req = str(req).split(' ')[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)
        print("Request:")
        print(req)
        while True:
            header = client_stream.readline()
            if header == b'' or header == b'\r\n':
                break
            print(header)
        resp = request_handler(req)
        client_stream.write(HEADER)
        client_stream.write(resp)
        client_stream.close()


def main():
    IIC.writeto(33, b'\x00')
    IRQ.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler)
    wifi.start()
    wifi_tmr = Timer(-1)
    wifi_tmr.init(period=10000, mode=Timer.PERIODIC, \
        callback=lambda t: wifi.status(t))
    print('Timer started.')
    http_server()


main()
