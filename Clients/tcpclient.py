from gevent import monkey, socket

monkey.patch_all()
from gevent import spawn,sleep
import time


conn=None

def testServer(msg):
    conn.send(msg.encode())
    reply = conn.recv(1024)
    if reply:
        print("%s %s" %(time.ctime(),reply.decode()))


def main():
    global conn
    conn=socket.socket()
    conn.connect(("127.0.0.1",8088))
    
    spawn(testServer,"123")
    sleep(1)
    spawn(testServer,"456")
    sleep(1)
    lst= spawn(testServer,"789")
    lst.join()

if __name__ == "__main__":
    main()