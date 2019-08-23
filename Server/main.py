from gevent import monkey, socket

monkey.patch_all()
from gevent import spawn,sleep
import time

sockets = []


def process_request(client, info):
    ip, port = info
    while True:
        data = client.recv(1024)
        if data:
            print("%s:%d %s - %s " % (ip, port, time.ctime(), data.decode()))
            if data.decode()=="456":
                sleep(5)
            client.send(data)
        else:
            client.close()
            sockets.remove(client)
            print("%s:%d was disconnected" % info)
            break


def main():
    tcp = socket.socket()
    tcp.bind(('', 8088))
    tcp.listen()
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockets.append(tcp)

    try:
        while True:
            client, addr = tcp.accept()
            sockets.append(client)
            print("%s:%d connected..." % addr)

            spawn(process_request, client, addr)
    except:
        pass
    finally:
        for sock in sockets:
            sock.close()
        sockets.clear()


if __name__ == '__main__':
    main()