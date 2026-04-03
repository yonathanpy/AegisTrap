from db.database import Database
from core.server import SSHServer

if __name__ == "__main__":
    db = Database()
    server = SSHServer(db)
    server.start()
