# -*- coding: utf-8 -*-
#File:server.py
#Desc:Unity3D work: FPS Game Server
#Author: ysshen

from collections import deque
import select
import socket
import sys
import signal
import logging
import time
import threading

from userdata import UserData
from handler import MessageHandler
from scence import ScenceManager

HOST = "127.0.0.1"
PORT = 50020
BUFSIZE = 1024

class SimpleHost(object):
    def __init__(self):
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, name, sa = res
            try:
                self.listen_socket = socket.socket(af, socktype, proto)
            except socket.error as msg:
                self.listen_socket = None
                #print msg
                continue
            try:
                self.listen_socket.bind(sa)
                self.listen_socket.listen(10)
            except socket.error as msg:
                self.listen_socket.close()
                self.listen_socket = None
                #print msg
                continue
            break
        if self.listen_socket is None:
            print 'Create server socket failed, please check your network configuration!'
            sys.exit(-1)
        try:
            self.messageHandler = MessageHandler()
        except:
            print 'Create game server failed!'
            sys.exit(-1)
        self.onConnection = [self.listen_socket]


    def start(self):
        print 'Game Host start...'
        outputs = []
        msg_queues = {}
        while self.onConnection:
            rpipes, wpipes, exceptions = select.select(self.onConnection, outputs, self.onConnection)
            for r in rpipes:
                if r is self.listen_socket:
                    conn_socket, cli_addr = r.accept()
                    print('New connection accepted:', cli_addr)
                    self.onConnection.append(conn_socket)
                    msg_queues[conn_socket] = deque()
                else:
                    try:
                        msg = r.recv(BUFSIZE)
                        #print msg
                    except Exception:
                        self.messageHandler.exceptionHandler()
                        self.onConnection.remove(r)
                    try:
                        if msg:
                            #print "do handler."
                            message =  self.messageHandler._handle(msg, r)
                            if message:
                                # append message terminator '#'
                                msg = str(len(message)) + '\t' + message + '#'
                                msg_queues[r].put(msg)
                                outputs.append(r)
                    except Exception:
                        pass

            for w in wpipes:
                try:
                    msg = msg_queues[w].get_nowait()
                    #print msg
                except Exception as e:
                    outputs.remove(w)
                else:
                    w.send(msg)

            for e in exceptions:
                self.onConnection.remove(e)
                if e in outputs:
                    outputs.remove(e)
                e.close()
                del msg_queues[e]

    def sync(self):
        for sock in self.onConnection:
            if sock == self.listen_socket:
                continue
            try:
                sock.send(self.messageHandler.scenceManager.getSyncInfo)
            except Exception:
                logging.info('sync msg to {} error.'.format(sock))


    def close(self):
        self.MessageHandler.exceptionHandler()
        self.listen_socket.close()
        sys.exit(-1)


def sync_function(host):
    while host.onConnection:
        time.sleep(0.02)
        host.sync()

def exit_program(signum, frame):
    mHost.close()
    sys.exit(1)

#startup server
mHost = SimpleHost()
mHost.start()

syncThread = threading.Thread(target=sync_function, args=(mHost,))

signal.signal(signal.SIGINT, exit_program)
signal.signal(signal.SIGTERM, exit_program)
