# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:05:33 2021

@author: bgool
"""
import random
import GeneralUse as gen
import lineOfSight as LOS

########################################
        # ENGINEER #
        ############

## TO DO: Make sure blueprints are working as intended

class EngineerMovement(gen.Movement):
    
    def availableMovement(self,unit,gameboard,origin,*effects):
        effects = effects[0]
        respawns = [x for x in gameboard if type(x).__name__ == 'Respawn']
        respawnSpaces = [a for b in [gameboard[unit].adjacentSpaces(x) for x in respawns if x.player == gameboard[unit].player] for a in b]
          
        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard or type(gameboard[x]).__name__ == 'StealthToken' or x == origin]
        if 'Unrestrained' in effects:
            spaces = self.adjacentSpaces(unit)
        if set(spaces) & set(respawnSpaces):
            spaces = list(set(spaces + respawnSpaces))
            
        relays = [x for x in gameboard if type(x).__name__ == 'Relay' and gameboard[x].playerID == gameboard[unit].playerID]
        if gameboard[unit].playerClass == 'Engineer' and relays:
            relaySpaces = [a for b in [gameboard[x].adjacentSpaces() for x in relays] for a in b if a not in gameboard]  
            if set(spaces) & set(relaySpaces):
                spaces = list(set(spaces + relaySpaces))
            
        for x in spaces: 
            if x[0] < 0 or x[0] > 20 or x[1] < 0 or x[1] > 20:
                spaces.remove[x]
        spaces = spaces + gameboard[unit].addMovementSpaces(self,unit,gameboard,spaces)
            
        return spaces

    def abilityEffect(self,unit,target,gameboard,*args):
        # args is a manually input distance
        gameboard[unit].setLastAction('Movement')
        args = args[0]
        effects = []
        if 'Ability' in args:
            effects = gameboard[unit].generateMovementEffects(args['Ability'])
        else:
            effects = gameboard[unit].generateMovementEffects()
            
        # pick the number of spaces you would like to move
        if 'Distance' not in args:
            numberOfSpaces = random.choice([x for x in range(1,gameboard[unit].attributeManager.getAttributes('Movement')+1)])
        elif 'Distance' in args:
            numberOfSpaces = args['Distance']
        # pick the path you would like to move through
        if 'Direction' not in args:
            target = random.choice(self.availableMovement(unit,gameboard,unit,effects))
            for x in range(1,numberOfSpaces-2):
                target = target + random.choice(self.availableMovement(target[x],gameboard,unit,args))
        else:
            target = gameboard[unit].adjacentSpacesDir(args['Direction'])
            for x in range(1,numberOfSpaces-2):
                target = target + self.adjacentSpacesDir({'Direction':args['Direction'],'Location':target[x-1]})
        
        playerUnit = gameboard[unit]
        distance = 0
        reducedCost = 0
        # execute number of movements
        # 'target' shows path of movement
        for x in target:
            directionTraveled = self.spacesToDir(unit,target)
            if directionTraveled == self.lastDirTraveled:
                self.straightLineTraveled = self.straightLineTraveled + 1
            else:
                self.straightLineTraveled = 1
            self.lastDirTraveled = directionTraveled

            # choose another Common for Linking Module
            if 'LinkingModule' in gameboard[unit].abilities:
                adjacentCommon = random.choice([x for x in gameboard[unit].adjacentSpaces if gameboard[x].unitType == 'Common' and gameboard[x].playerID == gameboard[unit].playerID] + ['Pass'])
                commonNumberSpace = self.numberSpaceAdjacentSpaces(gameboard[unit].direction,unit)
            # choose elite if adjacent
            if 'Sidecar' in gameboard[unit].abilities:
                elite = random.choice([x for x in gameboard[unit].adjacentSpaces if gameboard[x].unitType == 'Elite' and gameboard[x].playerID == gameboard[unit].playerID][0] + ['Pass'])
                eliteNumberSpace = self.numberSpaceAdjacentSpaces(gameboard[unit].direction,unit)

            if x not in gameboard or x == unit:
                lastOpenSpace = x
                
                # will have to add alternative situation where units can travel through occupied spaces
                if adjacentCommon != 'Pass':
                    newspace = self.directionSpaces(directionTraveled,adjacentCommon)
                    if newspace not in gameboard:
                        gameboard[newspace] = gameboard[adjacentCommon]
                        del gameboard[adjacentCommon]
                if elite != 'Pass':
                    newspace = self.directionSpaces(directionTraveled,elite)
                    if newspace not in gameboard:
                        gameboard[newspace] = gameboard[elite]
                        del gameboard[elite]
                
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
                    
        for x in gameboard:
            if gameboard[x].name == 'Unit':
                gameboard[x].checkReaction(x,gameboard,['Any'])
        
        if 'Cost' in args:
            if args['Cost'] != 'Passive':
                gameboard[unit].attributeManager.changeAttributes(args['Cost'],-(distance-reducedCost))
        else:            
            gameboard[unit].attributeManager.changeAttributes('Movement',-distance)
        
        for x in range(0,len(target)+1):        
            if x <= distance:
                gameboard = gameboard[unit].movementEffects(unit,target[x],gameboard)
                if gameboard[target[x]].name == 'StealthToken':
                    gameboard[target[x]].stealthTokenEffect(unit,gameboard)
                    del gameboard[target[x]]
                gameboard[target[x]].direction = random.choice(self.directions)
                gameboard[target[x]].location = x
                gameboard[target[x]].getLineOfSight(gameboard)
                    
            unit = target[x]

        gameboard[lastOpenSpace] = playerUnit
        
        return gameboard,lastOpenSpace    
    
class Railgun:
    name = 'Railgun'
    BPcost = 1
    
    def blueprintEffect(self,gameboard,unit):
        self.blueprintEnabled = True
        if 'BlueprintUpgrade' not in gameboard[unit].abilities:
            bpeffect = 1
        else:
            bpeffect = 2
        gameboard[unit].unitRange = gameboard[unit].unitRange + bpeffect
        # unit no longer has disadvantage on partial line of sight

class Biotechnology:
    name = 'Biotechnology'
    BPcost = 1
    
class TeslaCoil:
    name = 'TeslaCoil'
    BPcost = 1
    cost = {'Turn':['Attack']}
    
    def blueprintEffect(self,gameboard,unit):
        self.blueprintEnabled = True
        gameboard[unit].abilities['TeslaCoil'] = self
        return gameboard
        
    def abilityEffect(self, unit,target,gameboard):
        if 'BlueprintUpgrade' not in gameboard[unit].abilities:
            bpeffect = 1
        else:
            bpeffect = 2
        targets = self.getAOETargets(1,unit,gameboard)
        for x in targets:
            gameboard = self.combat(unit,target,gameboard,{'Damage':bpeffect,'Wounding':True,'Piercing':True})
        return gameboard        
    
class PulseCannon:
    name = 'PulseCannon'
    BPcost = 1
    cost = {'Turn':'Attack'}
    
    def blueprintEffect(self,gameboard,unit):
        self.blueprintEnabled = True
        gameboard[unit].abilities['PulseCannon'] = self
    
    def abilityEffect(self,unit,target,gameboard):
        if 'BlueprintUpgrade' not in gameboard[unit].abilities:
            bpeffect = 3
        else:
            bpeffect = 4
        if gameboard[target].playerID != gameboard[unit].playerID:
            self.combat(unit,target,gameboard)
        self.forcedMovement(bpeffect, gameboard[unit].direction, target, gameboard)
        return gameboard
    
class Thrusters:
    name = 'Thrusters'
    BPcost = 1
    
    def blueprintEffect(self,gameboard,unit):
        if 'BlueprintUpgrade' not in gameboard[unit].abilities:
            bpeffect = 2
        else:
            bpeffect = 3
        self.blueprintEnabled = True
        gameboard[unit].attributeManager.permBonusAttr['Movement'] = gameboard[unit].attributeManager.permBonusAttr['Movement'] + bpeffect
        # units can also move through occupied spaces
        
class ResponseProtocols:
    name = 'ResponseProtocols'
    BPcost = 1
    
    def blueprintEffect(self,gameboard,unit):
        if 'BlueprintUpgrade' not in gameboard[unit].abilities:
            bpeffect = 1
        else:
            bpeffect = 2
        self.blueprintEnabled = True
        gameboard[unit].attributeManager.permBonusAttr['Reaction'] = gameboard[unit].attributeManager.permBonusAttr['Reaction'] + bpeffect
        elite = [x for x in gameboard if gameboard[x].unitType == 'Elite' and gameboard[x].playerID == gameboard[unit].playerID]
        reactionAbilities = [x for x in gameboard[elite].abilities if 'Reaction' in gameboard[elite].abilities[x].cost]
        for x in reactionAbilities:
            gameboard[unit].abilities[x] = gameboard[elite].abilities[x]
        return gameboard
    
class Twinmount:
    name = 'Twinmount'
    BPcost = 2

    def blueprintEffect(self,gameboard,unit):
        if 'BlueprintUpgrade' not in gameboard[unit].abilities and 'UpgradeVersion20' not in gameboard[unit].abilities:
            bpeffect = 1
        else:
            bpeffect = 2
        self.blueprintEnabled = True
        gameboard[unit].attributeManager.permBonusAttr['Attack'] = gameboard[unit].attributeManager.permBonusAttr['Attack'] + bpeffect
 
class EnhancedAI:
    name = 'EnhancedAI'
    BPcost = 2

    def blueprintEffect(self,gameboard,unit):
        if 'BlueprintUpgrade' not in gameboard[unit].abilities and 'UpgradeVersion20' not in gameboard[unit].abilities:
            bpeffect = 1
        else:
            bpeffect = 2
        self.blueprintEnabled = True
        gameboard[unit].attributeManager.permBonusAttr['Special'] = gameboard[unit].attributeManager.permBonusAttr['Special'] + bpeffect
        elite = [x for x in gameboard if gameboard[x].unitType == 'Elite' and gameboard[x].playerID == gameboard[unit].playerID][0]
        specialAbilities = [x for x in gameboard[elite].abilities if 'Special' in gameboard[elite].abilities[x].cost]
        for x in specialAbilities:
            gameboard[unit].abilities[x] = gameboard[elite].abilities[x]
        return gameboard
        
class CloakingDevice:
    name = 'CloakingDevice'
    BPcost = 2
    
    def blueprintEffect(self,gameboard,unit):
        if 'BlueprintUpgrade' not in gameboard[unit].abilities and 'UpgradeVersion20' not in gameboard[unit].abilities:
            bpeffect = 2
        else:
            bpeffect = 3
        gameboard[unit].attributeManager.permBonusAttr['Evasion'] = gameboard[unit].attributeManager.permBonusAttr['Armor'] + bpeffect
        # advantage on evasion rolls
        
class GeomorphicEngine:
    name = 'GeomorphicEngine'
    BPcost = 2
    
    def blueprintEffect(self,gameboard,unit):
        gameboard[unit].abilities['GeomorphicEngine'] = self
        gameboard[unit].attributeManager.permBonusAttr['Movement'] = gameboard[unit].attributeManager.permBonusAttr['Movement'] - 4
        gameboard[unit].attributeManager.permBonusAttr['Armor'] = gameboard[unit].attributeManager.permBonusAttr['Armor'] + 1

    def abilityEffect(self,unit,target,gameboard):
        if 'BlueprintUpgrade' not in gameboard[unit].abilities and 'UpgradeVersion20' not in gameboard[unit].abilities:
            bpeffect = 4
        else:
            bpeffect = 5
        movetarget = random.choice([x for x in self.getAOETargets(bpeffect,unit,gameboard) if gameboard[x].unitType == 'Obstacle' or gameboard[x].built == True])
        newspace = random.choice(self.getAOETargets(bpeffect,unit,gameboard))
        gameboard[newspace] = gameboard[movetarget]
        del gameboard[movetarget]
        return gameboard
    
class ReinforcedFrame:
    name = 'EnhancedFrame'
    BPcost = 3
    
    def blueprintEffect(self,gameboard,unit):
        self.blueprintEnabled = True
        gameboard[unit].attributeManager.permBonusAttr['Health'] = gameboard[unit].attributeManager.permBonusAttr['Health'] + 4

class TeleportNode:
    name = 'TeleportNode'
    BPcost = 3
    
    def blueprintEffect(self,gameboard,unit):
        gameboard[unit].aura = 'Relay'
        return gameboard

class Tank:
    name = 'Tank'
    BPcost = 4

    def blueprintEffect(self,gameboard,unit):
        self.blueprintEnabled = True
        gameboard[unit].attributeManager.permBonusAttr['Armor'] = gameboard[unit].attributeManager.permBonusAttr['Armor'] + 2
        gameboard[unit].attributeManager.permBonusAttr['Movement'] = gameboard[unit].attributeManager.permBonusAttr['Armor'] - 1
        gameboard[unit].attributeManager.permBonusAttr['Evasion'] = gameboard[unit].attributeManager.permBonusAttr['Armor'] - 2

class StateOfTheArt:
    name = 'StateOfTheArt'
    BPcost = 5

class PlasmaCannon:
    name = 'PlasmaCannon'
    BPcost = 6
    
    def blueprintEffect(self,gameboard,unit):
        gameboard[unit].attributeManager.permBonusAttr['Damage'] = gameboard[unit].attributeManager.permBonusAttr['Damage'] + 5
        gameboard[unit].attributeManager.permBonusAttr['Attack'] = gameboard[unit].attributeManager.permBonusAttr['Attack'] -1
        gameboard[unit].unitRange = gameboard[unit].unitRange + 2

class Dreadnought:
    name = 'Dreadnought'
    BPcost = 8

class PowerArmor:
    name = 'PowerArmor' 
    BPcost = 3

    def blueprintEffect(self,gameboard,unit):
        gameboard[unit].attributeManager.permBonusAttr['Damage'] = gameboard[unit].attributeManager.permBonusAttr['Damage'] + 3
        gameboard[unit].attributeManager.permBonusAttr['Armor'] = gameboard[unit].attributeManager.permBonusAttr['Armor'] + 2
        gameboard[unit].attributeManager.permBonusAttr['Movement'] = gameboard[unit].attributeManager.permBonusAttr['Movement'] + 2           

class Jetpack:
    name = 'Jetpack' 
    BPcost = 3
    
    def blueprintEffect(self,gameboard,unit):
        gameboard[unit].attributeManager.permBonusAttr['Movement'] = gameboard[unit].attributeManager.permBonusAttr['Movement'] + 4           
        gameboard[unit].attributeManager.permBonusAttr['Evasion'] = gameboard[unit].attributeManager.permBonusAttr['Evasion'] + 3           

class WeaponsSystem:
    name = 'WeaponsSystem' 
    BPcost = 3

    def blueprintEffect(self,gameboard,unit):
        gameboard[unit].attributeManager.permBonusAttr['Hit'] = gameboard[unit].attributeManager.permBonusAttr['Hit'] + 4
        gameboard[unit].unitRange = gameboard[unit].unitRange + 2

class Blueprint:
    upgrade = False
    
    blueprints = {'Railgun':Railgun(),'Biotechnology':Biotechnology(),'TeslaCoil':TeslaCoil(),
                  'PulseCannon':PulseCannon(),'Thrusters':Thrusters(),'ResponseProtocols':ResponseProtocols(),
                  'Twinmount':Twinmount(), 'EnhancedAI':EnhancedAI(),'CloakingDevice':CloakingDevice(),
                  'GeomorphicEngine':GeomorphicEngine(), 'ReinforcedFrame':ReinforcedFrame(),'TeleportNode':TeleportNode(),
                  'Tank':Tank(), 'StateOfTheArt':StateOfTheArt(), 'PlasmaCannon': PlasmaCannon(), 'Dreadnought':Dreadnought()}
    
    blueprintCost = {1: ['Railgun','Biotechnology','TeslaCoil','PulseCannon','Thrusters','ResponseProtocols'],
            2: ['Twinmount','EnhancedAI','CloakingDevice','GeomorphicEngine'],
            3: ['ReinforcedFrame','TeleportNode'],
            4: ['Tank'],
            5: ['StateOfTheArt'],
            6: ['PlasmaCannon'],
            8: ['Dreadnought']
                }
    
    blueprintCostReduced = {1: ['Railgun','Biotechnology','TeslaCoil','PulseCannon','Thrusters','ResponseProtocols','Twinmount','EnhancedAI','CloakingDevice','GeomorphicEngine'],
            3: ['ReinforcedFrame','TeleportNode'],
            4: ['Tank'],
            5: ['StateOfTheArt'],
            6: ['PlasmaCannon'],
            8: ['Dreadnought']
                }
    
    blueprintNamesToCost = {
            'Railgun':1,
            'Biotechnology':1,
            'TeslaCoil':1,
            'PulseCannon':1,
            'Thrusters':1,
            'ResponseProtocols':1,
            'Twinmount':2,
            'EnhancedAI':2,
            'CloakingDevice':2,
            'GeomorphicEngine':2,
            'ReinforcedFrame':3,
            'TeleportNode':3,
            'Tank':4,
            'StateOfTheArt':5,
            'PlasmaCannon':6,
            'Dreadnought':8
            }
    
    blueprintNamesToCostReduced = {
            'Railgun':1,
            'Biotechnology':1,
            'TeslaCoil':1,
            'PulseCannon':1,
            'Thrusters':1,
            'ResponseProtocols':1,
            'Twinmount':1,
            'EnhancedAI':1,
            'CloakingDevice':1,
            'GeomorphicEngine':1,
            'ReinforcedFrame':3,
            'TeleportNode':3,
            'Tank':4,
            'StateOfTheArt':5,
            'PlasmaCannon':6,
            'Dreadnought':8
            }
    
    blueprintEnabled = False
    
    def getBlueprintCost(self,unit,gameboard):
        if 'UpdateVersion20' not in gameboard[unit].abilities:
            return self.blueprintCost
        else:
            return self.blueprintCostReduced
        
    
    def blueprintEffect(self, gameboard, unit, *upgrade):
        self.blueprintEnabled = True
        return gameboard
    
    def removeBlueprint(self,unitObj):
        self.blueprintEnabled = False
        return unitObj

class Build(gen.Ability):
    
    unusedBlueprints = 3
    
    name = 'Build' 
    cost = {'Turn':['Special']}
    buildChoice = 'None'
    numCommons = 5
    Blueprints = Blueprint()
    
    def getTargets(self,unit,gameboard):
        return [x for x in self.adjacentSpaces(unit) if x not in gameboard and x in gen.boardLocations]
    
    def buildCommon(self,unit,target,gameboard,unitObj):
        gameboard[target] = unitObj
        while True:
            
            # pick cost
            if 'UpdateVersion20' not in gameboard[unit].abilities:
                selectCost = random.choice([x for x in [0,1,2,3,4,5,6,8] if x <= self.unusedBlueprint])
            else:
                selectCost = random.choice([x for x in [0,1,3,4,5,6,8] if x <= self.unusedBlueprint])

            if selectCost == 0:
                break
            # pick blueprint name
            addBlueprint = random.choice(self.Blueprints.getBlueprintCost(unit,gameboard)[selectCost])
            # subtract cost from all units with Build ability
            self.unusedBlueprints = self.unusedBlueprints - selectCost
            for x in [x for x in gameboard if 'Build' in gameboard[x].abilities]:
                gameboard[x].abilities['Build'].unusedBlueprints = gameboard[x].abilities['Build'].unusedBlueprints - selectCost
            # add cost to unit blueprint cost to keep track of blueprints
            gameboard[target].numBlueprints = gameboard[target].numBlueprints + selectCost
            # add blueprint to unit
            gameboard[target].unitBlueprints[addBlueprint] = self.Blueprints[addBlueprint]
            # initialize blueprint
            gameboard = gameboard[target].unitBlueprints[addBlueprint].blueprintEffect(gameboard,target)
            
        return gameboard
            
    def buildObstacle(self,unit,target,gameboard):
        # Build costs a Special point. The individual build abilities are passive
        selectObstacle = random.choice([x for x in gameboard[unit].Obstacles if x in gameboard[unit].abilities])
        gameboard = gameboard[unit].abilities[selectObstacle].abilityEffect(unit,target,gameboard)
        return gameboard
    
    def abilityEffect(self,unit,target,gameboard):
        numCommons = len([x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == self.playerID])
        if numCommons < self.numCommons:
            buildChoice = random.choice(['Common','Obstacle'])
        else:
            buildChoice = 'Obstacle'
        if buildChoice == 'Obstacle':
            gameboard = self.buildObstacle(unit,target,gameboard)
        elif buildChoice == 'Common':
            common = random.choice([a for a in self.units if a not in [gameboard[x].unitName for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == self.playerID]])
            gameboard = self.buildCommon(unit,target,gameboard,self.units[common])
        return gameboard

# Tier 0
class PlaceRelay:
    name = 'PlaceRelay'
    cost = {'Passive':['Passive']}
    
    def abilityEffect(self,unit,target,gameboard):
        respawnSpaces = [a for b in [self.adjacentSpaces(x) for x in gameboard if gameboard[x].name == 'Respawn'] for a in b if a not in gameboard]

        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard and x not in respawnSpaces]
        if spaces:
            target = random.choice(spaces)
            gameboard[target] = Relay(gameboard[unit].playerID,target)
        return gameboard

class Relay(gen.Obstacle):
    name = 'Relay'
    aura = 'Relay'
    
    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location
        
class PlaceWall(gen.Ability):
    name = 'PlaceWall'
    cost = {'Passive':['Passive']}
    
    def abilityEffect(self,unit,target,gameboard):
        respawnSpaces = [a for b in [self.adjacentSpaces(x) for x in gameboard if gameboard[x].name == 'Respawn'] for a in b if a not in gameboard]

        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard and x not in respawnSpaces]
        if spaces:
            target = random.choice(spaces)
            gameboard[target] = Wall(gameboard[unit].playerID,target)
        return gameboard
        
class Wall(gen.Obstacle):
    name = 'Wall'

    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location

class PlaceTurret(gen.Ability):
    name = 'PlaceTurret'
    cost = {'Passive':['Passive']}
    damage = {1:2,2:2,3:3,4:3,5:3,6:3,7:3,8:3,9:4,10:4}
    
    def abilityEffect(self,unit,target,gameboard):
        respawnSpaces = [a for b in [self.adjacentSpaces(x) for x in gameboard if gameboard[x].name == 'Respawn'] for a in b if a not in gameboard]

        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard and x not in respawnSpaces]
        if spaces:
            target = random.choice(spaces)
            gameboard[target] = Turret(gameboard[unit].playerID,target,self.damage[gameboard[unit].levelManager.level])
        return gameboard

class TurretAttack(gen.Attack):
    name = 'TurretAttack'
    cost = {'Turn':['Attack'],'Reaction':['Reaction']}
    state = ['Any']

    def abilityEffect(self,unit,target,gameboard):
        return self.combat(unit,target,gameboard) 
        
    def getTargets(self,unit,gameboard,*args):
        if 'RotatingMount' not in gameboard[unit].abilities:
            return self.getLOSTargets(unit,gameboard)

        else:
            return self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location,gameboard)
     
class Turret(gen.Obstacle,gen.Unit):
    name = 'Turret'
    unitName = 'Turret'
    unitRange = 2
    
    def __init__(self,playerID,location,damage):
        self.playerID = playerID
        self.location = location
        self.abilities = {'TurretAttack':TurretAttack(playerID),'Movement':gen.Movement(playerID)}
        for x in self.abilities:
            self.abilities[x].unitName = self.unitName
        self.attributeManager = gen.AttributeManager({'Health':0,'Attack':1,'Movement':0,'Special':0,'Reaction':1,'Damage':damage,'Evasion':0,'Hit':1,'Armor':0})
        
    def getRange(self):
        return self.unitRange
            
class TeleportModule(gen.Ability):
    name = 'TeleportModule'
    cost = {'Turn':['Special'],'Reaction':['Reaction']}
    state = ['Any']
    
    def abilityEffect(self,unit,target,gameboard):
        relays = [x for x in [x for x in gameboard if hasattr(gameboard[x],'aura')] if gameboard[x].aura == 'Relay']
        target = random.choice([a for b in [self.adjacentSpaces(x) for x in relays] for a in b])
        gameboard[target] = gameboard[unit]
        del gameboard[unit]
        return gameboard
        
class MaterialRecall(gen.Ability):
    name = 'MaterialRecall'
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        target = random.choice([x for x in self.adjacentSpaces() if gameboard[x].playerID == self.playerID and gameboard[x].unitType != 'Elite'])
        if hasattr(gameboard[target], 'numBlueprints'):
            gameboard[unit].unusedBlueprints = gameboard[unit].unusedBlueprints + gameboard[target].numBlueprints
        del gameboard[target]
        return gameboard

        
class ManualOverride(gen.Ability):
    name = 'ManualOverride'
    cost = {'Passive':['Passive']}
    # If adjacent to your Elite, Commons may use your Elite's Reaction points as if it were their own.  
    
# Tier 1 2+
class Repair(gen.Ability):
    name = 'Repair'
    cost = {'Turn':['Special'],'Reaction':['Reaction']}
    state = ['Any']
    # add reaction
    def getTargets(self,unit,gameboard):
        targets = [x for x in self.adjacentSpaces(unit) if x in gameboard and gameboard[x].playerID == gameboard[unit].playerID and gameboard[x].name == 'Unit']
        # print('Targets:' + str(targets))
        # print('Unit:' + str(unit))
        return targets
    
    def abilityEffect(self,unit,target,gameboard,*combatSteps):
        gameboard[target].attributeManager.changeAttributes('Health',2)
        if gameboard[target].attributeManager.currentAttributes['Health'] > gameboard[target].maxHealth:
            gameboard[target].attributeManager.currentAttributes['Health'] = gameboard[target].maxHealth
        if combatSteps:
            return gameboard,combatSteps
        else:
            return gameboard
    
class PlaceMedbay(gen.Ability):
    name = 'PlaceMedbay'
    cost = {'Passive':['Passive']}
    auraRange = 2
    
    def abilityEffect(self,unit,target,gameboard):
        respawnSpaces = [a for b in [self.adjacentSpaces(x) for x in gameboard if gameboard[x].name == 'Respawn'] for a in b if a not in gameboard]

        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard and x not in respawnSpaces]
        if spaces:
            target = random.choice(spaces)
            gameboard[target] = Medbay(gameboard[unit].playerID,target)
        return gameboard
    
class Medbay(gen.Obstacle):
    name = 'Medbay'
    auraRange = 2
    aura = 'Medbay'

    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location
    
    def getAuraRange(self):
        return self.auraRange

class GrapplingHook(gen.Ability):
    name = 'GrapplingHook'
    cost = {'Turn':['Movement']}
    # need to code something to not use the ability in a nonideal manner        
    def abilityEffect(self,unit,target,gameboard):
        direction = random.choice(self.directions)
        targets = self.straightLine(4,random.choice(self.LOSDirections(direction)),unit,gameboard)
        newspace = unit
        # is this working as intended?
        for x in range(1,5):
            if x < len(targets):
                if targets[x] in gameboard:
                    newspace = targets[x-1]  
        if newspace == unit:
            return gameboard
        gameboard[newspace] = gameboard[unit]
        gameboard[newspace].location = newspace
        del gameboard[unit]
        
        return gameboard

class Armory(gen.Obstacle):
    name = 'Armory'
    auraRange = 3
    aura = 'Armory'

    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location 
    
    def getAuraRange(self):
        return self.auraRange
        
class PlaceArmory(gen.Ability):
    name = 'PlaceArmory'
    cost = {'Passive':['Passive']}
    auraRange = 3

    def abilityEffect(self,unit,target,gameboard):
        respawnSpaces = [a for b in [self.adjacentSpaces(x) for x in gameboard if gameboard[x].name == 'Respawn'] for a in b if a not in gameboard]

        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard and x not in respawnSpaces]
        if spaces:
            target = random.choice(spaces)
            gameboard[target] = Armory(gameboard[unit].playerID,target)
        return gameboard
    
class Recycling(gen.Ability):
    name = 'Recycling'
    cost = {'Reaction':['Reaction']}
    state = ['EliminatedCommon']
    buildOptions = ['Relay','Armory','Turret','Medbay','Bunker','EMPTower','RadarTower','Wall']
    
    def abilityEffect(self,unit,target,gameboard):
        buildoption = random.choice(list(set(self.buildOptions).intersection(set(gameboard[unit].abilities))))
        gameboard[target] = gameboard[unit].abilities[buildoption]
        return gameboard
    
# Tier 2 4+
class Bunker(gen.Obstacle):
    name = 'Bunker'
    aura = 'Bunker'
    auraRange = 3

    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location 
    
    def getAuraRange(self):
        return self.auraRange

class PlaceBunker(gen.Ability):
    name = 'PlaceBunker'
    cost = {'Passive':['Passive']}
    auraRange = 3

    def abilityEffect(self,unit,target,gameboard):
        respawnSpaces = [a for b in [self.adjacentSpaces(x) for x in gameboard if gameboard[x].name == 'Respawn'] for a in b if a not in gameboard]

        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard and x not in respawnSpaces]
        if spaces:
            target = random.choice(spaces)
            gameboard[target] = Bunker(gameboard[unit].playerID,target)
        return gameboard
    
class IncreasedRange(gen.Ability):
    name = 'IncreasedRange'
    cost = {'Passive':['Passive']}
    
    def initAbility(self,gameboard):
        return gameboard            

class Grenade(gen.Ability):
    name = 'Grenade'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        
        for i in range(0,3):
            spaces = list(set([a for b in [self.adjacentSpaces(x) for x in self.adjacentSpaces(unit)] for a in b]))        
        return spaces
    
    def abilityEffect(self,unit,target,gameboard):
        if target in gameboard:
            gameboard = self.combat(unit,target,gameboard,{'Wounding':True,'Damage':2})
        outertargets = [x for x in self.getAOETargets(1,target,gameboard) if x in gameboard]
        for x in outertargets:
            if x in gameboard:
                gameboard = self.dealIndirectDamage(target,x,gameboard,1,self.playerID,{'Wounding':True})
        return gameboard
        
class Sidecar(gen.Ability):
    name = 'Sidecar'
    cost = {'Passive':['Passive']}
    # check
    
class MechanicalArmy(gen.Ability):
    name = 'MechanicalArmy'
    cost = {'Passive':['Passive']}
    # check
                
# Tier 3 6+            
class AuraUpgrade(gen.Ability):
    name = 'AuraUpgrade'
    aura = 'AuraUpgrade'
    cost = {'Passive':['Passive']}

    def initAbility(self,gameboard):
        return gameboard               

class UrbanUpgrade(gen.Ability):
    name = 'UrbanUpgrade'
    cost = {'Passive':['Passive']}

    def initAbility(self,gameboard):
        return gameboard   
                
class RemoteConstruction(gen.Ability):
    name = 'RemoteConstruction'
    cost = {'Passive':['Passive']}
                
class Extension(gen.Ability):
    name = 'Extension'
    cost = {'Passive':['Passive']}

class EMPTower(gen.Obstacle):
    name = 'EMPTower'
    aura = 'EMPTower'
    auraRange = 3
    
    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location   
                
class PlaceEMPTower(gen.Ability):
    name = 'PlaceEMPTower'
    cost = {'Passive':['Passive']}
    auraRange = 4

    def abilityEffect(self,unit,target,gameboard):
        respawnSpaces = [a for b in [self.adjacentSpaces(x) for x in gameboard if gameboard[x].name == 'Respawn'] for a in b if a not in gameboard]

        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard and x not in respawnSpaces]
        if spaces:
            target = random.choice(spaces)
            gameboard[target] = EMPTower(gameboard[unit].playerID,target)
        return gameboard
    
class RadarTower(gen.Obstacle):
    name = 'RadarTower'
    aura = 'RadarTower'
    auraRange = 3

    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location         

    def getAuraRange(self):
        return self.auraRange

class PlaceRadarTower(gen.Ability):
    name = 'PlaceRadarTower'
    cost = {'Passive':['Passive']}
    auraRange = 3

    def abilityEffect(self,unit,target,gameboard):

        respawnSpaces = [a for b in [self.adjacentSpaces(x) for x in gameboard if gameboard[x].name == 'Respawn'] for a in b if a not in gameboard]

        spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard and x not in respawnSpaces]

        if spaces:
            target = random.choice(spaces)
            gameboard[target] = RadarTower(gameboard[unit].playerID,target)
        return gameboard
    
class MobileSecurity(gen.Ability):
    name = 'MobileSecurity'
    cost = {'Passive':['Passive']}

    def initAbility(self,gameboard,playerID):
        for x in gameboard:
            if gameboard[x].name == 'Turret' and gameboard[x].playerID == playerID:
                gameboard[x].abilities['MobileSecurity'] = self
                gameboard[x].attributeManager['Movement'] = 2
        return gameboard                      

class RotatingMount(gen.Ability):
    name = 'RotatingMount'
    cost = {'Passive':['Passive']}

    def initAbility(self,gameboard,playerID):
        for x in [x for x in gameboard if gameboard[x].name == 'Turret' and gameboard[x].playerID == playerID]:
            gameboard[x].abilities['RotatingMount'] = self
            
        return gameboard                      

class LinkingModule(gen.Ability):
    name = 'LinkingModule'
    cost = {'Passive':['Passive']}
    # check
                
# Tier 4 9+
class EfficientManufacturing(gen.Ability):
    name = 'EfficientManufacturing'
    cost = {'Passive':['Passive']}
                
class SniperTower(gen.Ability):
    name = 'SniperTower'
    cost = {'Passive':['Passive']}
    
    def initAbility(self,gameboard,playerID):
        for x in [x for x in gameboard if gameboard[x].name == 'Turret' and gameboard[x].playerID == playerID]:
            gameboard[x].abilities['SniperTower'] = self
        return gameboard                     

class MaterialResearch(gen.Ability):
    name = 'MaterialResearch'
    cost = {'Passive':['Passive']}
    
    def initAbility(self,gameboard,playerID):
        buildoptions = ['Relay','Armory','Turret','Medbay','Bunker','EMPTower','RadarTower','Wall']
        for x in [x for x in gameboard if gameboard[x].name in buildoptions and gameboard[x].playerID == playerID]:
            gameboard[x].abilities['MaterialResearch'] = self
        return gameboard                     

class BlueprintUpgrade(gen.Ability):
    name = 'BlueprintUpgrade'
    cost = {'Passive':['Passive']}
    #check
                
class UpdateVersion20(gen.Ability):
    name = 'UpdateVersion20'
    cost = {'Passive':['Passive']}
    #check
    
class AutomatedCover(gen.Ability):
    name = 'AutomatedCover'
    cost = {'Passive':['Passive'],'Reaction':['Passive']}
    state = ['TakeEliteDamage']
    
    def getTargets(self,unit,gameboard):
        return random.choice([x for x in gameboard[unit].adjacentSpaces() if gameboard[x].unitType == 'Common' and gameboard[x].playerID == self.playerID])
    
    def abilityEffect(self,unit,target,gameboard,damage):
        return self.combat(unit,target,gameboard,{'Wounding':True,'Damage':damage})

class EngineerUnit(gen.Unit):
    
    name = 'Unit'
    unitClass = 'Engineer'
    unitBlueprints = {}
    numBlueprints = 0
    unusedBlueprints = 0
    aura = 'None'
    built = True
    buildOptions = ['Relay','Armory','Turret','Medbay','Bunker','EMPTower','RadarTower','Wall']
    
    def __init__(self,unitType,unitName,numBlueprints):
        super().__init__(unitType,unitName)
        # self.abilities['Movement'] = EngineerMovement(self.name,self.playerID)
        self.numBlueprints = numBlueprints
    
    # blueprint coding strategy
    # types of blueprints: add ability, change attributes, change inherent properties (teleport node)
    # the biggest change is blueprints act as dynamic abilities that come and go
    # will need separate 'remove blueprint' functions
    def eliteSetClass(self,playerClass,playerID,captureCost):
        self.playerClass = playerClass
        self.playerID = playerID
        self.levelManager = gen.LevelManager(1,playerClass,self.unitType)
        self.currentAttributes = self.levelManager.getAttributes()
        self.maxHealth = self.currentAttributes['Health']
        self.attributeManager = gen.AttributeManager(self.currentAttributes)
        self.captureCost = captureCost
        self.abilities = {'Attack':gen.Attack(playerID), 'Movement':gen.Movement(playerID), 'Reorient':gen.Reorient(playerID), 'Perception':gen.Perception(playerID),
                 'AccurateStrike': gen.AccurateStrike(playerID),'Avoid':gen.Avoid(playerID),'PurposefulDodge':gen.PurposefulDodge(playerID),'RedirectedStrike':gen.RedirectedStrike(playerID),
                 'Build': Build(playerID), 'TeleportModule':TeleportModule(playerID),'MaterialRecall':MaterialRecall(playerID),'ManualOverride':ManualOverride(playerID)}
        for x in self.abilities:
            self.abilities[x].unitName = self.unitName
        self.boardImage = gen.MySprite(self.playerClass,self.unitType)
        
    def passiveMods(self,unit,target,gameboard,combatSteps):        
        
        elite = [x for x in gameboard if type(x) is tuple and gameboard[x].unitType == 'Elite' and gameboard[x].playerID == gameboard[x].playerID]
        if elite:
            elite = elite[0]
            gameboard[elite].location = elite
        else:   
            elite = unit
        if self.location == unit:
            if [y for y in [x for x in self.adjacentSpaces(unit) if x in gameboard] if 'Lethargy' in gameboard[y].abilities] and 'Wounding' in combatSteps['AttackMods']:
                combatSteps['AttackMods'].remove('Wounding')
            if elite:
                if 'RadarTower' in gameboard[elite].abilities:
                    rt = 0
                    radarTower = [x for x in gameboard if gameboard[x].name == 'RadarTower']
                    if radarTower:
                        for x in radarTower:
                            if elite in self.getAOETargets(gameboard[x].auraRange,x,gameboard):
                                rt = 1
                            if rt:
                                combatSteps['AddHit'] = combatSteps['AddHit'] + 2
                if 'Armory' in gameboard[elite].abilities:
                    am = 0
                    armory = [x for x in gameboard if type(x) is tuple and gameboard[x].name == 'Armory']
                    if armory:
                        for x in armory:
                            if elite in self.getAOETargets(gameboard[x].auraRange,x,gameboard):
                                am = 1
                            if am:
                                combatSteps['AddDamage'] = combatSteps['AddDamage'] + 1
                                combatSteps['AddHit'] = combatSteps['AddHit'] + 1
                                break

        if self.location == target:
            if [x for x in gameboard if type(x) is tuple and 'HoarFrost' in gameboard[x].abilities]:
                elites = [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]
                for x in elites:
                    if gameboard[x].getDistance(target) <= gameboard[x].attunement['Water']:
                        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] - 2
            if elite:
                if 'RadarTower' in gameboard[elite].abilities:
                    rt = 0
                    radarTower = [x for x in gameboard if gameboard[x].name == 'RadarTower']
                    if radarTower:
                        for x in radarTower:
                            if elite in self.getAOETargets(gameboard[x].auraRange,x,gameboard):
                                rt = 1
                            if rt:
                                combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + 2
                                if 'Wounding' in combatSteps['AttackMods']:
                                    combatSteps['AttackMods'].remove('Wounding')
                                    combatSteps['CalcHit'] = 6
                                    combatSteps['AddHit'] = 0   
                                break
                if 'Bunker' in gameboard[elite].abilities:
                    bk = 0
                    bunker = [x for x in gameboard if gameboard[x].name == 'Bunker']
                    if bunker:
                        for x in bunker:
                            if elite in self.getAOETargets(gameboard[x].auraRange,x,gameboard):
                                bk = 1
                            if bk:
                                combatSteps['AddArmor'] = combatSteps['AddArmor'] + 1
                                if 'Piercing' in combatSteps['AttackMods']:
                                    combatSteps['AttackMods'].remove('Piercing')      
                                break
                        
            if 'CloakingDevice' in self.unitBlueprints:
                eva = random.randint(1,6)
                if eva > combatSteps['CalcEvasion']:
                    combatSteps['CalcEvasion'] = eva

                
        return gameboard, combatSteps

class EngineerPlayer(gen.Player):
    captureCost = 'Special'
    bluePrint = Blueprint()
    
    units = {'Elite':EngineerUnit('Elite','Elite',0),'Common1':EngineerUnit('Common','Common1',0),\
              'Common2':EngineerUnit('Common','Common2',0),'Common3':EngineerUnit('Common','Common3',0),\
              'Common4':EngineerUnit('Common','Common4',0)}

    def __init__(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        # instantiate new units
        self.units = {'Elite':EngineerUnit('Elite','Elite',0),'Common1':EngineerUnit('Common','Common1',0),\
                      'Common2':EngineerUnit('Common','Common2',0),'Common3':EngineerUnit('Common','Common3',0),\
                      'Common4':EngineerUnit('Common','Common4',0)}
        for unit in self.units:
            if self.units[unit].unitType == 'Common':
                self.units[unit].setClass(self.playerClass,self.playerID,self.captureCost)
            elif self.units[unit].unitType == 'Elite':
                self.units[unit].setClass(self.playerClass,self.playerID,self.captureCost)
                
    
    # def turn(self,gameboard,players):
    #     # while not passed keep going
    #     self.refreshPoints(gameboard)

    #     unitChoices = {x:gameboard.get(x) for x in gameboard.keys() if type(gameboard[x]).__name__ == 'Unit' and gameboard.get(x).playerID == self.playerID}
    #     unitChoices['Pass'] = 'Pass'
        
    #     while True:
    #         for unit in self.units:
    #             self.units[unit].unitOptions = self.units[unit].createOptions()
    #         unitChoice = unitChoices.get(random.choice(list(unitChoices.keys())))
    #         if unitChoice == 'Pass':
    #             break
    #         # execute ability
    #         if unitChoice.unitOptions:
    #             abilityChoice = unitChoice.abilities.get(random.choice(unitChoice.unitOptions))
    #             if abilityChoice == 'Build':
    #                 numCommons = len([x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == self.playerID])
    #                 if numCommons < 5:
    #                     buildChoice = random.choice(['Common','Obstacle'])
    #                 elif numCommons < 9 and 'MechanicalArmy' in self.abilities:
    #                     buildChoice = random.choice(['Common','Obstacle'])
    #                 else:
    #                     buildChoice = 'Obstacle'
    #                 target = unitChoice.abilities['Build'].getTargets(unitChoice.location,gameboard)
    #                 if buildChoice == 'Common':
    #                     newCommon = random.choice([self.units[x] for x in self.units if x not in unitChoices and self.units[x].unitType == 'Common'])
    #                     unitChoice.abilities['Build'].buildCommon(unitChoice.location,target,gameboard,newCommon)
    #                 elif buildChoice == 'Obstacle':
    #                     newObstacle = random.choice([x for x in unitChoice.buildOptions if x in unitChoice.abilities])
    #                     unitChoice.abilities['Build'].buildObstacle(unitChoice.location,target,gameboard,newObstacle)
    #             else:
    #                 unitChoice.abilities[abilityChoice].execute(unit,gameboard)
    #         for unit in gameboard:
    #             if type(unit).__name__ == 'Unit' and unit.playerID == self.playerID:
    #                 if unit.attributeManager.getAttributes('Health') <= 0:
    #                     self.updateUnits(unit)
    #                     del gameboard[unit]
    #         # then pick an option
    #     return gameboard, players
    
    def beginningTurnEffects(self,gameboard):
        self.Obstacles = [x for x in [Wall('Wall',self.playerID),Turret('Turret',self.playerID,2),Relay('Relay',self.playerID),Medbay('Medbay',self.playerID),
                                 Armory('Armory',self.playerID),Bunker('Bunker',self.playerID),EMPTower('EMPTower',self.playerID),RadarTower('RadarTower',self.playerID)]]
        commons = [x for x in gameboard if type(x) is tuple and gameboard[x].unitType == 'Common' and gameboard[x].playerID == self.playerID]
        elite = [x for x in gameboard if type(x) is tuple and gameboard[x].unitType == 'Elite' and gameboard[x].playerID == self.playerID]
        if elite:
            elite = elite[0]
        
        # transfer any unusedblueprints to the elite
        for x in commons:
            if gameboard[x].unusedBlueprints > 0 and elite:
                gameboard[elite].unusedBlueprints = gameboard[elite].unusedBlueprints + gameboard[x].unusedBlueprints
                gameboard[x].unusedBlueprints = 0
            elif gameboard[x].unusedBlueprints > 0:
                self.units['Elite'].unusedBlueprints = self.units['Elite'].unusedBlueprints + gameboard[x].unusedBlueprints
        
        # if unit is eliminated, remove blueprints and return to elite
        gbunits = [gameboard[x].unitName for x in gameboard if type(x) is tuple and gameboard[x].unitType == 'Common' and gameboard[x].playerID == self.playerID]
        
        for x in [a for a in self.units if a not in gbunits]:
            for bp in self.units[x].unitBlueprints:
                self.units[x] = self.units[x].unitBlueprints[bp].removeBlueprint(self.units[x])
                if 'UpdateVersion20' not in self.abilities:
                    blueprints = self.bluePrint.blueprintNamesToCost[bp] 
                elif 'UpdateVersion20' in self.abilities:
                    blueprints = self.bluePrint.blueprintNamesToCostReduced[bp]
                self.units['Elite'].unusedBlueprints = self.units['Elite'].unusedBlueprints + blueprints
            self.units[x].unitBlueprints = {}
        
        return gameboard
    
    def endTurnEffects(self,gameboard):
        units = [x for x in gameboard if type(x) is tuple and gameboard[x].playerID == self.playerID and gameboard[x].unitType == 'Common']
        if [x for x in units if 'Biotechnology' in gameboard[x].unitBlueprints]:
            for x in [x for x in units if 'Biotechnology' in gameboard[x].unitBlueprints]:
                if 'BlueprintUpgrade' not in gameboard[x].abilities:
                    bpeffect = 2
                else:
                    bpeffect = 3
                gameboard[x].attributeManager.changeAttributes('Health',bpeffect)
                if gameboard[x].attributeManager.getAttributes('Health') > gameboard[x].maxHealth:
                    gameboard[x].attributeManager.currentAttributes['Health'] = gameboard[x].maxHealth

        if 'Medbay' in self.units['Elite'].abilities:
            elite = [x for x in gameboard if type(x) is tuple and gameboard[x].name == 'Unit' and gameboard[x].unitName == 'Elite' and gameboard[x].playerID == self.playerID]
            medbay = [x for x in gameboard if type(x) is tuple and gameboard[x].name == 'Medbay' and gameboard[x].playerID == self.playerID]
            if elite and medbay:
                self.units['Elite'].location = elite[0]
                for mb in medbay:
                    if elite in self.getAOETargets(gameboard[mb].getAuraRange(),self.units['Elite'].location,gameboard):
                        gameboard[elite] = self.units['Elite'].maxHealth
            else:
                self.units['Elite'].location = 'None'
        return gameboard
    
    def respawnUnits(self,gameboard):
        # finds units not in gameboard but in player unit list
        respawnPoints = [b for c in [self.adjacentSpaces(a) for a in [x for x in gameboard if type(x) is tuple and gameboard[x].name == 'Respawn' and gameboard[x].playerID == self.playerID]] for b in c]
        respawnPoints = [x for x in respawnPoints if x in self.boardLocations and x not in gameboard]
        gameboardUnits = [gameboard[x].unitName for x in gameboard if type(x) is tuple and gameboard[x].playerID == self.playerID and gameboard[x].unitName == 'Elite']
        units = []
        if 'Elite' not in gameboardUnits:
            units = ['Elite']

        if self.level > 1:
            if respawnPoints:
                if 'Elite' in units:
                    location = random.choice(respawnPoints)
                    gameboard = self.addUnit(self.units['Elite'], location , gameboard)
                    gameboard[location].direction = random.choice(self.directions)
        elif self.level == 1:
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

        return gameboard
    
    def tier1(self):
        return {'Repair':Repair(self.playerID),'Medbay':PlaceMedbay(self.playerID),'GrapplingHook':GrapplingHook(self.playerID),'Armory':PlaceArmory(self.playerID),'Recycling':Recycling(self.playerID)}
    def tier2(self):
        return {'Bunker':PlaceBunker(self.playerID), 'Grenade':Grenade(self.playerID), 'Sidecar':Sidecar(self.playerID), 'MechanicalArmy':MechanicalArmy(self.playerID)}
    def tier3(self):
        return {'AuraUpgrade':AuraUpgrade(self.playerID),'UrbanUpgrade':UrbanUpgrade(self.playerID),'AutomatedCover':AutomatedCover(self.playerID),'RemoteConstruction':RemoteConstruction(self.playerID),'Extension':Extension(self.playerID),\
                'EMPTower':PlaceEMPTower(self.playerID),'RadarTower':PlaceRadarTower(self.playerID),'MobileSecurity':MobileSecurity(self.playerID),'RotatingMount':RotatingMount(self.playerID),'LinkingModule':LinkingModule(self.playerID)}
    def tier4(self):
        return {'EfficientManufacturing':EfficientManufacturing(self.playerID),'SniperTower':SniperTower(self.playerID),'MaterialResearch':MaterialResearch(self.playerID)}
    
    def availableAbilities(self):
        if self.level < 4:
            return {x:self.tier1().get(x) for x in self.tier1() if x not in self.abilities}
        elif self.level < 6:
            options = {**self.tier1(),**self.tier2()}
            return {x:options.get(x) for x in options if x not in self.abilities}
        elif self.level < 9:
            options = {**self.tier1(),**self.tier3()}
            return {x:options.get(x) for x in options if x not in self.abilities}
        elif self.level >= 9:
            options = {**self.tier1(),**self.tier4(),**self.tier3()}
            return {x:options.get(x) for x in options if x not in self.abilities}


# gameboard = {(0,0):EngineerUnit('Elite','Elite',0),(1,1):EngineerUnit('Common','Common1',0)}
# repair = Repair('test')
# test = repair.getTargets((0,0),gameboard)