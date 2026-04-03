import socket
import threading
import paramiko
from core.logger import Logger

HOST_KEY = paramiko.RSAKey.generate(2048)

class HoneypotServer(paramiko.ServerInterface):
    def __init__(self):
        self.username = None
        self.password = None

    def check_auth_password(self, username, password):
        self.username = username
        self.password = password
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED


class SSHServer:
    def __init__(self, db):
        self.logger = Logger(db)

    def emulate_command(self, cmd):
        if cmd == "whoami":
            return "root\n"
        elif cmd == "uname -a":
            return "Linux aegis 5.15.0 x86_64\n"
        elif cmd.startswith("ls"):
            return "bin etc home var\n"
        else:
            return "command not found\n"

    def handle(self, client, addr):
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)

        server = HoneypotServer()
        transport.start_server(server=server)

        chan = transport.accept(10)
        if chan is None:
            return

        chan.send("Ubuntu 22.04 LTS\n$ ")

        while True:
            try:
                cmd = chan.recv(1024).decode().strip()
                self.logger.log(addr[0], server.username, server.password, cmd)

                if cmd == "exit":
                    break

                response = self.emulate_command(cmd)
                chan.send(response + "$ ")

            except:
                break

        chan.close()

    def start(self):
        sock = socket.socket()
        sock.bind(("0.0.0.0", 2222))
        sock.listen(100)

        print("AegisTrap listening on 2222")

        while True:
            client, addr = sock.accept()
            threading.Thread(target=self.handle, args=(client, addr)).start()
