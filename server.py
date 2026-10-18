import socket
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()
s = Session()

class Player(Base):
    __tablename__ = 'gamers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    address = Column(String)
    x = Column(Integer, default=500)
    y = Column(Integer, default=500)
    size = Column(Integer, default=50)
    errors = Column(Integer, default=0)
    abs_speed = Column(Integer, default=1)
    speed_x = Column(Integer, default=0)
    speed_y = Column(Integer, default=0)

    def __init__(self, name, address):
        self.name = name
        self.address = address
Base.metadata.create_all(engine)

class localplayer(Base):
    def __init__(self, id, name, sock, addr):
        self.id = id
        self.db: Player = s.get(Player, self.id)
        self.sock = sock
        self.name = name
        self.address = addr
        self.x = 500
        self.y = 500
        self.size = 50
        self.errors = 0
        self.abs_speed = 1
        self.speed_x = 0
        self.speed_y = 0

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(("localhost", 10000))
main_socket.setblocking(False)
main_socket.listen(5)

players = {}
while True:
    try:
        new_socket, addr = main_socket.accept()
        print("подключился", addr)
        new_socket.setblocking(False)
        player = Player("Имя", addr)
        players.append(new_socket)
        s.merge(player)
        s.commit()


    except BlockingIOError:
        pass

    for sock in players:
        try:
            data = sock.recv(1024).decode()
            print("получил", data)
        except:
            pass

    for sock in players:
        try:
            sock.send("LOL".encode())
        except:
            players.remove(sock)
            sock.close()
            print("СОКЕТ ЗАКРЫТ")
    time.sleep(1)