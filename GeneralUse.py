
#need to choose from options, picking an option calls use ability
#if called from turn, call 'turn' costs
#if called from reaction, call 'reaction' costs

# create players
# turns
# end turn
# end round
import random
import math
import lineOfSight as LOS
import pygame


indices = [(0,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2),(3,2),(4,2),
(0,3),(1,3),(2,2),(3,3),(4,3),(5,3),(6,3),
(0,4),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),
(0,5),(1,5),(2,5),(3,5),(4,5),(5,5),(5,6),(7,5),(8,5),(9,5),(10,5),
(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),(11,6),(12,6),
(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(10,7),(11,7),(12,7),(13,7),(14,7),
(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),(9,8),(10,8),(11,8),(12,8),(13,8),(14,8),(15,8),(16,8),
(0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(8,9),(9,9),(10,9),(11,9),(12,9),(13,9),(14,9),(15,9),(16,9),
(0,10),(1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10),(8,10),(9,10),(10,10),(11,10),(12,10),(13,10),(14,10),(15,10),(16,10),
(0,11),(1,11),(2,11),(3,11),(4,11),(5,11),(6,11),(7,11),(8,11),(9,11),(10,11),(11,11),(12,11),(13,11),(14,11),(15,11),(16,11),
(0,12),(1,12),(2,12),(3,12),(4,12),(5,12),(6,12),(7,12),(8,12),(9,12),(10,12),(11,12),(12,12),(13,12),(14,12),(15,12),(16,12),
(0,13),(1,13),(2,13),(3,13),(4,13),(5,13),(6,13),(7,13),(8,13),(9,13),(10,13),(11,13),(12,13),(13,13),(14,13),(15,13),(16,13),
(0,14),(1,14),(2,14),(3,14),(4,14),(5,14),(6,14),(7,14),(8,14),(9,14),(10,14),(11,14),(12,14),(13,14),(14,14),(15,14),(16,14),
(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),
(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),(9,3),(10,3),(11,3),(12,3),(13,3),(14,3),(15,3),(16,3),
(5,5),(6,5),(7,5),(8,5),(9,5),(10,5),(11,5),(12,5),(13,5),(14,5),(15,5),(16,5),
(7,7),(8,7),(9,7),(10,7),(11,7),(12,7),(13,7),(14,7),(15,7),(16,7),
(9,9),(10,9),(11,9),(12,9),(13,9),(14,9),(15,9),(16,9),
(11,11),(12,11),(13,11),(14,11),(15,11),(16,11),
(13,13),(14,13),(15,13),(16,13),
(15,15),(16,15)
]

boardLocations = [(0,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2),(3,2),(4,2),
(0,3),(1,3),(2,2),(3,3),(4,3),(5,3),(6,3),
(0,4),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),
(0,5),(1,5),(2,5),(3,5),(4,5),(5,5),(5,6),(7,5),(8,5),(9,5),(10,5),
(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),(11,6),(12,6),
(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(10,7),(11,7),(12,7),(13,7),(14,7),
(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),(9,8),(10,8),(11,8),(12,8),(13,8),(14,8),(15,8),(16,8),
(0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(8,9),(9,9),(10,9),(11,9),(12,9),(13,9),(14,9),(15,9),(16,9),
(0,10),(1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10),(8,10),(9,10),(10,10),(11,10),(12,10),(13,10),(14,10),(15,10),(16,10),
(0,11),(1,11),(2,11),(3,11),(4,11),(5,11),(6,11),(7,11),(8,11),(9,11),(10,11),(11,11),(12,11),(13,11),(14,11),(15,11),(16,11),
(0,12),(1,12),(2,12),(3,12),(4,12),(5,12),(6,12),(7,12),(8,12),(9,12),(10,12),(11,12),(12,12),(13,12),(14,12),(15,12),(16,12),
(0,13),(1,13),(2,13),(3,13),(4,13),(5,13),(6,13),(7,13),(8,13),(9,13),(10,13),(11,13),(12,13),(13,13),(14,13),(15,13),(16,13),
(0,14),(1,14),(2,14),(3,14),(4,14),(5,14),(6,14),(7,14),(8,14),(9,14),(10,14),(11,14),(12,14),(13,14),(14,14),(15,14),(16,14),
(1,15),(2,15),(3,15),(4,15),(5,15),(6,15),(7,15),(8,15),(9,15),(10,15),(11,15),(12,15),(13,15),(14,15),(15,15),(16,15),
(3,17),(4,17),(5,17),(6,17),(7,17),(8,17),(9,17),(10,17),(11,17),(12,17),(13,17),(14,17),(15,17),(16,17),
(5,19),(6,19),(7,19),(8,19),(9,19),(10,19),(11,19),(12,19),(13,19),(14,19),(15,19),(16,19),
(7,21),(8,21),(9,21),(10,21),(11,21),(12,21),(13,21),(14,21),(15,21),(16,21),
(9,23),(10,23),(11,23),(12,23),(13,23),(14,23),(15,23),(16,23),
(11,25),(12,25),(13,25),(14,25),(15,25),(16,25),
(13,27),(14,27),(15,27),(16,27),
(15,29),(16,29)
]

index_to_pixel = {}
for x in range(0,len(indices)):
    if indices[x][0]%2 == 1:
    
        offset = math.sqrt(3)/2 *1280/48
    else:
        offset = 0
    index_to_pixel[boardLocations[x]] = (40 + 40*indices[x][0], 720 - 720 / 16*indices[x][1] - offset)


class MySprite(pygame.sprite.Sprite):
    def __init__(self,playerClass,unitType):  
        super(MySprite, self).__init__()
        self.playerClass = playerClass
        self.unitType = unitType
        self.loadImage(playerClass)
        self.rect = pygame.Rect(0, 0, 85, 85)
        
    def loadImage(self,playerClass):
        self.images = []
        self.images.append(pygame.image.load('warrior.PNG')),
        self.images.append(pygame.image.load('assassin.PNG')),
        self.images.append(pygame.image.load('mage.PNG')),
        self.images.append(pygame.image.load('engineer.PNG')),
        self.images.append(pygame.image.load('obstacle_sprite.PNG')),
        self.images.append(pygame.image.load('obstacle_sprite.PNG')),
        self.images.append(pygame.image.load('obstacle_sprite.PNG')),
        self.images.append(pygame.image.load('stealth.PNG'))
        switch = {
            'Warrior': 0,
            'Assassin': 1,
            'Mage': 2,
            'Engineer': 3,
            'Obstacle': 4,
            'Objective': 5,
            'Respawn': 6,
            'StealthToken':7
            }
        self.image = self.images[switch[playerClass]]
        
    def update(self,pos):
        try:
            coordinates = index_to_pixel[pos]
            self.rect.x = coordinates[0]
            self.rect.y = coordinates[1]
            return False
        except:
            return True

        

class GeneralUse:
    name = 'General'
    unitType = 'NoType'
    playerID = 'NoPlayer'
    abilities = {}
    directions = ['n','ne','se','s','sw','nw']
    oppositeDirections = {'n':'s','ne':'sw','se':'nw','s':'n','sw':'ne','nw':'se'}
    boardLocations = boardLocations
    
    def allSpaces(self):
        return [(x,y) for x in range(0,10) for y in range(0,10)]
    
    def adjacentSpaces(self,loc):
        x = loc[0]
        y = loc[1]
        return [a for a in [(x,y+1),(x+1,y+1),(x+1,y),(x,y-1),(x-1,y-1),(x-1,y)] if a in boardLocations]
    
    def LOSDirections(self,direction):
        dirs = {
            'n': ['nw','n','ne'],
            'ne': ['n','ne','se'],
            'se': ['ne','se','s'],
            's': ['se','s','sw'],
            'sw': ['s','sw','nw'],
            'nw': ['sw','nw','n']
        }
        return dirs[direction]
    
    def faceDirection(self,direction,num):
        switchDir = {
            'n': {1:'n', 2:'ne', 3:'se', 4:'s', 5:'sw', 6:'nw'},
            'ne': {1:'ne', 2:'se', 3:'s', 4:'sw', 5:'nw', 6:'n'},
            'se': {1:'se', 2:'s', 3:'sw', 4:'nw', 5:'n', 6:'ne'},
            's': {1:'s', 2:'sw', 3:'nw', 4:'n', 5:'ne', 6:'se'},
            'sw': {1:'sw', 2:'nw', 3:'n', 4:'ne', 5:'se', 6:'s'},
            'nw': {1:'nw', 2:'n', 3:'ne', 4:'se', 5:'s', 6:'sw'}
        } 
        return switchDir[direction][num]
    
    def attackDirection(self,unit,target):
        # returns the direction the attack is coming from
        
        xu = unit[0]
        yu = unit[1]
        xt = target[0]
        yt = target[1]
        
        if xu == xt and yu < yt:
            return 'n'
        elif xu < xt and yu < yt:
            return 'ne'
        elif xu < xt and yu == yt:
            return 'se'
        elif xu == xt and yu > yt:
            return 's'
        elif xu > xt and yu > yt:
            return 'sw'
        elif xu > xt and yu < yt:
            return 'nw'
        
    def directionAdjacentSpaces(self,direction,space):
        x = space[0]
        y = space[1]
        switch = {
            'n': {1:(x,y+1),2:(x+1,y+1),3:(x+1,y),4:(x,y-1),5:(x-1,y-1),6:(x-1,y)},
            'ne': {1:(x+1,y+1),2:(x+1,y),3:(x,y-1),4:(x-1,y-1),5:(x-1,y),6:(x,y+1)},
            'se': {1:(x-1,y-1),2:(x-1,y),3:(x,y+1),4:(x+1,y+1),5:(x+1,y),6:(x,y-1)},
            's': {1:(x,y-1),2:(x-1,y-1),3:(x-1,y),4:(x,y+1),5:(x+1,y+1),6:(x+1,y)},
            'sw': {1:(x+1,y),2:(x,y-1),3:(x-1,y-1),4:(x-1,y),5:(x,y+1),6:(x+1,y+1)},
            'nw': {1:(x-1,y),2:(x,y+1),3:(x+1,y+1),4:(x+1,y),5:(x,y-1),6:(x-1,y-1)}
        }
        return switch[direction]
    
    # need to review accuracy of spaces and directions
    def numberSpaceAdjacentSpaces(self,direction,space):
        x = space[0]
        y = space[1]
        switch = {
            'n': {(x,y+1):1,(x+1,y+1):2,(x+1,y):3,(x,y-1):4,(x-1,y-1):5,(x-1,y):6},
            'ne': {(x+1,y+1):1,(x+1,y):2,(x,y-1):3,(x-1,y-1):4,(x-1,y):5,(x,y+1):6},
            'se': {(x-1,y-1):1,(x-1,y):2,(x,y+1):3,(x+1,y+1):4,(x+1,y):5,(x,y-1):6},
            's': {(x,y-1):1,(x-1,y-1):2,(x-1,y):3,(x,y+1):4,(x+1,y+1):5,(x+1,y):6},
            'sw': {(x+1,y):1,(x,y-1):2,(x-1,y-1):3,(x-1,y):4,(x,y+1):5,(x+1,y+1):6},
            'nw': {(x-1,y):1,(x,y+1):2,(x+1,y+1):3,(x+1,y):4,(x,y-1):5,(x-1,y-1):6}
        }
        return switch[direction]
    
    def directionSpaces(self,direction,unit):
        x = unit[0]
        y = unit[1]
        switch = {
            'n': (x,y+1),
            'ne': (x-1,y+1),
            'se': (x-1,y),
            's': (x,y-1),
            'sw': (x+1,y),
            'nw': (x-1,y)
        }
        return switch[direction]
        
    def targetDirectionUnitAttack(self,targetDirection):
        # when target is facing a direction and given unit direction of attack, what # space is it from 
        # target perspective?
        # example: target facing north, attack coming from south (attack facing north) = # 4 space (from behind)
        switch = {
            'n': {'n': 4, 'ne': 5, 'se': 6, 's': 1, 'sw': 2, 'nw': 3},
            'ne': {'n': 3, 'ne': 4, 'se': 5, 's': 6, 'sw': 1, 'nw': 2},
            'se': {'n': 2, 'ne': 3, 'se': 4, 's': 5, 'sw': 6, 'nw': 1},
            's': {'n': 1, 'ne': 2, 'se': 3, 's': 4, 'sw': 5, 'nw': 6},
            'sw': {'n': 6, 'ne': 1, 'se': 2, 's': 3, 'sw': 4, 'nw': 5},
            'nw': {'n': 5, 'ne': 6, 'se': 1, 's': 2, 'sw': 3, 'nw': 4},
        }
        return switch[targetDirection]
    
    def adjacentSpacesDir(self,*args):
        #[1,2,3,4,5,6]
        x = self.location[0]
        y = self.location[1]
        if args:
            if 'Location' in args[0]:
                x = args[0]['Location'][0]
                y = args[0]['Location'][1]

            
        switch = {
            'n': {1:(x,y+1),2:(x+1,y+1),3:(x+1,y),4:(x,y-1),5:(x-1,y-1),6:(x-1,y)},
            'ne': {1:(x+1,y+1),2:(x+1,y),3:(x,y-1),4:(x-1,y-1),5:(x-1,y),6:(x,y+1)},
            'se': {1:(x-1,y-1),2:(x-1,y),3:(x,y+1),4:(x+1,y+1),5:(x+1,y),6:(x,y-1)},
            's': {1:(x,y-1),2:(x-1,y-1),3:(x-1,y),4:(x,y+1),5:(x+1,y+1),6:(x+1,y)},
            'sw': {1:(x+1,y),2:(x,y-1),3:(x-1,y-1),4:(x-1,y),5:(x,y+1),6:(x+1,y+1)},
            'nw': {1:(x-1,y),2:(x,y+1),3:(x+1,y+1),4:(x+1,y),5:(x,y-1),6:(x-1,y-1)}
        }
        if args:
            if 'Direction' in args[0]:
                return switch.get(args[0]['Direction'])
                
        return switch.get(self.direction)
  
    def spacesToDir(self,unit,target):
        # start with unit, move to target, give direction
        x = unit[0]
        y = unit[1]
        moveSwitch = {
            (x,y+1):'n',
            (x+1,y+1):'ne',
            (x+1,y):'se',
            (x,y-1):'s',
            (x-1,y-1):'sw',
            (x-1,y):'nw'
        }
        return moveSwitch.get(target)
    
    def oppositeSpacesDir(self,unit,target):
        x_t = target[0]
        y_t = target[1]
        
        switch = {
                #location of unit: opposite of target; both in reference to target
                (x_t,y_t+1):(x_t,y_t-1),
                (x_t+1,y_t+1):(x_t-1,y_t-1),
                (x_t+1,y_t):(x_t-1,y_t),
                (x_t,y_t-1):(x_t,y_t+1),
                (x_t-1,y_t-1):(x_t+1,y_t+1),
                (x_t-1,y_t):(x_t+1,y_t)
        }
        return switch.get(unit)
    
    def dealDamage(self,unit,target,gameboard,damage,*args):
        if target not in gameboard:
            return gameboard
        if gameboard[target].name == 'Objective' or gameboard[target].name == 'Obstacle':
            damage = damage - gameboard[target].getArmor(gameboard)
        
        reaction = gameboard[unit].reactionManager.checkReaction(target,unit,gameboard,['GiveDamage'])
        gameboard, damage = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,damage)
        if gameboard[target].name == 'Unit':
            reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['TakeDamage'])
            if reaction:
                gameboard, damage = gameboard[target].abilities[reaction].abilityEffect(target,unit,gameboard,damage)
        
        if 'AetherPulse' in args and damage > 0:
            gameboard[unit].abilities['AetherPulse'].recoverHealth(unit,gameboard)
        
        if 'Aegis' in gameboard[target].abilities:
            targetfacing = self.targetDirectionUnitAttack(gameboard[target].direction)
            if targetfacing[self.attackDirection(unit,target)] in [6,1,2]:
                damage = 0
        
        if 'Sunder' in gameboard[unit].abilities:
            multiplier = random.choice([x for x in range(0,gameboard[unit].attributeManager.getAttributes('Attack'))+1])
            if multiplier > 0:
                damage = damage * (multiplier+1)
                
        if 'Barter' in gameboard[target].abilities:
            for x in range(0,damage):
                gameboard[target].abilities['Attack'].abilityEffect(target,unit,gameboard)  
                
        gameboard[target].attributeManager.changeAttributes('Health',-damage)
        if gameboard[target].attributeManager.getAttributes('Health') <= 0:

            reaction = gameboard[unit].reactionManager.checkReaction(unit,target,gameboard,['EliminateUnit'])            
            gameboard = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard)
            if gameboard[target].name == 'Unit':
                reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['EliminateUnit'])            
                gameboard = gameboard[target].abilities[reaction].abilityEffect(target,unit,gameboard)

            gameboard = gameboard[unit].eliminateUnit(gameboard[target].unitType,unit,gameboard[target].playerID,gameboard)
            
        return gameboard      
        
    def getDistance(self,target,location):
        if (target[0] - location[0] >= 0 and target[1] - location[1] <= 0) or (target[0] - location[0] <= 0 and target[1] - location[1] >= 0):
            return abs(target[1]-location[1])+abs(target[0]-location[0])

        if (target[0] - location[0] >= 0 and target[1] - location[1] >= 0) or (target[0] - location[0] <= 0 and target[1] - location[1] <= 0):
            return max(abs(target[1]-location[1]),abs(target[0]-location[0]))
    
    def straightLine(self,spaces,direction,unit,gameboard):
        line = [unit]
        nextSpace = {
            'n': (lambda x: [(x[0],x[1]+1)]),        
            'ne': (lambda x: [(x[0]+1,x[1]+1)]),
            'se': (lambda x: [(x[0]+1,x[1])]),
            's': (lambda x: [(x[0],x[1]-1)]),
            'sw': (lambda x: [(x[0]-1,x[1]-1)]),
            'nw': (lambda x: [(x[0]-1,x[1])])
        }
        for x in range(0,spaces):
            nextInLine = nextSpace.get(direction)(line[x])
            if nextInLine[0] not in gameboard and nextInLine[0] in self.boardLocations:
                line = line + nextInLine
            else:
                break
        return line
    
    def forcedMovement(self,spaces,direction,unit,target,gameboard,*args):
        # Unit is the unit forcing the movement
        # Target is the forced unit
        # target space is the start space
        movedSpaces = [target]
        maxSpace = 0
        forced = {
                'n': (lambda x: [(x[0],x[1]+1)]),        
                'ne': (lambda x: [(x[0]+1,x[1]+1)]),
                'se': (lambda x: [(x[0]+1,x[1])]),
                's': (lambda x: [(x[0],x[1]-1)]),
                'sw': (lambda x: [(x[0]-1,x[1]-1)]),
                'nw': (lambda x: [(x[0]-1,x[1])])
        }
        if 'Stonewrought' in gameboard[target].abilities:
            moveable = gameboard[target].abilities['Stonewrought'].abilityEffect()
        else:
            moveable = True
        if gameboard[target].moveable and moveable:
            for x in range(1,spaces):
                movedSpaces = movedSpaces + forced.get(direction)(movedSpaces[x-1])
                if movedSpaces[x] in gameboard:
                    maxSpace = x-1
                    print('Forced Movement')
                    print(movedSpaces)
                    gameboard[movedSpaces[x-1]] = gameboard[target]
                    del gameboard[target]
                    # At this point the moved unit is at movedSpaces[x-1]
                    blockedSpace = movedSpaces[x]
                    index = x
            if maxSpace > 0:
                if 'Shockwave' in gameboard[movedSpaces[index-1]].abilities:
                    for x in gameboard[movedSpaces[index-1]].getAOETargets(1,movedSpaces[index-1],gameboard):
                        gameboard = self.forcedMovementDamage(spaces-maxSpace,blockedSpace,movedSpaces[index-1],index,gameboard,direction)
                else:    
                    gameboard = self.forcedMovementDamage(spaces-maxSpace,blockedSpace,movedSpaces[index-1],movedSpaces[index],gameboard,direction)

        else:
            return gameboard
        return gameboard
        
    def forcedMovementDamage(self,blockedSpaces,blockedSpace,unit,target,gameboard,direction):
        # unit is the initially moved unit
        # target is the incident unit
        damage = round(blockedSpaces/2)
        
        unitArmor = gameboard[unit].attributeManager.getAttributes('Armor')
        unitDamage = damage - unitArmor
        targetArmor = gameboard[target].attributeManager.getAttributes('Armor')
        targetDamage = damage - targetArmor
        
        if 'Stonewrought' in gameboard[unit].abilities:
            unitDamage = 0
        if 'Gigalith' in gameboard[unit].abilities:
            unitDamage = unitDamage + gameboard[unit].attributeManager.getAttributes('Armor')
        if unitDamage > 0:
            gameboard[unit].attributeManager.changeAttributes('Health',-unitDamage)
        
        if 'Stonewrought' in gameboard[target].abilities:
            targetDamage = 0
        if targetDamage > 0:
            gameboard[target].attributeManager.changeAttributes('Health',targetDamage)
        
        if gameboard[blockedSpace].name == 'Objective' or gameboard[target].name == 'Obstacle':
            damage = damage - gameboard[target].getArmor(gameboard)
        gameboard[blockedSpace].attributeManager.changeAttributes('Health',-damage)
        
        if gameboard[target].attributeManager.getAttributes('Health') <= 0:
            gameboard[unit].eliminateUnit(gameboard[target].unitType,gameboard[target].playerID)
            
        if target in gameboard and blockedSpaces > 0 and 'Avalanche' in gameboard[unit].abilities:
            self.forcedMovement(blockedSpaces,direction,unit,target,gameboard)
            
        return gameboard

    def getAOETargets(self, unitRange, unitLocation, gameboard):
        for i in range(0,unitRange):
            spaces = list(set([a for b in [self.adjacentSpaces(x) for x in self.adjacentSpaces(unitLocation)] for a in b]))
        spaces = [x for x in spaces if x in boardLocations and x in gameboard]
        # if x and y are changing in different directions (+/-) it is 2 spaces
        # if x and y are changing in the same direction (+/+) it is 1 space
        # if only x or y are changing it is 1 space
        return spaces

