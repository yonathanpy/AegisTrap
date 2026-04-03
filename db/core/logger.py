import datetime

class Logger:
    def __init__(self, db):
        self.db = db

    def log(self, ip, username, password, command):
        ts = str(datetime.datetime.now())
        self.db.insert(ip, username, password, command, ts)
        print(f"[{ts}] {ip} {username}:{password} -> {command}")
