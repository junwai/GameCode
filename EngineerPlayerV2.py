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
        targets = [x for x in self.getAOETargets(1,unit) if x in gameboard]
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
        movetarget = random.choice([x for x in self.getAOETargets(bpeffect,unit) if gameboard[x].unitType == 'Obstacle' or gameboard[x].built == True])
        newspace = random.choice([x for x in self.getAOETargets(bpeffect,unit) if x not in gameboard])
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
    
    blueprintEnabled = False
    
    def getBlueprintCost(self,unit,gameboard):
        if 'UpdateVersion20' not in gameboard[unit].abilities:
            return self.blueprintCost
        else:
            return self.blueprintCostReduced
        
    
    def blueprintEffect(self, gameboard, unit, *upgrade):
        self.blueprintEnabled = True
        return gameboard
    
    def removeBlueprint(self,gameboard,unit):
        self.blueprintEnabled = False
        return gameboard

class Build(gen.Ability):
    
    unusedBlueprints = 3
    
    name = 'Build' 
    cost = {'Turn':'Special'}
    buildChoice = 'None'
    numCommons = 5
    Blueprints = Blueprint()
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard and x in gen.boardLocations]
    
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
        selectObstacle = random.choice([x for x in gameboard[unit].Obstacles if x in gameboard[unit].abilities])
        gameboard[target] = selectObstacle
        return gameboard
    
    def abilityEffect(self,unit,target,gameboard):
        numCommons = len([x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == self.playerID])
        if numCommons < self.numCommons:
            self.buildChoice = random.choice(['Common','Obstacle'])
        else:
            self.buildChoice = 'Obstacle'

        return gameboard

# Tier 0
class PlaceRelay:
    name = 'PlaceRelay'
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
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
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
        gameboard[target] = Wall(gameboard[unit].playerID,target)
        return gameboard
        
class Wall(gen.Obstacle):
    name = 'Wall'

    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location

class PlaceTurret(gen.Ability):
    name = 'PlaceTurret'
    cost = {'Turn':['Special']}
    damage = {1:2,2:2,3:3,4:3,5:3,6:3,7:3,8:3,9:4,10:4}
    
    def abilityEffect(self,unit,target,gameboard):
        target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
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
            return self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location)
     
class Turret(gen.Obstacle,gen.Unit):
    name = 'Turret'
    unitRange = 2
    
    def __init__(self,playerID,location,damage):
        self.playerID = playerID
        self.location = location
        self.abilities = {'TurretAttack':TurretAttack(self.name,playerID),'Movement':gen.Movement(self.name,playerID)}
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
    cost = ['Special']
    
    def abilityEffect(self,unit,target,gameboard):
        target = random.choice([x for x in self.adjacentSpaces() if gameboard[x].playerID == self.playerID and gameboard[x].unitType != 'Elite'])
        if hasattr(gameboard[target], 'numBlueprints'):
            gameboard[unit].unusedBlueprints = gameboard[unit].unusedBlueprints + gameboard[target].numBlueprints
        del gameboard[target]
        return gameboard

        
class ManualOverride(gen.Ability):
    name = 'ManualOverride'
    cost = {'Turn':['Passive']}
    # If adjacent to your Elite, Commons may use your Elite's Reaction points as if it were their own.  
    
# Tier 1 2+
class Repair(gen.Ability):
    name = 'Repair'
    cost = {'Turn':['Special'],'Reaction':['Reaction']}
    state = ['Any']
    # add reaction
    def getTargets(self,unit,gameboard):
        return random.choice([x for x in self.adjacentSpaces(unit)])
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target].attributeManager.changeAttributes['Health',2]
        if gameboard[target].attributeManager.currentAttributes['Health'] > gameboard[target].maxHealth:
            gameboard[target].attributeManager.currentAttributes['Health'] = gameboard[target].maxHealth
        return gameboard
    
class PlaceMedbay(gen.Ability):
    name = 'PlaceMedbay'
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
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
        targets = self.straightLine(4,self.LOSDirections(direction),unit,gameboard)
        oldspace = unit
        for x in range(1,5):
            newspace = [y for y in targets if self.getDistance(unit,y) == x][0]
            if x>1:
                oldspace = newspace[x]
            if newspace in gameboard and x>1:
                gameboard[newspace] = gameboard[oldspace]
                del gameboard[oldspace]
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
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        target = random.choice([x for x in gameboard[unit].adjacentSpaces(gameboard[unit].location) if x not in gameboard])
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
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
        gameboard[target] = Bunker(gameboard[unit].playerID,target)
        return gameboard
    