class Ability(GeneralUse):
    
    state = 'None'
    use = 'All'
    unitType = 'None'
    actionLog = {}
    
    def __init__(self,playerID):
        self.playerID = playerID
    
    def initAbility(self, gameboard):
        return gameboard
    
    def getTargets(self,unit,gameboard):
        return [unit]
    
    def getLOSTargets(self,unit,gameboard,*args):
        if args:
            args = args[0]
        if 'Range' in args:
            spaces = self.getAOETargets(args['Range'],unit,gameboard)
        else:
            spaces = self.getAOETargets(gameboard[unit].unitRange,unit,gameboard)

        LOS = gameboard[unit].lineOfSightManager.lineOfSight['Clear']+gameboard[unit].lineOfSightManager.lineOfSight['Partial']
        potentialTargets = [x for x in list(set(LOS).intersection(set(spaces))) if x in gameboard]
        potentialTargets = [x for x in potentialTargets if gameboard[x].name != 'Respawn']
        return potentialTargets
    
    def getMeleeTargets(self,unit,gameboard):
        spaces = gameboard[unit].adjacentSpacesDir()
        return [x for x in [spaces[6],spaces[1],spaces[2]] if x in gameboard]
    
    def execute(self,unit,gameboard,*args):
        self.actionLog = {}
        potentialTargets = self.getTargets(unit,gameboard)
        if potentialTargets:
            target = random.choice(potentialTargets)
            # combatSteps is required for reactions but not others
            gameboard = self.abilityEffect(unit,target,gameboard)
            if target in gameboard and gameboard[target].name == 'Unit':
                gameboard[target].reactionManager.setState('None')
            self.actionLog = {'Unit':unit,'Target':target}
        return gameboard

    def combat(self,unit,target,gameboard,*mods):
        if unit in gameboard:
            unitObject = gameboard[unit]
        targetObject = gameboard[target]
        gameboard[unit].setLastAction('Combat')
        if mods:
            mods = mods[0]
        # if stealth token is attacked, remove from board
        if target in gameboard and gameboard[target].name == 'StealthToken':
            del gameboard[target]
            return gameboard
        
        if target not in gameboard:
            return gameboard
        if gameboard[target].name == 'Respawn':
            return gameboard
        
        combatSteps = {
                'CalcHit': random.randint(1,6),
                'AddHit': gameboard[unit].attributeManager.getAttributes('Hit'),
                'HitResult': 0,
                'CalcEvasion': random.randint(1,6),
                'AddEvasion':gameboard[target].attributeManager.getAttributes('Evasion'),
                'EvasionResult':0,
                'CombatResult':[],
                'Damage': gameboard[unit].attributeManager.getAttributes('Damage'),
                'AddDamage': 0,
                'Armor': gameboard[target].attributeManager.getAttributes('Armor'),
                'AddArmor': 0,
                'ResultingDamage': 0,
                'newPosition': False,
                'AttackMods': mods
        }

        for x in mods: 
            if x in combatSteps:
                combatSteps[x] = combatSteps[x] + mods[x]

        if 'Armory' in gameboard[unit].abilities:
            if [x for x in gameboard[unit].abilities['Armory'].getAOETargets(gameboard[unit].abilities['Armory'].auraRange,unit,gameboard) if gameboard[x].name == 'Armory']:
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + 1
                combatSteps['AddHit'] = combatSteps['AddHit'] + 1
        
        if 'Bunker' in gameboard[target].abilities:
            if [x for x in gameboard[target].abilities['Bunker'].getAOETargets(gameboard[target].abilities['Bunker'].auraRange,unit,gameboard) if gameboard[x].name == 'Bunker']:
                combatSteps['Armor'] = combatSteps['Armor'] + 1
                if 'Piercing' in combatSteps['AttackMods']:
                    del combatSteps['AttackMods']['Piercing']        

        if 'UAVTower' in gameboard[unit].abilities:
            if [x for x in gameboard[unit].abilities['UAVTower'].getAOETargets(gameboard[unit].abilities['UAVTower'].auraRange,unit,gameboard) if gameboard[x].name == 'UAVTower']:
                combatSteps['AddHit'] = combatSteps['AddHit'] + 2           
        
        if gameboard[unit].playerClass == 'Warrior':
            gameboard,combatSteps = gameboard[unit].hitDiceMods(unit,target,gameboard,combatSteps)
        if gameboard[target].name == 'Unit' and gameboard[target].playerClass == 'Warrior':
            gameboard,combatSteps = gameboard[target].evasionDiceMods(unit,target,gameboard,combatSteps)
        
        # target reaction from melee
        if self.getDistance(unit,target) == 1:
            reaction = gameboard[unit].reactionManager.checkReaction(unit,target,gameboard,['TargetedMelee'])
            gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)
        
        # add additional hit modifiers
        if gameboard[target].name == 'Unit':
            reaction = gameboard[unit].reactionManager.checkReaction(unit,target,gameboard,['AddHit'])
            gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)
            
        combatSteps['HitResult'] = combatSteps['CalcHit'] + combatSteps['AddHit']
            
        # add additional evasion modifiers
        if gameboard[target].name == 'Unit':
            reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['AddEvasion'])
            gameboard,combatSteps = gameboard[target].abilities[reaction].abilityEffect(target,unit,gameboard,combatSteps)
            
        if combatSteps['newPosition']:
            unit = combatSteps['newPosition']
            combatSteps['newPosition'] = False
        
        if unit in gameboard:
            gameboard, combatSteps = gameboard[unit].passiveMods(unit,target,gameboard,combatSteps)
        if target in gameboard and gameboard[target].name == 'Unit':
            gameboard, combatSteps = gameboard[target].passiveMods(unit,target,gameboard,combatSteps)
        
        if target in gameboard and [x for x in gameboard if 'RadarTower' in gameboard[target].abilities]:
            if 'RadarTower' in gameboard[target].abilities:
                if [x for x in gameboard[target].abilities['RadarTower'].getAOETargets(gameboard[target].abilities['RadarTower'].auraRange,target,gameboard) if gameboard[x].name == 'UAVTower']:
                    combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + 2
                    if 'Wounding' in combatSteps['AttackMods']:
                        del combatSteps['AttackMods']['Wounding']
                        combatSteps['HitResult'] = 6
        
        if 'Wounding' in combatSteps['AttackMods']:
            combatSteps['CombatResult'] = 'Hit'
            
        if combatSteps['HitResult'] > combatSteps['EvasionResult']:
            combatSteps['CombatResult'] = 'Hit'

        if 'Piercing' in combatSteps['AttackMods'] and target in gameboard:
            if gameboard[target].unitClass == 'Engineer':
                if 'Tank' in gameboard[target].unitBlueprints or 'Dreadnought' in gameboard[target].unitBlueprints:
                    del combatSteps['AttackMods']['Piercing']
            combatSteps['Armor'] = 0
            combatSteps['AddArmor'] = 0

        if combatSteps['CombatResult'] == 'Evasion':
            if combatSteps['EvasionResult'] >= combatSteps['HitResult'] + 3:
                reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['GreaterEvasion'])
                gameboard, combatSteps = gameboard[target].abilities[reaction].abilityEffect(target,unit,gameboard,combatSteps)
            else:
                reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['Evasion','Any'])
                gameboard, combatSteps = gameboard[target].abilities[reaction].abilityEffect(target,unit,gameboard,combatSteps)                
            reaction = gameboard[unit].reactionManager.checkReaction(unit,target,gameboard,['MissedMeleeAttack','Any'])
            gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)
        
        if target in gameboard:
            if 'ArcaneShield' in gameboard[target].abilities:
                if gameboard[target].abilities['ArcaneShield'].stacks > 0:
                    gameboard[target].abilities['ArcaneShield'].useStack()
                    combatSteps['ResultingDamage'] = 0 
     
            if combatSteps['CombatResult'] == 'Hit' and 'Wounding' not in 'AttackMods' and gameboard[target].name == 'Unit':
                reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['LostEvasion'])
                gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)                                  

        if combatSteps['CombatResult'] == 'Hit':
            if 'Axe' in combatSteps['AttackMods']:
                gameboard[unit].attributeManager.bonusAttributes['Damage'] = gameboard[unit].attributeManager.bonusAttributes['Damage'] + 1
            combatSteps['ResultingDamage'] = combatSteps['Damage'] + combatSteps['AddDamage'] - combatSteps['Armor'] - combatSteps['AddArmor']
            if combatSteps['ResultingDamage'] < 0:
                combatSteps['ResultingDamage'] = 0
            elif 'Assassin' in mods:
                # for simplicity, damage bonus updates at the end of the turn for now
                # elite = [x for x in gameboard if gameboard[unit].playerID == gameboard[x].playerID and gameboard[x].unitType == 'Elite'][0]
                # gameboard[elite].damageBonus = gameboard[elite].damageBonus + mods['Assassin']
                if unitObject.unitType == 'Common':
                    gameboard['DamageBonus'] = mods['Assassin']
                
            gameboard = self.dealDamage(unit,target,gameboard,combatSteps['ResultingDamage'],mods)
        if unit in gameboard and target in gameboard:
            reaction = gameboard[unit].reactionManager.checkReaction(unit,target,gameboard,['AfterAttack'])
            gameboard = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard)
        # ask if you want to react -> yes? ->  call function from inside here
        
        return gameboard
        
    def updatePosition(self,combatSteps):
        if combatSteps['newPosition']:
            unit = combatSteps['newPosition']
            combatSteps['newPosition'] = False
        return unit,combatSteps
    
    def abilityEffect(self,unit,target,gameboard):
        return gameboard

