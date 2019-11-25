import pygame
from network import Network
import pickle
pygame.font.init()

width = 800
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client") # Caption name

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("arial", 40) #Questionable...
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((72, 54, 191))#Window color
    
    if not(game.connected()):
        font = pygame.font.SysFont("arial", 60)#Questionable...
        text = font.render("Waiting...", 1, (255,0,0), True) 
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("arial", 45)
        text = font.render("Your move", 1, (255,255,255))#Player one text
        win.blit(text, (80, 200))
        text = font.render("Your opponent", 1, (219, 18, 51))#Player two text
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (10,10,1))
            text2 = font.render(move2, 1, (10,10,1))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (10,10,1))
            elif game.p1Went:
                text1 = font.render("Move Locked", 1, (10,10,1))
            else:
                text1 = font.render("Waiting..", 1, (10,10,1))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (10,10,1))
            elif game.p2Went:
                text2 = font.render("Move Locked", 1, (10,10,1))
            else:
                text2 = font.render("Waiting..", 1, (10,10,1))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns: #Drawing the buttons
            btn.draw(win)

    pygame.display.update()


#                     position   color                        position    color                      position    color
btns = [Button("Rock", 100, 500, (112, 91, 107)), Button("Scissors", 300, 500, (107, 33, 37)), Button("Paper", 500, 500, (223, 240, 235))]
# btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("Player: " + str(player))

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Can't get game") #In case the other player disconnected
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(600)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Can't get game")# In case a player dissconnects after finishing a game
                break

            font = pygame.font.SysFont("arial", 75)#Questionable...
            if(game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!!", 1, (44,200,69))
            elif game.winner() == -1:
                text = font.render("Tied!", 1 , (44,200,69))
            else:
                text = font.render("You lost...", 1, (44,200,69))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2 ))
            pygame.display.update()
            pygame.time.delay(2000)#Two seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)#rock or paper or scissors
                        else:
                            if not game.p2Went:
                                n.send(btn.text)#rock or paper or scissors

        redrawWindow(win,game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((72, 54, 191))
        font = pygame.font.SysFont("arial", 60)
        text = font.render("Play!", 1, (124, 184, 22))
        win.blit(text, (350,350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()