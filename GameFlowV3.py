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

class Ability:
    
    def findTargets(self):
        return
    
    def execute(self,unit,gameboard,*args):
#        target = random.choice(self.findTargets())
        return

class Attack(Ability):
    name = 'Attack'
    cost = 'Attack'
    
class Movement(Ability):
    name = 'Movement'
    cost = 'Movement'

class Special(Ability):
    name = 'Special'
    cost = 'Special'

class Reaction(Ability):
    name = 'Reaction'
    cost = 'Reaction'

class AttributeManager:
    def __init__(self,currentAttributes):
        self.currentAttributes = currentAttributes
    
    def getAttributes(self,attribute):
        return self.currentAttributes.get(attribute)
    
    def changeAttributes(self,attribute,value):
        self.currentAttributes[attribute] = self.currentAttributes[attribute] + value

    def setAttributes(self,attribute,value):
        self.currentAttributes[attribute] = value
        
class Unit:
    
    abilities = {'Attack':Attack(), 'Movement':Movement(),'Special':Special(),'Reaction':Reaction()}
    
    def __init__(self,unitType,unitName):
        self.unitType = unitType
        self.unitName = unitName    
        self.options = self.createOptions()

    def setClass(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        self.levelManager = LevelManager(1,playerClass,self.unitType)
        self.unitAttributes = self.levelManager.getAttributes()
        self.attributeManager = AttributeManager(self.unitAttributes)
        
    def createOptions(self):
        # match ability costs to available points
        availablePoints = [x for x in self.AttributeManager.currentAttributes if self.AttributeManager.currentAttributes.get(x) != 0]
        options = [x for x in self.abilities.keys() if self.abilities.get(x).cost in availablePoints]
        return options # this is ability names
    
    def useAbility(self,ability):
        self.AttributeManager.changeAttributes(self.abilities.get(ability).cost,-1)
    
class Player:
    
    def __init__(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        # instantiate new units
        self.units = {'Elite':Unit('Elite','Elite1'),'Common1':Unit('Common','Common1'),\
                      'Common2':Unit('Common','Common2'),'Common3':Unit('Common','Common3'),\
                      'Common4':Unit('Common','Common4')}
        for unit in self.units:
            self.unit.setClass(self.playerClass,self.playerID)
        self.experiencePoints = 0
        self.victoryPoints = 0
        self.level = 1
        
    def turn(self,gameboard):
        # while not passed keep going
        unitChoices = {x:gameboard.get(x) for x in gameboard.keys() if gameboard.get(x).PlayerID == self.playerID}
        unitChoices['Pass'] = 'Pass'
        
        while True:
            for unit in self.units:
                unit.unitOptions = unit.createOptions()
            unitChoice = unitChoices.get(random.choice(unitChoices.keys()))
            if unitChoice == 'Pass':
                break
            unitChoice.abilities.get(random.choice(unitChoice.unitOptions)).execute()
            
            # then pick an option
        return gameboard
    
    def addUnit(self,name,location,gameboard):
        # add one of your units to the board game
        gameboard[location] = self.units.get(name)
        return gameboard
    
    def gainExp(self):
        self.experiencePoints = self.experiencePoints + 1
    
    def manageExp(self):
        # handle leveling and returning abilities
        for x in range(0,self.experiencePoints):
            self.levelUp()
        self.experiencePoints = 0
    
    def levelUp(self):
        self.level = self.level + 1
        for unit in self.units:
            unit.levelManager.level = self.level
    
class Game:
    
    directions = ['n','ne','se','s','sw','nw']
    
    def __init__(self,players):
        self.players = players
        
    def gameLoop(self):
        
        while True:
            for player in self.players:
                player.turn()
            self.endRound()
            
    def endRound(self):
        for player in self.players:
            player.manageExp()
            for unit in player.units:
                # note health, set max attributes, set current health
                health = unit.attributeManager.getAttributes('Health')
                unit.levelManager.classAttributes()
                unit.attributeManager.setAttributes('Health',health)
        
# instantiate game
Game([Player('Warrior','Player1'),Player('Assassin','Player2'), \
      Player('Mage','Player3'),Player('Engineer','Player4')])