# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:23:32 2021

@author: bgool
"""

import GeneralUse as gen
import WarriorPlayerV2, AssassinPlayerV2, MagePlayerV2, EngineerPlayerV2
from math import sin, cos, pi, sqrt
import pygame


def draw_regular_polygon(surface, color, vertex_count, radius, position):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(surface, color, [
        (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
        for i in range(n)
    ])


bg_color = (0, 0, 0)
fg_color = (0, 255, 255)
white = (255,255,255)
black = (0,0,0)
w, h = 1280, 720
vertex_count = 6

pygame.init()
FONT = pygame.font.Font("freesansbold.ttf", 25)
root = pygame.display.set_mode((w, h))

class Game:
    turnCounter = 0
    directions = ['n','ne','se','s','sw','nw']
        
    gameboard = {(1,5):gen.Objective((1,5),'Player2'), (4,5):gen.Respawn((4,5),'Player2'), (7,5):gen.Respawn((7,5),'Player3'), (10,5):gen.Objective((10,5),'Player3'),
                (1,11):gen.Respawn((1,11),'Player3'), (4,11):gen.Objective((4,11),'None'), (7,11):gen.Respawn((7,11),'Player1'), (10,11):gen.Objective((10,11),'Player1'), (13,11):gen.Respawn((13,11),'Player4'), (15,10):gen.Objective((15,10),'Player4'),
                (7,17):gen.Respawn((7,17),'Player1'), (10,17):gen.Objective((10,17),'None'), (13,17):gen.Respawn((13,17),'Player1'), (15,17):gen.Objective((15,17),'None'),
                'EliminatedUnits':gen.EliminatedUnitManager()}
                     
        
    def __init__(self,players):
        self.players = players
        
    def gameLoop(self):
        button1 = pygame.Rect(1100, 200, 100, 100)
        for player in self.players:
            self.gameboard = player.respawnUnits(self.gameboard) 
                
        while True:
 
            root.fill(bg_color)
            pygame.draw.rect(root, white, button1)
            button_text = FONT.render('Round',True, black)
            button_rect = button_text.get_rect(center=(1140,250))
            root.blit(button_text,button_rect)
            # draw initial board
            for j in range(0,17):
                for i in range(1,16):
                    if j%2 == 1:
                        offset = sqrt(3)/2 *w/48
                    else:
                        offset = 0
                    draw_regular_polygon(root, fg_color, 6, 22, (40 + 40*j, 720 - 720 / 16*i - offset))
            for x in self.gameboard:
                if hasattr(self.gameboard[x],'boardImage'):
                    # convert location to boardgame location
                    errorFlag = self.gameboard[x].boardImage.update(x)
                    if errorFlag:
                        print(self.gameboard[x])
                        errorFlag = False
                    my_group = pygame.sprite.Group(self.gameboard[x].boardImage)
                    my_group.draw(root)
            pygame.display.flip()
          
            done = False
            
            while not done:
                # Update game board per player turn
                for player in self.players:
                    buttonpress = False
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                done = True
                            # This block is executed once for each MOUSEBUTTONDOWN event.
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                # 1 is the left mouse button, 2 is middle, 3 is right.
                                if event.button == 1:
                                    # `event.pos` is the mouse position.
                                    if button1.collidepoint(event.pos):       
                                        self.gameboard = player.respawnUnits(self.gameboard)
                                        self.currentPlayer = player
                                        self.gameboard, self.players = player.turn(self.gameboard,self.players)
                                        buttonpress = True
                        if buttonpress:
                            break
                        
                    root.fill(bg_color)
                    # draw_regular_polygon(root, fg_color, vertex_count,
                    #                      min(w, h) / 6, (w / 2, h / 2))
                        
                    for j in range(0,17):
                        for i in range(1,16):
                            if j%2 == 1:
                                offset = sqrt(3)/2 *w/48
                            else:
                                offset = 0
                            draw_regular_polygon(root, fg_color, 6, 22, (40 + 40*j, 720 - 720 / 16*i - offset))
                            # if j == 4 and i == 5:
                    # units = 0
                    for x in self.gameboard:
                        # units = units + 1
                        if hasattr(self.gameboard[x],'boardImage'):
                            # convert location to boardgame location
                            errorFlag = self.gameboard[x].boardImage.update(x)
                            if errorFlag:
                                print(self.gameboard[x])
                                errorFlag = False
                            my_group = pygame.sprite.Group(self.gameboard[x].boardImage)
                            my_group.draw(root)
                    playerNameClass = FONT.render(player.playerClass + ' ' + player.playerID, True, white)
                    playerNameRect = playerNameClass.get_rect(center=(900, 40))
                    root.blit(playerNameClass,playerNameRect)
                    for x in player.actionLog:
                        text_surf = FONT.render(str(player.actionLog[x]), True, white)
                        # You can pass the center directly to the `get_rect` method.
                        text_rect = text_surf.get_rect(center=(900, 30*x + 80))
                        root.blit(text_surf, text_rect)
                    pygame.draw.rect(root, white, button1)
                    button_text = FONT.render('Round',True, black)
                    button_rect = button_text.get_rect(center=(1140,250))
                    root.blit(button_text,button_rect)
                    
                    # TO DO: validate leveling up is working as intended
                    # Validate adding abilities
                    # Troubleshoot normal vs unhindered movement
                    
                    pygame.display.flip()
                    # if buttonpress:
                    #     break
                                
                self.turnCounter = self.turnCounter + 1
                self.endRound()
            

            # display.flip() will update the contents of the entire display
            # display.update() allows to update a portion of the screen, instead of the entire area of the screen. Passing no arguments, updates the entire display
            
            
            # Flip will always update the entire screen. 
            # Update also update the entire screen, if you don't give argument. 
            # But if you give surface(s) as arguments, it will update only these surfaces. 
            # So it can be faster, depending on how many surfaces you give it and their width and height.

            if self.turnCounter == 10:
                print('end')
                pygame.quit()
                # break
                
    def endRound(self):
        for player in self.players:
            self.gameboard = player.manageExp(self.gameboard)
            player.gainVictoryPoints(len([x for x in self.gameboard if self.gameboard[x].name == 'Objective' and self.gameboard[x].playerID == player.playerID]))




# instantiate game
game = Game([WarriorPlayerV2.WarriorPlayer('Warrior','Player1'),AssassinPlayerV2.AssassinPlayer('Assassin','Player2'), \
      MagePlayerV2.MagePlayer('Mage','Player3'),EngineerPlayerV2.EngineerPlayer('Engineer','Player4')])
game.gameLoop()

# Gameflow: Players take a turn(), which initiates all options for unit selection (including Pass), 
# then all options for unitOptions(). Select a random option in unit selection, then random option for
# the unit. For each ability, need to return a random target