#_____________________ implement capturing
class CaptureObjective(Ability):
    name = 'CaptureObjective'
    cost = {'Passive':['Passive']}
    
    def abilityEffect(self,unit,target,gameboard):
        if target in gameboard[unit].adjacentSpaces(unit) and hasattr(gameboard[target],'player'):
            if gameboard[target].player == 'None':
                gameboard[target].player = gameboard[unit].player
                gameboard[unit].attributeManager.changeAttributes(gameboard[unit].captureCost,-1)
        return gameboard

class CaptureRespawn(Ability):
    name = 'CaptureRespawn'
    cost = {'Passive':['Passive']}
    def abilityEffect(self,unit,target,gameboard):
        
        if target in gameboard[unit].adjacentSpaces() and hasattr(gameboard[target],'player'):
            if gameboard[target].player == 'None':
                gameboard[target].player = gameboard[unit].player
                gameboard[unit].attributeManager.changeAttributes(gameboard[unit].captureCost,-1)
        return gameboard
#__________________________________- 

class Attack(Ability):
    name = 'Attack'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Attack',-1)
        return self.combat(unit,target,gameboard) 
        
    def getTargets(self,unit,gameboard,*args):
        return self.getLOSTargets(unit,gameboard,args)
    
class Movement(Ability):
    
    name = 'Movement'
    cost = {'Turn':['Movement']}
    straightLineTraveled = 0
    lastDirTraveled = None
    
    def availableMovement(self,unit,gameboard,origin,*effects):
        effects = effects[0]
        respawns = [x for x in gameboard if gameboard[x].name == 'Respawn']
        respawnSpaces = [a for b in [self.adjacentSpaces(x) for x in respawns if gameboard[x].playerID == self.playerID] for a in b if a not in gameboard]
        
        spaces = [x for x in self.adjacentSpaces(unit) if x not in gameboard or x == origin or (x in gameboard and gameboard[x].name == 'StealthToken')]
        if effects != None:
            if 'Unrestrained' in effects:
                spaces = self.adjacentSpaces(unit)
        if set(spaces) & set(respawnSpaces):
            spaces = list(set(spaces + respawnSpaces))
            
        # 'origin' is location in gameboard of unit object before executing movement
        # 'unit' is the unit placeholder when calculating unit path
        spaces = spaces + gameboard[origin].addMovementSpaces(unit,origin,gameboard,spaces)
        spaces = [x for x in spaces if x in self.boardLocations]
        return spaces
    
    def abilityEffect(self,unit,target,gameboard,*args):
        if gameboard[unit].name != 'Unit':
            return gameboard
        # args is a manually input distance
        gameboard[unit].setLastAction('Movement')
        if args:
            args = args[0]
        effects = []
        if 'Ability' in args:
            effects = gameboard[unit].generateMovementEffects(args['Ability'])
        else:
            effects = gameboard[unit].generateMovementEffects()
            
        # pick the number of spaces you would like to move
        if 'Distance' not in args:
            movePoints = gameboard[unit].attributeManager.getAttributes('Movement')
            if movePoints > 0:
                numberOfSpaces = random.choice([x for x in range(1,movePoints+1)])
            else:
                return gameboard
        elif 'Distance' in args:
            numberOfSpaces = args['Distance']
        # pick the path you would like to move through
        if 'Direction' not in args:
            potentialTargets = self.availableMovement(unit,gameboard,unit,effects)
            if potentialTargets:
                target = [random.choice(potentialTargets)]
                for x in range(1,numberOfSpaces-2):
                    potentialTargets = self.availableMovement(target[x-1],gameboard,unit,args)
                    if potentialTargets:
                        target = target + [random.choice(potentialTargets)]
                    else:
                        break
            else:
                return gameboard
        else:
            target = [gameboard[unit].adjacentSpacesDir(args['Direction'])]
            if target in gameboard and gameboard[target].name != 'StealthToken':
                return gameboard                
            for x in range(1,numberOfSpaces-2):
                target = target + [self.adjacentSpacesDir({'Direction':args['Direction'],'Location':target[x-1]})]
            
        playerUnit = gameboard[unit]
        distance = 0
        reducedCost = 0
        lastOpenSpace = unit
        # execute number of movements
        
        # passive movement checks
        for x in target:
            directionTraveled = self.spacesToDir(unit,x)
            if directionTraveled == self.lastDirTraveled:
                self.straightLineTraveled = self.straightLineTraveled + 1
            else:
                self.straightLineTraveled = 1
            self.lastDirTraveled = directionTraveled
                
            if x not in gameboard or x == unit:
                lastOpenSpace = x
                distance = distance + 1
            if 'Stalk' in gameboard[unit].abilities:
                if [x for x in self.adjacentSpaces(x) if gameboard[x].name == 'Unit' and gameboard[x].playerID != gameboard[unit].playerID]:
                    reducedCost = reducedCost = reducedCost + 1
            if 'Sneak' in gameboard[unit].abilities:
                enemies = [x for x in gameboard if gameboard[x].name == 'Unit' and gameboard[x].playerID != gameboard[unit].playerID]
                seen = False
                for y in enemies: 
                    if target in y.lineOfSight['Clear']:
                        seen = True
                if not seen:
                    reducedCost = reducedCost = reducedCost + 1
                    
        # check reactions
        for x in gameboard:
            if gameboard[x].name == 'Unit':
                gameboard[x].reactionManager.checkReaction(x,target,gameboard,['Any'])
        
        # remove movement points from unit
        if 'Cost' in args:
            if args['Cost'] != 'Passive':
                gameboard[unit].attributeManager.changeAttributes(args['Cost'],-(distance-reducedCost))
        else:            
            gameboard[unit].attributeManager.changeAttributes('Movement',-distance)
        
        for x in range(0,len(target)):        
            if x <= distance:
                gameboard = gameboard[unit].movementEffects(unit,target[x],gameboard)
                if target[x] in gameboard:
                    if gameboard[target[x]].name == 'StealthToken':
                        gameboard = gameboard[target[x]].stealthTokenEffect(unit,gameboard)
                        del gameboard[target[x]]
                gameboard[unit].setDirection(random.choice(self.directions),gameboard)
                
                if target[x] not in gameboard:
                    gameboard[unit].location = target[x]
                    playerUnit.location = target[x]
                    gameboard[target[x]] = playerUnit
                    del gameboard[unit]
                    unit = target[x]
                    
                    gameboard[unit].getLineOfSight(gameboard)
            if 'Fissure' in playerUnit.abilities:
                if x != 0:
                    gameboard[target[x-1]] = Obstacle()
                    gameboard[target[x-1]].temporary = True
                    gameboard[target[x-1]].playerID = playerUnit.playerID
                elif x == 0:
                    gameboard[unit] = Obstacle()
                    gameboard[unit].temporary = True
                    gameboard[unit].playerID = playerUnit.playerID
                    
            unit = target[x]

        gameboard[lastOpenSpace] = playerUnit
        gameboard[lastOpenSpace].reactionManager.setState('None')
        
        return gameboard

