import os, sys
import pygame
import serial
import threading
import pygame.transform
from game.registry import adjpos, adjrect, adjwidth, adjheight
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import time 
# Game parameters
SCREEN_WIDTH, SCREEN_HEIGHT = adjpos (800, 500)
TITLE = "Symons Media (Traveser touch): Duck Hunt"
FRAMES_PER_SEC = 50
BG_COLOR = 255, 255, 255

# Initialize pygame before importing modules

from test_serial import SERIAL_EVENT
ser=serial.Serial("COM8",9600)

def read_cord():
    speed = 150
    x, y = 0, 0
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            
            try:
                xAcc, yAcc,gun= map(float, data.split(','))  # Keep as float for calculations

                # Update rectangle position using only integers
                x += round(xAcc * speed)  # Convert result to integer after multiplication
                y += round(yAcc * speed)
                gun=round(gun)
                
                x = max(0, min(SCREEN_WIDTH - 50, x))
                y = max(0, min(SCREEN_HEIGHT - 50, y))
                
                # Ensure message contains only integers
                data = f"{x},{y},{gun}"
                
                event = pygame.event.Event(SERIAL_EVENT, message=data)
                pygame.event.post(event)

            except ValueError:
                print("Invalid data received:", data)  # Handle errors gracefully
            
            time.sleep(0.01)  # Small delay to prevent spamming

st=threading.Thread(target=read_cord,daemon=True)
st.start()
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)

import game.driver

class Game(object):
    def __init__(self):
        self.running = True
        self.surface = None
        self.clock = pygame.time.Clock()
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
        background = os.path.join('media', 'background.jpg')
        bg = pygame.image.load(background)
        self.background = pygame.transform.smoothscale (bg, self.size)
        self.driver = None

    def init(self):
        self.surface = pygame.display.set_mode(self.size)   
        self.driver = game.driver.Driver(self.surface)

    def handleEvent(self, event):
       
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key is 27):
            self.running = False
        else:
            self.driver.handleEvent(event)

    def loop(self):
        self.clock.tick(FRAMES_PER_SEC)
        self.driver.update()

    def render(self):
        self.surface.blit(self.background, (0,0))
        self.driver.render()
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()
        sys.exit(0)

    def execute(self):
        self.init()

        while (self.running):
            for event in pygame.event.get():
                self.handleEvent(event)
            self.loop()
            self.render()

        self.cleanup()

if __name__ == "__main__":
    theGame = Game()
    theGame.execute()
