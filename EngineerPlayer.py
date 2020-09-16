# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:47:48 2020

@author: bgool
"""

class EngineerUnit(Unit):
    
    unitBlueprints = {}
    numBlueprints = 0
    
    def __init__(self,unitType,unitName,numBlueprints):
        super().__init__(unitType,unitName)
        self.numBlueprints = numBlueprints
    
    def blueprintEffects(self,gameboard):
        for x in self.unitBlueprints:
            x.blueprintEffect(gameboard, self.location)
    
    def passiveMods(self,unit,target,gameboard,combatSteps):
        if self.location == unit:
            if [y for y in [x for x in self.adjacentSpaces()] if 'Lethargy' in gameboard[y].abilities] and 'Wounding' in combatSteps['AttackMods']:
                combatSteps['AttackMods'].remove('Wounding')
        if self.location == target:
            if [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]:
                elites = [x for x in gameboard if 'HoarFrost' in gameboard[x].abilities]
                for x in elites:
                    if gameboard[x].getDistance(target) <= gameboard[x].attunement['Water']:
                        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] - 2
        return gameboard, combatSteps
        
class EngineerPlayer(Player):

    blueprintTotal = 3
    
    class Build:
        name = 'Build' 
        cost = {'Turn':'Special'}
        # need to add special handling of obstacle auras
        
        Blueprints = Blueprint()
        
        def getTargets(self,unit,gameboard):
            return [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard]
        
        def buildCommon(self,unit,target,gameboard,unitObj):
            gameboard[target] = unitObj
            while True:
                selectCost = random.choice([x for x in range(0,gameboard[unit].blueprints+1) if x in self.blueprintCost])
                if selectCost == 0:
                    break
                addBlueprint = random.choice(self.blueprintCost[selectCost])
                gameboard[unit].numBlueprints = gameboard[unit].numBlueprints - selectCost
                gameboard[target].numBlueprints = gameboard[target].numBlueprints + selectCost
                gameboard[target].unitBlueprints[addBlueprint] = self.Blueprints[addBlueprint]
            return gameboard
                
        def buildObstacle(self,unit,target,gameboard):
            selectObstacle = random.choice(gameboard[unit].Obstacles)
            
        def abilityEffect(self):
            choice = random.choice(['Common','Obstacle'])
            return choice
        
    def turn(self,gameboard,players):
        # while not passed keep going

        unitChoices = {x:gameboard.get(x) for x in gameboard.keys() if type(gameboard[x]).__name__ == 'Unit' and gameboard.get(x).playerID == self.playerID}
        unitChoices['Pass'] = 'Pass'
        
        while True:
            gameboard = self.blueprintEffects(gameboard)
            for unit in self.units:
                self.units[unit].unitOptions = self.units[unit].createOptions()
            unitChoice = unitChoices.get(random.choice(list(unitChoices.keys())))
            if unitChoice == 'Pass':
                break
            # execute ability
            if unitChoice.unitOptions:
                abilityChoice = unitChoice.abilities.get(random.choice(unitChoice.unitOptions))
                if abilityChoice == 'Build':
                    buildChoice = unitChoice.abilities['Build'].abilityEffect()
                    target = unitChoice.abilities['Build'].getTargets(unitChoice.location,gameboard)
                    if buildChoice == 'Common':
                        newCommon = random.choice([self.units[x] for x in self.units if x not in unitChoices and self.units[x].unitType == 'Common'])
                        unitChoice.abilities['Build'].buildCommon(unitChoice.location,target,gameboard,newCommon)
                    elif buildChoice == 'Obstacle':
                        unitChoice.abilities['Build'].buildObstacle(unitChoice.location,target,gameboard,newObstacle)
                else:
                    unitChoice.abilities[abilityChoice].execute(unit,gameboard)
            for unit in gameboard:
                if type(unit).__name__ == 'Unit' and unit.playerID == self.playerID:
                    if unit.attributeManager.getAttributes('Health') <= 0:
                        self.updateUnits(unit)
                        del gameboard[unit]
            # then pick an option
        return gameboard
    
    def endTurnEffects(self,gameboard):
        units = [x for x in gameboard if gameboard[x].playerID == self.playerID and gameboard[x].unitType == 'Common']
        if [x for x in units if 'Biotechnology' in gameboard[x].unitBlueprints]:
            for x in [x for x in units if 'Biotechnology' in gameboard[x].unitBlueprints]:
                if gameboard[x].attributeManager.getAttributes('Health') == gameboard[x].maxHealth:
                    gameboard[x].attributeManager.changeAttributes('Health',1)
        if 'Medbay' in self.units['Elite'].abilities:
            if [x for x in self.units['Elite'].abilities['Medbay'].getAOETargets(self.units['Elite'].abilities['Medbay']._range,self.units['Elite'].location) if type(gameboard[x]).__name__ == 'Medbay']:
                self.units['Elite'].attributeManager.currentAttributes['Health'] = self.units['Elite'].maxHealth
    
    def blueprintEffects(self,gameboard):
        units = [x for x in gameboard if gameboard[x].playerID == self.playerID and gameboard[x].unitType in ['Elite','Common']]
        for x in units:
            x.blueprintEffects()
        return gameboard
        
    class Blueprint:
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
        
        blueprintEnabled = False
        
        def blueprintEffect(self, gameboard, unit):
            self.blueprintEnabled = True
            return gameboard
        
    class Railgun(Blueprint):
        name = 'Railgun'
        BPcost = 1
        
        def blueprintEffect(self,gameboard,unit):
            self.blueprintEnabled = True    
            gameboard[unit].unitRange = gameboard[unit].unitRange + 1
            # unit no longer has disadvantage on partial line of sight
            
    class Biotechnology(Blueprint):
        name = 'Biotechnology'
        BPcost = 1
    
    class TeslaCoil(Blueprint):
        name = 'TeslaCoil'
        BPcost = 1
        cost = {'Turn':'Attack'}
        
        def blueprintEffect(self,gameboard,unit):
            self.blueprintEnabled = True
            gameboard[unit].abilities['TeslaCoil'] = self
            return gameboard
            
        def abilityEffect(self, unit,target,gameboard):
            targets = [x for x in self.getAOETargets(1,unit) if x in gameboard]
            for x in targets:
                gameboard = self.combat(unit,target,gameboard,{'Damage':1,'Wounding':True,'Piercing':True})
            return gameboard        
        
    class PulseCannon(Blueprint):
        name = 'PulseCannon'
        BPcost = 1
        cost = {'Turn':'Attack'}
        
        def blueprintEffect(self,gameboard,unit):
            self.blueprintEnabled = True
            gameboard[unit].abilities['PulseCannon'] = self
        
        def abilityEffect(self,unit,target,gameboard):
            if gameboard[target].playerID != gameboard[unit].playerID:
                self.combat(unit,target,gameboard)
            self.forcedMovement(3, gameboard[unit].direction, target, gameboard)
            return gameboard
            
    class Thrusters(Blueprint):
        name = 'Thrusters'
        BPcost = 1
        
        def blueprintEffect(self,gameboard,unit):
            self.blueprintEnabled = True
            gameboard[unit].attributeManager.permBonusAttr['Movement'] = gameboard[unit].attributeManager.permBonusAttr['Movement'] + 2
            # units can also move through occupied spaces
            
    class ResponseProtocols(Blueprint):
        name = 'ResponseProtocols'
        BPcost = 1
        
        def blueprintEffect(self,gameboard,unit):
            self.blueprintEnabled = True
            gameboard[unit].attributeManager.permBonusAttr['Reaction'] = gameboard[unit].attributeManager.permBonusAttr['Reaction'] + 1
            
    class Twinmount(Blueprint):
        name = 'Twinmount'
        BPcost = 2

        def blueprintEffect(self,gameboard,unit):
            self.blueprintEnabled = True
            gameboard[unit].attributeManager.permBonusAttr['Attack'] = gameboard[unit].attributeManager.permBonusAttr['Attack'] + 1
     
    class EnhancedAI(Blueprint):
        name = 'EnhancedAI'
        BPcost = 2

        def blueprintEffect(self,gameboard,unit):
            self.blueprintEnabled = True
            gameboard[unit].attributeManager.permBonusAttr['Special'] = gameboard[unit].attributeManager.permBonusAttr['Special'] + 1
     
    class CloakingDevice(Blueprint):
        name = 'CloakingDevice'
        BPcost = 2
    
    class GeomorphicEngine(Blueprint):
        name = 'GeomorphicEngine'
        BPcost = 2
    
    class ReinforcedFrame(Blueprint):
        name = 'EnhancedFrame'
        BPcost = 3
        
        def blueprintEffect(self,gameboard,unit):
            self.blueprintEnabled = True
            gameboard[unit].attributeManager.permBonusAttr['Health'] = gameboard[unit].attributeManager.permBonusAttr['Health'] + 4
    
    class TeleportNode(Blueprint):
        name = 'TeleportNode'
        BPcost = 3
    
    class Tank(Blueprint):
        name = 'Tank'
        BPcost = 4

        def blueprintEffect(self,gameboard,unit):
            self.blueprintEnabled = True
            gameboard[unit].attributeManager.permBonusAttr['Armor'] = gameboard[unit].attributeManager.permBonusAttr['Armor'] + 2
            gameboard[unit].attributeManager.permBonusAttr['Movement'] = gameboard[unit].attributeManager.permBonusAttr['Armor'] - 1
            gameboard[unit].attributeManager.permBonusAttr['Evasion'] = gameboard[unit].attributeManager.permBonusAttr['Armor'] - 2
    
    class StateOfTheArt(Blueprint):
        name = 'StateOfTheArt'
        BPcost = 5
    
    class PlasmaCannon(Blueprint):
        name = 'PlasmaCannon'
        BPcost = 6
        
        def blueprintEffect(self,gameboard,unit):
            gameboard[unit].attributeManager.permBonusAttr['Damage'] = gameboard[unit].attributeManager.permBonusAttr['Damage'] + 5
            gameboard[unit].attributeManager.permBonusAttr['Attack'] = gameboard[unit].attributeManager.permBonusAttr['Attack'] -1
            gameboard[unit].unitRange = gameboard[unit].unitRange + 2
    
    class Dreadnought(Blueprint):
        name = 'Dreadnought'
        BPcost = 8
    
    class PowerArmor(Blueprint):
        name = 'PowerArmor' 
        BPcost = 3

        def blueprintEffect(self,gameboard,unit):
            gameboard[unit].attributeManager.permBonusAttr['Damage'] = gameboard[unit].attributeManager.permBonusAttr['Damage'] + 3
            gameboard[unit].attributeManager.permBonusAttr['Armor'] = gameboard[unit].attributeManager.permBonusAttr['Armor'] + 2
            gameboard[unit].attributeManager.permBonusAttr['Movement'] = gameboard[unit].attributeManager.permBonusAttr['Movement'] + 2           

    class Jetpack(Blueprint):
        name = 'Jetpack' 
        BPcost = 3
        
        def blueprintEffect(self,gameboard,unit):
            gameboard[unit].attributeManager.permBonusAttr['Movement'] = gameboard[unit].attributeManager.permBonusAttr['Movement'] + 4           
            gameboard[unit].attributeManager.permBonusAttr['Evasion'] = gameboard[unit].attributeManager.permBonusAttr['Evasion'] + 3           

    class WeaponsSystem(Blueprint):
        name = 'WeaponsSystem' 
        BPcost = 3

        def blueprintEffect(self,gameboard,unit):
            gameboard[unit].attributeManager.permBonusAttr['Hit'] = gameboard[unit].attributeManager.permBonusAttr['Hit'] + 4
            gameboard[unit].unitRange = gameboard[unit].unitRange + 2
    
    # Tier 0
    class PlaceRelay:
        name = 'PlaceRelay'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
            gameboard[target] = Relay(gameboard[unit].playerID)
    
    
    class Relay(Obstacle):
        name = 'Relay'
            
        def __init__(self,playerID,location):
            self.playerID = playerID
            self.location = location
            
    class PlaceWall:
        name = 'PlaceWall'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
            gameboard[target] = Wall()
            
    class Wall(Obstacle):
        name = 'Wall'

        def __init__(self,playerID,location):
            self.playerID = playerID
            self.location = location
    
    class PlaceTurret:
        name = 'PlaceTurret'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
            gameboard[target] = Turret()
            
    class Turret(Obstacle):
        name = 'Turret'

        def __init__(self,playerID,location):
            self.playerID = playerID
            self.location = location
            
    class TeleportModule:
        name = 'TeleportModule'
        cost = {'Turn':'Special','Reaction':'Reaction'}
        
        def abilityEffect(self,unit,target,gameboard):
            
    class MaterialRecall:
        name = 'MaterialRecall'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class ManualOverride:
        name = 'ManualOverride'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
        
    # Tier 1 2+
    class Repair:
        name = 'Repair'
        cost = ['Special','Reaction']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class PlaceMedbay:
        name = 'PlaceMedbay'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
            gameboard[target] = Medbay()
            
    class Medbay(Obstacle):
        name = 'Medbay'
        _range = 2
        
    class GrapplingHook:
        name = 'GrapplingHook'
        cost = ['Movement']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class PlaceArmory:
        name = 'PlaceArmory'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
            gameboard[target] = Armory()
            
    class Armory(Obstacle):
        name = 'Armory'
        _range = 3
        
    class Recycling:
        name = 'Recycling'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    # Tier 2 4+
    class PlaceBunker:
        name = 'PlaceBunker'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
            gameboard[target] = Bunker()
            
    class Bunker(Obstacle):
        name = 'Bunker'
        _range = 3
        
    class IncreasedRange:
        name = 'IncreasedRange'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Grenade:
        name = 'Grenade'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Sidecar:
        name = 'Sidecar'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class MechanicalArmy:
        name = 'MechanicalArmy'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    # Tier 3 6+
    class PlaceCellTower:
        name = 'PlaceCellTower'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
            gameboard[target] = CellTower()
            
    class CellTower:
        name = 'CellTower'
            
    class UrbanUpgrade:
        name = 'UrbanUpgrade'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class AutomatedCover:
        name = 'AutomatedCover'
        cost = ['Reaction']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class RemoteConstruction:
        name = 'RemoteConstruction'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Extension:
        name = 'Extension'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class PlaceEMPTower:
        name = 'PlaceEMPTower'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
            gameboard[target] = EMPTower()
            
    class EMPTower:
        name = 'EMPTower'
            
    class PlaceUAVTower:
        name = 'PlaceUAVTower'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])
            gameboard[target] = UAVTower()
            
    class UAVTower:
        name = 'UAVTower'
        _range = 3
        
    class MobileSecurity:
        name = 'MobileSecurity'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class RotatingMount:
        name = 'RotatingMount'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class LinkingModule:
        name = 'LinkingModule
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    # Tier 4 9+
    class EfficientManufacturing:
        name = 'EfficientManufacturing'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class SniperTower:
        name = 'SniperTower'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class MaterialResearch:
        name = 'MaterialResearch'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class BlueprintUpgrade:
        name = 'BlueprintUpgrade'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class UpdateVersion20:
        name = 'UpdateVersion20'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):