class Reorient(Ability):
    name = 'Reorient'
    cost = {'Passive':['Passive']}
    state = ['ReceiveDamage']
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].direction = random.choice([x for x in ['n','ne','se','s','sw','nw'] if x != gameboard[unit].direction])
        return gameboard
    
class Perception(Ability):
    name = 'Perception'
    cost = {'Reaction':['Reaction']}
    state = ['Any']
    
    def abilityEffect(self,unit,target,gameboard):
        if [x for x in gameboard if 'Misdirection' in gameboard[x].abilities and gameboard[x].playerID != gameboard[unit].playerID]:
            if gameboard[unit].attributeManager.getAttributes('Reaction') == 0:
                return gameboard
            else:
                gameboard[unit].attributeManager.changeAttribute('Reaction',-1)
        gameboard[unit].direction = random.choice([x for x in ['n','ne','se','s','sw','nw'] if x != gameboard[unit].direction])
        return gameboard
    
class AccurateStrike(Ability):
    name = 'AccurateStrike'
    cost = {'Reaction':['Reaction']}
    state = 'Hit'
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['AddHit'] = combatSteps['AddHit'] + 1
        return (gameboard,combatSteps)
    
class Avoid(Ability):
    name = 'Avoid'
    cost = {'Reaction':['Reaction','Movement']}
    state = 'LostEvasion'
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Movement',1)
        gameboard[unit].abilities.get('Movement').execute(unit,target,gameboard,1)
        return gameboard
    

