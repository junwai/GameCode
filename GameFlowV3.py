# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:16:28 2020

@author: bgool
"""
#need to choose from options, picking an option calls use ability
#if called from turn, call 'turn' costs
#if called from reaction, call 'reaction' costs

# create players
# turns
# end turn
# end round
import random
import lineOfSight as LOS

class GeneralUse:

    directions = ['n','ne','se','s','sw','nw']
    
    def adjacentSpaces(self):
        x = self.location[0]
        y = self.location[1]        
        
        return [(x,y+1),(x+1,y+1),(x+1,y),(x,y-1),(x-1,y-1),(x-1,y)]
        
    def adjacentSpacesDir(self):
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
        return switch.get(self.direction,'error')            
           
    def dealDamage(self,unit,target,gameboard,damage):
        if type(gameboard[target]).__name__ == 'Objective' or type(gameboard[target]).__name__ == 'Obstacle':
            damage = damage - gameboard[target].getArmor(gameboard)
        gameboard[target].attributeManager.changeAttributes('Health',-damage)
        if gameboard[target].attributeManager.getAttributes('Health') <= 0:
            gameboard[unit].eliminateUnit(gameboard[target].unitType,gameboard[target].playerID)

            reaction = gameboard[unit].checkReaction(unit,target,gameboard,['EliminateUnit'])            
            gameboard = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard)

        return gameboard
        
class StealthToken(GeneralUse):
    
    # this is the token object
    name = 'StealthToken'
    
    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location
    
    def stealthTokenEffect(self,unit,gameboard):
        if 'BlastTrap' in [x for x in gameboard if gameboard[x].playerID == self.playerID and gameboard[x].unitType == 'Elite'][0].abilities and gameboard[unit].playerID != self.playerID:
            if random.randint(1,6) > gameboard[unit].attributeManager.getAttribute('Evasion'):
                self.dealDamage(self.location,unit,gameboard,5)
        return gameboard

class Ability(GeneralUse):
    
    state = 'None'
    use = 'All'
    
    def __init__(self,unitName,player):
        self.unitName = unitName
        self.player = player
    
    def getTargets(self,unit,gameboard,*args):
        return unit
    
    def getLOSTargets(self,unit,gameboard,*args):
        if 'Range' in args:
            spaces = self.getAOETargets(args['Range'],unit)
        else:
            spaces = self.getAOETargets(gameboard[unit].unitRange,unit)

        LOS = gameboard[unit].lineOfSight['Clear']+gameboard[unit].lineOfSight['Partial']
        potentialTargets = list(set(LOS).intersection(set(spaces)))
        return potentialTargets
    
    def getMeleeTargets(self,unit,gameboard):
        spaces = gameboard[unit].adjacentSpacesDir()
        return [spaces[6],spaces[1],spaces[2]]
    
    def getAOETargets(self,unitRange,unitLocation):
        
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
        potentialTargets = self.getTargets(unit,gameboard,args)
        target = random.choice(potentialTargets)
        gameboard = self.abilityEffect(unit,target,gameboard)
        gameboard[unit].reactionManager.setState('None')
        gameboard[target].reactionManager.setState('None')
        return gameboard

    def combat(self,unit,target,gameboard,mods):
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
                'ResultingDamage': 0,
                'newPosition': False,
                'AttackMods': mods
        }
        
        gameboard, combatSteps = gameboard[unit].rollModifiers(unit,target,gameboard,combatSteps)
        gameboard, combatSteps = gameboard[target].rollModifiers(unit,target,gameboard,combatSteps)
        
        for x in mods: 
            if x in combatSteps:
                combatSteps[x] = combatSteps[x] + mods[x]
                
        # add additional hit modifiers
        reaction = gameboard[unit].checkReaction(unit,target,gameboard,['AddHit'])
        gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)
        
        combatSteps['HitResult'] = combatSteps['CalcHit'] + combatSteps['AddHit']

        # add additional evasion modifiers
        reaction = gameboard[target].checkReaction(unit,target,gameboard,['AddEvasion'])
        gameboard,combatSteps = gameboard[target].abilities[reaction].execute(unit,gameboard)
        
        if combatSteps['newPosition']:
            unit = combatSteps['newPosition']
            combatSteps['newPosition'] = False
                    
        gameboard, combatSteps = gameboard[unit].passiveMods(unit,target,gameboard,combatSteps)
        gameboard, combatSteps = gameboard[target].passiveMods(unit,target,gameboard,combatSteps)
        
        if 'Wounding' in combatSteps['AttackMods']:
            combatSteps['CombatResult'] = 'Hit'
            
        if combatSteps['HitResults'] > combatSteps['EvasionResults']:
            combatSteps['CombatResult'] = 'Hit'
            
        if 'Piercing' in mods:
            combatSteps['Armor'] = 0

        if combatSteps['CombatResult'] == 'Evasion':
            if combatSteps['EvasionResult'] >= combatSteps['HitResult'] + 3:
                reaction = gameboard[target].checkReaction(target,unit,gameboard,['GreaterEvasion'])
                gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)
            else:
                reaction = gameboard[target].checkReaction(target,unit,gameboard,['Evasion','Any'])
                gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)                
            reaction = gameboard[unit].checkReaction(unit,target,gameboard,['MissedMeleeAttack','Any'])
            gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)
                                    
        if combatSteps['CombatResult'] == 'Hit':
            combatSteps['ResultingDamage'] = combatSteps['Damage'] + combatSteps['AddDamage'] - combatSteps['Armor']
            if combatSteps['ResultingDamage'] < 0:
                combatSteps['ResultingDamage'] = 0
            elif 'Assassin' in mods:
                elite = [x for x in gameboard if gameboard[unit].playerID == x.playerID and x.unitType == 'Elite']
                gameboard[elite].damageBonus = gameboard[elite].damagebonus + mods['Assassin']
            reaction = gameboard[target].checkReaction(target,unit,gameboard,['TakeDamage'])
            gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)

            gameboard = self.dealDamage(unit,target,gameboard,combatSteps['ResultingDamage'])
            
        if combatSteps['CombatResult'] == 'Hit' and 'Wounding' not in 'AttackMods':
            reaction = gameboard[target].checkReaction(target,unit,gameboard,['LostEvasion'])
            gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)

        gameboard, combatSteps = gameboard[unit].passiveMods(unit,target,gameboard,combatSteps)
        gameboard, combatSteps = gameboard[target].passiveMods(unit,target,gameboard,combatSteps)
        # ask if you want to react -> yes? ->  call function from inside here
        return gameboard
        
    def updatePosition(self,combatSteps):
        if combatSteps['newPosition']:
            unit = combatSteps['newPosition']
            combatSteps['newPosition'] = False
        return unit,combatSteps
    
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
    name = 'CaptureRespawn'
    cost = {'Passive':['Passive']}
    def abilityEffect(self,unit,target,gameboard):
        
        if target in gameboard[unit].adjacentSpaces() and hasattr(gameboard[target],'player'):
            if gameboard[target].player == 'None':
                gameboard[target].player = gameboard[unit].player
                gameboard[unit].attributeManager.changeAttributes(gameboard[unit].captureCost,-1)
        return gameboard
    
class Attack(Ability):
    name = 'Attack'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].changeAttributes('Attack',-1)
        return self.combat(unit,target,gameboard,gameboard[unit].createCombatModifiers({'unit':unit,'target':target,'gameboard':gameboard})) 
        
    def getTargets(self,unit,gameboard,*args):
        return list(set(self.getLOSTargets(unit,gameboard,args)).intersection(set(self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location))))
    
class Movement(Ability):
    
    name = 'Movement'
    cost = {'Turn':['Movement']}
    
    def availableMovement(self,unit,gameboard,origin,*args):
        respawns = [x for x in gameboard if type(x).__name__ == 'Respawn']
        respawnSpaces = [a for b in [gameboard[unit].adjacentSpaces(x) for x in respawns if x.player == gameboard[unit].player] for a in b]
        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard or type(gameboard[x]).__name__ == 'StealthToken' or x == origin]
        if 'unrestrained' in args:
            spaces = self.adjacentSpaces(unit)
        if set(spaces) & set(respawnSpaces):
            spaces = list(set(spaces + respawnSpaces))
        for x in spaces: 
            if x[0] < 0 or x[0] > 20 or x[1] < 0 or x[1] > 20:
                spaces.remove[x]
        spaces = spaces + gameboard[unit].addMovementSpaces(self,unit,gameboard,spaces)
            
        return spaces
    
    def abilityEffect(self,unit,target,gameboard,*args):
        # args is a manually input distance
        args = args[0]
        # pick the number of spaces you would like to move
        if not args:
            numberOfSpaces = random.choice([x for x in range(1,gameboard[unit].attributeManager.getAttributes('Movement')+1)])
        elif 'Distance' in args:
            numberOfSpaces = args['Distance']
        # pick the path you would like to move through
        
        target = random.choice(self.availableMovement(unit,gameboard,unit,args))
        for x in range(1,numberOfSpaces-2):
            target = target + random.choice(self.availableMovement(target[x],gameboard,unit,args))
        
        playerUnit = gameboard[unit]
        distance = 0        
        # execute number of movements
        for x in target:
            if x not in gameboard or x == unit:
                lastOpenSpace = x
                distance = distance + 1  
                        
        for x in gameboard:
            if type(x).__name__ == 'Unit':
                gameboard[x].checkReaction(x,gameboard,['Any'])
        
        if 'Cost' in args:
            if args['Cost'] != 'Passive':
                gameboard[unit].attributeManager.changeAttributes(args['Cost'],-distance)
        else:            
            gameboard[unit].attributeManager.changeAttributes('Movement',-distance)
        
        for x in range(0,len(target)+1):        
            if x <= distance:
                gameboard = gameboard[unit].movementEffects(unit,target[x],gameboard)
                if type(gameboard[target[x]]).__name__ == 'StealthToken':
                    gameboard[target[x]].stealthTokenEffect(unit,gameboard)
                    del gameboard[target[x]]
                gameboard[target[x]].direction = random.choice(self.directions)
                gameboard[target[x]].location = x
                gameboard[target[x]].getLineOfSight(gameboard)
            unit = target[x]
        gameboard[lastOpenSpace] = playerUnit
        
        return gameboard,lastOpenSpace

class Reorient(Ability):
    name = 'Reorient'
    cost = {'Passive':['Passive']}
    state = 'ReceiveDamage'
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].direction = random.choice([x for x in ['n','ne','se','s','sw','nw'] if x != gameboard[unit].direction])
        return gameboard
    
class Perception(Ability):
    name = 'Perception'
    cost = {'Reaction':['Reaction']}
    state = 'Any'
    
    def abilityEffect(self,unit,target,gameboard):
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
    cost = {'Passive':['Passive']}
    state = 'GreaterEvasion'
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        gameboard[unit].attributeManager.changeAttributes('Movement',1)
        gameboard, newpos = gameboard[unit].abilities.get('Movement').execute(unit,target,gameboard,1)
        if 'Jaunt' in gameboard[target].abilities:
            gameboard[unit] = StealthToken(gameboard[target].unitName,gameboard[target].playerID)
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

class ReactionManager(GeneralUse):
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
        return random.choice(self.availableReactions(gameboard[unit]))
        
    def availableReactions(self,unit):
        # find available reactions with corresponding state
        reactions = ['Pass'] + [x.name for x in unit.abilities.values() if 'Reaction' in x.cost and set(x.cost['Reaction']).issubset(set(unit.availablePoints())) and self.state in x.state]
        return reactions #reaction names
    
    def multipleReactionPoints(self,unit,gameboard):
        maxReactions = gameboard[unit].attributeManager.getAttributes('Reaction')
        return random.choice([x for x in range(1,maxReactions)])
        
class AttributeManager(GeneralUse):
    def __init__(self,currentAttributes):
        self.currentAttributes = currentAttributes
    
    def getAttributes(self,attribute):
        return self.currentAttributes.get(attribute)
    
    def changeAttributes(self,attribute,value):
        if attribute != 'Passive':
            self.currentAttributes[attribute] = self.currentAttributes[attribute] + value

    def setAttributes(self,attribute,value):
        self.currentAttributes[attribute] = value + self.bonusAttributes[attribute]
    
    # bonus attributes set at the end of your turn
    def setBonusAttributes(self,attribute,value):
        self.bonusAttributes[attribute] = self.bonusAttributes[attribute] + value

class Unit(GeneralUse):
    
    reactionManager = ReactionManager()
    lineOfSightManager = LOS.LineOfSight()
    bonusAttributes = {'Attack':0,'Movement':0,'Reaction':0,'Special':0}
    eliminatedUnits = {'Elite':0, 'Common':0, 'Objective':0}
    permBonusAttr = {'Health':0,'Attack':0,'Movement':0,'Special':0,'Reaction':0,'Damage':0,'Evasion':0,'Hit':0,'Armor':0}
    unitRange = 1
    
    def __init__(self,unitType,unitName):
        self.unitType = unitType
        self.unitName = unitName
        self.direction = 'n'
    
    def setClass(self,playerClass,playerID,captureCost):
        self.playerClass = playerClass
        self.playerID = playerID
        self.levelManager = LevelManager(1,playerClass,self.unitType)
        self.unitAttributes = self.levelManager.getAttributes()
        self.attributeManager = AttributeManager(self.unitAttributes)
        self.captureCost = captureCost
        self.abilities = {'Attack':Attack(self.unitName,playerID), 'Movement':Movement(self.unitName,playerID), 'Reorient':Reorient(self.unitName,playerID), 'Perception':Perception(self.unitName,playerID),
                 'AccurateStrike': AccurateStrike(self.unitName,playerID),'Avoid':Avoid(self.unitName,playerID),'PurposefulDodge':PurposefulDodge(self.unitName,playerID),'RedirectedStrike':RedirectedStrike(self.unitName,playerID)}
    
    def addBonuses(self):
        for x in self.permBonusAttr:
            self.attributeManager.changeAttributes(x,self.permBonusAttr[x])
        self.Range = self.Range + self.rangeBonus
    
    def createOptions(self):
        # match ability costs to available points
        # excludes passives since it matches available points to cost
        options = [x.name for x in self.abilities.values() if 'Turn' in x.cost and set(x.cost['Turn']).issubset(set(self.availablePoints()))]
        return options # this is ability names
    
    def availablePoints(self):
        return [x for x in self.attributeManager.currentAttributes if self.attributeManager.currentAttributes.get(x) != 0]
    
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
    
    def addMovementSpaces(self,unit,gameboard,spaces):
        return spaces
    
    def eliminateUnit(self,unit,playerID):
        if self.playerID != playerID:
            self.eliminatedUnits[unit] = self.eliminatedUnits[unit] + 1
        
    def classUpgrades(self,unit):
        return 
    
    def changePermanentUpgrade(self,attribute,value):
        self.permBonusAttr[attribute] = self.permBonusAttr[attribute] + value
        
    def statEffect(self,unitObj):
        return unitObj
    
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
            self.units[unit].setClass(self.playerClass,self.playerID,self.captureCost)
        
    def turn(self,gameboard,players):
        # while not passed keep going

        unitChoices = {x:gameboard.get(x) for x in gameboard.keys() if type(gameboard[x]).__name__ == 'Unit' and gameboard.get(x).playerID == self.playerID}
        unitChoices['Pass'] = 'Pass'
        
        while True:
            for unit in self.units:
                self.units[unit].unitOptions = self.units[unit].createOptions()
            unitChoice = unitChoices.get(random.choice(list(unitChoices.keys())))
            if unitChoice == 'Pass':
                for x in self.units:
                    for attr in ['Attack','Movement','Reaction','Special']:
                        gameboard[x].attributeManager.setBonusAttributes[attr,0]
                break
            # execute ability
            if unitChoice.unitOptions:
                unitChoice.abilities.get(random.choice(unitChoice.unitOptions)).execute(unit,gameboard)
            for unit in gameboard:
                if type(gameboard[unit]).__name__ == 'Unit': 
                    if gameboard[unit].playerID == self.playerID:
                        self.updateUnits(gameboard[unit])
                        self.classUpgrades(gameboard[unit])
                        gameboard[unit] = self.units[gameboard[unit].unitName]
                    if gameboard[unit].attributeManager.getAttributes('Health') <= 0:
                        del gameboard[unit]
        
        return gameboard
    
    def updateUnits(self,unit):
        self.units[unit.unitName] = unit
    
    def respawnUnits(self,gameboard):
        # finds units not in gameboard but in player unit list
        respawnPoints = [b for c in [gameboard[a].adjacentSpaces() for a in [x for x in gameboard if type(gameboard[x]).__name__ == 'Respawn' and gameboard[x].playerID == self.playerID]] for b in c]
        units = list(set(self.units.keys()).difference(set([gameboard[x] for x in gameboard if gameboard[x].playerID == self.playerID])))
        for x in units:
            location = random.choice(respawnPoints)
            gameboard = self.addUnit(self.units[x], location , gameboard)
            gameboard[location].direction = random.choice(self.directions)
            respawnPoints.remove(location)
    
    def addUnit(self,unit,location,gameboard):
        # add one of your units to the board game
        gameboard[location] = unit
        gameboard[location].location = location
        gameboard[location].lineOfSight = gameboard[location].getLineOfSight(gameboard)
        gameboard[location].addBonuses()
        return gameboard
    
    def gainExp(self):
        self.experiencePoints = self.experiencePoints + 1
    
    def manageExp(self):
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
    
    def levelUp(self):
        if self.level < 10:
            self.level = self.level + 1
            for unit in self.units.values():
                unit.levelManager.level = self.level
#            self.chooseAbility(random.choice(self.availableAbilities()))
            
    def chooseAbility(self,ability):
        self.abilities = {**ability,**self.abilities}
        return
    
    def gainVictoryPoints(self,points):
        self.victoryPoints = self.victoryPoints + points
        
    def availableAbilities(self):
        return
    
class Objective(GeneralUse):
    
    playerID = 'None'
    armor = 0
    health = 0
    
    def __init__(self,location,player):
        self.location = location
        self.playerID = player
    
    def regainNeutral(self,gameboard):
        gameboard[self.location].player = 'None'
        
    def getArmor(self,gameboard):
        return len([x for x in self.adjacentSpaces(self.location) if gameboard[x].player == self.player])
        
    
class Respawn(GeneralUse):
    
    def __init__(self,location,player):
        self.location = location
        self.playerID = player

class Obstacle(GeneralUse):
    armor = 2
    
    def getArmor(self):
        return self.armor

class Game:
    turnCounter = 0
    directions = ['n','ne','se','s','sw','nw']
    gameboard = {(3,3):Respawn((3,3),'Player3'), (7,3):Objective((7,3),'Player4'), (11,3):Respawn((11,3),'None'), (15,3):Objective((15,3),'None'), (19,3):Respawn((19,3),'None'),\
                 (3,7):Objective((3,7),'None'), (7,7):Respawn((7,7),'Player1'), (11,7):Objective((11,7),'Player2'), (15,7):Respawn((15,7),'None'), (19,7):Objective((19,7),'None'),\
                 (3,11):Respawn((3,11),'Player3'), (7,11):Objective((7,11),'Player4'), (11,11):Respawn((11,11),'Player2'), (15,11):Objective((15,11),'None'), (19,11):Respawn((19,11),'None'),\
                 (3,15):Objective((3,15),'None'), (7,15):Respawn((7,15),'Player1'), (11,15):Objective((11,15),'Player2'), (15,15):Respawn((15,15),'None'), (19,15):Objective((19,15),'None'),\
                 (3,19):Respawn((3,19),'None'), (7,19):Objective((7,19),'None'), (11,19):Respawn((11,19),'Player4'), (15,19):Objective((15,19),'None'), (19,19):Respawn((19,19),'None')\
                 }
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
                print('end')
                break
                
    def endRound(self):
        for player in self.players:
            player.manageExp()
            player.gainVictoryPoints(len([x for x in self.gameboard if type(self.gameboard[x]).__name__ == 'Objective' and self.gameboard[x].playerID == player.playerID]))
            for unit in player.units.values():
                # note health, set max attributes, set current health
                health = unit.attributeManager.getAttributes('Health')
                unit.levelManager.classAttributes()
                unit.attributeManager.setAttributes('Health',health)
        
# instantiate game
game = Game([Player('Warrior','Player1'),Player('Assassin','Player2'), \
      Player('Mage','Player3'),Player('Engineer','Player4')])
game.gameLoop()

# Gameflow: Players take a turn(), which initiates all options for unit selection (including Pass), 
# then all options for unitOptions(). Select a random option in unit selection, then random option for
# the unit. For each ability, need to return a random target