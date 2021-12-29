from machine import Pin, I2C, Timer
import time
import socket
import config
import temperature
import wifi


IRQ = Pin(12, Pin.IN)
IIC = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

TEMPERATURE = 0

def request_handler(query):
    if query == '/commands':
        vals = (b'ВЫКЛ.', b'ВКЛ.')
        ch_val = []
        response = readfile('content/commands.json', 'rb')
        state = int.from_bytes(IIC.readfrom(33, 1), 'big')
        ch_val = [vals[state >> i & 1] for i in range(8)]
        response = response % tuple(ch_val)
        return response

    ch_list = ('/0', '/1', '/2', '/3', '/4', '/5', '/6', '/7')
    if query in ch_list:
        response = readfile('content/complete.json', 'rb')
        mask = 1 << ch_list.index(query)
        switch(mask)
        return response

    if query == '/temperature':
        response = b'"indoor": {"title": "Дома:  %s°C", "summary": ""}' % TEMPERATURE
        return response

    response = readfile('error.json', 'rb')
    return response


def readfile(filename, mode):
    f = open(filename, mode)
    data = f.read()
    f.close()
    return data


def writefile(filename, mode, data):
    f = open(filename, mode)
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
    while True:
        res = s.accept()
        client_sock, client_addr = res
        client_stream = client_sock.makefile("rwb")
        req = client_stream.readline()
        req = str(req).split(' ')[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)
        print("Request: " + req)
        while True:
            header = client_stream.readline()
            if header == b'' or header == b'\r\n':
                break
            # print(header)
        resp = request_handler(req)
        client_stream.write(HEADER)
        client_stream.write(resp)
        client_stream.close()


def main():
    global TEMPERATURE
    IIC.writeto(33, b'\x00')
    IRQ.irq(trigger=Pin.IRQ_FALLING, handler=irq_handler)

    wifi.start()
    wifi_tmr = Timer(-1)
    wifi_tmr.init(period=30000, mode=Timer.PERIODIC, callback=lambda w: wifi.status(w))
    print('Timer started.')

    TEMPERATURE = temperature.get_temp()
    temp_tmr = Timer(-1)
    temp_tmr.init(period=600000, mode=Timer.PERIODIC, callback=lambda t: wifi.status(t))

    http_server()


main()
