import socket
import pygame
import math

radius = 50
width = 800
height = 600

CC = (width // 2, height // 2)
old = (0, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("бактерии")



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(("localhost", 10000))
pygame.init()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            vector = pos[0] - CC[0], pos[1] - CC[1]
            lenv = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
            vector = vector[0] / lenv, vector[1] / lenv
            if lenv <= radius:
                vector = 0, 0
            if vector != old:
                old = vector
                msg = f"<{vector[0]},{vector[1]}>"
                sock.send(msg.encode())
    data = sock.recv(1024).decode()
    print("получил", data)

    screen.fill(("gray"))
    pygame.draw.circle(screen, (255, 0, 0), CC, radius)
    pygame.display.update()
pygame.quit()