class IncreasedRange(gen.Ability):
    name = 'IncreasedRange'
    cost = {'Turn':['Passive']}
    
    def initAbility(self,gameboard):
        return gameboard            

class Grenade(gen.Ability):
    name = 'Grenade'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return [x for x in self.getAOETargets(3,unit) if x not in gameboard]
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.combat(unit,target,gameboard,{'Wounding':True,'Damage':2})
        outertargets = [x for x in self.getAOETargets(1,target) if x in gameboard]
        for x in outertargets:
            gameboard = self.combat(unit,target,gameboard,{'Wounding':True,'Damage':1})
        return gameboard
        
class Sidecar(gen.Ability):
    name = 'Sidecar'
    cost = {'Turn':['Passive']}
    # check
    
class MechanicalArmy(gen.Ability):
    name = 'MechanicalArmy'
    cost = {'Turn':['Passive']}
    # check
                
# Tier 3 6+            
class AuraUpgrade(gen.Obstacle):
    name = 'CellTower'
    aura = 'CellTower'
    cost = {'Turn':['Passive']}
    
    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location 

    def initAbility(self,gameboard):
        return gameboard               

class UrbanUpgrade(gen.Ability):
    name = 'UrbanUpgrade'
    cost = {'Turn':['Passive']}

    def initAbility(self,gameboard):
        return gameboard   
                
class RemoteConstruction(gen.Ability):
    name = 'RemoteConstruction'
    cost = {'Turn':['Passive']}
                
class Extension(gen.Ability):
    name = 'Extension'
    cost = {'Turn':['Passive']}

class EMPTower(gen.Obstacle):
    name = 'EMPTower'
    aura = 'EMPTower'
    auraRange = 3
    
    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location   
                
class PlaceEMPTower(gen.Ability):
    name = 'PlaceEMPTower'
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
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
    name = 'PlaceUAVTower'
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
        gameboard[target] = RadarTower(gameboard[unit].playerID,target)
        return gameboard
    
class MobileSecurity(gen.Ability):
    name = 'MobileSecurity'
    cost = {'Turn':['Passive']}

    def initAbility(self,gameboard,playerID):
        for x in gameboard:
            if gameboard[x].name == 'Turret' and gameboard[x].playerID == playerID:
                gameboard[x].abilities['MobileSecurity'] = self
                gameboard[x].attributeManager['Movement'] = 2
        return gameboard                      

class RotatingMount(gen.Ability):
    name = 'RotatingMount'
    cost = {'Turn':['Passive']}

    def initAbility(self,gameboard,playerID):
        for x in [x for x in gameboard if gameboard[x].name == 'Turret' and gameboard[x].playerID == playerID]:
            gameboard[x].abilities['RotatingMount'] = self
            
        return gameboard                      

class LinkingModule(gen.Ability):
    name = 'LinkingModule'
    cost = {'Turn':['Passive']}
    # check
                
# Tier 4 9+
class EfficientManufacturing(gen.Ability):
    name = 'EfficientManufacturing'
    cost = {'Turn':['Passive']}
                
class SniperTower(gen.Ability):
    name = 'SniperTower'
    cost = {'Turn':['Passive']}
    
    def initAbility(self,gameboard,playerID):
        for x in [x for x in gameboard if gameboard[x].name == 'Turret' and gameboard[x].playerID == playerID]:
            gameboard[x].abilities['SniperTower'] = self
        return gameboard                     

class MaterialResearch(gen.Ability):
    name = 'MaterialResearch'
    cost = {'Turn':['Passive']}
    
    def initAbility(self,gameboard,playerID):
        buildoptions = ['Relay','Armory','Turret','Medbay','Bunker','EMPTower','RadarTower','Wall']
        for x in [x for x in gameboard if gameboard[x].name in buildoptions and gameboard[x].playerID == playerID]:
            gameboard[x].abilities['MaterialResearch'] = self
        return gameboard                     

class BlueprintUpgrade(gen.Ability):
    name = 'BlueprintUpgrade'
    cost = {'Turn':['Passive']}
    #check
                
class UpdateVersion20(gen.Ability):
    name = 'UpdateVersion20'
    cost = {'Turn':['Passive']}
    #check
    