class PurposefulDodge(Ability):
    name = 'PurposefulDodge'
    cost = {'Reaction':['Passive']}
    state = 'GreaterEvasion'
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        spaces = 1
        if 'TimeDilation' in gameboard[target].abilities:
            spaces = 3
        gameboard[unit].attributeManager.changeAttributes('Movement',spaces)
        gameboard, newpos = gameboard[unit].abilities['Movement'].execute(unit,target,gameboard,spaces)
        return gameboard,newpos
    
class RedirectedStrike(Ability):
    name = 'RedirectedStrike'
    cost = {'Reaction':['Reaction']}
    state = 'MissedMeleeAttack'
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        #damage = gameboard[unit].reactionManager.multipleReactionPoints(unit,gameboard)
        self.combat(unit,target,gameboard)
        gameboard[unit].abilities.get('Attack').execute(unit,target,gameboard)
        return gameboard
    
class Pass(Ability):
    
    name = 'Pass'
    cost = {'Turn':['Passive'],'Reaction':['Passive']}
    def abilityEffect(self,unit,target,gameboard,*args):
        if args:
            combatSteps = args[0] 
            return gameboard,combatSteps
        else:
            return gameboard
        
class AttributeManager(GeneralUse):
    
    bonusAttributes = {'Health':0,'Attack':0,'Movement':0,'Reaction':0,'Special':0,'Hit':0,'Evasion':0,'Armor':0}
    permBonusAttr = {'Health':0,'Attack':0,'Movement':0,'Special':0,'Reaction':0,'Damage':0,'Evasion':0,'Hit':0,'Armor':0}
    
    def __init__(self,currentAttributes):
        self.currentAttributes = currentAttributes
    
    def getAttributes(self,attribute):
        return self.currentAttributes[attribute]
    
    def changeAttributes(self,attribute,value):
        if attribute != 'Passive':
            self.currentAttributes[attribute] = self.currentAttributes[attribute] + value

    def setAttributes(self,attribute,value):
        self.currentAttributes[attribute] = value + self.bonusAttributes[attribute]
    
    # bonus attributes set at the end of your turn
    def setBonusAttributes(self,attribute,value):
        self.currentAttributes[attribute] = self.bonusAttributes[attribute] + value

    def changePermanentUpgrade(self,attribute,value):
        self.permBonusAttr[attribute] = self.permBonusAttr[attribute] + value
    
