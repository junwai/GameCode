# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:05:23 2020

@author: bgool
"""

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
import math
import lineOfSight as LOS

class GeneralUse:
    name = 'General'
    unitType = 'NoType'
    playerID = 'NoPlayer'
    abilities = {}
    directions = ['n','ne','se','s','sw','nw']
    
    oppositeDirections = {'n':'s','ne':'sw','se':'nw','s':'n','sw':'ne','nw':'se'}
    
    def allSpaces(self):
        return [(x,y) for x in range(0,10) for y in range(0,10)]
    
    def adjacentSpaces(self,loc):
        x = loc[0]
        y = loc[1]
        return [(x,y+1),(x+1,y+1),(x+1,y),(x,y-1),(x-1,y-1),(x-1,y)]
    
    def LOSDirections(direction):
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
        if 'Location' not in args[0]:
            x = self.location[0]
            y = self.location[1]
        else:
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
        if 'Direction' not in args[0]:
            return switch.get(self.direction)
        else:
            return switch.get(args[0]['Direction'])
    
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
        if type(gameboard[target]).__name__ == 'Objective' or type(gameboard[target]).__name__ == 'Obstacle':
            damage = damage - gameboard[target].getArmor(gameboard)
        
        reaction = gameboard[unit].reactionManager.checkReaction(target,unit,gameboard,['GiveDamage'])
        gameboard, damage = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,damage)
            
        reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['TakeDamage'])
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
            if nextInLine not in gameboard:
                line = line + nextInLine
        return line
    
    def forcedMovement(self,spaces,direction,unit,target,gameboard,*args):
        # Unit is the unit forcing the movement
        # Target is the forced unit
        movedSpaces = [self.location]
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
                    gameboard[movedSpaces[x-1]] = gameboard[target]
                    del gameboard[target]
                    # At this point the moved unit is at movedSpaces[x-1]
                    blockedSpace = movedSpaces[x]
            if maxSpace > 0:
                if 'Shockwave' in gameboard[movedSpaces[x-1]].abilities:
                    for x in gameboard[movedSpaces[x-1]].getAOETargets(1,movedSpaces[x-1]):
                        gameboard = self.forcedMovementDamage(spaces-maxSpace,blockedSpace,movedSpaces[x-1],x,gameboard,direction)
                else:    
                    gameboard = self.forcedMovementDamage(spaces-maxSpace,blockedSpace,movedSpaces[x-1],movedSpaces[x],gameboard,direction)

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
        
        if type(gameboard[blockedSpace]).__name__ == 'Objective' or type(gameboard[target]).__name__ == 'Obstacle':
            damage = damage - gameboard[target].getArmor(gameboard)
        gameboard[blockedSpace].attributeManager.changeAttributes('Health',-damage)
        
        if gameboard[target].attributeManager.getAttributes('Health') <= 0:
            gameboard[unit].eliminateUnit(gameboard[target].unitType,gameboard[target].playerID)
            
        if target in gameboard and blockedSpaces > 0 and 'Avalanche' in gameboard[unit].abilities:
            self.forcedMovement(blockedSpaces,direction,unit,target,gameboard)
            
        return gameboard

    def getAOETargets(self, unitRange, unitLocation):
        for i in range(0,unitRange):
            spaces = list(set([a for b in [self.adjacentSpaces(x) for x in self.adjacentSpaces(unitLocation)] for a in b]))
        # if x and y are changing in different directions (+/-) it is 2 spaces
        # if x and y are changing in the same direction (+/+) it is 1 space
        # if only x or y are changing it is 1 space
        return spaces

class Ability(GeneralUse):
    
    state = 'None'
    use = 'All'
    unitType = 'None'
    
    def __init__(self,unitName,playerID):
        self.unitName = unitName
        self.playerID = playerID
    
    def initAbility(self, gameboard):
        return gameboard
    
    def getTargets(self,unit,gameboard):
        return [unit]
    
    def getLOSTargets(self,unit,gameboard,*args):
        args = args[0]
        if 'Range' in args:
            spaces = self.getAOETargets(args['Range'],unit)
        else:
            spaces = self.getAOETargets(gameboard[unit].unitRange,unit)

        LOS = gameboard[unit].lineOfSightManager.lineOfSight['Clear']+gameboard[unit].lineOfSightManager.lineOfSight['Partial']
        potentialTargets = [x for x in list(set(LOS).intersection(set(spaces))) if x in gameboard]
        potentialTargets = [x for x in potentialTargets if gameboard[x].name != 'Respawn']
        return potentialTargets
    
    def getMeleeTargets(self,unit,gameboard):
        spaces = gameboard[unit].adjacentSpacesDir()
        return [spaces[6],spaces[1],spaces[2]]
    
    def execute(self,unit,gameboard,*args):
        potentialTargets = self.getTargets(unit,gameboard)
        if potentialTargets:
            target = random.choice(potentialTargets)
            gameboard = self.abilityEffect(unit,target,gameboard)
            if target in gameboard:
                gameboard[target].reactionManager.setState('None')
        return gameboard

    def combat(self,unit,target,gameboard,*mods):
        gameboard[unit].setLastAction('Combat')
        
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

        for x in mods: 
            if x in combatSteps:
                combatSteps[x] = combatSteps[x] + mods[x]

        if 'Armory' in gameboard[unit].abilities:
            if [x for x in gameboard[unit].abilities['Armory'].getAOETargets(gameboard[unit].abilities['Armory']._range,unit) if type(gameboard[x]).__name__ == 'Armory']:
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + 1
                combatSteps['AddHit'] = combatSteps['AddHit'] + 1
        
        if 'Bunker' in gameboard[target].abilities:
            if [x for x in gameboard[unit].abilities['Bunker'].getAOETargets(gameboard[unit].abilities['Bunker']._range,unit) if type(gameboard[x]).__name__ == 'Bunker']:
                combatSteps['Armor'] = combatSteps['Armor'] + 1
                if 'Piercing' in combatSteps['AttackMods']:
                    del combatSteps['AttackMods']['Piercing']        

        if 'UAVTower' in gameboard[unit].abilities:
            if [x for x in gameboard[unit].abilities['UAVTower'].getAOETargets(gameboard[unit].abilities['UAVTower']._range,unit) if type(gameboard[x]).__name__ == 'UAVTower']:
                combatSteps['AddHit'] = combatSteps['AddHit'] + 2           
        
        if gameboard[unit].playerClass == 'Warrior':
            gameboard,combatSteps = gameboard[unit].hitDiceMods(unit,target,gameboard,combatSteps)
        
        if gameboard[target].playerClass == 'Warrior':
            gameboard,combatSteps = gameboard[target].evasionDiceMods(unit,target,gameboard,combatSteps)
        
        # target reaction from melee
        if self.getDistance(unit,target) == 1:
            reaction = gameboard[unit].reactionManager.checkReaction(unit,target,gameboard,['TargetedMelee'])
            gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)
        
        # add additional hit modifiers
        reaction = gameboard[unit].reactionManager.checkReaction(unit,target,gameboard,['AddHit'])
        gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)
        
        combatSteps['HitResult'] = combatSteps['CalcHit'] + combatSteps['AddHit']
            
        # add additional evasion modifiers
        reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['AddEvasion'])
        gameboard,combatSteps = gameboard[target].abilities[reaction].abilityEffect(target,unit,gameboard,combatSteps)
        
        if combatSteps['newPosition']:
            unit = combatSteps['newPosition']
            combatSteps['newPosition'] = False
                    
        gameboard, combatSteps = gameboard[unit].passiveMods(unit,target,gameboard,combatSteps)
        gameboard, combatSteps = gameboard[target].passiveMods(unit,target,gameboard,combatSteps)

        if 'UAVTower' in gameboard[target].abilities:
            if [x for x in gameboard[target].abilities['UAVTower'].getAOETargets(gameboard[target].abilities['UAVTower']._range,target) if gameboard[x].name == 'UAVTower']:
                combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + 2
                if 'Wounding' in combatSteps['AttackMods']:
                    del combatSteps['AttackMods']['Wounding']
                    combatSteps['HitResult'] = 6
        
        if 'Wounding' in combatSteps['AttackMods']:
            combatSteps['CombatResult'] = 'Hit'
            
        if combatSteps['HitResult'] > combatSteps['EvasionResult']:
            combatSteps['CombatResult'] = 'Hit'

        if 'Piercing' in combatSteps['AttackMods']:
            if gameboard[target].unitClass == 'Engineer':
                if 'Tank' in gameboard[target].unitBlueprints or 'Dreadnought' in gameboard[target].unitBlueprints:
                    del combatSteps['AttackMods']['Piercing']
            combatSteps['Armor'] = 0

        if combatSteps['CombatResult'] == 'Evasion':
            if combatSteps['EvasionResult'] >= combatSteps['HitResult'] + 3:
                reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['GreaterEvasion'])
                gameboard, combatSteps = gameboard[target].abilities[reaction].abilityEffect(target,unit,gameboard,combatSteps)
            else:
                reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['Evasion','Any'])
                gameboard, combatSteps = gameboard[target].abilities[reaction].abilityEffect(target,unit,gameboard,combatSteps)                
            reaction = gameboard[unit].reactionManager.checkReaction(unit,target,gameboard,['MissedMeleeAttack','Any'])
            gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)

        if 'ArcaneShield' in gameboard[target].abilities:
            if gameboard[target].abilities['ArcaneShield'].stacks > 0:
                gameboard[target].abilities['ArcaneShield'].useStack()
                combatSteps['ResultingDamage'] = 0 
 
        if combatSteps['CombatResult'] == 'Hit' and 'Wounding' not in 'AttackMods':
            reaction = gameboard[target].reactionManager.checkReaction(target,unit,gameboard,['LostEvasion'])
            gameboard, combatSteps = gameboard[unit].abilities[reaction].abilityEffect(unit,target,gameboard,combatSteps)                                  

        gameboard, combatSteps = gameboard[unit].passiveMods(unit,target,gameboard,combatSteps)
        gameboard, combatSteps = gameboard[target].passiveMods(unit,target,gameboard,combatSteps)

        if combatSteps['CombatResult'] == 'Hit':
            if 'Axe' in combatSteps['AttackMods']:
                gameboard[unit].attributeManager.bonusAttributes['Damage'] = gameboard[unit].attributeManager.bonusAttributes['Damage'] + 1
            combatSteps['ResultingDamage'] = combatSteps['Damage'] + combatSteps['AddDamage'] - combatSteps['Armor']
            if combatSteps['ResultingDamage'] < 0:
                combatSteps['ResultingDamage'] = 0
            elif 'Assassin' in mods:
                elite = [x for x in gameboard if gameboard[unit].playerID == x.playerID and x.unitType == 'Elite']
                gameboard[elite].damageBonus = gameboard[elite].damagebonus + mods['Assassin']
                        
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

class CaptureObjective(Ability):
    name = 'CaptureObjective'
    cost = {'Turn':'Passive'}
    
    def abilityEffect(self,unit,target,gameboard):
        if target in gameboard[unit].adjacentSpaces() and hasattr(gameboard[target],'player'):
            if gameboard[target].player == 'None':
                gameboard[target].player = gameboard[unit].player
                gameboard[unit].attributeManager.changeAttributes(gameboard[unit].captureCost,-1)
        return gameboard

class CaptureRespawn(Ability):
    name = 'CaptureRespawn'
    cost = {'Turn':['Passive']}
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
        respawnSpaces = [a for b in [gameboard[unit].adjacentSpaces(x) for x in respawns if gameboard[x].playerID == gameboard[unit].playerID] for a in b]
          
        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard or gameboard[x].name == 'StealthToken' or x == origin]
        if effects != None:
            if 'Unrestrained' in effects:
                spaces = self.adjacentSpaces(unit)
        if set(spaces) & set(respawnSpaces):
            spaces = list(set(spaces + respawnSpaces))
            
        for x in spaces: 
            if x[0] < 0 or x[0] > 20 or x[1] < 0 or x[1] > 20:
                spaces.remove(x)
        spaces = spaces + gameboard[unit].addMovementSpaces(unit,gameboard,spaces)
            
        return spaces
    
    def abilityEffect(self,unit,target,gameboard,*args):
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
            target = [random.choice(self.availableMovement(unit,gameboard,unit,effects))]
            for x in range(1,numberOfSpaces-2):
                target = target + [random.choice(self.availableMovement(target[x],gameboard,unit,args))]
        else:
            target = [gameboard[unit].adjacentSpacesDir(args['Direction'])]
            for x in range(1,numberOfSpaces-2):
                target = target + [self.adjacentSpacesDir({'Direction':args['Direction'],'Location':target[x-1]})]
            
        playerUnit = gameboard[unit]
        distance = 0
        reducedCost = 0
        lastOpenSpace = unit
        # execute number of movements
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
                if [x for x in self.adjacentSpaces(x) if type(gameboard[x]).__name__ == 'Unit' and gameboard[x].playerID != gameboard[unit].playerID]:
                    reducedCost = reducedCost = reducedCost + 1
            if 'Sneak' in gameboard[unit].abilities:
                enemies = [x for x in gameboard if type(gameboard[x]).__name__ == 'Unit' and gameboard[x].playerID != gameboard[unit].playerID]
                seen = False
                for y in enemies: 
                    if target in y.lineOfSight['Clear']:
                        seen = True
                if not seen:
                    reducedCost = reducedCost = reducedCost + 1
                    
        for x in gameboard:
            if type(x).__name__ == 'Unit':
                gameboard[x].checkReaction(x,gameboard,['Any'])
        
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
    cost = {'Passive':['Passive']}
    state = 'GreaterEvasion'
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        spaces = 1
        if 'TimeDilation' in gameboard[target].abilities:
            spaces = 3
        gameboard[unit].attributeManager.changeAttributes('Movement',spaces)
        gameboard, newpos = gameboard[unit].abilities['Movement'].execute(unit,target,gameboard,spaces)
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
        
class AttributeManager(GeneralUse):
    
    bonusAttributes = {'Health':0,'Attack':0,'Movement':0,'Reaction':0,'Special':0,'Hit':0,'Evasion':0,'Armor':0}
    permBonusAttr = {'Health':0,'Attack':0,'Movement':0,'Special':0,'Reaction':0,'Damage':0,'Evasion':0,'Hit':0,'Armor':0}
    
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
        self.currentAttributes[attribute] = self.bonusAttributes[attribute] + value

    def changePermanentUpgrade(self,attribute,value):
        self.permBonusAttr[attribute] = self.permBonusAttr[attribute] + value
    

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
        self.unitAttributes = self.levelManager.getAttributes()
        self.maxHealth = self.unitAttributes['Health']
        self.attributeManager = AttributeManager(self.unitAttributes)
        self.captureCost = captureCost
        self.baseAbilities = {'Attack':Attack(self.name,playerID), 'Movement':Movement(self.name,playerID), 'Reorient':Reorient(self.name,playerID), 'Perception':Perception(self.name,playerID),
                 'AccurateStrike': AccurateStrike(self.name,playerID),'Avoid':Avoid(self.name,playerID),'PurposefulDodge':PurposefulDodge(self.name,playerID),'RedirectedStrike':RedirectedStrike(self.name,playerID),
                 'Pass': Pass(self.name,playerID)}
        self.abilities = self.baseAbilities
        
    def addBonuses(self):
        for x in self.attributeManager.permBonusAttr:
            self.attributeManager.changeAttributes(x,self.attributeManager.permBonusAttr[x])
        self.unitRange = self.unitRange + self.rangeBonus
    
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
    
    def eliminateUnit(self,unitType,unit,playerID,gameboard):
        if self.playerID != playerID:
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
        
        gameboard = self.beginningTurnEffects(gameboard)
        while True:
            unitChoices = {x:gameboard[x] for x in gameboard.keys() if gameboard[x].name == 'Unit' and gameboard.get(x).playerID == self.playerID}
            unitChoices['Pass'] = 'Pass'
            for unit in self.units:
                if self.units[unit].location not in gameboard:
                    self.units[unit].location = 'None'
                if self.units[unit].location != 'None':
                    self.units[unit].unitOptions = self.units[unit].createOptions()
                    if [x for x in self.getAOETargets(4,self.units[unit].location) if x in gameboard and gameboard[x].name == 'EMPTower']:
                        for x in self.units[unit].unitOptions:
                            abil = self.units[unit].abilities[self.units[unit].unitOptions[x]]
                            if 'Turn' in abil.cost:
                                if abil.cost['Turn'] == 'Special':
                                    del self.units[unit].unitOptions[x]
            # unit choice key (x,y)
            unitChoiceKey = random.choice(list(unitChoices.keys()))
            # unit object 
            unitChoiceObject = unitChoices.get(unitChoiceKey)
            if unitChoiceObject == 'Pass':
                for x in self.units:
                    for attr in ['Attack','Movement','Reaction','Special']:
                        self.units[x].attributeManager.setBonusAttributes(attr,0)
                        if self.units[x].location in gameboard:
                            gameboard[self.units[x].location].attributeManager.setBonusAttributes(attr,0)
                break
            # execute ability
            elif unitChoiceObject.unitOptions:
                ability = unitChoiceObject.abilities.get(random.choice(unitChoiceObject.unitOptions))
                print(ability)
                # subtract cost from unit points
                if ability != 'Movement':
                    for x in ability.cost['Turn']:
                        gameboard[unitChoiceKey].attributeManager.changeAttributes(x,-1)
                # call ability execute function
                gameboard = ability.execute(unitChoiceKey,gameboard)
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
                        self.updateUnits(gameboard[unit])
#                        self.classUpgrades(gameboard[unit])
                        gameboard[unit] = self.units[gameboard[unit].name]
                    if gameboard[unit].attributeManager.getAttributes('Health') <= 0:
                        del gameboard[unit]
        gameboard = self.endTurnEffects(gameboard)
        return gameboard, players
    
    def updateUnits(self,unit):
        self.units[unit.name] = unit
        self.units[unit.name].unrestrainedMovement = False
        for x in self.units[unit.name].attributeManager.bonusAttributes:
            self.units[unit.name].attributeManager.bonusAttributes[x] = 0
    
    def respawnUnits(self,gameboard):
        # finds units not in gameboard but in player unit list
        respawnPoints = [b for c in [self.adjacentSpaces(a) for a in [x for x in gameboard if gameboard[x].name == 'Respawn' and gameboard[x].playerID == self.playerID]] for b in c]
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
        gameboard[location].lineOfSightManager.setDirection(gameboard[location].direction,location,gameboard)
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
    moveable = False
    playerID = 'None'
    playerClass = 'None'
    armor = 0
    health = 0
    attributeManager = AttributeManager({'Health':0,'Evasion':-10,'Armor':0})
    reactionManager = ReactionManager()
    abilities = {'Pass':Pass('None','None')}
    
    
    class AttributeManager:
        
        def __init__(self,attributes):
            self.currentAttributes = attributes
        
        def getAttributes(self,attr):
            return self.currentAttributes[attr]
    
    def __init__(self,location,player):
        self.location = location
        self.playerID = player
    
    def regainNeutral(self,gameboard):
        gameboard[self.location].player = 'None'
        
    def getArmor(self,gameboard):
        return len([x for x in self.adjacentSpaces(self.location) if gameboard[x].player == self.player])
        
    
class Respawn(GeneralUse):
    name = 'Respawn'
    moveable = False
    
    def __init__(self,location,player):
        self.location = location
        self.playerID = player

class Obstacle(GeneralUse):
    name = 'Obstacle'
    unitType = 'Obstacle'
    moveable = False
    aura = 'None'

    attributeManager = AttributeManager({'Health':1,'Attack':0,'Movement':0,'Reaction':0,'Special':0,'Hit':0,'Evasion':0,'Armor':2})

    def getArmor(self):
        return self.attributeManager.getAttributes('Armor')

class EliminatedUnitManager(GeneralUse):

    name = 'EUM'
    eliminatedUnits = {}


class Game:
    turnCounter = 0
    directions = ['n','ne','se','s','sw','nw']
    gameboard = {(3,3):Respawn((3,3),'Player3'), (7,3):Objective((7,3),'Player4'), (11,3):Respawn((11,3),'None'), (15,3):Objective((15,3),'None'), (19,3):Respawn((19,3),'None'),\
                 (3,7):Objective((3,7),'None'), (7,7):Respawn((7,7),'Player1'), (11,7):Objective((11,7),'Player2'), (15,7):Respawn((15,7),'None'), (19,7):Objective((19,7),'None'),\
                 (3,11):Respawn((3,11),'Player3'), (7,11):Objective((7,11),'Player4'), (11,11):Respawn((11,11),'Player2'), (15,11):Objective((15,11),'None'), (19,11):Respawn((19,11),'None'),\
                 (3,15):Objective((3,15),'None'), (7,15):Respawn((7,15),'Player1'), (11,15):Objective((11,15),'Player2'), (15,15):Respawn((15,15),'None'), (19,15):Objective((19,15),'None'),\
                 (3,19):Respawn((3,19),'None'), (7,19):Objective((7,19),'None'), (11,19):Respawn((11,19),'Player4'), (15,19):Objective((15,19),'None'), (19,19):Respawn((19,19),'None'),\
                 'EliminatedUnits':EliminatedUnitManager()}
    def __init__(self,players):
        self.players = players
        
    def gameLoop(self):
        
        for player in self.players:
            player.respawnUnits(self.gameboard)            
        
        while True:
            for player in self.players:
                print(self.turnCounter)
                player.respawnUnits(self.gameboard)
                self.gameboard, self.players = player.turn(self.gameboard,self.players)
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

class StealthToken(GeneralUse):
    
    # this is the token object
    name = 'StealthToken'
    attributeManager = AttributeManager({'Health':0,'Attack':0,'Movement':0,'Reaction':0,'Special':0,'Hit':0,'Evasion':0,'Armor':0})
    
    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location
    
    def stealthTokenEffect(self,unit,gameboard):
        if 'BlastTrap' in [x for x in gameboard if gameboard[x].playerID == self.playerID and gameboard[x].unitType == 'Elite'][0].abilities and gameboard[unit].playerID != self.playerID:
            if random.randint(1,6) > gameboard[unit].attributeManager.getAttributes('Evasion'):
                self.dealDamage(self.location,unit,gameboard,5)
        return gameboard

class PlaceStealthToken(Ability):
    name = 'StealthToken'
    cost = 'Movement'
    
    def getTargets(self,unit,gameboard):
        return random.choice([x for x in self.adjacentSpaces(unit) if x not in gameboard])
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = StealthToken(self.playerID,target)
        return gameboard
        

class AssassinAvoid(Ability):
    name = 'Avoid'
    cost = {'Reaction':['Reaction','Movement']}
    state = 'LostEvasion'
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Movement',1)
        if 'HeightenedSenses' in gameboard[unit].abilities:
            move = 2
        else:
            move = 1
        gameboard = gameboard[unit].abilities.get('Movement').execute(unit,target,gameboard,move)
        return gameboard       
    
class AssassinAttack(Ability):
    name = 'Attack'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].changeAttributes('Attack',-1)
        mods = gameboard[unit].createCombatModifiers({'unit':unit,'target':target,'gameboard':gameboard})
        if mods:
            return self.combat(unit,target,gameboard,mods)
        return self.combat(unit,target,gameboard) 
        
    def getTargets(self,unit,gameboard,*args):
        if 'PsychicScream' in gameboard[unit].abilities:
            if gameboard[unit].abilities['PsychicScream'].active:
                spaces = self.getAOETargets(1,unit)
        else:
            spaces = list(set(self.getLOSTargets(unit,gameboard,args)).intersection(set(self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location))))
    
        return spaces    
    
class AssassinUnit(Unit):
    
    def setClass(self,playerClass,playerID,captureCost):
        self.playerClass = playerClass
        self.playerID = playerID
        self.levelManager = LevelManager(1,playerClass,self.unitType)
        self.unitAttributes = self.levelManager.getAttributes()
        self.attributeManager = AttributeManager(self.unitAttributes)
        self.captureCost = captureCost
        self.abilities = {'Pass':Pass(self.unitName,playerID),'Attack':Attack(self.unitName,playerID), 'Movement':Movement(self.unitName,playerID), 'Reorient':Reorient(self.unitName,playerID), 'Perception':Perception(self.unitName,playerID),
                 'AccurateStrike': AccurateStrike(self.unitName,playerID),'Avoid':AssassinAvoid(self.unitName,playerID),'PurposefulDodge':PurposefulDodge(self.unitName,playerID),'RedirectedStrike':RedirectedStrike(self.unitName,playerID),
                 'StealthToken':PlaceStealthToken(self.unitName,playerID),'Efficiency':Efficiency(self.unitName,playerID),'Notoriety':Notoriety(self.unitName,playerID),
                 'Stealth':Stealth(self.unitName,playerID),'Jaunt':Jaunt(self.unitName,playerID)}
    
    def createCombatModifiers(self,mods):
        target = mods['target']
        gameboard = mods['gameboard']
        mods = {}
        if self.unitType == 'Common' and 'Efficiency' in self.abilities:
            mods['Piercing'] = True
            mods['Assassin'] = 1
        if self.unitType == 'Elite' and 'Interrogate' in self.abilities:
            mods['Assassin'] = 2
        notoriety = gameboard[target].level - self.level
        if notoriety > 0:
            mods['AddHit'] = mods['AddHit'] + notoriety
        return mods
    
    def rollModifiers(self,unit,target,gameboard,combatRolls):
        if unit == self.location:
            if 'Cripple' in self.abilities:
                if combatRolls['CalcHit'] >= 5:
                    combatRolls['AddEvasion'] = 0
            if 'CriticalStrike' in self.abilities:
                if combatRolls['CalcHit'] >= 5:
                    combatRolls['AddDamage'] = combatRolls['AddDamage'] + gameboard[unit].attributeManager.getAttributes('Evasion')
            if 'Infect' in self.abilities:
                if combatRolls['CalcHit'] <= 2:
                    gameboard[unit].dealDamage(unit,target,gameboard,1)
                    
        if target == self.location:
            if 'Virulency' in self.abilities:
                if combatRolls['CalcHit'] <= 2:
                    gameboard[target].dealDamage(target,unit,gameboard,2)
            
        return gameboard,combatRolls
        
    def passiveMods(self,unit,target,gameboard,combatSteps):
        if self.location == unit:
            if 'KidneyShot' in self.abilities:
                if self.location in [gameboard[target].adjacentSpacesDir()[3],gameboard[target].adjacentSpacesDir()[5]]:
                    combatSteps['AddDamage'] = combatSteps['AddDamage'] + 1
            if 'BackStab' in self.abilities:
                if self.location in [gameboard[target].adjacentSpacesDir()[3],gameboard[target].adjacentSpacesDir()[5]]:
                    combatSteps['AddHit'] = combatSteps['AddHit'] + 2
            if 'FamiliarTerritory' in self.abilities:
                spaces = self.abilities['FamiliarTerritory'].getAdjacentSpaces(target)
                if [x for x in spaces if type(gameboard[x]).__type__ == 'Objective']:
                    combatSteps['AddHit'] = combatSteps['AddHit'] + 3
                    combatSteps['AddDamage'] = combatSteps['AddDamage'] + 2
            if 'Killshot' in self.abilities:
                if gameboard[target].attributeManager.getAttribute('Health')/2 < self.attributeManager.getAttribute('Damage') + self.damageBonus:
                    combatSteps['AttackMods'].append('Wounding')
            if 'Phantom' in self.abilities and 'Evasion' in combatSteps['CombatResult'] and self.unitType == 'Elite':
                self.damageBonus = self.damageBonus + 1
            if [y for y in [x for x in self.adjacentSpaces(self.location) if x in gameboard] if 'Lethargy' in gameboard[y].abilities and gameboard[y].playerID != gameboard[unit].playerID] and 'Wounding' in combatSteps['AttackMods']:
                combatSteps['AttackMods'].remove('Wounding')
            if [y for y in [x for x in self.adjacentSpaces(self.location) if x in gameboard] if 'Dyskinesia' in gameboard[y].abilities and gameboard[y].playerID != gameboard[unit].playerID]:
                disadv = random.randint(1,6)
                if combatSteps['CalcHit'] > disadv:
                    combatSteps['CalcHit'] = disadv
            if [y for y in [x for x in gameboard[target].adjacentSpaces(self.location) if x in gameboard] if 'Mark' in gameboard[y].abilities and gameboard[y].playerID == self.playerID and self.unitType == 'Elite']:
                combatSteps['AddEvasion'] = combatSteps['AddEvasion'] - 2
            if 'Sniper' in self.abilities and gameboard[unit].getDistance(target) > 1:
                combatSteps['AddHit'] = combatSteps['AddHit'] + 4
                self.lineOfSight['Clear'] = self.lineOfSight['Clear'] + self.lineOfSight['Partial']
                self.lineOfSight['Partial'] = []
            if 'Communications' in self.abilities:
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + len([x for x in gameboard if gameboard[x].playerID == self.playerID and gameboard[x].unitType == 'Common' and target in gameboard[x].lineOfSight['Clear']])
            if 'Vantage' in self.abilities:
                stealthtokens = [x for x in gameboard if type(gameboard[x]).__name__ == 'StealthToken']
                blocked = False
                for x in stealthtokens:
                    los = LOS.getBlockedPartialLineOfSight(gameboard[unit].direction,unit)
                    if target in los[x]['Blocked'] or target in los[x]['Partial']:
                        blocked = True
                        break
                if blocked:
                    combatSteps['AddHit'] = combatSteps['AddHit'] + 3
                    combatSteps['AddDamage'] = combatSteps['AddDamage'] + 3
            if 'Eviscerate' in self.abilities:
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + len([x for x in self.adjacentSpaces() if gameboard[x].name == 'StealthToken' and gameboard[x].playerID == self.playerID])
            if 'Portent' in self.abilities:
                if self.abilities['Portent'].active:
                    combatSteps['CalcEvasion'] = 2
                    self.abilities['Portent'].active = False
            
        if self.location == target:
            if 'Meld' in self.abilities:
                combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + len([x for x in self.adjacentSpaces() if gameboard[x].name == 'StealthToken'])
            if 'Wounding' in combatSteps['AttackMods']:
                if 'Blur' in self.abilities:
                    combatSteps['AttackMods'].remove('Wounding')
                    combatSteps['CalcHit'] = 0
                    combatSteps['AddHit'] = 7
            if 'Anonymity' in self.abilities:
                spaces = len([x for x in gameboard[target].adjacentSpaces() if type(gameboard[x]).__name__ == 'Unit' and gameboard[x].playerID != gameboard[unit].playerID])
                combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + spaces
            if [y for y in [x for x in self.adjacentSpaces(self.location) if x in gameboard] if 'Dyskinesia' in gameboard[y].abilities and gameboard[y].playerID != gameboard[unit].playerID]:
                disadv = random.randint(1,6)
                if combatSteps['CalcEvasion'] > disadv:
                    combatSteps['CalcEvasion'] = disadv            
            if 'Portent' in self.abilities:
                if self.abilities['Portent'].active:
                    combatSteps['CalcHit'] = 2
                    self.abilities['Portent'].active = False
            if [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]:
                elites = [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]
                for x in elites:
                    if gameboard[x].getDistance(target) <= gameboard[x].attunement['Water']:
                        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] - 2        
        return gameboard,combatSteps
    
    def movementEffects(self,unit,target,gameboard):
        if 'ShadowStep' in self.abilities:
            token = random.choice([x for x in gameboard[unit].adjacentSpaces(unit) if type(gameboard[x]).__name__ == 'StealthToken'])
            gameboard[random.choice([x for x in gameboard[unit].abilities['ShadowStep'].adjacentSpaces(token) if x not in gameboard])] = gameboard[token]
            del gameboard[token]
        return gameboard
        
    def addMovementSpaces(self,unit,gameboard,spaces):
        if 'Reaper' in self.abilities:
            if [x for x in [type(x).__name__ for x in gameboard[unit].adjacentSpaces()] if x in ['Objective','Respawn']]:
                spaces = [x for x in gameboard if type(gameboard[x]).__name__ in ['Objective','Respawn']]
        return spaces

# Tier 0
class Efficiency(Ability):
    name = 'Efficiency'
    cost = {'Passive':['Passive']}
    
class Notoriety(Ability):
    name = 'Notoriety'
    cost = {'Passive':['Passive']}
    
class Stealth(Ability):
    name = 'Stealth'
    cost = {'Turn':['Movement']}
    
    def abilityEffect(self,unit,target,gameboard):
        if 'EffectiveCover' not in gameboard[unit].abilities:
            place = random.choice([x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard])
            gameboard[place] = StealthToken(gameboard[unit].playerID,place)
            return gameboard
        else:
            place = random.choice([x for x in gameboard[unit].getAOETargets(2,unit) if x not in gameboard])
            gameboard[place] = StealthToken(gameboard[unit].playerID,place)
            return gameboard

class Jaunt(Ability):
    name = 'Jaunt'
    cost = {'Turn':['Passive']}
    
# Tier 1: 2+
class QuickStep(Ability):
    name = 'Quickstep'
    cost = {'Reaction':['Reaction']}
    state = ['AddEvasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + 1
        gameboard,newpos = gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,{'Distance':1})
        combatSteps['newPosition'] = newpos
        return gameboard,combatSteps
    
class KidneyShot(Ability):
    name = 'KidneyShot'
    cost = {'Passive':['Passive']}
            
class Backstab(Ability):
    name = 'Backstab'
    cost = {'Passive':['Passive']}
            
class Shift(Ability):
    name = 'Shift'
    cost = {'Reaction':['Passive']}
    state = ['Evasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        gameboard,newpos = gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,{'Distance':1,'Cost':'Passive'})
        combatSteps['newPosition'] = newpos
        return gameboard,combatSteps
    
class Rope(Ability):
    name = 'Rope'
    cost = {'Turn':['Special'],'Reaction':['Reaction']}
    state = ['Any']
    
    def getTargets(self,unit,gameboard,*args):
        return self.LOSTargets(unit,gameboard,args)
    
    def getLOSTargets(self,unit,gameboard,*args):
        spaces = [x for x in self.getAOETargets(3,unit) if type(gameboard[x]).__name__ == 'Unit']
        LOS = gameboard[unit].lineOfSight['Clear']+gameboard[unit].lineOfSight['Partial']
        potentialTargets = list(set(LOS).intersection(set(spaces)))
        return potentialTargets
    
    def abilityEffect(self,unit,target,gameboard):
        targetSpace = random.choice([x for x in gameboard[target].adjacentSpaces() if gameboard[unit].getDistance(x) < gameboard[unit].getDistance(target)])
        gameboard[targetSpace] = gameboard[target]
        gameboard[targetSpace].changeLocation(targetSpace)
        del gameboard[target]
        return gameboard
    
class Sabotage(Ability):
    name = 'Sabotage'
    cost = {'Turn':['Attack']}
    
    def getTargets(self,unit,gameboard,*args):
        return [x for x in self.getMeleeTargets(unit,gameboard) if type(gameboard[x]) in ['Obstacle','Objective']]
        
    def abilityEffect(self,unit,target,gameboard):
        if type(gameboard[target]).__name__ == 'Objective':
            gameboard = self.dealDamage(unit,target,gameboard,3)
        if type(gameboard[target]).__name__ == 'Obstacle':
            gameboard = self.dealDamage(unit,target,gameboard,4)
        return gameboard
    
class HeightenedSenses(Ability):
    name = 'HeightenedSenses'
    cost = {'Passive':['Passive']}
            
class Undercover(Ability):
    name = 'Undercover'
    cost = {'Turn':['Movement']}
    
    def getTargets(unit,gameboard):
        return [x for x in gameboard if type(gameboard[x]).__name__ == 'StealthToken']
    
    def abilityEffect(self,unit,target,gameboard):
        moveStealthToken = random.choice([x for x in self.adjacentSpaces(target) if x not in gameboard])
        gameboard[moveStealthToken] = gameboard[target]
        del gameboard[target]
        return gameboard
        
class Interrogate(Ability):
    name = 'Interrogate'
    cost = {'Passive':['Passive']}
            
class Afterimage(Ability):
    name = 'Afterimage'
    cost = {'Turn':['Movement'],'Reaction':['Reaction']}
    state = ['Evasion']
    
    def getTargets(self,unit,gameboard):
        return [x for x in list(set(self.getAOETargets(3,unit)).intersection(set(gameboard))) if gameboard[x].name == 'StealthToken']
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = gameboard[unit]
        gameboard[target].location = target
        del gameboard[unit]
        return gameboard
        
class DeepStrike(Ability):
    name = 'DeepStrike'
    cost = {'Turn':['Movement']}
    
    def getTargets(self,unit,gameboard):
        spaces = [x for x in gameboard if type(gameboard[x]).__name__ == 'Respawn' or gameboard[x].name == 'Objective']
        return [x for x in list(set([y for y in [self.adjacentSpaces(x) for x in spaces]])) if gameboard[x].name == 'StealthToken']
    
    def abilityEffect(self,unit,target,gameboard):  
        gameboard[target] = gameboard[unit]
        del gameboard[unit]
        return gameboard
        
class Meld(Ability):
    name = 'Meld'
    cost = {'Turn':['Passive']}
            
class Cripple(Ability):
    name = 'Cripple'
    cost = {'Turn':['Passive']}
            
# Tier 2: 5+

class SurpriseAttack(Ability):
    name = 'SurpriseAttack'
    cost = {'Turn':['Passive']}
    
class AssassinCounter(Ability):
    name = 'Counter'
    cost = {'Reaction':['Reaction']}
    state = ['Evasion']
    
    def abilityEffect(self,unit,target,gameboard):
        if target in self.getMeleeTargets(target,gameboard):
            return self.combat(unit,target,gameboard,{'AddHit':3})
        else:
            return gameboard
    
class Blur(Ability):
    name = 'Blur'
    cost = {'Reaction':['Reaction']}
    state = ['PreEvasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        advantage = random.randint(1,6)
        if advantage > combatSteps['CalcHit']:
            combatSteps['CalcHit'] < advantage
            combatSteps['CalcHit'] = advantage
        return gameboard,combatSteps
    
class FamiliarTerritory(Ability):
    name = 'FamiliarTerritory'
    cost = {'Passive':'Passive'}
            
class CriticalStrike(Ability):
    name = 'CriticalStrike'
    cost = {'Passive':'Passive'}
    
class BodyDouble(Ability):
    name = 'BodyDouble'
    cost = {'Turn':['Special'],'Reaction':['Reaction']}
    state = ['']
    use = 'Elite'
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == gameboard[unit].playerID]
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        temp = gameboard[unit]
        gameboard[unit] = gameboard[target]
        gameboard[target] = temp
        return gameboard,combatSteps
    
class Shadowstep(Ability):
    name = 'Shadowstep'
    cost = {'Passive':['Passive']}
            
class BlastTrap(Ability):
    name = 'BlastTrap'
    cost = {'Passive':['Passive']}
            
class Anonymity(Ability):
    name = 'Anonymity'
    cost = {'Passive':['Passive']}
            
class Phantom(Ability):
    name = 'Phantom'
    cost = {'Passive':['Passive']}
            
# Tier 3: 9+
class Killshot(Ability):
    name = 'Killshot'
    cost = {'Passive':['Passive']}
            
class Aversion(Ability):
    name = 'Aversion'
    cost = {'Reaction':['Reaction']}
    state = ['Wounding']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['Damage'] = math.floor((combatSteps['Damage'] + combatSteps['AddDamage'])/2)
        return gameboard,combatSteps
    
class Vendetta(Ability):
    name = 'Vendetta'
    cost = {'Reaction':['Reaction']}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        if damage >= 4:
            self.attributeManager.setBonusAttributes('Attack',1)
        return gameboard, damage
        
class Reaper(Ability):
    name = 'Reaper'
    cost = {'Turn':['Passive']}

class House(GeneralUse):
    houseRanks = {1:'Resident',2:'Seneschal',3:'Vizier',4:'Grand Master'}
    
class Conium(House):
    name = 'Conium'
    abilities = {
            1: ['Virulency','Infect'],
            2: ['PoisonedDagger','Lethargy'],
            3: ['Metastasis','Biohazard'],
            4: ['Plagelord','Dyskinesia']
        }
    
class Virulency(Ability):
    name = 'Virulency'
    cost = {'Turn':['Passive']}
            
class Infect(Ability):
    name = 'Infect'
    cost = {'Turn':['Passive']}
            
class PoisonedDagger(Ability):
    name = 'PoisonedDagger'
    cost = {'Reaction':['Special']}
    state = ['MissedMeleeAttack']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['CombatResult'] = 'Hit'
        combatSteps['Damage'] = gameboard[unit].attributeManager.getAttribute['Damage']
        combatSteps['AddDamage'] = 0
        combatSteps['AttackMods'] = combatSteps['AttackMods'] + ['Wounding']
        return gameboard, combatSteps
    
class Lethargy(Ability):
    name = 'Lethargy'
    cost = {'Turn':['Passive']}
            
class Metastasis(Ability):
    name = 'Metastasis'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return self.getLOSTargets(unit,gameboard,{'Range':3})
    
    def abilityEffect(self,unit,target,gameboard):
        return self.dealDamage(unit,target,gameboard,3)
    
class Biohazard(Ability):
    name = 'Biohazard'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return self.getAOETargets(2,unit)
    
    def abilityEffect(self,unit,target,gameboard):
        for x in target:
            self.combat(unit,target,gameboard,{'AttackMods':'Wounding','Damage':3})
        return gameboard
    
    def execute(self,unit,gameboard,*args):
        potentialTargets = self.getTargets(unit,gameboard,args)
        target = potentialTargets
        gameboard = self.abilityEffect(unit,target,gameboard)
        gameboard[unit].reactionManager.setState('None')
        gameboard[target].reactionManager.setState('None')
        return gameboard
    
class Plaguelord(Ability):
    name = 'Plaguelord'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return self.getAOETargets(1,unit)            
    
    def abilityEffect(self,unit,target,gameboard):
        for x in target:
            self.dealDamage(unit,target,gameboard,gameboard[unit].damageBonus)
        gameboard[unit].damageBonus = 0
        return gameboard
        
    def execute(self,unit,gameboard,*args):
        potentialTargets = self.getTargets(unit,gameboard,args)
        target = [x for x in potentialTargets if type(gameboard[x]).__name__ == 'Unit']
        gameboard = self.abilityEffect(unit,target,gameboard)
        gameboard[unit].reactionManager.setState('None')
        gameboard[target].reactionManager.setState('None')
        return gameboard
        
class Dyskinesia(Ability):
    name = 'Dyskinesia'
    cost = {'Turn':['Passive']}
                    
class Naal(House):
    name = 'Naal'
    
    abilities = {
            1: ['Ranger','Mark'],
            2: ['Sniper','EffectiveCover'],
            3: ['Camouflage','Communications'],
            4: ['Vantage','Spotter']
        }
    
class Ranger(Ability):
    name = 'Ranger'
    cost = {'Turn':['Passive']}
    
    def __init__(self,unitName,player):
        self.unitName = unitName
        self.player = player
    
    def statEffect(self,unitObj):
        unitObj.changePermanentUpgrade('Special',-1)
        unitObj.unitRange = 3
        return unitObj
    
class Mark(Ability):
    name = 'Mark'
    cost = {'Turn':['Passive']}
                
class Sniper(Ability):
    name = 'Sniper'
    cost = {'Turn':['Passive']}
                
    def statEffect(self,unitObj):
        unitObj.changePermanentUpgrade('Hit',-2)
        return unitObj
    
class EffectiveCover(Ability):
    name = 'EffectiveCover'
    cost = {'Turn':['Passive']}
                
class Camouflage(Ability):
    name = 'Camouflage'
    cost = {'Turn':['Passive']}
    
    def abilityEffect(self,unit,gameboard):
        spaces = [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard]
        for x in spaces:
            gameboard[x] = StealthToken()
        gameboard[unit].attributeManager.currentAttributes['Movement'] = 0
        return gameboard
        
class Communications(Ability):
    name = 'Communications'
    cost = {'Turn':['Passive']}
                
class Vantage(Ability):
    name = 'Vantage'
    cost = {'Turn':['Passive']}
                
class Spotter(Ability):
    name = 'Spotter'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard]
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = SpotterUnit(gameboard[unit].playerID)

class SpotterUnit(Unit):
    
    def __init__(self,playerID):
        self.playerID = playerID
        
class Caecus(House):
    name = 'Caecus'
    
    abilities = {
            1:['ShadowStrike','CloakAndDagger'],
            2:['Infiltrate','Misdirection'],
            3:['Stalk','Smokescreen'],
            4:['Eviscerate','Sneak']
        }
    
class Shadowstrike:
    name = 'Shadowstrike'
    cost = {'Reaction':['Passive']}
    state = ['EliminateUnit']
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = StealthToken(gameboard[unit].playerID,target)
        return gameboard
        
class CloakAndDagger:
    name = 'CloakAndDagger'
    cost = {'Turn':['Passive']}
            
class Infiltrate:
    name = 'Infiltrate'
    cost = {'Turn':['Passive']}
            
class Misdirection:
    name = 'Misdirection'
    cost = {'Turn':['Passive']}
            
class Stalk:
    name = 'Stalk'
    cost = {'Turn':['Passive']}
                
class Smokescreen:
    name = 'Smokescreen'
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        self.getAOETargets(3,gameboard[unit].location)
        
    def abilityEffect(self,unit,target,gameboard):
        spaces = [x for x in self.adjacentSpaces(target) if x not in gameboard]
        for x in spaces:
            gameboard[x] = StealthToken(gameboard[unit].playerID,gameboard[unit].location)
        return gameboard
    
class Eviscerate:
    name = 'Eviscerate'
    cost = {'Passive':'Passive'}
                
class Sneak:
    name = 'Sneak'
    cost = {'Passive':'Passive'}
            
class Esper(House):
    name = 'Esper'
    
    abilities = {
            1:['Levitation','TimeDilation'],
            2:['Portent','PsychicScream'],
            3:['Kineblade','Barrier'],
            4:['Crumple','Savant']
        }
    
class Levitation:
    name = 'Levitation'
    cost = {'Turn':'Special'}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].unrestrainedMovement = True
        gameboard[unit].attributeManager.changeAttribute('Evasion',2)
        gameboard[unit].attributeManager.changeAttribute('Movement',2)
        return gameboard
        
class TimeDilation:
    name = 'TimeDilation'
    cost = {'Passive':'Passive'}
                
class Portent:
    name = 'Portent'
    cost = {'Turn':'Special'}
    active = False
    
    def abilityEffect(self,unit,target,gameboard):
        self.active = True
        return gameboard
    
class PsychicScream:
    name = 'PsychicScream'
    cost = {'Turn':'Special'}
    active = False
    
    def abilityEffect(self,unit,target,gameboard):
        self.active = True
        return gameboard
    
class Kineblade:
    name = 'Kineblade'
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard]
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = SpotterUnit(gameboard[unit].playerID)   
        return gameboard         
        
class KinebladeUnit(Unit):
    name = 'KinebladeUnit'

    def __init__(self,playerID):
        self.playerID = playerID        

class Barrier:
    name = 'Barrier'
    cost = {'Reaction':'Reaction'}
    state = ['AddEvasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['Armor'] = combatSteps['Armor'] + 3
        combatSteps['Evasion'] = combatSteps['Evasion'] + 1
        return gameboard, combatSteps
        
class Crumple:
    name = 'Crumple'
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return self.getLOSTargets(unit,gameboard,{'Range':3})
    
    def abilityEffect(self,unit,target,gameboard):
        mods = gameboard[unit].createCombatModifiers({'unit':unit,'target':target,'gameboard':gameboard})
        mods['Wounding'] = True
        mods['Piercing'] = True
        gameboard[unit].changeAttributes('Attack',-1)
        return self.combat(unit,target,gameboard,mods)               
        
class Savant(Unit):
    name = 'Savant'
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard]
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = SpotterUnit(gameboard[unit].playerID)
        return gameboard
        
class SavantUnit(Unit):
    name = 'SavantUnit'
    
    def __init__(self,playerID):
        self.playerID = playerID
        
class Accipiter(House):
    
    name = 'Accipiter'
    abilities = {
            1:['Airborne','Disengage'],
            2:['Lift','Rush'],
            3:['RendingStrike','Flurry'],
            4:['ConcussiveJump','Flock']
        }
    
class Airborne:
    name = 'Airborne'
    cost = {'Passive':'Passive'}
                
class Disengage:
    name = 'Disengage'
    cost = {'Reaction':'Reaction'}
    state = ['AfterAttack']
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Movement',3)
        gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,{'Distance':3})
        return gameboard
    
class Lift:
    name = 'Lift'
    cost = {'Turn':['Special','Movement']}
    
    def abilityEffect(self,unit,target,gameboard):
        space = random.choice([x for x in self.getAOETargets(6,unit) if x not in gameboard])
        gameboard[space] = gameboard[unit]
        del gameboard[unit]
        return gameboard
       
class Rush:
    name = 'Rush'
    cost = {'Turn':['Movement','Attack']}
    
    def getTargets(self,unit,gameboard):
        return []
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Movement',3)
        gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,{'Distance':3})            
        return gameboard[unit].abilities['Attack'].execute(unit,gameboard)
        
class RendingStrike:
    name = 'RendingStrike'
    cost = {'Reaction':['Movement']}
    state = ['AddHit']
    # add piercing and swift to an attack
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['AttackMods']['Piercing'] = True
        combatSteps['AttackMods']['Swift'] = True
        return gameboard, combatSteps
    
class Flurry:
    name = 'Flurry'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Attack',1)            
        gameboard[unit].abilities['Attack'].execute(unit,gameboard)
        gameboard[unit].abilities['Attack'].execute(unit,gameboard)
        return gameboard
    
class ConcussiveJump:
    name = 'ConcussiveJump'
    cost = {'Turn':['Special','Movement']}
    
    def abilityEffect(self,unit,target,gameboard):
        targets = [x for x in self.getAOETargets(1,unit) if x not in gameboard]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Wounding':True})
        space = random.choice([x for x in self.getAOETargets(4,unit) if x not in gameboard])
        gameboard[space] = gameboard[unit]
        del gameboard[unit]
        targets = [x for x in self.getAOETargets(1,space) if x not in gameboard]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Wounding':True})
        return gameboard
    
class Flock:
    name = 'Flock'
    cost = {'Passive':'Passive'}
                
class AssassinPlayer(Player):
    
    houseRank = {'Conium':0,'Naal':0,'Caecus':0,'Esper':0,'Accipiter':0}
    houses = {'Conium':Conium(),'Naal':Naal(),'Caecus':Caecus(),'Esper':Esper(),'Accipiter':Accipiter()}
    damageBonus = 0
    attackMods = []

    def __init__(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        # instantiate new units
        self.units = {'Elite':AssassinUnit('Elite','Elite1'),'Common1':AssassinUnit('Common','Common1'),\
                      'Common2':AssassinUnit('Common','Common2'),'Common3':AssassinUnit('Common','Common3'),\
                      'Common4':AssassinUnit('Common','Common4')}
        for unit in self.units:
            self.units[unit].setClass(self.playerClass,self.playerID,self.captureCost)
    
    def availableAbilities(self):
        if self.level < 5:
            return {x:self.tier1().get(x) for x in self.tier1() if x not in self.abilities}
        elif self.level >= 5 and self.level < 9:
            options = {**self.tier1(),**self.tier2()}
            return {x:options.get(x) for x in options if x not in self.abilities}
        else:
            options = {**self.tier1(),**self.tier2(),**self.tier3()}
            return {x:options.get(x) for x in options if x not in self.abilities}
        
    def classUpgrades(self,unit):
        if self.units[unit.unitName].eliminatedUnits['Elite'] > 0 or self.units[unit.unitName].eliminatedUnits['Objective'] > 0:
            numUpgrades = self.units[unit.unitName].eliminatedUnits['Elite'] + self.units[unit.unitName].eliminatedUnits['Objective']
            for x in range(1,numUpgrades+1):
                house = random.choice(self.houseRank.keys())
                self.houseUpgrades[house] = self.houseRank[house] + 1
                for x in self.units:
                    for houseAbility in self.houses[house].abilities[self.houseRank[house]]:
                        self.units[x].abilities[houseAbility] = self.houses[house].abilities[self.houseRank[house]][houseAbility]
                        self.units[x] = self.units[x].abilities[houseAbility].statEffect(self.units[x])
        if 'Flock' in self.units[unit.unitName].abilities:
            self.units[unit.unitName].captureCost = 'Movement'
        
    def beginningTurnEffects(self,gameboard):
        tokens = [x for x in gameboard if type(gameboard[x]).__name__ == 'StealthToken' and self.playerID == gameboard[x].playerID]
        if 'Camouflage' in self.abilities:
            if random.choice(['Pass','Camouflage']) == 'Camouflage':
                elite = [x for x in gameboard if gameboard[x].unitType == 'Elite' and gameboard[x].playerID == self.playerID]
                self.abilities['Camouflage'].abilityEffect(elite[0],gameboard)
        if 'CloakAndDagger' in self.abilities:
            for x in random.sample(tokens,3):
                tokens.remove(x)
        if 'Infiltrate' in self.abilities:
            for x in range(0,3):
                self.abilities['Movement'].abilityEffect(self.location,[],gameboard,{'Distance':3,'Passive':'Passive'})
        for x in tokens:
            del gameboard[x]
        return gameboard
    
    def endTurnEffects(self,gameboard):
        if [x for x in gameboard if 'Tectonics' in gameboard[x].abilities]:
            unit = [x for x in gameboard if 'Tectonics' in gameboard[x].abilities]
            for x in gameboard[unit].abilities['Tectonics'].locations:
                if x in gameboard:
                    if gameboard[x].moveable:
                        gameboard = self.forcedMovement(self.attunements['Earth']+5, gameboard[x].direction, [], x, gameboard)
        return gameboard
    
    def generateMovementEffect(self,*ability):
        effects = {}
        if 'Airborne' in self.abilities:
            effects['Unrestrained'] = True
        return effects
            
    def tier1():
        return {'Quickstep':QuickStep(),'KidneyShot':KidneyShot(),'Backstab':Backstab(),'Shift':Shift(),'Rope':Rope(),\
                'Sabotage':Sabotage(),'HeightenedSenses':HeightenedSenses(),'Undercover':Undercover(),\
                'Interrogate':Interrogate(),'Afterimage':Afterimage(),'DeepStrike':DeepStrike(),'Meld':Meld(),'Cripple':Cripple()}
    def tier2():
        return {'Counter':AssassinCounter(),'Blur':Blur(),'FamiliarTerritory':FamiliarTerritory(),\
                'CriticalStrike':CriticalStrike(),'SurpriseAttack':SurpriseAttack(),'BodyDouble':BodyDouble(),\
                'Shadowstep':Shadowstep(),'BlastTrap':BlastTrap(),'Anonymity':Anonymity(),'Phantom':Phantom()}
    def tier3():
        return {'Killshot':Killshot(),'Aversion':Aversion(),'Vendetta':Vendetta(),'Reaper':Reaper()}


class AttunementStats:
    
    level = 1
    
    def __init__(self):
        self.AttunementStats = {
                'Air':self.AirAttunementStats(self.level),
                'Water':self.WaterAttunementStats(self.level),
                'Fire':self.FireAttunementStats(self.level),
                'Earth':self.EarthAttunementStats(self.level),
                'Mana':self.ManaAttunementStats(self.level),
                'Void':self.VoidAttunementStats(self.level)
                }

    def AirAttunementStats(level):
        stats = {
            2:['Evasion'],
            3:['Movement'],
            4:['Evasion'],
            5:['Movement'],
            6:['Evasion'],
            7:['Movement'],
            8:['Evasion'],
            9:['Movement'],
            10:['Evasion']
        }
        return stats[level]
        
    def WaterAttunementStats(level):
        stats = {
            2:['Hit'],
            3:['Movement'],
            4:['Hit'],
            5:['Movement'],
            6:['Hit'],
            7:['Movement'],
            8:['Hit'],
            9:['Movement'],
            10:['Hit']
        }
        return stats[level]
    
    def FireAttunementStats(level):
        stats = {
            2:['Movement'],
            3:['Hit'],
            4:['Damage'],
            5:['Attack'],
            6:['Hit'],
            7:['Hit'],
            8:['Hit'],
            9:['Attack'],
            10:['Damage']
        }
        return stats[level]
    
    def EarthAttunementStats(level):
        stats = {
            2:['Health'],
            3:['Health'],
            4:['Armor'],
            5:['Health'],
            6:['Health'],
            7:['Armor'],
            8:['Health'],
            9:['Health'],
            10:['Armor']
        }
        return stats[level]    
    def ManaAttunementStats(level):
        stats = {
            2:['Hit'],
            3:['Health'],
            4:['Damage'],
            5:['Attack'],
            6:['Hit'],
            7:['Damage'],
            8:['Health'],
            9:['Attack'],
            10:['Hit']
        }        
        return stats[level]
    
    def VoidAttunementStats(level):
        stats = {
            2:['Hit'],
            3:['Movement'],
            4:['Health'],
            5:['Damage'],
            6:['Movement'],
            7:['Hit'],
            8:['Evasion'],
            9:['Hit'],
            10:['Movement']
        }
        return stats[level]
        
class MageUnit(Unit):

    attunements = {'Air':0,'Water':0,'Fire':0,'Earth':0,'Mana':0,'Void':0}
    
    def __init__(self,unitType,unitName):
        super().__init__(unitType,unitName)        
        if unitType == 'Elite':
            self.unitRange = 3
        else:
            self.unitRange = 1
        self.direction = 'n'
    
    def passiveMods(self,unit,target,gameboard,combatSteps):
        if self.location == unit:
            if [y for y in [x for x in self.adjacentSpaces(unit) if x in gameboard] if 'Lethargy' in gameboard[y].abilities] and 'Wounding' in combatSteps['AttackMods']:
                combatSteps['AttackMods'].remove('Wounding')
            if 'Frostbite' in self.abilities:
                if 'Swift' in combatSteps['AttackMods']:
                    combatSteps['AddDamage'] = combatSteps['AddDamage'] + self.attunements['Water']
        if self.location == target:
            if 'MirrorShroud' in self.abilities:
                if 'Wounding' in combatSteps['AttackMods']:
                    combatSteps['AttackMods'].remove('Wounding')
                    combatSteps['CalcHit'] = 6
                    combatSteps['AddHit'] = 0
            if [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]:
                elites = [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]
                for x in elites:
                    if gameboard[x].getDistance(target) <= gameboard[x].attunement['Water']:
                        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] - 2
            if [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]:
                elites = [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]
                for x in elites:
                    if gameboard[x].getDistance(target) <= gameboard[x].attunement['Water']:
                        combatSteps['AttackMods']['Swift'] = True
            if 'Flare' in self.abilities:
                newroll = random.randint(1,6)
                if newroll < combatSteps['CalcHit']:
                    combatSteps['CalcHit'] = newroll
                    
        return gameboard,combatSteps
    
    def movementEffects(self,unit,target,gameboard):
        if 'WindShear' in gameboard[unit].abilities:
            if target in gameboard and gameboard[target].playerID != gameboard[unit].playerID and type(gameboard[target]).__name__ == 'Unit':
                damage = 2 - gameboard[target].attributeManager.getAttribute('Armor')
                if damage > 0:
                    self.dealDamage(unit,target,gameboard,2)
                    newSpace = random.choice([x for x in gameboard[target].adjacentSpaces() if x not in gameboard])
                    gameboard[target].location = newSpace
                    gameboard[newSpace] = gameboard[target]
                    del gameboard[target]
        if 'StepsOfCinder' in gameboard[unit].abilities:
            if gameboard[unit].abilities['StepsOfCinder'].active > 0:        
                for x in self.adjacentSpaces(target):
                    gameboard = self.combat(unit,x,gameboard,{'Wounding':True,'Damage':3})
                    gameboard[unit].abilities['StepsOfCinder'].active = gameboard[unit].abilities['StepsOfCinder'].active - 1
        return gameboard

    def createCombatModifiers(self,**kwargs):
        unit,target,gameboard = kwargs['unit'],kwargs['target'],kwargs['gameboard']
        mods = {}
        if 'Oxidize' in gameboard[unit].abilities:
            if target in gameboard[unit].adjacentSpaces():
                mods['Piercing'] = True
        return mods
                            
class ManaInfusion:
    name = 'ManaInfusion'
    cost = {'Turn':'Passive'}

class ManaPool:
    name = 'ManaPool'
    cost = {'Turn':'Passive'}

class Teleport:
    name = 'Teleport'
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in self.getAOETargets(3,unit) if x not in gameboard]
        
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = gameboard[unit]
        gameboard[target].location = target
        del gameboard[unit]
        return gameboard
   
class ChainLightning(Ability):
    name = 'ChainLightning'
    level = 1
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        self.getLOSTargets(unit,gameboard)
    
    def abilityEffect(self,unit,target,gameboard):
        
        allTargets = [target] 
        newTargets = [target]
        targets = [x for x in gameboard[target].adjacentSpaces() if x not in gameboard]
        while newTargets:
            for space in targets:
                newTargets = [x for x in gameboard[space].adjacentSpaces() if x not in allTargets]
                allTargets = list(set(allTargets).union(set(newTargets)))
                targets = list(set(target).union(set(newTargets)))
                targets.remove(space)
        for x in allTargets:
            if gameboard[x].playerID != gameboard[unit].playerID:
                self.combat(unit,x,gameboard,{'Damage':1,'Wounding':True,'Piercing':True})
        return gameboard
    
class Nimbus(Ability):
    name = 'Nimbus'
    level = 2
    cost = {'Turn':'Passive'}
                    
class Whirlwind(Ability):
    name = 'Whirlwind'
    level = 3
    cost = {'Turn':'Passive'}

    def abilityEffect(self,gameboard,playerID):
        units = [x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == playerID]
        for x in units:
            gameboard[x].abilities['Movement'].abilityEffect(x,[],gameboard,{'Direction':random.choice(self.directions),'Cost':'Passive','Distance':gameboard[x].attunements['Air'] + 2})
        return gameboard
    
class WindShear(Ability):
    name = 'WindShear'
    level = 4
    cost = {'Turn':'Passive'}
    
class Zephyr(Ability):
    name = 'Zephyr'
    level = 5
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == gameboard[unit].playerID]
    
    def abilityEffect(self,unit,target,gameboard):
        tempUnit = gameboard[target]
        gameboard[target] = gameboard[unit]
        gameboard[target].location = target
        gameboard[unit] = tempUnit
        gameboard[unit].location = unit
        gameboard[target].abilities['Movement'].abilityEffect(unit,[],gameboard,{'Direction':random.choice(self.directions),'Cost':'Passive','Distance':gameboard[unit].attunements['Air'] + 2})
        return gameboard
    
class Haste(Ability):
    name = 'Haste'
    level = 6
    cost = {'Turn':'Passive'}
                
class ManifestAir(Ability):
    name = 'ManifestAir'
    level = 7
    cost = {'Turn':'Passive'}
                
class MirrorShroud(Ability):
    name = 'MirrorShroud'
    level = 8
    cost = {'Turn':'Passive'}
                
class Prismata(Ability):
    name = 'Prismata'
    level = 9
    cost = {'Reaction':'Reaction'}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        for x in gameboard[unit].adjacentSpaces:
            gameboard = self.combat(unit,x,gameboard,{'Wounding':True,'Damage':damage})
        return gameboard
    
class LightningStrike(Ability):
    name = 'LightningStrike'
    level = 10
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard]
    
    def abilityEffect(self,unit,target,gameboard):
        return self.combat(unit,target,gameboard,{'Wounding':True,'Piercing':True,'Damage':10})
    
class Air:
    name = 'Air'
    def __init__(self,playerID):
        self.abilities = {'ChainLightning':ChainLightning('Elite',playerID),'Nimbus':Nimbus('Elite',playerID),'Whirlwind':Whirlwind('Elite',playerID),'WindShear':WindShear('Elite',playerID),'Zephyr':Zephyr('Elite',playerID),'Haste':Haste('Elite',playerID),'ManifestAir':ManifestAir('Elite',playerID),'MirrorShroud':MirrorShroud('Elite',playerID),'Prismata':Prismata('Elite',playerID),'LightningStrike':LightningStrike('Elite',playerID)}
 
class IceBlast(Ability):
    name = 'IceBlast'
    level = 1
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return self.getLOSTargets(unit,gameboard)
    
    def abilityEffect(self,unit,target,gameboard):
        return self.combat(unit,target,gameboard,{'AddHit':gameboard[unit].attunements['Water'],'Damage':1+gameboard[unit].attunements['Water']})
        
class Hoarfrost(Ability):
    name = 'Hoarfrost'
    level = 2
    cost = {'Turn':'Passive'}
                
class FlashFlood(Ability):
    name = 'FlashFlood'
    level = 3
    cost = {'Turn':'Attack'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard[unit].adjacentSpaces() if type(gameboard[x]).__name__ == 'Unit']

    def abilityEffect(self,unit,target,gameboard):
        commons = [x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == gameboard[unit].playerID]
        newSpace = random.choice([x for y in [self.adjacentSpaces(x) for x in commons] for x in y if x not in gameboard])
        gameboard[newSpace] = gameboard[target]
        gameboard[newSpace].location = newSpace
        del gameboard[target]
        return gameboard
                
class ManifestWater(Ability):
    name = 'ManifestWater'
    level = 4
    cost = {'Turn':'Reaction'}
    maxReactions = 0
    usedReactions = 0
    
    def getTargets(self,unit,gameboard,*args):
        self.maxReactions = gameboard[unit].attunements['Water']
        return list(set(self.getLOSTargets(unit,gameboard,args)).intersection(set(self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location))))

    def abilityEffect(self,unit,target,gameboard):
        if self.usedReactions < self.maxReactions:
            gameboard[unit].changeAttributes('Reaction',-1)
            self.usedReactions = self.usedReactions + 1
            return self.combat(unit,target,gameboard,gameboard[unit].createCombatModifiers({'unit':unit,'target':target,'gameboard':gameboard})) 
        else:
            return gameboard
    
class Oxidize(Ability):
    name = 'Oxidize'
    level = 5
    cost = {'Turn':'Passive'}
                
class Hailstorm(Ability):
    name = 'Hailstorm'
    level = 6
    cost = {'Turn':'Passive'}
    
    def getTargets(self,unit,gameboard):
        return list(set(self.getLOSTargets(unit,gameboard)).intersection(set(self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location))))            
    
    def abilityEffect(self,unit,target,gameboard):
        commons = [x for x in self.getAOETargets(3,unit) if gameboard[x].unitType == 'Common' and gameboard[x].playerID == gameboard[unit].playerID]
        availableCommon = [x for x in commons if commons[x].attributeManager.getAttribute['Attack'] > 0]
        if availableCommon:
            gameboard[availableCommon].changeAttributes('Attack',-1)
            return self.combat(unit,target,gameboard,gameboard[unit].createCombatModifiers({'unit':unit,'target':target,'gameboard':gameboard})) 
        else:
            return gameboard
        
class LiquidShield(Ability):
    name = 'LiquidShield'
    level = 7
    cost = {'Reaction':'Reaction'}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        damage = damage - 2
        return gameboard,damage
        
class Geyser(Ability):
    name = 'Geyser'
    level = 8
    cost = {'Reaction':'Reaction'}
    state = ['Any']
    
    def getTargets(self,unit,gameboard):
        spaces = [x for x in gameboard if type(gameboard[x]).__name__ == 'Objective' and gameboard[x].playerID == gameboard[unit].playerID]
        targetSpaces = [x for y in [self.adjacentSpaces(x) for x in spaces] if gameboard[y].playerID != gameboard[unit].playerID for x in y]
        return targetSpaces
    
    def abilityEffect(self,unit,target,gameboard):
        for x in self.getTargets(unit,gameboard):
            gameboard = self.combat(unit,target,gameboard,{'Damage':2,'Wounding':True,'Piercing':True}) 
        return gameboard
    
class Frostbite(Ability):
    name = 'Frostbite'
    level = 9
    cost = {'Turn':'Passive'}
                
class HarbingerOfWinter(Ability):
    name = 'HarbingerOfWinter'
    level = 10
    cost = {'Turn':'Passive'}

class Water:
    name = 'Water'
    def __init__(self,playerID):
        self.abilities = {'IceBlast':IceBlast('Elite',playerID),'Hoarfrost':Hoarfrost('Elite',playerID),'FlashFlood':FlashFlood('Elite',playerID),'ManifestWater':ManifestWater('Elite',playerID),'Oxidize':Oxidize('Elite',playerID),'Hailstorm':Hailstorm('Elite',playerID),'LiquidShield':LiquidShield('Elite',playerID),'Geyser':Geyser('Elite',playerID),'Frostbite':Frostbite('Elite',playerID),'HarbingerOfWinter':HarbingerOfWinter('Elite',playerID)}
    
class Fireball(Ability):
    name = 'Fireball'
    level = 1
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return self.getLOSTargets(unit,gameboard)
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.combat(unit,target,gameboard,{'Damage':4})
        spaces = [x for x in self.adjacentSpaces(target)]
        for x in spaces:
            gameboard = self.combat(unit,x,gameboard,{'Damage':1,'Piercing':True,'Wounding':True})
        return gameboard
    
class SearingAura(Ability):
    name = 'SearingAura'
    level = 2
    cost = {'Turn':'Passive'}
                
class Combust(Ability):
    name = 'Combust'
    level = 3
    cost = {'Reaction':'Passive'}
    state = ['EliminateUnit']            
    
    def abilityEffect(self,unit,target,gameboard):
        targets = [x for x in gameboard[unit].adjacentSpaces()]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Damage':3})
        return gameboard
    
class Flare(Ability):
    name = 'Flare'
    level = 4
    cost = {'Passive':'Passive'}
                
class StepsOfCinder(Ability):
    name = 'StepsOfCinder'
    level = 5
    cost = {'Turn':'Special'}
    active = 0
    
    def abilityEffect(self,unit,target,gameboard):
        self.active = gameboard[unit].attunements['Fire']
        return gameboard
        
class TraceFlames(Ability):
    name = 'TraceFlames'
    level = 6
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == gameboard[unit].playerID]
    
    def abilityEffect(self,unit,target,gameboard):
        tempUnit = gameboard[target]
        gameboard[target] = gameboard[unit]
        gameboard[target].location = target
        gameboard[unit] = tempUnit
        gameboard[unit].location = unit
        for x in gameboard[target].adjacentSpaces():
            gameboard = self.combat(target,x,gameboard,{'Damage':3})
        return gameboard
    
class ThermalRadiation(Ability):
    name = 'ThermalRadiation'
    level = 7
    cost = {'Reaction':'Passive'}
    state = ['GiveDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        return gameboard, damage + gameboard[unit].attunements['Fire']
        
class Pyre(Ability):
    name = 'Pyre'
    level = 8
    cost = {'Turn':'Special'}
    damage = {0:5, 1:4, 2:3}
    active = 3
    locations = []
    
    def getTargets(self,unit,gameboard):
        self.getAOETargets(2,unit)
    
    def abilityEffect(self,unit,target,gameboard):
        self.locations = self.locations + target
        return gameboard
    
    def dealDamage(self,gameboard):
        spaces = self.getAOETargets(2,self.location)
        for x in spaces: 
            if x in gameboard and self.getDistance(x,self.location) == 2:
                gameboard[x].attributeManager.currentAttributes['Health'] = gameboard[x].attributeManager.currentAttributes['Health'] - 3
            elif x in gameboard and self.getDistance(x,self.location) == 1:
                gameboard[x].attributeManager.currentAttributes['Health'] = gameboard[x].attributeManager.currentAttributes['Health'] - 4                    
            elif x == self.location:
                gameboard[x].attributeManager.currentAttributes['Health'] = gameboard[x].attributeManager.currentAttributes['Health'] - 5
        return gameboard
    
class Meteor(Ability):
    name = 'Meteor'
    level = 9
    cost = {'Turn':'Special'}
    active = 0
    
    def getTargets(self,unit,gameboard):
        return [space for space in [(x,y) for x in range(0,20) for y in range(0,20)] if space not in gameboard]
        
    def abilityEffect(self,unit,target,gameboard):
        self.location = target
        self.active = 2
        return gameboard
    
    def dealDamage(self,gameboard):
        elite = [x for x in gameboard if gameboard[x].unitType == 'Elite' and gameboard[x].playerID == self.playerID]
        for x in [self.adjacentSpaces(self.location) + [self.location]]:
            if x in gameboard:
                self.combat(elite[0],gameboard[x],gameboard,{'Wounding':True,'Damage':12})
        return gameboard

class Incinerate(Ability):
    name = 'Incinerate'
    level = 10
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return self.getLOSTargets(unit,gameboard)
    
    def abilityEffect(self,unit,target,gameboard):
        return self.combat(unit,target,gameboard,{'Wounding':True,'Piercing':True,'Swift':True,'Damage':5})


class Fire:
    name = 'Fire'
    
    def __init__(self,playerID):
        self.abilities = {'Fireball':Fireball('Elite',playerID),'SearingAura':SearingAura('Elite',playerID),'Combust':Combust('Elite',playerID),'Flare':Flare('Elite',playerID),'StepsOfCinder':StepsOfCinder('Elite',playerID),'TraceFlames':TraceFlames('Elite',playerID),'ThermalRadiation':ThermalRadiation('Elite',playerID),'Pyre':Pyre('Elite',playerID),'Meteor':Meteor('Elite',playerID),'Incinerate':Incinerate('Elite',playerID)}
               
class KineticImpulse(Ability):
    name = 'KineticImpulse'
    level = 1
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in self.getMeleeTargets(unit,gameboard) if type(gameboard[x]).__name__ == 'Unit']
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.forcedMovement(1+gameboard[unit].attunements['Earth'],gameboard[unit].direction,target,gameboard)
        return gameboard
    
class Stonewrought(Ability):
    name = 'Stonewrought'
    level = 2
    cost = {'Turn':'Passive'}
    
    def abilityEffect(self):
        return random.choice([True,False])            
        
class Tremor(Ability):
    name = 'Tremor'
    level = 3
    cost = {'Turn':'Special'}
              
    def abilityEffect(self,unit,target,gameboard):
        commons = [x for x in gameboard if gameboard[x].playerID == gameboard[unit].playerID and gameboard[x].unitType == 'Common']
        targets = [x for y in [self.getAOETargets(gameboard[unit].attunements['Earth'],x) for x in commons] for x in y]
        
        for x in targets:
            choice = random.choice(['Damage','Move'])
            if choice == 'Damage':
                self.combat(unit,x,gameboard,{'Wounding':True,'Damage':3})
            elif choice == 'Move':
                gameboard[x].abilities['Movement'].abilityEffect(x,[],gameboard,{'Cost':'Passive','Distance':3})
        return gameboard
    
class Tectonics(Ability):
    name = 'Tectonics'
    level = 4
    cost = {'Turn':'Special'}
    
    locations = []
    
    def abilityEffect(self,unit,gameboard):
        if gameboard[unit].attunements['Earth'] < 5:
            self.locations = random.sample([x for x in self.getAOETargets(gameboard[unit].attunements['Earth'],unit)], gameboard[unit].attunements['Earth'])
        elif gameboard[unit].attunements['Earth'] >= 5: 
            self.locations = random.sample([x for x in self.getAOETargets(gameboard[unit].attunements['Earth'],unit)], 5)
        return gameboard
    
class Terraform(Ability):
    name = 'Terraform'
    level = 5
    cost = {'Turn':'Special'}
    
    def abilityEffect(self,unit,target,gameboard):
        choice = random.choice(['Create','Move'])

        if choice == 'Create':
            target = random.choice([x for x in self.getAOETargets(3,unit) if x not in gameboard])
            gameboard[target] = Obstacle()
        if choice == 'Move':
            target = random.choice([x for x in self.getAOETargets(3,unit) if type(gameboard[x]).__name__ == 'Obstacle'])
            moveSpace = random.choice([x for x in self.getAOETargets(3,unit) if x not in gameboard])
            gameboard[moveSpace] = gameboard[target]
            del gameboard[target]
        return gameboard
        
class Fissure(Ability):
    name = 'Fissure'
    level = 6
    cost = {'Turn':'Passive'}
                
class Avalanche(Ability):
    name = 'Avalanche'
    level = 7
    cost = {'Turn':'Passive'}
                
class Gleization(Ability):
    name = 'Gleization'
    level = 8
    cost = {'Turn':'Special'}
    
    def abilityEffect(self,unit,target,gameboard):
        commons = [x for x in gameboard if gameboard[x].playerID == gameboard[unit].playerID and gameboard[x].unitType == 'Common']
        for x in commons:
            maxHealth = gameboard[x].levelManager.classAttributes()['Health'] + gameboard[x].permBonusAttr['Health']
            gameboard[x].bonusAttributes['Armor'] = gameboard[x].bonusAttributes['Armor'] + maxHealth - gameboard[x].attributeManager.getAttributes['Health']
        return gameboard
    
class Shockwave(Ability):
    name = 'Shockwave'
    level = 9
    cost = {'Turn':'Passive'}
                
class Gigalith(Ability):
    name = 'Gigalith'
    level = 10
    cost = {'Turn':'Passive'}

class Earth:
    name = 'Earth'
    
    def __init__(self,playerID):
        self.abilities = {'KineticImpulse':KineticImpulse('Elite',playerID),'Stonewrought':Stonewrought('Elite',playerID),'Tremor':Tremor('Elite',playerID),'Tectonics':Tectonics('Elite',playerID),'Terraform':Terraform('Elite',playerID),'Fissure':Fissure('Elite',playerID),'Avalanche':Avalanche('Elite',playerID),'Gleization':Gleization('Elite',playerID),'Shockwave':Shockwave('Elite',playerID),'Gigalith':Gigalith('Elite',playerID)}  
            
class ManaLeech(Ability):
    name = 'ManaLeech'
    level = 1
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in self.getLOSTargets(unit,gameboard,{'Range':3})]
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.combat(unit,target,gameboard,{'Wounding':True,'Piercing':True,'Damage':True})
        if gameboard[unit].attributeManager.getAttributes('Health') < gameboard[unit].maxHealth:
            gameboard[unit].attributeManager.changeAttributes('Health',2)
            if gameboard[unit].attributeManager.getAttributes('Health') == gameboard[unit].maxHealth + 1:
                gameboard[unit].attributeManager.changeAttributes('Health',-1)
        return gameboard
        
class Phase(Ability):
    name = 'Phase'
    level = 2
    cost = {'Reaction':'Reaction'}
    state = ['AddEvasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + 3
        if 'Wounding' in combatSteps['AttackMods']:
            combatSteps['AttackMods'].remove('Wounding')
            combatSteps['HitResults'] = 6
        return gameboard,combatSteps
        
class Substitute(Ability):
    name = 'Substitute'
    level = 3
    cost = {'Reaction':'Reaction'}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        common = random.choice([x for x in gameboard if gameboard[x].playerID == gameboard[unit].playerID and gameboard[x].unitType == 'Common'])
        tempUnit = gameboard[common]
        gameboard[common] = gameboard[unit]
        gameboard[unit] = tempUnit
        return gameboard
        
        
class AetherBeam(Ability):
    name = 'AetherBeam'
    level = 4
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in self.getMeleeTargets(unit,gameboard)]        
    
    def abilityEffect(self,unit,target,gameboard):
        direction = random.choice[0,1,2]
        targets = [self.adjacentSpacesDir({'Location':unit})[direction]]
        for x in range(0,2):
            targets = targets + self.adjacentSpacesDir({'Location':targets[x]})[direction]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Damage':1+gameboard[unit].attunements['Mana']})
        return gameboard
        
class Channel(Ability):
    name = 'Channel'
    level = 5
    cost = {'Turn':'Passive'}
    # need to do this        
        
class Reflect(Ability):
    name = 'Reflect'
    level = 6
    cost = {'Reaction':'Reaction'}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        gameboard = self.forcedMovement(damage,self.oppositeDirections[gameboard[target].direction],unit,target,gameboard)
        return gameboard, 0
        
class InfusedElementals(Ability):
    name = 'InfusedElementals'
    level = 7
    cost = {'Turn':'Passive'}
    # need to do this            
    
class MindFlay(Ability):
    name = 'MindFlay'
    level = 8
    cost = {'Turn':'Special'}

    def getTargets(self,unit,gameboard):
        return [x for x in self.getLOSTargets(unit,gameboard,{'Range':3})]
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.combat(unit,target,gameboard,{'Wounding':True,'Piercing':True,'Damage':gameboard[unit].attunements['Mana']})
        return gameboard
    
class ArcaneShield(Ability):
    name = 'ArcaneShield'
    level = 9
    cost = {'Turn':'Special'}
    stacks = 0
    
    def abilityEffect(self,unit,target,gameboard):
        self.stacks = self.stacks + 1
        return gameboard
    
    def useStack(self):
        if self.stacks > 0:
            self.stacks = self.stacks - 1
        
class AetherPulse(Ability):
    name = 'AetherPulse'
    level = 10
    cost = {'Turn':'Special'}
    
    def abilityEffect(self,unit,target,gameboard):
        targets = [x for x in self.getAOETargets(1,unit) if x in gameboard]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Damage':gameboard[unit].attunements['Mana'],'Wounding':True,'AetherPulse':True})
        return gameboard
    
    def recoverHealth(self,unit,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Health',1)
        return gameboard

class Mana:
    name = 'Mana'
    def __init__(self,playerID):
        self.abilities = {'ManaLeech':ManaLeech('Elite',playerID),'Phase':Phase('Elite',playerID),'Substitute':Substitute('Elite',playerID),'AetherBeam':AetherBeam('Elite',playerID),'Channel':Channel('Elite',playerID),'Reflect':Reflect('Elite',playerID),'InfusedElementals':InfusedElementals('Elite',playerID),'MindFlay':MindFlay('Elite',playerID),'ArcaneShield':ArcaneShield('Elite',playerID),'AetherPulse':AetherPulse('Elite',playerID)}

class PairedDecay(Ability):
    name = 'PairedDecay'
    level = 1
    cost = {'Turn':'Special'}

    def getTargets(self,unit,gameboard):
        return [x for x in self.getLOSTargets(unit,gameboard,{'Range':3})]
    
    def abilityEffect(self,unit,target,gameboard):
        damage = random.choice(range(1,gameboard[unit].attributeManager.getAttributes('Health')))
        gameboard[unit].attributeManager.changeAttributes('Health',-damage)
        gameboard = self.dealDamage(unit,target,gameboard)
        return gameboard
    
class GravitationalCollapse(Ability):
    name = 'GravitationalCollapse'
    level = 2
    cost = {'Turn':'Special'}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target].dealDamage(target,unit,gameboard,2)
        if target not in gameboard:
            for x in self.adjacentSpaces(target):
                if x in gameboard:
                    gameboard = self.combat(unit,x,gameboard,{'Wounding':True,'Damage':1+gameboard[unit].attunements['Void']})
        return gameboard
        
class Portal(Ability):
    name = 'Portal'
    level = 3
    cost = {'Turn':'Passive'}
                
class Rift(Ability):
    name = 'Rift'
    level = 4
    cost = {'Turn':'Passive'}
                
class TransverseManifold(Ability):
    name = 'TransverseManifold'
    level = 5
    cost = {'Turn':'Passive'}
                
class Singularity(Ability):
    name = 'Singularity'
    level = 6
    cost = {'Turn':'Special'}
    
    def abilityEffect(self,unit,target,gameboard):
        target = [x for x in self.getAOETargets(3,unit) if gameboard[x].name == 'Objective']
        gameboard[target].playerID = 'None'
        gameboard[target].health = 0
        return gameboard
    
class Orbitals(Ability):
    name = 'Orbitals'
    level = 7
    cost = {'Turn':'Passive'}
                
class MassTeleport(Ability):
    name = 'MassTeleport'
    level = 8
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        spaces = random.choice([x for x in self.allSpaces() if x not in gameboard])
        return spaces
        
    def abilityEffect(self,unit,target,gameboard):
        adjacentUnits = [x for x in self.directionAdjacentSpaces(gameboard[unit].direction,unit) if gameboard[x].name == 'Unit']
        newAdjacentSpaces = [x for x in self.directionAdjacentSpaces(gameboard[unit].direction,target)]
        for x in adjacentUnits:
            if newAdjacentSpaces[x] not in gameboard:
                gameboard[newAdjacentSpaces[x]] = gameboard[adjacentUnits[x]]
                gameboard[newAdjacentSpaces[x]].location = newAdjacentSpaces[x]
                del gameboard[adjacentUnits[x]]
        return gameboard
                
class Simulacrum(Ability):
    name = 'Simulacrum'
    level = 9
    cost = {'Turn':'Passive'}
        
class Duality(Ability):
    name = 'Duality'
    level = 10
    cost = {'Turn':'Passive'}

class Void:
    name = 'Void'
    def __init__(self,playerID):
        self.abilities = {'PairedDecay':PairedDecay('Elite',playerID),'GravitationalCollapse':GravitationalCollapse('Elite',playerID),'Portal':Portal('Elite',playerID),'Rift':Rift('Elite',playerID),'TransverseManifold':TransverseManifold('Elite',playerID),'Singularity':Singularity('Elite',playerID),'Orbitals':Orbitals('Elite',playerID),'MassTeleport':MassTeleport('Elite',playerID),'Simulacrum':Simulacrum('Elite',playerID),'Duality':Duality('Elite',playerID)}

class MagePlayer(Player):
    
    captureCost = 'Special'
    attunements = {'Air':0,'Water':0,'Fire':0,'Earth':0,'Mana':0,'Void':0}
    attunement = []

    def __init__(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        # instantiate new units
        self.units = {'Elite':MageUnit('Elite','Elite1'),'Common1':MageUnit('Common','Common1'),\
                      'Common2':MageUnit('Common','Common2'),'Common3':MageUnit('Common','Common3'),\
                      'Common4':MageUnit('Common','Common4')}
        for unit in self.units:
            self.units[unit].setClass(self.playerClass,self.playerID,self.captureCost)
        self.elements = {'Air':Air(self.playerID),'Water':Water(self.playerID),'Fire':Fire(self.playerID),'Earth':Earth(self.playerID),'Mana':Mana(self.playerID),'Void':Void(self.playerID)}
        
#    def levelUp(self):
#        if self.level < 10:
#            self.level = self.level + 1
#            for unit in self.units.values():
#                unit.levelManager.level = self.level
#                unit.attributeManager.permBonusAttr[self.attunement] = unit.attributeManager.permBonusAttr[self.attunement] + 1
#            self.chooseAbility(random.choice(self.availableAbilities()))
    
    def Attune(self):
        baseClassAbilities = {'Teleport':Teleport(),'ManaPool':ManaPool(),'ManaInfusion':ManaInfusion()}
        element = random.choice(self.elements)
        self.attunement = element
        self.attunements[element] = self.attunements[element] + 1
        for unit in self.units:
            self.units[unit].attunements = self.attunements
            elementAbilities = [{x:self.elements[self.attunement].abilities[x]} for x in self.elements[self.attunement].abilities if self.elements[self.attunement].abilities[x].level <= self.level]
            if self.units[unit].unitType == 'Elite':
                self.units[unit].abilities = self.baseAbilites | baseClassAbilities | elementAbilities
                
#    def turn(self,gameboard,players):
#        # while not passed keep going
#
#        unitChoices = {x:gameboard.get(x) for x in gameboard.keys() if type(gameboard[x]).__name__ == 'Unit' and gameboard.get(x).playerID == self.playerID}
#        unitChoices['Pass'] = 'Pass'
#        
#        while True:
#            for unit in self.units:
#                self.units[unit].unitOptions = self.units[unit].createOptions()
#            unitChoice = unitChoices.get(random.choice(list(unitChoices.keys())))
#            if unitChoice == 'Pass':
#                break
#            # execute ability
#            if unitChoice.unitOptions:
#                abilityChoice = random.choice(unitChoice.unitOptions)
#                print(abilityChoice)
#                unitChoice.abilities.get(abilityChoice).execute(unit,gameboard)
#            for unit in gameboard:
#                if type(unit).__name__ == 'Unit' and unit.playerID == self.playerID:
#                    if unit.attributeManager.getAttributes('Health') <= 0:
#                        self.updateUnits(unit)
#                        del gameboard[unit]
#            # then pick an option
#        return gameboard
    
    def beginningTurnEffects(self,gameboard):
        if 'ManifestAir' in self.abilities:
            units = [x for x in gameboard if gameboard[x].playerID == self.playerID]
            spaces = [space for space in [(x,y) for x in range(0,20) for y in range(0,20)] if space not in gameboard]
            for x in units:
                newSpace = random.choice(spaces)
                gameboard[newSpace] = gameboard[x]
                gameboard[newSpace].location = newSpace
                del gameboard[x]
                spaces.remove(newSpace)
        if 'Whirlwind' in self.abilities:
            gameboard = self.abilities['Whirlwind'].abilityEffect(gameboard,self.playerID)
        if 'Haste' in self.abilities:
            units = [x for x in gameboard if gameboard[x].playerID == self.playerID]
            for x in units:
                gameboard[x].attributeManager.bonusAttributes['Movement'] = gameboard[x].attributeManager.bonusAttributes['Movement'] + self.attunements['Air']
        if 'Tectonics' in self.abilities:
            self.abilities['Tectonics'].abilityEffect(self.units['Elite'].location,gameboard)
        if 'Fissure' in self.abilities:
            for x in gameboard:
                if gameboard[x].playerID == self.playerID and type(gameboard[x]).__name__ == 'Obstacle' and gameboard[x].temporary:
                    del gameboard[x]
        if 'Gleization' in self.abilities:
            for x in self.units:
                x.bonusAttributes['Armor'] = 0    
        return gameboard
    
    def generateMovementEffect(self,*ability):
        effects = {}
        if 'Nimbus' in self.abilities:
            effects['Unrestrained'] = True
        return effects
    
    def endTurnEffects(self,gameboard):
        if 'SearingAura' in self.abilities:
            units = [x for x in gameboard if gameboard[x].playerID == self.playerID and type(gameboard[x]).__name__ == 'Unit']
            targets = [x for y in [gameboard[z].getAOETargets(gameboard[z].attunements['Fire']) for z in units if gameboard[z].playerID != self.playerID] for x in y]
            for x in targets:
                self.dealDamage(gameboard[random.choice(units)],x,gameboard,1)
        if 'StepsOfCinder' in self.abilities:        
            for x in units: 
                if 'StepsOfCinder' in x.abilities: 
                    x.abilities['StepsOfCinder'].active = 0
        if 'Tectonics' in self.abilities:
            for x in self.abilities['Tectonics'].locations:
                if x in gameboard:
                    if gameboard[x].moveable:
                        gameboard = self.forcedMovement(self.attunements['Earth']+5, gameboard[x].direction, [], x, gameboard)

        return gameboard

#########################################
        # WARRIOR DEF #
        ###############

class WarriorAttack(Attack):
    name = 'WarriorAttack'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].changeAttributes('Attack',-1)
        self.weapon = random.choice(['Warhammer','Spear','Katana','Rapier','Axe','Greatsword','Bow'])
        weaponswitch = {
            1: gameboard[unit].weapons[self.weapon.Form1(unit,target,gameboard)],
            2: gameboard[unit].weapons[self.weapon.Form2(unit,target,gameboard)],
            3: gameboard[unit].weapons[self.weapon.Form3(unit,target,gameboard)],
            4: gameboard[unit].weapons[self.weapon.Form4(unit,target,gameboard)]
        }
        gameboard = weaponswitch.get(gameboard[unit].form)
        gameboard[unit].increaseForm()
        return gameboard
        
    def getTargets(self,unit,gameboard,*args):
        return list(set(self.getLOSTargets(unit,gameboard,args)).intersection(set(self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location))))
   

class Block(Ability):
    name = 'Block'
    cost = {'Reaction':['Reaction']}
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        blockDamage = combatSteps['CalcHit'] + combatSteps['AddHit'] - combatSteps['CalcEvasion'] - combatSteps['AddEvasion']
        combatSteps['AddDamage'] = -blockDamage
        return gameboard, combatSteps

class Push(Ability):
    name = 'Push'
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.forcedMovement(2,gameboard[unit].direction,target,gameboard)        
        return gameboard

class Parry(Ability):
    name = 'Parry'
    cost = {'Reaction':['Reaction']}
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + gameboard[target].attributeManager.getAttributes('Hit')
        return gameboard, combatSteps

class WarriorCounter(Ability):
    name = 'Counter'
    cost = {'Reaction':['Reaction']}
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        gameboard = self.combat(unit,target,gameboard)
        return gameboard, combatSteps  
        
#    class Cleave:
#        name = 'Cleave'
#        cost = ['Passive']
#        def abilityEffect(self,unit,target,gameboard):
#    class Sweeping:
#        name = 'Sweeping'
#        cost = ['Passive']
#        def abilityEffect(self,unit,target,gameboard):
#    class Counter:
#        name = 'Counter'
#        cost = ['Reaction']
#        def abilityEffect(self,unit,target,gameboard):
#    class Parry:
#        name = 'Parry'
#        cost = ['Reaction']
#        def abilityEffect(self,unit,target,gameboard):
#    class Block:
#        name = 'Block'
#        cost = ['Reaction']
#        def abilityEffect(self,unit,target,gameboard):
#    class Push:
#        name = 'Push'
#        cost = ['Special']
#        def abilityEffect(self,unit,target,gameboard):
#    class Regroup:
#        name = 'Regroup'
#        cost = ['Passive']
#        def abilityEffect(self,unit,target,gameboard):
#    class FocusEnergy:
#        name = 'FocusEnergy'
#        cost = ['Special']
#        def abilityEffect(self,unit,target,gameboard):
#    class Sprint:
#        name = 'Sprint'
#        cost = ['Passive']
#        def abilityEffect(self,unit,target,gameboard):
#    class Assault:
#        name = 'Assault'
#        cost = ['Passive']
#        def abilityEffect(self,unit,target,gameboard):
#    class Charge:
#        name = 'Charge'
#        cost = ['Passive']
#        def abilityEffect(self,unit,target,gameboard):
    
    
class Warhammer:
    name = 'Warhammer'
    def Form1(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)
        gameboard = self.combat(unit,target,gameboard,combatSteps)
        self.increaseForm()
        return gameboard[unit].abilities['Push'].abilityEffect(unit,target,gameboard)
    def Form2(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)
        self.increaseForm()
        if self.oppositeSpacesDir(unit,target) in gameboard:
            return self.combat(unit,target,gameboard,{'Wounding':True}) 
        else:
            return self.combat(unit,target,gameboard,combatSteps) 
    def Form3(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)
        for x in self.getMeleeTargets(unit,gameboard):
            gameboard = self.combat(unit,target,gameboard,combatSteps)
            gameboard = gameboard[unit].abilities['Push'].abilityEffect(unit,target,gameboard)
        self.increaseForm()    
        return gameboard
    def Form4(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)
        combatSteps['AddDamage'] = combatSteps['AddDamage'] + gameboard[target].attributeManager.getAttributes('Armor')
        combatSteps['Piercing'] = True
        self.increaseForm()
        return self.combat(unit,target,gameboard,combatSteps)
    
class Spear:
    name = 'Spear'
    def Form1(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)
        if gameboard[unit].weaponUpgrades['Spear'] == 3:
            combatSteps['AddHit'] = combatSteps['AddHit'] + 2
        target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':2})])
        self.increaseForm()
        return self.combat(unit,target,gameboard,combatSteps)
        
    def Form2(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Spear'] == 3:
            combatSteps['AddHit'] = combatSteps['AddHit'] + 2
        targets = self.getMeleeTargets(unit,gameboard)
        for x in targets:
            gameboard = self.combat(unit,target,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
        
    def Form3(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Spear'] == 3:
            combatSteps['AddHit'] = combatSteps['AddHit'] + 2            
        gameboard = self.combat(unit,target,gameboard,combatSteps)
        newSpace = random.choice(self.straightLine(3,random.choice(self.directions),unit,gameboard))
        gameboard[newSpace] = gameboard[unit]
        del gameboard[unit]
        self.increaseForm()
        return gameboard
        
    def Form4(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Spear'] == 3:
            combatSteps['AddHit'] = combatSteps['AddHit'] + 2
        targets = self.straightLine(3,random.choice(self.LOSDirections(gameboard[unit].direction)),unit,gameboard)
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
        
class Rapier:
    name = 'Rapier'
    
    def Form1(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)
        
        damage = gameboard[unit].attributeManager.getAttributes['Damage'] - 1
        combatSteps['Damage'] = damage
        gameboard = self.combat(unit,target,gameboard,combatSteps)
        gameboard = self.combat(unit,target,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
        
    def Form2(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        gameboard[unit].attributeManager.bonusAttributes['Reaction'] = gameboard[unit].attributeManager.bonusAttributes['Reaction'] + 1
        gameboard = self.combat(unit,target,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
    
    def Form3(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)
        combatSteps['Swift'] = True
        gameboard = self.combat(unit,target,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
    
    def Form4(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        damage = gameboard[unit].attributeManager.getAttributes['Damage'] - 2
        combatSteps['Damage'] = damage
        gameboard = self.combat(unit,target,gameboard,combatSteps)
        gameboard = self.combat(unit,target,gameboard,combatSteps)            
        gameboard = self.combat(unit,target,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
    
class Katana:
    name = 'Katana'
    Form4 = False
    
    def Form1(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        target = random.choice([x for x in gameboard[unit].getAOETargets(2,unit) if x not in gameboard])
        space = gameboard[target].adjacentSpacesDir()[1]
        if space not in gameboard:
            gameboard[space] = gameboard[unit]
            gameboard = self.combat(space,target,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
        
    def Form2(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        target = random.choice([x for x in gameboard[unit].getAOETargets(2,unit) if x not in gameboard])
        spaces = gameboard[target].adjacentSpaces()
        newtarget = random.choice([x for x in spaces if x not in gameboard])
        gameboard[newtarget] = gameboard[unit]
        gameboard[newtarget].location = newtarget
        del gameboard[unit]
        
        self.increaseForm()
        return self.combat(unit,target,gameboard,combatSteps)
        
    def Form3(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        gameboard = self.combat(unit,target,gameboard,combatSteps)
        gameboard = gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,{'Distance':2,'Cost':'Passive'})
        self.increaseForm()
        return gameboard
        
    def Form4(self,unit,target,gameboard,combatSteps):    
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        self.Form4 = True
        self.increaseForm()
        return self.combat(unit,target,gameboard,combatSteps)

        
class Axe:
    name = 'Axe'
    
    def Form1(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Axe'] == 3:
            combatSteps['AddDamage'] = combatSteps['AddDamage'] + combatSteps['AddEvasion']
        combatSteps['Axe'] = True
        self.increaseForm()
        return self.combat(unit,target,gameboard,combatSteps)
        
    def Form2(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Axe'] == 3:
            combatSteps['AddDamage'] = combatSteps['AddDamage'] + combatSteps['AddEvasion']
        combatSteps['AddHit'] = combatSteps['AddHit'] + 1
        combatSteps['Piercing'] = True
        self.increaseForm()
        return self.combat(unit,target,gameboard,combatSteps)
        
    def Form3(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Axe'] == 3:
            combatSteps['AddDamage'] = combatSteps['AddDamage'] + combatSteps['AddEvasion']
        cleave = self.oppositeSpacesDir(unit,target)
        gameboard = self.combat(unit,target,gameboard,combatSteps)
        if cleave in gameboard:
            gameboard = self.combat(unit,cleave,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
    
    def Form4(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Axe'] == 3:
            combatSteps['AddDamage'] = combatSteps['AddDamage'] + combatSteps['AddEvasion']
        damage = gameboard[target].levelManager.classAttributes()['Movement'] - gameboard[target].attributeManager.getAttribute('Movement')
        combatSteps['AddDamage'] = combatSteps['AddDamage'] + damage
        self.increaseForm()
        return self.combat(unit,target,gameboard,combatSteps)
        
class GreatSword:
    name = 'GreatSword'
    def Form1(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)
        combatSteps['AddDamage'] = combatSteps['AddDamage'] + 2
        gameboard = self.combat(unit,target,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
    
    def Form2(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)
        combatSteps['AddHit'] = combatSteps['AddHit'] - 1
        
        targets = self.getMeleeTargets(unit,gameboard)
        for x in targets:
            gameboard = self.combat(unit,target,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
        
    def Form3(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        targets = [x for x in self.getAOETargets(1,unit) if x in gameboard]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
        
    def Form4(self,unit,target,gameboard,combatSteps):    
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)
        combatSteps['AddHit'] = combatSteps['AddHit'] + 4
        self.increaseForm()
        return self.combat(unit,target,gameboard,combatSteps)

class Bow:
    name = 'Bow'
    def Form1(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Bow'] >= 2:
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':4})])
        else:
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
            
        if gameboard[unit].weaponUpgrades['Bow'] >= 1:
            combatSteps['AddHit'] = combatSteps['AddHit'] + 1
            
        return self.combat(unit,target,gameboard,combatSteps)            
        
    def Form2(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Bow'] >= 2:
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':4})])
        else:
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
        if gameboard[unit].weaponUpgrades['Bow'] >= 1:
            combatSteps['AddHit'] = combatSteps['AddHit'] + 1
            if gameboard[unit].weaponUpgrades['Bow'] == 3:
                combatSteps['AddHit'] = combatSteps['AddHit'] + 2
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + 1
                combatSteps['Swift'] = True
                
        return self.combat(unit,target,gameboard,combatSteps)                

    def Form3(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Bow'] >= 2:
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':4})])
        else:
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
        if gameboard[unit].weaponUpgrades['Bow'] >= 1:
            combatSteps['AddHit'] = combatSteps['AddHit'] + 1
            if gameboard[unit].weaponUpgrades['Bow'] == 3:
                combatSteps['AddHit'] = combatSteps['AddHit'] + 2
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + 1
                combatSteps['Swift'] = True
        return self.combat(unit,target,gameboard,combatSteps)                

    def Form4(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        if gameboard[unit].weaponUpgrades['Bow'] >= 2:
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':4})])
        else:
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
        if gameboard[unit].weaponUpgrades['Bow'] >= 1:
            combatSteps['AddHit'] = combatSteps['AddHit'] + 1
            if gameboard[unit].weaponUpgrades['Bow'] == 3:
                combatSteps['AddHit'] = combatSteps['AddHit'] + 2
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + 1
                combatSteps['Swift'] = True
        return self.combat(unit,target,gameboard,combatSteps)
            
class Distension(Ability):
    name = 'Distension'
    cost = {'Turn':['Attack']}
        
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.forcedMovement(2,gameboard[unit].direction,self.adjacentSpacesDir()[1],gameboard)
        gameboard[unit].direction = gameboard[unit].faceDirection(gameboard[unit].direction,4)
        targets = [x for x in self.getMeleeTargets(unit,gameboard) if x in gameboard]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard)
        gameboard = gameboard[unit].abilities['Movement'].abilityEffect(gameboard[unit].location,[],gameboard,{'Distance':1,'Passive':'Passive'})
    
class ClearingAPath(Ability):
    name = 'ClearingAPath'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.combat(unit,self.adjacentSpacesDir()[1],gameboard)
        gameboard = self.forcedMovement(2,gameboard[unit].direction,self.adjacentSpacesDir()[1],gameboard)
        for x in range(0,2):
            space = self.adjacentSpacesDir()[1]
            if space not in gameboard:
                gameboard[space] = gameboard[unit]
                gameboard[space].location = space
                del gameboard[unit]
                unit = space
        gameboard = self.combat(unit,gameboard[unit].adjacentSpacesDir()[1],gameboard)
        gameboard = self.forcedMovement(2,gameboard[unit].direction,self.adjacentSpacesDir()[1],gameboard)            
        
class Contusion(Ability):
    name = 'Contusion'
    cost = {'Turn':['Passive']}
    #check
        
class Rage(Ability):
    name = 'Rage'
    damage = 0
    cost = {'Reaction':['Passive']}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        self.damage = self.damage + 1
        return gameboard, damage
        
class Momentum(Ability):
    name = 'Momentum'
    cost = {'Turn':['Passive']}
    
    #check
class HeavyBolts(Ability):
    name = 'HeavyBolts'
    cost = {'Turn':['Passive']}
    #check
    
class BladeDance(Ability):
    name = 'BladeDance'
    cost = {'Turn':['Passive']}
    #check
    
class PruningBranches(Ability):
    name = 'PruningBranches'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        target1 = random.choice([x for x in self.getMeleeTargets(unit,gameboard) if x in gameboard])
        gameboard = self.combat(unit,target1,gameboard)    
        gameboard = gameboard[unit].abilities['Movement'].abilityEffect(gameboard[unit].location,[],gameboard,{'Distance':1,'Passive':'Passive'})
        target2 = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':2}) if x in gameboard and x != target1])
        return self.combat(unit,target2,gameboard)    

class Incision(Ability):
    name = 'Incision'
    cost = {'Turn':['Passive']}
    #check

class Harvest(Ability):
    name = 'Harvest'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        targets = [x for x in self.getAOETargets(1,unit) if x in gameboard]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Wounding':True})
        targets = [x for x in self.getAOETargets(2,unit) if x in gameboard and x not in [x for x in self.getAOETargets(1,unit)]]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Wounding':True})
        return gameboard
        
class Tranquility(Ability):
    name = 'Tranquility'
    cost = {'Turn':['Passive']}
    #check
    
class Rebuke(Ability):
    name = 'Rebuke'
    cost = {'Reaction':['Passive']}
    state = ['Evasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        if target in gameboard[unit].getMeleeTargets(unit,gameboard):
            gameboard = gameboard[unit].abilities['WarriorAttack'].abilityEffect(unit,target,gameboard)
            gameboard = gameboard[unit].abilities['Movement'].execute(unit,target,gameboard,1)
        return gameboard, combatSteps
    
class Collateral(Ability):
    name = 'Collateral'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        for x in self.straightLine(2,gameboard[unit].direction,unit,gameboard):
            gameboard = self.combat(unit,x,gameboard)
        mov = gameboard[unit].adjacentSpacesDir()[2]
        if mov not in gameboard:
            gameboard[mov] = gameboard[unit]
            del gameboard[unit]
            gameboard[mov].location = mov
            unit = mov
        for x in self.straightLine(2,self.LOSDirections(gameboard[unit].direction)[0],unit,gameboard):
            gameboard = self.combat(unit,x,gameboard)
                   
class DescribingAnArc(Ability):
    name = 'DescribingAnArc'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = gameboard[unit].abilities['Movement'].abilityEffect(gameboard[unit].location,[],gameboard,{'Distance':1,'Passive':'Passive'})
        for x in range(0,3):
            target = random.choice([x for x in self.getMeleeTargets(unit,gameboard) if x in gameboard])
            gameboard = self.combat(unit,target,gameboard,{'Damage':gameboard[unit].attributeManager.getAttributes('Damage')-2})
        targets = self.getMeleeTargets(unit,gameboard)
        for x in targets:
            gameboard = self.combat(unit,target,gameboard)

        
class Brushstrokes(Ability):
    name = 'Brushstrokes'
    cost = {'Turn':['Attack']}
    hit = 0
    damage = 0
    
    def useBonuses(self, attribute):
        if attribute == 'Damage':
            dmg = self.damage
            self.damage = 0
            return dmg
        elif attribute == 'Hit':
            hit = self.hit
            self.hit = 0
            return hit
        
    def abilityEffect(self,unit,target,gameboard):
        for x in range(0,3):
            choice = random.choice(['Move','Attack','Hit','Damage'])
            if choice == 'Move':
                gameboard = gameboard[unit].abilities['Movement'].abilityEffect(gameboard[unit].location,[],gameboard,{'Distance':1,'Passive':'Passive'})
            elif choice == 'Hit':
                self.hit = self.hit + 1
            elif choice == 'Damage':
                self.damage = self.damage + 1
            elif choice == 'Attack':
                gameboard = self.combat(unit,target,gameboard,{'Damage':gameboard[unit].attributeManager.getAttributes('Damage')-2,'AddHit':self.useBonuses('Hit'),'AddDamage':self.useBonuses('Damage')})

class Barter(Ability):
    name = 'Barter'
    cost = {'Reaction':['Attack']}
    state = ['TargetedMelee']
    active = False
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['AttackMods']['Wounding'] = True
        self.active = True
        return 
    
class Gardener(Ability):
    name = 'Gardener'
    cost = {'Turn':['Special']}
    active = False
    
    def abilityEffect(self,unit,target,gameboard):
        self.active = True
        
class FleurDeLis(Ability):
    name = 'FleurDeLis'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        targets = self.getMeleeTargets(unit,gameboard)
        for x in targets:
            gameboard = self.combat(unit,target,gameboard)
        gameboard[unit].direction = gameboard[unit].faceDirection(gameboard[unit].direction,4)

        targets = [x for x in self.getLOSTargets(unit,gameboard,{'Range':3}) if x in gameboard]
        if len(targets) < 3:
            for x in targets:
                gameboard = self.combat(unit,x,gameboard)
        elif len(targets) >=3:
            newTargets = random.sample(targets,3)
            for x in newTargets:
                gameboard = self.combat(unit,x,gameboard)
        return gameboard            
            
class Sunder(Ability):
    name = 'Sunder'
    cost = {'Turn':'Passive'}
    #check
    
class Scattershot(Ability):
    name = 'Scattershot'
    cost = {'Turn':'Passive'}
    #check

class Aegis(Ability):
    name = 'Aegis'
    cost = {'Turn':'Passive'}
    #check

class WarriorUnit(Unit):
    
    weaponUpgrades = {'Warhammer':0,'Spear':0,'Katana':0,'Rapier':0,'Axe':0,'Greatsword':0,'Bow':0}
    weapons = {'Warhammer':Warhammer(),'Spear':Spear(),'Katana':Katana(),'Rapier':Rapier(),'Axe':Axe(),'GreatSword':GreatSword(),'Bow':Bow}
    form = 1
    
    def increaseForm(self):
        while True:
            self.form = self.form + 1
            if self.form == 5:
                self.form == 1
            yield self.form
            
    def upgradeWeapon(self,weapon):
        if self.weaponUpgrades[weapon] < 3:
            self.weaponUpgrades[weapon] = self.weaponUpgrades[weapon] + 1
        if weapon == 'Warhammer' and self.weaponUpgrades[weapon] == 1:
            self.abilities['Block'] = Block(self.playerType,self.playerClass)
        if weapon == 'Rapier' and self.weaponUpgrades[weapon] == 2:
            self.abilities['Parry'] = Parry(self.playerType,self.playerClass)            
        if weapon == 'Greatsword' and self.weaponUpgrades[weapon] == 3:
            self.attributeManager.permBonusAttr['Armor'] = 1
        if weapon == 'Katana' and self.weaponUpgrades[weapon] == 3:
            self.attributeManager.permBonusAttr['Evasion'] == 2

    def attackPassiveEffects(self,unit,target,gameboard,combatSteps):
        if 'Contusion' in gameboard[unit].abilities and self.oppositeSpacesDir(unit,target) in gameboard:
            combatSteps['AddDamage'] = combatSteps['AddDamage'] + gameboard[unit].attributeManager.getAttributes['Evasion']
        if 'Rage' in gameboard[unit].abilities:
            combatSteps['AddDamage'] = combatSteps['AddDamage'] + gameboard[unit].abilities['Rage'].damage
        if 'Momentum' in gameboard[unit].abilities:
            combatSteps['AddDamage'] = combatSteps['AddDamage'] + gameboard[unit].abilities['Movement'].straightLineTraveled
            gameboard[unit].abilities['Movement'].straightLineTraveled = 0
        if 'HeavyBolts' in gameboard[unit].abilities and self.getDistance(unit,target) > 1:
            combatSteps['AttackMods']['ForcedMovement'] = True
            
        if 'BladeDance' in gameboard[unit].abilities:
            if gameboard[unit].lastAction == 'Movement':
                combatSteps['AttackMods']['Swift'] = True
                
        if 'Incision' in gameboard[unit].abilities:
            if combatSteps['HitResult'] >= combatSteps['EvasionResult'] + 3:
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + 2
                
        if 'Tranquility' in gameboard[unit].abilities:
            if not [x for x in gameboard[unit].adjacentSpaces() if type(gameboard[unit]).__name__ == 'Unit']:
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + 1
                combatSteps['AddHit'] = combatSteps['AddHit'] + 3
                
        if 'Scattershot' in gameboard[unit].abilities:
            if self.getDistance(target,unit) > 1:
                spaces = self.directionAdjacentSpaces(self.attackDirection(unit,target),target)
                gameboard = self.combat(unit,spaces[3],gameboard)
                gameboard = self.combat(unit,spaces[5],gameboard)            
        
        return gameboard, combatSteps
        
    def passiveMods(self,unit,target,gameboard,combatSteps):
        if self.location == unit:
            if [y for y in [x for x in self.adjacentSpaces(self.location) if x in gameboard] if 'Lethargy' in gameboard[y].abilities] and 'Wounding' in combatSteps['AttackMods']:
                combatSteps['AttackMods'].remove('Wounding')
        if self.location == target:
            if [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]:
                elites = [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]
                for x in elites:
                    if gameboard[x].getDistance(target) <= gameboard[x].attunement['Water']:
                        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] - 2
            
        return gameboard,combatSteps        
    
    def hitDiceMods(self,unit,target,gameboard,combatSteps):
        # 3 or 4 push
        # 1 or 4 gain reaction: could already be coded
        # 5 or 6 add hit mod to damage
        # 2 or 3 move
        # 5 or 6 add evasion to damage
        #
        if self.weaponUpgrades['Warhammer'] >= 2:
            if combatSteps['CalcHit'] == 3 or combatSteps['CalcHit'] == 4:
                self.combatSteps['Push'] = True
        if self.weaponUpgrades['Spear'] >= 2:
            if combatSteps['CalcHit'] == 1 or combatSteps['CalcHit'] == 4:
                gameboard[unit].attributeManager.changeAttributes('Reaction',1)
        if self.weaponUpgrades['Rapier'] == 3:
            if combatSteps['CalcHit'] == 5 or combatSteps['CalcHit'] == 6:
                combatSteps['Attack'] = True
        if self.weaponUpgrades['Katana'] >= 1:
            if combatSteps['CalcHit'] == 2 or combatSteps['CalcHit'] == 3:
                combatSteps['Move'] = True
        if self.weaponUpgrades['Katana'] >= 2:
            if combatSteps['CalcHit'] == 5 or combatSteps['CalcHit'] == 6:
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + combatSteps['AddEvasion']
    
        return gameboard,combatSteps
    
    def evasionDiceMods(self,unit,target,gameboard,combatSteps):
        if self.weaponUpgrades['Spear'] >= 1:
            if combatSteps['CalcEvasion'] == 1 or combatSteps['CalcEvasion'] == 2:
                combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + gameboard[target].attributeManager.getAttributes('Hit')
        if self.weaponUpgrades['Rapier'] >= 1:
            if combatSteps['CalcEvasion'] == 1 or combatSteps['CalcEvasion'] == 2:
                combatSteps['Counter'] == True
        if self.weaponUpgrades['Greatsword'] >= 2:
            if combatSteps['CalcEvasion'] == 1:
                gameboard = gameboard[target].abilities['Block'].abilityEffect(unit,target,gameboard,combatSteps)
        return gameboard,combatSteps
    
    def movementEffects(self,unit,target,gameboard):
        return gameboard

    def createOptions(self):
        # match ability costs to available points
        # excludes passives since it matches available points to cost
        options = [x.name for x in self.abilities.values() if 'Turn' in x.cost and set(x.cost['Turn']).issubset(set(self.availablePoints()))]

        return options # this is ability names
    
class WarriorPlayer(Player):

    def __init__(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        # instantiate new units
        self.units = {'Elite':WarriorUnit('Elite','Elite1'),'Common1':WarriorUnit('Common','Common1'),\
                      'Common2':WarriorUnit('Common','Common2'),'Common3':WarriorUnit('Common','Common3'),\
                      'Common4':WarriorUnit('Common','Common4')}
        for unit in self.units:
            self.units[unit].setClass(self.playerClass,self.playerID,self.captureCost)
    
#    def turn(self,gameboard,players):
#        # while not passed keep going
#
#        unitChoices = {x:gameboard.get(x) for x in gameboard.keys() if type(gameboard[x]).__name__ == 'Unit' and gameboard.get(x).playerID == self.playerID}
#        unitChoices['Pass'] = 'Pass'
#        
#        while True:
#            for unit in self.units:
#                self.units[unit].unitOptions = self.units[unit].createOptions()
#            unitChoice = unitChoices.get(random.choice(list(unitChoices.keys())))
#            if unitChoice == 'Pass':
#                break
#            # execute ability
#            if unitChoice.unitOptions:
#                unitChoice.abilities.get(random.choice(unitChoice.unitOptions)).execute(self.units[unit],gameboard)
#            for unit in gameboard:
#                if type(unit).__name__ == 'Unit' and unit.playerID == self.playerID:
#                    if unit.attributeManager.getAttributes('Health') <= 0:
#                        self.updateUnits(unit)
#                        del gameboard[unit]
#            # then pick an option
#        return gameboard,players
    
    # need both warriorattack and attack to differentiate a normal attack and a form attack
    # both need to access passives
     

                
#    def beginningTurnEffects(self,gameboard):
#        return gameboard
#        
    def endTurnEffects(self,gameboard):
        for x in self.units:
            if 'Rage' in self.units[x].abilities:
                self.units[x].abilities['Rage'].damage = 0
        return gameboard

# instantiate game
game = Game([WarriorPlayer('Warrior','Player1'),AssassinPlayer('Assassin','Player2'), \
      MagePlayer('Mage','Player3'),Player('Engineer','Player4')])
game.gameLoop()

# Gameflow: Players take a turn(), which initiates all options for unit selection (including Pass), 
# then all options for unitOptions(). Select a random option in unit selection, then random option for
# the unit. For each ability, need to return a random target