class AutomatedCover(gen.Ability):
    name = 'AutomatedCover'
    cost = {'Turn':['Passive'],'Reaction':['Passive']}
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
    
    def passiveMods(self,unit,target,gameboard,combatSteps):
        elite = [x for x in gameboard if gameboard[x].unitType == 'Elite' and gameboard[x].playerID == gameboard[x].playerID]
        if elite:
            elite = elite[0]
        else:   
            elite = unit
        if self.location == unit:
            if [y for y in [x for x in self.adjacentSpaces(unit) if x in gameboard] if 'Lethargy' in gameboard[y].abilities] and 'Wounding' in combatSteps['AttackMods']:
                combatSteps['AttackMods'].remove('Wounding')
            if 'RadarTower' in gameboard[elite].abilities:
                if len([x for x in self.getAOETargets(gameboard[unit].abilities['RadarTower'].getAuraRange(),unit) if gameboard[x].aura == 'RadarTower']) > 0:
                    combatSteps['AddHit'] = combatSteps['AddHit'] + 2
            if 'Armory' in gameboard[elite].abilities:
                if len([x for x in self.getAOETargets(gameboard[unit].abilities['Armory'].getAuraRange(),unit) if gameboard[x].aura == 'Armory']) > 0:
                    combatSteps['AddDamage'] = combatSteps['AddDamage'] + 1
                    combatSteps['AddHit'] = combatSteps['AddHit'] + 1

        if self.location == target:
            if [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]:
                elites = [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]
                for x in elites:
                    if gameboard[x].getDistance(target) <= gameboard[x].attunement['Water']:
                        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] - 2
            if 'RadarTower' in gameboard[elite].abilities:
                if len([x for x in self.getAOETargets(gameboard[unit].abilities['RadarTower'].getAuraRange(),unit) if gameboard[x].aura == 'RadarTower']) > 0:
                    combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + 2
                    if 'Wounding' in combatSteps['AttackMods']:
                        combatSteps['AttackMods'].remove('Wounding')
                        combatSteps['CalcHit'] = 6
                        combatSteps['AddHit'] = 0
                    
            if 'CloakingDevice' in self.unitBlueprints:
                eva = random.randint(1,6)
                if eva > combatSteps['CalcEvasion']:
                    combatSteps['CalcEvasion'] = eva
            if 'Bunker' in gameboard[elite].abilities:
                if len([x for x in self.getAOETargets(gameboard[unit].abilities['Bunker'].getAuraRange(),unit) if gameboard[x].aura == 'Bunker']) > 0:
                    combatSteps['AddArmor'] = combatSteps['AddArmor'] + 1
                if 'Piercing' in combatSteps['AttackMods']:
                    combatSteps['AttackMods'].remove('Piercing')
                
        return gameboard, combatSteps

class EngineerPlayer(gen.Player):
    captureCost = 'Special'
    
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
        self.Obstacles = [x for x in [Wall(self.name,self.playerID),Turret(self.name,self.playerID,2),Relay(self.name,self.playerID),Medbay(self.name,self.playerID),
                                 Armory(self.name,self.playerID),Bunker(self.name,self.playerID),EMPTower(self.name,self.playerID),RadarTower(self.name,self.playerID)]]
        commons = [x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == self.playerID]
        elite = [x for x in gameboard if gameboard[x].unitType == 'Elite' and gameboard[x].playerID == self.playerID]
        for x in commons:
            if gameboard[x].unusedBlueprints > 0 and elite:
                gameboard[elite].unusedBlueprints = gameboard[elite].unusedBlueprints + gameboard[x].unusedBlueprints
                gameboard[x].unusedBlueprints = 0
        return gameboard
    
    def endTurnEffects(self,gameboard):
        units = [x for x in gameboard if gameboard[x].playerID == self.playerID and gameboard[x].unitType == 'Common']
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
            if [x for x in self.units['Elite'].abilities['Medbay'].getAOETargets(self.units['Elite'].abilities['Medbay']._range,self.units['Elite'].location) if type(gameboard[x]).__name__ == 'Medbay']:
                self.units['Elite'].attributeManager.currentAttributes['Health'] = self.units['Elite'].maxHealth
        return gameboard
    
    def blueprintEffects(self,gameboard):
        # Shouldn't be used. Any blueprint effects should be migrated to other beginning/ending functions
        units = [x for x in gameboard if gameboard[x].playerID == self.playerID and gameboard[x].unitType in ['Elite','Common']]
        for x in units:
            gameboard[x].blueprintEffects()
        return gameboard

# test = EngineerUnit('Engineer','Elite',0)
