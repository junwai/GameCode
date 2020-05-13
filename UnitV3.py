# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 22:04:10 2020

@author: bgool
"""

# Player class initiates combat
# Unit class initiates attack? or Player class?
# player tells unit to initiate attack. 
# Each unit has a combat manager object that handles abilities

import collections
import random

class Player:
    def __init__(self,unitClass,playerID):
        self.unitClass = unitClass
        self.level = 1
        self.playerID = playerID
        self.experience = 0
        self.combatManager = CombatManager()
        
    def levelUP(self,newLevel):
        self.level = newLevel

    def getLevel(self):
        return self.level
    
    def receiveEXP(self, exp):
        self.experience = self.experience + 1
    
    def initiateCombat(self,unit,target,gameboard,ability):
        # pass which ability you want to use
        gameboard = gameboard[unit].combatManager(ability,unit,target,gameboard)
        if gameboard[target].getAttributes('Health') <= 0:
            self.receiveEXP(1)
            gameboard = gameboard[target].elimination(gameboard,self)
            del gameboard[target]
        return gameboard
    
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
       
class AttributeManager:
    def __init__(self,currentAttributes):
        self.currentAttributes = currentAttributes
    
    def getAttributes(self,attribute):
        return self.currentAttributes.get(attribute)
    
    def changeAttributes(self,attribute,value):
        self.currentAttributes[attribute] = self.currentAttributes[attribute] + value


# Organization: Each ability is its own object that is passed to the appropriate manager
# For each ability, there will be a standard ability (attack,move,etc.) that is modified by the ability
# This way the program has a standard reference that is changed by each ability object
# Each unit will have an instance of the ability object that is referenced
# Each ability will exploit overridden inherited functions if available
        
class AttackManager:
    
    #Define 'Incoming' vs 'Outgoing' Damage
    
    def rollCombat(unit,target,gameboard):
        hitRoll = random.randint(1,6) + gameboard[unit].attributeManager.get('Hit')
        evasionRoll = random.randint(1,6) + gameboard[unit].attributeManager.get('Evasion')
        return {'HitRoll':hitRoll,'EvasionRoll':evasionRoll}
    
    def calculateDamage(damage,armor):
        if damage - armor < 0:
            return 0
        return damage - armor
        
    def attack(self,unit,target,gameboard,*args):
        gameboard[unit].attributeManager.changeAttributes('Attack',-1)
        passedValues = (self.rollCombat(unit,target,gameboard),gameboard,unit,target)
        # change rolls/add more stuff to hit/evasion
        
        if 'Piercing' in args:
            passedValues = passedValues + 'Piercing'
        if 'Wounding' in args:
            passedValues = passedValues + 'Success'
            
        self.assignDamage(passedValues)
        return gameboard
    
    def assignDamage(self,rollResults,unit,target,gameboard,*args):
        if 'Success' in args:
            if 'Piercing' not in args:
                damage = self.calcArmor(gameboard,gameboard[unit].attributeManager.getAttributes('Damage'),target)
                if damage < 0:
                    damage = 0
                gameboard[target].attributeManager.changeAttributes('Health',-damage)
            else:
                gameboard[target].attributeManager.changeAttributes('Health',-gameboard[unit].attributeManager.getAttributes('Damage'))                
            if gameboard[target].attributeManager.getAttributes('Health') <= 0:
                self.elimination(gameboard,)
            return gameboard
        elif 'Failure' in args:
            return gameboard
        #checkReactions
    
    def calcArmor(self,gameboard,damage,target):
        newDamage = damage - gameboard[target].get('Armor')
        return newDamage
    
    def special(self,special,classSpecial):
        self.attributeManager.changeAttributes('Special',-1)
        classSpecial.execute()
        
    def reaction(self,reaction,classReaction):
        self.attributeManager.changeAttributes('Reaction',-1)
        classReaction.execute()
    
    def elimination(self,gameboard):
        return gameboard
        
class MovementManager:
    def moveUnit(self,unit,target,gameboard,direction):
        gameboard[unit].direction = direction
        gameboard[unit].attributeManager.changeAttributes('Movement',-1)
        if target not in gameboard:
            gameboard[target] = unit
        return gameboard
    
    def changeDirectionality(gameboard,unit,direction):
        gameboard[unit].direction = direction
        return gameboard
        
class Unit:
    def __init__(self,metadata,location,direction,players):
        self.metadata = metadata
        # metadata includes playerID, unitClass, unitType, number, board location, and directionality
        self.unitID = metadata.playerID+'_'+metadata.unitType+str(metadata.number)
        self.location = location
        self.direction = direction
        self.level = self.getPlayerLevel(players)[0]
        self.levelManager = LevelManager(self.level,metadata.unitClass,metadata.unitType)
        self.unitAttributes = self.levelManager.getAttributes()
        self.attributeManager = AttributeManager(self.unitAttributes)
        self.getPlayerLevel(players)
        self.attackManager = AttackManager()
        
    def getPlayerLevel(self,players):
        return [x.level for x in players if x.playerID == self.metadata.playerID]
        
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

        
class Game:
    def __init__(self):
        self.gameboard = {}
        self._unit = collections.namedtuple('unit','playerID unitClass unitType number')
        self.players = [Player('Warrior','Player1'), Player('Assassin','Player2')]
        
    def placeUnit(self,location,drn,players):
        self.gameboard[location] = Unit(self._unit(playerID = 'Player1', unitClass= 'Warrior', unitType='Common', number = 1), location,drn,players)

    def main(self):
        self.gameboard[(0,0)] = Unit(self._unit(playerID = self.players[0].playerID, unitClass= 'Warrior', unitType='Common', number = 1),[0,0],'n',self.players)
        self.placeUnit((0,0),'n',self.players)
        
Game().main()
