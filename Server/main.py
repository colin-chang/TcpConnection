from gevent import monkey, socket
from gevent import spawn, sleep
import time

monkey.patch_all()
sockets = []


def process_request(client, addr):
    while True:
        data = client.recv(1024)
        if data:
            print("[%s:%d] [recv] %s - %s " % (addr[0], addr[1], time.ctime()[-13:-5], data.decode()))
            if data.decode() == "A456":
                sleep(3)  # 模拟耗时任务
            client.send(data)
        else:
            client.close()
            sockets.remove(client)
            print("%s:%d was disconnected" % addr)
            break


def main():
    tcp = socket.socket()
    tcp.bind(('', 8086))
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