class LevelManager:
    def __init__(self,level,unitClass,unitType):
        self.unitClass = unitClass
        self.level = level
        self.unitType = unitType
        self.updateAttributes()
      
    def updateAttributes(self):
        self.unitAttributes = self.classAttributes()
        
    def setAttributes(self,attributes):
        return dict(zip(['Health','Attack','Movement','Special','Reaction','Damage','Evasion','Hit','Armor'],attributes))

    def getAttributes(self):
        return self.unitAttributes
    
    def classAttributes(self):
        classSwitch = {
            'Warrior': self.WarriorAttributes(),
            'Assassin': self.AssassinAttributes(),
            'Mage': self.MageAttributes(),
            'Engineer': self.EngineerAttributes()
        }
        return classSwitch.get(self.unitClass)
    
    def WarriorAttributes(self):
        levelSwitchE = {
            1: self.setAttributes([5,1,3,1,1,2,0,0,0]),
            2: self.setAttributes([5,1,3,1,1,2,0,0,0]),
            3: self.setAttributes([7,2,3,1,2,2,0,1,0]),
            4: self.setAttributes([7,2,3,1,2,2,1,1,0]),
            5: self.setAttributes([7,3,3,1,3,3,1,1,1]),
            6: self.setAttributes([9,3,3,1,3,3,1,2,1]),
            7: self.setAttributes([9,4,3,2,3,3,2,2,1]),
            8: self.setAttributes([11,4,3,2,3,3,2,2,1]),
            9: self.setAttributes([11,4,3,2,3,3,2,2,1]),
            10: self.setAttributes([13,4,3,2,4,4,2,3,2])
        }
        levelSwitchC = {
            1: self.setAttributes([3,1,3,1,1,2,0,0,0]),
            2: self.setAttributes([3,1,3,1,1,2,0,0,0]),
            3: self.setAttributes([5,1,3,1,2,2,0,0,0]),
            4: self.setAttributes([5,1,3,1,2,2,0,0,0]),
            5: self.setAttributes([5,2,3,1,2,2,0,1,0]),
            6: self.setAttributes([6,2,3,1,3,2,0,1,1]),
            7: self.setAttributes([6,2,3,1,3,2,1,1,1]),
            8: self.setAttributes([7,2,3,1,3,3,1,1,1]),
            9: self.setAttributes([7,2,3,2,3,3,1,1,1]),
            10: self.setAttributes([8,2,3,2,3,3,1,2,1])
        }

        typeSwitch = {
            'Elite': levelSwitchE.get(self.level),
            'Common': levelSwitchC.get(self.level)
        }
        return typeSwitch.get(self.unitType)

    def AssassinAttributes(self):
        levelSwitchE = {
            1: self.setAttributes([4,1,3,1,2,1,1,0,0]),
            2: self.setAttributes([4,1,3,1,2,1,1,0,0]),
            3: self.setAttributes([5,1,3,1,2,2,1,0,0]),
            4: self.setAttributes([5,1,3,1,3,2,2,0,0]),
            5: self.setAttributes([7,1,4,1,3,3,2,0,0]),
            6: self.setAttributes([7,1,4,1,3,3,2,0,0]),
            7: self.setAttributes([8,2,4,1,4,4,3,0,0]),
            8: self.setAttributes([8,2,4,1,4,4,3,0,0]),
            9: self.setAttributes([8,2,4,1,4,5,3,0,0]),
            10: self.setAttributes([10,2,4,1,5,5,4,2,2])
        }
        levelSwitchC = {
            1: self.setAttributes([3,1,3,1,2,1,1,1,0]),
            2: self.setAttributes([3,1,3,1,2,1,1,1,0]),
            3: self.setAttributes([4,1,3,1,2,1,2,2,0]),
            4: self.setAttributes([4,1,4,1,3,2,2,2,0]),
            5: self.setAttributes([5,1,4,1,3,2,2,2,0]),
            6: self.setAttributes([5,1,4,1,3,2,2,2,1]),
            7: self.setAttributes([6,2,4,1,3,2,2,2,1]),
            8: self.setAttributes([6,2,4,1,4,2,2,2,1]),
            9: self.setAttributes([7,2,4,1,4,2,2,3,1]),
            10: self.setAttributes([7,2,4,1,4,3,3,3,1])
        }

        typeSwitch = {
            'Elite': levelSwitchE.get(self.level),
            'Common': levelSwitchC.get(self.level)
        }
        return typeSwitch.get(self.unitType)

    def MageAttributes(self):
        levelSwitchE = {
            1: self.setAttributes([4,1,3,3,1,1,0,0,0]),
            2: self.setAttributes([4,1,3,3,1,1,0,0,0]),
            3: self.setAttributes([5,1,3,3,2,1,0,0,0]),
            4: self.setAttributes([5,1,3,3,2,1,0,1,1]),
            5: self.setAttributes([5,1,3,4,3,1,1,1,1]),
            6: self.setAttributes([7,1,3,4,3,1,1,1,1]),
            7: self.setAttributes([7,1,3,4,4,1,1,1,2]),
            8: self.setAttributes([8,1,3,4,4,1,2,1,2]),
            9: self.setAttributes([8,1,3,5,5,1,2,1,2]),
            10: self.setAttributes([10,1,3,5,5,1,3,1,2])
        }
        levelSwitchC = {
            1: self.setAttributes([3,1,3,0,0,1,0,0,0]),
            2: self.setAttributes([3,1,3,0,0,1,0,0,0]),
            3: self.setAttributes([4,1,3,0,0,2,0,0,0]),
            4: self.setAttributes([4,1,3,0,0,2,1,0,0]),
            5: self.setAttributes([4,1,3,0,0,2,1,0,0]),
            6: self.setAttributes([4,1,3,0,0,2,1,1,0]),
            7: self.setAttributes([4,1,3,0,0,2,1,1,0]),
            8: self.setAttributes([5,1,3,0,0,2,1,1,0]),
            9: self.setAttributes([5,1,4,0,0,2,1,1,0]),
            10: self.setAttributes([5,1,4,0,0,2,2,1,0])
        }

        typeSwitch = {
            'Elite': levelSwitchE.get(self.level),
            'Common': levelSwitchC.get(self.level)
        }
        return typeSwitch.get(self.unitType)

    def EngineerAttributes(self):
        levelSwitchE = {
            1: self.setAttributes([4,1,2,2,1,1,-2,-2,0]),
            2: self.setAttributes([4,1,2,2,1,1,-2,-2,0]),
            3: self.setAttributes([4,1,2,2,1,1,-2,-2,0]),
            4: self.setAttributes([5,1,2,2,1,1,-2,-2,0]),
            5: self.setAttributes([5,1,2,2,1,1,-2,-2,0]),
            6: self.setAttributes([5,1,2,2,1,1,-2,-2,0]),
            7: self.setAttributes([6,1,2,2,1,1,-2,-2,0]),
            8: self.setAttributes([6,1,2,2,1,1,-2,-2,0]),
            9: self.setAttributes([6,1,2,2,1,1,-2,-2,0]),
            10: self.setAttributes([7,1,2,2,1,1,-2,-2,0])
        }
        levelSwitchC = {
            1: self.setAttributes([4,1,3,0,0,1,-1,0,0]),
            2: self.setAttributes([4,1,3,0,0,1,-1,1,0]),
            3: self.setAttributes([5,2,3,0,0,2,-1,1,0]),
            4: self.setAttributes([5,2,4,0,0,2,-1,1,1]),
            5: self.setAttributes([5,2,4,0,0,2,0,2,1]),
            6: self.setAttributes([6,2,4,0,0,2,0,2,1]),
            7: self.setAttributes([6,2,4,0,0,2,0,2,2]),
            8: self.setAttributes([6,2,5,0,0,2,0,2,2]),
            9: self.setAttributes([7,2,5,0,0,3,0,2,2]),
            10: self.setAttributes([7,3,5,0,0,3,0,2,3])
        }
        
        typeSwitch = {
            'Elite': levelSwitchE.get(self.level),
            'Common': levelSwitchC.get(self.level)
        }
        return typeSwitch.get(self.unitType)

# Each unit gets an instance of the ability? Or each player?
# Add name of each ability to the list available options?
# I think each ability will need to be integrated into the class-specific
# code. i.e. add code to check name of available abilities at normal places

class ReactionManager(GeneralUse):
    # give state to reaction manager
    # search for reactions with given trigger state
    # ask user if they want to react
    # if yes trigger reaction
    
    state = 'None'
    
    def setState(self,state):
        # give state to reaction manager
        self.state = state
        
    def checkReaction(self,unit,target,gameboard,states):
        # ask if user wants to do a reaction
        # do the reaction (call ability effect)
        self.setState(states)
        reactionChoices = self.availableReactions(gameboard[unit],gameboard)
        if reactionChoices:
            return random.choice(reactionChoices)
        else:
            return 'Pass'
        
    def availableReactions(self,unit,gameboard):
        # find available reactions with corresponding state
        reactions = [x.name for x in unit.abilities.values() if 'Reaction' in x.cost and set(x.cost['Reaction']).issubset(set(unit.availablePoints())) and self.state == x.state]
        return reactions #reaction names
    
    def multipleReactionPoints(self,unit,gameboard):
        maxReactions = gameboard[unit].attributeManager.getAttributes('Reaction')
        return random.choice([x for x in range(1,maxReactions)])

