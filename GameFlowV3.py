# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:16:28 2020

@author: bgool
"""

# create players
# turns
# end turn
# end round
import random

class GeneralUse:

    directions = ['n','ne','se','s','sw','nw']

    def adjacentSquares(self):
        #[1,2,3,4,5,6]
        x = self.location[0]
        y = self.location[1]
        switch = {
            'n': {1:(x,y+1),2:(x+1,y+1),3:(x+1,y),4:(x,y-1),5:(x-1,y-1),6:(x-1,y)},
            'ne': {1:(x+1,y+1),2:(x+1,y),3:(x,y-1),4:(x-1,y-1),5:(x-1,y),6:(x,y+1)},
            'se': {1:(x-1,y-1),2:(x-1,y),3:(x,y+1),4:(x+1,y+1),5:(x+1,y),6:(x,y-1)},
            's': {1:(x,y-1),2:(x-1,y-1),3:(x-1,y),4:(x,y+1),5:(x+1,y+1),6:(x+1,y)},
            'sw': {1:(x+1,y),2:(x,y-1),3:(x-1,y-1),4:(x-1,y),5:(x,y+1),6:(x+1,y+1)},
            'nw': {1:(x-1,y),2:(x,y+1),3:(x+1,y+1),4:(x+1,y),5:(x,y-1),6:(x-1,y-1)}
        }
        switch.get(self.direction,'error')            
        
    def dealDamage(self,unit,target,gameboard,damage):
        if type(gameboard[target]).__name__ == 'Objective':
            damage = damage - gameboard[target].getArmor(gameboard)
        gameboard[unit].checkReaction(unit,target,gameboard,['ReceiveDamage','Any'])        
        gameboard[target].attributeManager.changeAttributes('Health',-damage)            
        return gameboard

class Ability(GeneralUse):
    
    state = 'None'
    
    def getTargets(self,unitRange,unitLocation):
        
        for i in range(0,unitRange):
            spaces = list(set([a for b in [self.adjacentSpaces(x) for x in self.adjacentSpaces(unitLocation)] for a in b]))
        # if x and y are changing in different directions (+/-) it is 2 spaces
        # if x and y are changing in the same direction (+/+) it is 1 space
        # if only x or y are changing it is 1 space
        return spaces
    
    def adjacentSpaces(location):
        (x,y) = location
        return [(x,y+1),(x+1,y+1),(x+1,y),(x,y-1),(x-1,y-1),(x-1,y)]
    
    def execute(self,unit,gameboard,*args):
        target = random.choice(self.getTargets(unit.unitRange,unit.location))
        gameboard = self.abilityEffect(unit,target,gameboard)
        gameboard[unit].reactionManager.setState('None')
        gameboard[target].reactionManager.setState('None')
        return

    def combat(self,unit,target,gameboard,*args):
        hit = random.randint(1,6) + gameboard[unit].getAttributes('Hit')
        
        reaction = gameboard[unit].checkReaction(unit,target,gameboard,['Hit'])
        if reaction == True:
            hit = hit + 1
        evasion = random.randint(1,6) + gameboard[target].getAttributes('Evasion')
        if hit > evasion or 'Wounding' in args:
            damage = gameboard[unit].attributeManager.getAttributes('Damage')
            if 'Piercing' in args:
                gameboard = self.dealDamage(damage)
            else:
                gameboard = self.dealDamage(damage-gameboard[target].attributeManager.getAttributes('Armor'))
        if hit > evasion and 'Wounding' not in args:
            gameboard[target].checkReaction(target,unit,gameboard,['LostEvasion'])
        if evasion >= hit + 3:
            gameboard[target].checkReaction(target,unit,gameboard,['GreaterEvasion'])
        if evasion >= hit:
            gameboard[unit].checkReaction(unit,target,gameboard,['MissedMeleeAttack','Any'])
            gameboard[target].checkReaction(target,unit,gameboard,['Any'])                        
        return gameboard    
        
    def abilityEffect(self,unit,target,gameboard):
        return gameboard

class CaptureObjective(Ability):
    
    def abilityEffect(self,unit,target,gameboard):
        if target in gameboard[unit].adjacentSpaces() and hasattr(gameboard[target],'player'):
            if gameboard[target].player == 'None':
                gameboard[target].player = gameboard[unit].player
                gameboard[unit].attributeManager.changeAttributes(gameboard[unit].captureCost,-1)
        return gameboard

class CaptureRespawn(Ability):

    def abilityEffect(self,unit,target,gameboard):
        
        if target in gameboard[unit].adjacentSpaces() and hasattr(gameboard[target],'player'):
            if gameboard[target].player == 'None':
                gameboard[target].player = gameboard[unit].player
                gameboard[unit].attributeManager.changeAttributes(gameboard[unit].captureCost,-1)
        return gameboard
    
class Attack(Ability):
    name = 'Attack'
    cost = 'Attack' 
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].changeAttributes('Attack',-1)
        return self.combat(unit,target,gameboard) 
        
    
class Movement(Ability):
    
    name = 'Movement'
    cost = 'Movement'
    
    def availableMovement(self,unit,gameboard,*args):
        respawns = [x for x in gameboard if type(x).__name__ == 'Respawn']
        respawnSpaces = [a for b in [gameboard[unit].adjacentSpaces(x) for x in respawns if x.player == gameboard[unit].player] for a in b]
        spaces = [x for x in gameboard[unit].adjacentSpaces(gameboard[unit].location) if x not in gameboard]
        if 'unrestrained' in args:
            spaces = self.adjacentSpaces(gameboard[unit].location)
        if set(spaces) & set(respawnSpaces):
            spaces = list(set(spaces + respawnSpaces))
        return spaces
    
    def abilityEffect(self,unit,target,gameboard,*args):
        # pick the number of spaces you would like to move
        numberOfSpaces = random.choice([x for x in range(1,gameboard[unit].attributeManager.getAttributes('Movement')+1)])
        # pick the path you would like to move through
        target = random.choice(self.availableMovement(unit,gameboard,args))
        for x in range(1,numberOfSpaces-2):
            target = target + random.choice(self.availableMovement(target[x],gameboard,args))
        
        # take out unit from gameboard temporarily
        playerUnit = gameboard[unit]
        del gameboard[unit]
        distance = 0
        lastOpenSpace = unit
        # execute number of movements
        for x in target:
            if x not in gameboard:
                lastOpenSpace = x
                distance = distance + 1  
                        
        for x in gameboard:
            if type(x).__name__ == 'Unit':
                gameboard[x].checkReaction(x,gameboard,['Any'])
                
        gameboard[unit].attributeManager.changeAttributes('Movement',-distance)
        gameboard[lastOpenSpace] = playerUnit
        return gameboard

class Reorient(Ability):
    name = 'Reorient'
    cost = 'Passive'
    state = 'ReceiveDamage'
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].direction = random.choice([x for x in ['n','ne','se','s','sw','nw'] if x != gameboard[unit].direction])
        return gameboard
    
class Perception(Ability):
    name = 'Perception'
    cost = 'Reaction'
    state = 'Any'
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].direction = random.choice([x for x in ['n','ne','se','s','sw','nw'] if x != gameboard[unit].direction])
        return gameboard
    
class AccurateStrike(Ability):
    name = 'AccurateStrike'
    cost = 'Reaction'
    state = 'Hit'
    
    def abilityEffect(*args):
        return True
    
class Avoid(Ability):
    name = 'Avoid'
    cost = ('Reaction','Movement')
    state = 'LostEvasion'
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].abilities.get('Movement').execute()
        return gameboard
    
class PurposefulDodge(Ability):
    name = 'PurposefulDodge'
    cost = 'Passive'
    state = 'GreaterEvasion'
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].abilities.get('Movement').execute()
        return gameboard
    
class RedirectedStrike(Ability):
    name = 'RedirectedStrike'
    cost = 'Reaction'
    state = 'MissedMeleeAttack'
    
    def abilityEffect(self,unit,target,gameboard):
        damage = gameboard[unit].reactionManager.multipleReactionPoints(unit,gameboard)
        self.combat(unit,target,gameboard)
        gameboard[unit].abilities.get('Attack').execute()
        return gameboard
    
class Pass(Ability):
    
    name = 'Pass'
    def abilityEffect(self,unit,target,gameboard):
        return

class LevelManager:
    def __init__(self,level,unitClass,unitType):
        self.unitClass = unitClass
        self.level = level
        self.unitType = unitType
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

class ReactionManager:
    # give state to reaction manager
    # search for reactions with given trigger state
    # ask user if they want to react
    # if yes trigger reaction
    
    def setState(self,state):
        # give state to reaction manager
        self.state = state
        
    def checkReaction(self,unit,target,gameboard,states):
        # ask if user wants to do a reaction
        # do the reaction (call ability effect)
        self.setState(states)
        random.choice(self.availableReactions(gameboard[unit])).abilityEffect(unit,target,gameboard)
        
    def availableReactions(self,unit):
        # find available reactions with corresponding state
        return [x for x in unit.abilities if self.state in x.state] + [Pass()]
    
    def multipleReactionPoints(self,unit,gameboard):
        maxReactions = gameboard[unit].attributeManager.getAttributes('Reaction')
        return random.choice([x for x in range(1,maxReactions)])
        
class AttributeManager:
    def __init__(self,currentAttributes):
        self.currentAttributes = currentAttributes
    
    def getAttributes(self,attribute):
        return self.currentAttributes.get(attribute)
    
    def changeAttributes(self,attribute,value):
        if attribute != 'Passive':
            self.currentAttributes[attribute] = self.currentAttributes[attribute] + value

    def setAttributes(self,attribute,value):
        self.currentAttributes[attribute] = value
        
class Unit(GeneralUse):
    
    abilities = {'Attack':Attack(), 'Movement':Movement()}
    reactionManager = ReactionManager()
    
    def __init__(self,unitType,unitName):
        self.unitType = unitType
        self.unitName = unitName    
        self.options = self.createOptions()
        
    def setClass(self,playerClass,playerID,captureCost):
        self.playerClass = playerClass
        self.playerID = playerID
        self.levelManager = LevelManager(1,playerClass,self.unitType)
        self.unitAttributes = self.levelManager.getAttributes()
        self.attributeManager = AttributeManager(self.unitAttributes)
        self.captureCost = captureCost
        
    def createOptions(self):
        # match ability costs to available points
        availablePoints = [x for x in self.attributeManager.currentAttributes if self.attributeManager.currentAttributes.get(x) != 0]
        options = [x for a in self.abilities.keys() for x in a if self.abilities.get(x).cost in availablePoints]
        return options # this is ability names
    
    def useAbility(self,ability):
        [self.attributeManager.changeAttributes(self.abilities.get(ability).cost,-1) for x in self.abilities.get(ability).cost]
    
    def getDistance(self,target):
        if (target[0] - self.location[0] >= 0 and target[1] - self.location[1] <= 0) or (target[0] - self.location[0] <= 0 and target[1] - self.location[1] >= 0):
            return abs(target[1]-self.location[1])+abs(target[0]-self.location[0])

        if (target[0] - self.location[0] >= 0 and target[1] - self.location[1] >= 0) or (target[0] - self.location[0] <= 0 and target[1] - self.location[1] <= 0):
            return max(abs(target[1]-self.location[1]),abs(target[0]-self.location[0]))
    
class Player(GeneralUse):
    
    abilities = []
    victoryPoints = 0
    level = 1
    experiencePoints = 0
    captureCost = 'Attack'
    
    def __init__(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        # instantiate new units
        self.units = {'Elite':Unit('Elite','Elite1'),'Common1':Unit('Common','Common1'),\
                      'Common2':Unit('Common','Common2'),'Common3':Unit('Common','Common3'),\
                      'Common4':Unit('Common','Common4')}
        for unit in self.units:
            unit.setClass(self.playerClass,self.playerID,self.captureCost)
        
    def turn(self,gameboard,players):
        # while not passed keep going

        unitChoices = {x:gameboard.get(x) for x in gameboard.keys() if gameboard.get(x).PlayerID == self.playerID}
        unitChoices['Pass'] = 'Pass'
        
        while True:
            for unit in self.units:
                unit.unitOptions = unit.createOptions()
            unitChoice = unitChoices.get(random.choice(unitChoices.keys()))
            # add feature that updates units in player
            if unitChoice == 'Pass':
                break
            # execute ability
            unitChoice.abilities.get(random.choice(unitChoice.unitOptions)).execute()
            for unit in gameboard:
                if type(unit).__name__ == 'Unit' and unit.playerID == self.playerID:
                    if unit.attributeManager.getAttributes('Health') <= 0:
                        self.updateUnits(unit)
                        del gameboard[unit]
            # then pick an option
        return gameboard
    
    def updateUnits(self,unit):
        self.units[unit.unitName] = unit
    
    def respawnUnits(self,name,location,direction,gameboard):
        # need to create objectives and respawns
        respawnPoints = [b for c in [self.adjacentSpaces(a) for a in [x for x in gameboard if type(x).__name__ == 'Respawn' and x.player == self.player]] for b in c]
        units = list(set(self.units.keys()).difference(set([gameboard[x] for x in gameboard if gameboard[x].player == self.player])))
        for x in units:
            location = random.choice(respawnPoints)
            gameboard = self.addUnit(self.units[x], location , gameboard)
            gameboard[location].direction = random.choice(self.directions)
            respawnPoints.remove(location)
    
    def addUnit(self,unit,location,gameboard):
        # add one of your units to the board game
        gameboard[location] = unit
        return gameboard
    
    def gainExp(self):
        self.experiencePoints = self.experiencePoints + 1
    
    def manageExp(self):
        # handle leveling and returning abilities
        
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
    
    def levelUp(self):
        if self.level < 10:
            self.level = self.level + 1
            for unit in self.units:
                unit.levelManager.level = self.level
            self.chooseAbility(random.choice(self.availableAbilities()))
            
    def chooseAbility(self,ability):
        self.abilities = {**ability,**self.abilities}
        return
    
    def gainVictoryPoints(self,points):
        self.victoryPoints = self.victoryPoints + points
        
    def availableAbilities(self):
        return
    
    
class Objective(GeneralUse):
    
    player = 'None'
    armor = 0
    health = 0
    
    def __init__(self,location):
        self.location = location
    
    def regainNeutral(self,gameboard):
        gameboard[self.location].player = 'None'
        
    def getArmor(self,gameboard):
        return len([x for x in self.adjacentSquares if gameboard[x].player == self.player])
        
    
class Respawn(GeneralUse):
    
    owner = 'None'
    def __init__(self,location):
        self.location = location

class Game:
    turnCounter = 0
    directions = ['n','ne','se','s','sw','nw']
    gameboard = {(0,0):Objective((0,0)),(2,2):Respawn((2,2))}
    def __init__(self,players):
        self.players = players
        
    def gameLoop(self):
        
        while True:
            for player in self.players:
                player.respawnUnits(self.gameboard)
                self.gameboard = player.turn(self.gameboard,self.players)
                self.turnCounter = self.turnCounter + 1

            self.endRound()
            if self.turnCounter == 10:
                    break
                
                
    def endRound(self):
        for player in self.players:
            player.manageExp()
            player.addPoints(len([x for x in self.gameboard if type(self.gameboard[x]).__name__ == 'Objective' and self.gameboard[x].player == player]))
            for unit in player.units:
                # note health, set max attributes, set current health
                health = unit.attributeManager.getAttributes('Health')
                unit.levelManager.classAttributes()
                unit.attributeManager.setAttributes('Health',health)
        
# instantiate game
Game([Player('Warrior','Player1'),Player('Assassin','Player2'), \
      Player('Mage','Player3'),Player('Engineer','Player4')])
    
# Gameflow: Players take a turn(), which initiates all options for unit selection (including Pass), 
# then all options for unitOptions(). Select a random option in unit selection, then random option for
# the unit. For each ability, need to return a random target