class Unit(GeneralUse):
    
    built = False
    reactionManager = ReactionManager()
    eliminatedUnits = {'Elite':0, 'Common':0, 'Objective':0}
    unitRange = 1
    rangeBonus = 0
    unrestrainedMovement = False
    moveable = True
    aura = 'None'
    location = (-1,-1)
    name = 'Unit'
    
    def __init__(self,unitType,unitName):
        self.unitType = unitType
        self.unitName = unitName
        self.direction = random.choice(self.directions)
        self.lineOfSightManager = LOS.LineOfSight(self.direction)
    
    def setClass(self,playerClass,playerID,captureCost):
        self.playerClass = playerClass
        self.playerID = playerID
        self.levelManager = LevelManager(1,playerClass,self.unitType)
        self.currentAttributes = self.levelManager.getAttributes()
        self.maxHealth = self.currentAttributes['Health']
        self.attributeManager = AttributeManager(self.currentAttributes)
        self.captureCost = captureCost
        self.baseAbilities = {'Attack':Attack(playerID), 'Movement':Movement(playerID), 'Reorient':Reorient(playerID), 'Perception':Perception(playerID),
                 'AccurateStrike': AccurateStrike(playerID),'Avoid':Avoid(playerID),'PurposefulDodge':PurposefulDodge(playerID),'RedirectedStrike':RedirectedStrike(playerID),
                 'Pass':Pass(playerID)}
        self.abilities = self.baseAbilities
        for x in self.abilities:
            self.abilities[x].unitName = self.unitName
        self.boardImage = MySprite(self.playerClass,self.unitType)

        
    def addBonuses(self):
        for x in self.attributeManager.permBonusAttr:
            self.attributeManager.changeAttributes(x,self.attributeManager.permBonusAttr[x])
        self.unitRange = self.unitRange + self.rangeBonus
    
    def createOptions(self):
        # match ability costs to available points
        
        # excludes passives since it matches available points to cost
        useableAbilities = []
        # for each ability, check if the number of points if available in cost, extending to multiple costs
        useablePoints = [x for x in self.availablePoints() if x in ['Attack','Movement','Special','Reaction']]

        options = [x for x in self.abilities]
        for ability in options:
            if 'Turn' in self.abilities[ability].cost:
                for cost in self.abilities[ability].cost['Turn']:
                    if set([cost]).issubset(set(useablePoints)):                        
                        useableAbilities = useableAbilities + [ability]
        # if not useableAbilities:
        #     print(self.unitType + self.unitClass)
        return useableAbilities # this is ability names
    
    def availablePoints(self):
        # return nonzero attribute points
        return [x for x in self.attributeManager.currentAttributes if self.attributeManager.currentAttributes[x] > 0]
    
    def useAbility(self,ability,time):
        [self.attributeManager.changeAttributes(x,-1) for x in self.abilities.get(ability).cost[time]]
    
    def getDistance(self,target):
        if (target[0] - self.location[0] >= 0 and target[1] - self.location[1] <= 0) or (target[0] - self.location[0] <= 0 and target[1] - self.location[1] >= 0):
            return abs(target[1]-self.location[1])+abs(target[0]-self.location[0])

        if (target[0] - self.location[0] >= 0 and target[1] - self.location[1] >= 0) or (target[0] - self.location[0] <= 0 and target[1] - self.location[1] <= 0):
            return max(abs(target[1]-self.location[1]),abs(target[0]-self.location[0]))
    
    def getLineOfSight(self,gameboard):
        self.lineOfSight = self.lineOfSightManager.allLineOfSight(self.direction,self.location,gameboard)
    
    def createCombatModifiers(self,*args):
        return args
    
    def changeLocation(self,location):
        self.location = location
        return
    
    def passiveMods(self,unit,target,gameboard,combatSteps):
        return gameboard,combatSteps
    
    def movementEffects(self,unit,target,gameboard):
        return gameboard
    
    def addMovementSpaces(self,unit,origin,gameboard,spaces):
        return spaces
    
    def eliminateUnit(self,unitType,unit,playerID,gameboard):
        if self.playerID != playerID and unitType in ['Elite','Common','Objective']:
            self.eliminatedUnits[unitType] = self.eliminatedUnits[unitType] + 1
            if 'WarriorAttack' in self.abilities:
                if self.unitType == 'Elite':
                    for x in [y for y in gameboard if gameboard[y].playerID == playerID]:
                        if x.weaponUpgrades[self.weapon] < 3:
                            x.weaponUpgrades[self.weapon] = x.weaponUpgrades[self.weapon] + 1
                elif self.weaponUpgrades[self.weapon] < 3:
                    self.weaponUpgrades[self.weapon] = self.weaponUpgrades[self.weapon] + 1
        gameboard[unit].location = 'None'
        gameboard['EliminatedUnits'].eliminatedUnits[playerID + ' ' + gameboard[unit].name] = gameboard[unit]
        del gameboard[unit]
        return gameboard
        
    def classUpgrades(self,unit):
        return 
        
    def statEffect(self,unitObj):
        return unitObj
    
    def generateMovementEffects(self,*args):
        return
    
    def setLastAction(self,action):
        self.lastAction = action
    
    def setDirection(self,direction,gameboard):
        self.direction = direction
        self.lineOfSightManager.setDirection(direction,self.location,gameboard)
    
class Player(GeneralUse):
    
    abilities = []
    victoryPoints = 0
    level = 1
    experiencePoints = 0
    captureCost = 'Attack'
    actionLog = {}
    logNumber = 0
    
    def __init__(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        # instantiate new units
        self.units = {'Elite':Unit('Elite','Elite1'),'Common1':Unit('Common','Common1'),\
                      'Common2':Unit('Common','Common2'),'Common3':Unit('Common','Common3'),\
                      'Common4':Unit('Common','Common4')}


        for unit in self.units:
            self.units[unit].setClass(self.playerClass,self.playerID,self.captureCost)
        
    def turn(self,gameboard,players):
        
        
        # Each player needs an ability / action log to be printed to the screen after each turn
        
        # while not passed keep going
        
        # refresh ability points from player object to gameboard
        gameboard = self.refreshPoints(gameboard)
        gameboard = self.beginningTurnEffects(gameboard)
        # init action log
        self.actionLog = {}
        while True:
            
            # find units on the gameboard that you can use
            
            # unit choices looks at gameboard
            unitChoices = {x:gameboard[x] for x in gameboard if gameboard[x].name == 'Unit' and gameboard[x].playerID == self.playerID}
            
            # temp solution to update location
            for x in unitChoices:
                unitChoices[x].location = x
            
            for unit in unitChoices:
                unitChoices[unit].unitOptions = unitChoices[unit].createOptions()
                # if EMP tower on the field, cannot use special abilities in proximity
                if [x for x in self.getAOETargets(4,unit,gameboard) if gameboard[x].name == 'EMPTower']:
                    for x in unitChoices[unit].unitOptions:
                        abil = unitChoices[unit].abilities[x]
                        if 'Turn' in abil.cost:
                            if abil.cost['Turn'] == 'Special':
                                del unitChoices[unit].unitOptions[x]
            # unit choice key (x,y)
            # unitChoices['Pass'] = 'Pass'
            unitChoices = {x:unitChoices[x] for x in unitChoices if unitChoices[x].unitOptions}
            # print(unitChoices)
            # TO DO: Remove option to pass units or abilities. Use all available points
            if unitChoices:    
                unitChoiceKey = random.choice(list(unitChoices))
            else:
                unitChoices['Pass'] = 'Pass'
                unitChoiceKey = 'Pass'
            self.unitChoice = unitChoiceKey

            # unit object 
            unitChoiceObject = unitChoices[unitChoiceKey]

            # choosing 'pass' in unitchoice will pass your turn since you don't act
            if unitChoiceObject == 'Pass':
                # print('Pass')
                for x in self.units:
                    for attr in ['Attack','Movement','Reaction','Special']:
                        self.units[x].attributeManager.setBonusAttributes(attr,0)
                        if self.units[x].location in gameboard:
                            gameboard[self.units[x].location].attributeManager.setBonusAttributes(attr,0)
                self.logNumber = 0
                break
            # execute ability
            elif unitChoiceObject.unitOptions:
                
                ability = unitChoiceObject.abilities[random.choice(unitChoiceObject.unitOptions)]
                self.abilityChoice = ability
                # print(ability.name)
                # subtract cost from unit points
                for x in ability.cost['Turn']:
                    gameboard[unitChoiceKey].attributeManager.changeAttributes(x,-1)

                gameboard = ability.execute(unitChoiceKey,gameboard)
                
                # if ability causes a change in damage bonus, add it to elite on board
                if self.playerClass == 'Assassin' and 'DamageBonus' in gameboard:
                    self.damageBonus = self.damageBonus + gameboard['DamageBonus']
                    del gameboard['DamageBonus']
                    elite = [x for x in gameboard if gameboard[x].playerID == self.playerID and gameboard[x].unitType == 'Elite']
                    if elite:
                        gameboard[elite[0]].damageBonus = self.damageBonus
                        
                # if ability == 'Build':
                #     target = unitChoiceObject.abilities['Build'].getTargets(unitChoiceObject.location,gameboard)
                #     if unitChoiceObject.abilities['Build'].buildChoice == 'Common':
                #         newCommon = random.choice([self.units[x] for x in self.units if x not in unitChoices and self.units[x].unitType == 'Common'])
                #         gameboard = unitChoiceObject.abilities['Build'].buildCommon(unitChoiceObject.location,target,gameboard,newCommon)
        
                #     elif unitChoiceObject.abilities['Build'].buildChoice == 'Obstacle':
                #         gameboard = unitChoiceObject.abilities['Build'].buildObstacle(unitChoiceObject.location,target,gameboard)
                    
                # call ability execute function
                if 'Target' in ability.actionLog and 'Unit' in ability.actionLog:
                    self.actionLog[self.logNumber] = unitChoiceObject.unitName + str(ability.actionLog['Unit']) + ' ' + ability.name + ' ' + str(ability.actionLog['Target'])
                elif 'Unit' in ability.actionLog:
                    self.actionLog[self.logNumber] = unitChoiceObject.unitName + str(ability.actionLog['Unit']) + ' ' + ability.name
                else:
                    self.actionLog[self.logNumber] = unitChoiceObject.unitName + ' ' + ability.name
                    
                self.logNumber = self.logNumber + 1               
                # create log of ability to be printed from action log
                
                
            # else:
                # print('Pass both')
                
            # check gameboard for eliminated units and update players' units
            eliminatedUnits = [x for x in gameboard['EliminatedUnits'].eliminatedUnits]
            for elimUnit in eliminatedUnits:
                player = [x for x in players if x.playerID == gameboard['EliminatedUnits'].eliminatedUnits[elimUnit].playerID][0]
                updateUnit = [x for x in player.units if player.units[x].name == gameboard['EliminatedUnits'].eliminatedUnits[elimUnit].name][0]
                player.units[updateUnit] = gameboard['EliminatedUnits'].eliminatedUnits[elimUnit]
            gameboard['EliminatedUnits'].eliminatedUnits = {}
            
            possibleUnits = [x for x in gameboard if gameboard[x].name == 'Unit']
            for unit in possibleUnits:
                if unit in gameboard:
                    if gameboard[unit].playerID == self.playerID:
                        # update units from gameboard to player object
                        gameboard = self.updateUnits(unit,gameboard)
                        gameboard[unit].location = unit
#                        self.classUpgrades(gameboard[unit])
                        gameboard[unit] = self.units[gameboard[unit].unitName]
                    if gameboard[unit].attributeManager.getAttributes('Health') <= 0:
                        del gameboard[unit]
        gameboard = self.endTurnEffects(gameboard)
        # print([x for x in gameboard if gameboard[x].name == 'Respawn'])
        return gameboard, players
    
    def updateUnits(self,unit,gameboard):
        self.units[gameboard[unit].unitName] = gameboard[unit]
        self.units[gameboard[unit].unitName].unrestrainedMovement = False
        self.units[gameboard[unit].unitName].location = unit
        for x in self.units[gameboard[unit].unitName].attributeManager.bonusAttributes:
            self.units[gameboard[unit].unitName].attributeManager.bonusAttributes[x] = 0
        return gameboard
    
    def respawnUnits(self,gameboard):
        # finds units not in gameboard but in player unit list
        respawnPoints = [b for c in [self.adjacentSpaces(a) for a in [x for x in gameboard if gameboard[x].name == 'Respawn' and gameboard[x].playerID == self.playerID]] for b in c]
        respawnPoints = [x for x in respawnPoints if x in self.boardLocations and x not in gameboard]
        print('available respawn points')
        print(respawnPoints)
        gameboardUnits = [gameboard[x].unitName for x in gameboard if gameboard[x].playerID == self.playerID and gameboard[x].name == 'Unit']
        
        units = [x for x in self.units if x not in gameboardUnits]
        
        if respawnPoints:
            for x in units:
                location = random.choice(respawnPoints)
                gameboard = self.addUnit(self.units[x], location , gameboard)
                respawnPoints.remove(location)
                if not respawnPoints:
                    break
                gameboard[location].direction = random.choice(self.directions)
        return gameboard
    
    def addUnit(self,unit,location,gameboard):
        # add one of your units to the board game
        gameboard[location] = unit
        gameboard[location].location = location
        gameboard[location].lineOfSightManager.setDirection(gameboard[location].direction,location,gameboard)
        gameboard[location].addBonuses()
        return gameboard
    
    def gainExp(self):
        self.experiencePoints = self.experiencePoints + 1
    
    def manageExp(self,gameboard):
        # handle leveling and returning abilities
        for unit in self.units:
            self.experiencePoints = self.units[unit].eliminatedUnits['Elite'] + self.units[unit].eliminatedUnits['Common'] + self.units[unit].eliminatedUnits['Objective']
        
        if self.experiencePoints != 0 and self.level < 6:
            self.victoryPoints = self.victoryPoints + 1
        elif self.experiencePoints == 0 and self.level < 6:
            self.experiencePoints = 1
        
        if self.experiencePoints < 3:
            for x in range(0,self.experiencePoints):
                self.levelUp()
        else:
            for x in range(0,2):
                self.levelUp()
            self.victoryPoints = self.victoryPoints + self.experiencePoints -2
        self.experiencePoints = 0
        
        # update abilities in units in gameboard
        units = [x for x in gameboard if gameboard[x].name == 'Unit' and gameboard[x].playerID == self.playerID]
        for x in units:
            gameboard[x].ablities = self.units[gameboard[x].unitName].abilities
        return gameboard
    
    def levelUp(self):
        if self.level < 10:
            self.level = self.level + 1
            for unit in self.units.values():
                unit.levelManager.level = self.level
            self.chooseAbility()
    
    def chooseAbility(self):
        ability = random.choice([x for x in self.availableAbilities()])
        abilityPair = {ability:self.availableAbilities()[ability]}
        for x in self.units:
            self.units[x].abilities = {**self.units[x].abilities,**abilityPair}
            self.units[x].abilities[ability].unitName = self.units[x].unitName
        
    def gainVictoryPoints(self,points):
        self.victoryPoints = self.victoryPoints + points
        
    def availableAbilities(self):
        return

    def refreshPoints(self,gameboard):
        unitChoices = {x:gameboard[x] for x in gameboard.keys() if gameboard[x].name == 'Unit' and gameboard[x].playerID == self.playerID}

        for unit in self.units:
            # note health, set max attributes, set current health
            health = self.units[unit].attributeManager.getAttributes('Health')
            self.units[unit].levelManager.updateAttributes()
            unitAttributes = self.units[unit].levelManager.unitAttributes
            self.units[unit].attributeManager = AttributeManager(unitAttributes)
            self.units[unit].attributeManager.setAttributes('Health',health)
        
        # update gameboard units from player object
        for unit in unitChoices:
            gameboard[unit] = self.units[gameboard[unit].unitName]
            # print(gameboard[unit].attributeManager.currentAttributes)
            # print(gameboard[unit].playerClass + gameboard[unit].playerID + gameboard[unit].unitType)
        
        return gameboard
    
    def beginningTurnEffects(self,gameboard):
        return gameboard
    
    def endTurnEffects(self,gameboard):
        if 'Pyre' in gameboard:
            for x in gameboard['Pyre']:
                x.dealDamage(gameboard)
                x.active = x.active - 1
                if x.active == 0:
                    del gameboard['Pyre'][x]
        if 'Meteor' in self.abilities:
            if self.abilities['Meteor'].active != 0:
                self.abilities['Meteor'].active = self.abilities['Meteor'].active - 1
            if self.abilities['Meteor'].active == 0:
                self.abilities['Meteor'].dealDamage(gameboard)
                        
        return gameboard
    
class Objective(GeneralUse):
    name = 'Objective'
    unitName = 'Objective'
    moveable = False
    playerID = 'None'
    playerClass = 'None'
    unitClass = 'Objective'
    unitType = 'Objective'
    armor = 0
    health = 0
    attributeManager = AttributeManager({'Health':0,'Evasion':-10,'Armor':0})
    reactionManager = ReactionManager()
    abilities = {'Pass':Pass('None')}
        
    class AttributeManager:
        
        def __init__(self,attributes):
            self.currentAttributes = attributes
        
        def getAttributes(self,attr):
            return self.currentAttributes[attr]
    
    def __init__(self,location,player):
        self.location = location
        self.playerID = player
        self.boardImage = MySprite('Objective','Objective')

    def availablePoints(self):
        return 'None'
    
    def regainNeutral(self,gameboard):
        gameboard[self.location].player = 'None'
        
    def getArmor(self,gameboard):
        return len([y for y in [x for x in self.adjacentSpaces(self.location) if x in gameboard] if gameboard[y].playerID == self.playerID])
            
    def passiveMods(self,unit,target,gameboard,combatSteps):
        return gameboard, combatSteps
    
class Respawn(GeneralUse):
    name = 'Respawn'
    unitName = 'Respawn'
    moveable = False
    
    def __init__(self,location,player):
        self.location = location
        self.playerID = player
        self.boardImage = MySprite('Respawn','Respawn')

class Obstacle(GeneralUse):
    name = 'Obstacle'
    unitName = 'Obstacle'
    unitType = 'Obstacle'
    moveable = False
    aura = 'None'

    attributeManager = AttributeManager({'Health':1,'Attack':0,'Movement':0,'Reaction':0,'Special':0,'Hit':0,'Evasion':0,'Armor':2})
    boardImage = MySprite('Obstacle','Obstacle')

    def getArmor(self,gameboard):
        return self.attributeManager.getAttributes('Armor')

class EliminatedUnitManager(GeneralUse):

    name = 'EUM'
    eliminatedUnits = {}

# need to ensure abilities are added correctly. not showing up in graphics 

# gen = GeneralUse()
# # spaces = 4
# # direction = 'n'
# # unit = (5,5)
# # gameboard = []
# # test = gen.straightLine(spaces,direction,unit,gameboard)
# gameboard = {(0,0):'StealthToken',(4,4):'StealthToken',(2,2):'StealthToken'}
# spaces = [(0,0),(4,4),(2,2),(1,1)]
# test = [gen.adjacentSpaces(x) for x in spaces]
# test2 = [x for y in [gen.adjacentSpaces(x) for x in spaces] for x in y if x in gameboard and gameboard[x] == 'StealthToken']
