# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:41:25 2020

@author: bgool
"""

import random

class AttunementStats:
    
    level = 1
    
    AttunementStats = {
            'Air':AirAttunementStats(level),
            'Water':WaterAttunementStats(level),
            'Fire':FireAttunementStats(level),
            'Earth':EarthAttunementStats(level),
            'Mana':ManaAttunementStats(level),
            'Void':VoidAttunementStats(level)
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

    self.attunements = {'Air':0,'Water':0,'Fire':0,'Earth':0,'Mana':0,'Void':0}
    
    def __init__(self,unitType,unitName):
        self.unitType = unitType
        if unitType == 'Elite':
            self.unitRange = 3
        else:
            self.unitRange = 1
        self.unitName = unitName
        self.direction = 'n'
    
    def passiveMods(self,unit,target,gameboard,combatSteps):
        if self.location == unit:
            if [y for y in [x for x in self.adjacentSpaces()] if 'Lethargy' in gameboard[y].abilities] and 'Wounding' in combatSteps['AttackMods']:
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
                    self.combat(unit,x,gameboard,{'Wounding':True,'Damage':3})
                    gameboard[unit].abilities['StepsOfCinder'].active = gameboard[unit].abilities['StepsOfCinder'].active - 1
        return gameboard

    def createCombatModifiers(self,**kwargs):
        unit,target,gameboard = kwargs['unit'],kwargs['target'],kwargs['gameboard']
        mods = {}
        if 'Oxidize' in gameboard[unit].abilities:
            if target in gameboard[unit].adjacentSpaces():
                mods['Piercing'] = True
        return mods
    
class MagePlayer(Player):
    
    self.elements = ['Air','Water','Fire','Earth','Mana','Void']
    self.attunements = {'Air':0,'Water':0,'Fire':0,'Earth':0,'Mana':0,'Void':0}
    self.attunement = []
    
    def levelUp(self):
        if self.level < 10:
            self.level = self.level + 1
            for unit in self.units.values():
                unit.levelManager.level = self.level
                unit.attributeManager.permBonusAttr[self.attunement] = unit.attributeManager.permBonusAttr[self.attunement] + 1
#            self.chooseAbility(random.choice(self.availableAbilities()))
    
    def Attune(self):
        element = random.choice(self.elements)
        self.attunement = element
        self.attunements[element] = self.attunements[element] + 1
        for unit in self.units:
            units[unit].attunements = self.attunements
            self.updateUnits(unit)
    
    def turn(self,gameboard,players):
        # while not passed keep going

        unitChoices = {x:gameboard.get(x) for x in gameboard.keys() if type(gameboard[x]).__name__ == 'Unit' and gameboard.get(x).playerID == self.playerID}
        unitChoices['Pass'] = 'Pass'
        
        while True:
            for unit in self.units:
                self.units[unit].unitOptions = self.units[unit].createOptions()
            unitChoice = unitChoices.get(random.choice(list(unitChoices.keys())))
            if unitChoice == 'Pass':
                break
            # execute ability
            if unitChoice.unitOptions:
                unitChoice.abilities.get(random.choice(unitChoice.unitOptions)).execute(unit,gameboard)
            for unit in gameboard:
                if type(unit).__name__ == 'Unit' and unit.playerID == self.playerID:
                    if unit.attributeManager.getAttributes('Health') <= 0:
                        self.updateUnits(unit)
                        del gameboard[unit]
            # then pick an option
        return gameboard
    
    def beginningTurnEffects(self,gameboard):
        if 'ManifestAir' in self.abilities:
            units = [x for x in gameboard if gameboard[x].playerID == self.playerID]
            spaces = [space for space in [(x,y) for x in range(0,20) for y in range(0,20)] if space not in boardgame]
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
            
    def generateMovementEffect(self,*ability):
        effects = {}
        if 'Nimbus' in self.abilities:
            effect['Unrestrained'] = True
        return effects
    
    def endTurnEffects(self,gameboard):
        if 'SearingAura' in self.abilities:
            units = [x for x in gameboard if gameboard[x].playerID == self.playerID and type(gameboard[x]).__name__ == 'Unit']
            targets = [x for y in [gameboard[x].getAOETargets(gameboard[unit].attunements['Fire']) for x in unit] if gameboard[x].playerID != self.playerID for x in y]
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
                        
class ManaInfusion:
    name = 'ManaInfusion'

class ManaPool:
    name = 'ManaPool'

class Teleport:
    name = 'Teleport'
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in self.getAOETargets(3,unit) if x not in gameboard]
        
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = gameboard[unit]
        gameboard[target].location = target
        del gameboard[unit]

class Air:
    name = 'Air'
    class ChainLightning:
        name = 'ChainLightning'
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
            
    class Nimbus:
        name = 'Nimbus'
        cost = {'Passive':'Passive'}
                        
    class Whirlwind:
        name = 'Whirlwind'
        cost = {'Passive':'Passive'}

        def abilityEffect(self,gameboard,playerID):
            units = [x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == playerID]
            for x in units:
                gameboard[x].abilities['Movement'].abilityEffect(x,[],gameboard,{'Direction':random.choice(self.directions),'Cost':'Passive','Distance':gameboard[x].attunements['Air'] + 2})
                        
    class WindShear(Ability):
        name = 'WindShear'
        cost = {'Passive':'Passive'}
        
    class Zephyr:
        name = 'Zephyr'
        cost = {'Turn':'Special'}
        
        def getTargets(self,unit,gameboard):
            return [x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == gameboard[unit].playerID]
        
        def abilityEffect(self,unit,target,gameboard):
            tempUnit = gameboard[target]
            gameboard[target] = gameboard[unit]
            gameboard[target].location = target
            gameboard[unit] = tempUnit
            gameboard[unit].location = unit
            gameboard[target].abilities['Movement'].abilityEffect(x,[],gameboard,{'Direction':random.choice(self.directions),'Cost':'Passive','Distance':gameboard[x].attunements['Air'] + 2})
            return gameboard
        
    class Haste:
        name = 'Haste'
        cost = {'Passive':'Passive'}
                    
    class ManifestAir:
        name = 'ManifestAir'
        cost = {'Passive':'Passive'}
                    
    class MirrorShroud:
        name = 'MirrorShroud'
        cost = {'Passive':'Passive'}
                    
    class Prismata:
        name = 'Prismata'
        cost = {'Reaction':'Reaction'}
        state = ['TakeDamage']
        
        def abilityEffect(self,unit,target,gameboard,damage):
            for x in gameboard[unit].adjacentSpaces:
                gameboard = self.combat(unit,x,gameboard,{'Wounding':True,'Damage':damage})
            
    class LightningStrike:
        name = 'LightningStrike'
        cost = {'Turn':'Special'}
        
        def getTargets(self,unit,gameboard):
            return [x for x in gameboard]
        
        def abilityEffect(self,unit,target,gameboard):
            return self.combat(unit,target,gameboard,{'Wounding':True,'Piercing':True,'Damage':10})

class Water:
    class IceBlast:
        name = 'IceBlast'
        cost = {'Turn':'Special'}
        
        def getTargets(self,unit,gameboard):
            return getLOSTargets(unit,gameboard)
        
        def abilityEffect(self,unit,target,gameboard):
            return self.combat(unit,target,gameboard,{'AddHit':gameboard[x].attunements['Water'],'Damage':1+gameboard[x].attunements['Water']})
            
    class Hoarfrost:
        name = 'Hoarfrost'
        cost = {'Passive':'Passive'}
                    
    class FlashFlood:
        name = 'FlashFlood'
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
                    
    class ManifestWater:
        name = 'ManifestWater'
        cost = {'Turn':'Reaction'}
        maxReactions = 0
        usedReactions = 0
        
        def getTargets(self,unit,gameboard,*args):
            self.maxReactions = gameboard[unit].attunements['Water']
            return list(set(self.getLOSTargets(unit,gameboard,args)).intersection(set(self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location))))

        def abilityEffect(self,unit,target,gameboard):
            if self.usedReactions < maxReactions:
                gameboard[unit].changeAttributes('Reaction',-1)
                self.usedReactions = self.usedReactions + 1
                return self.combat(unit,target,gameboard,gameboard[unit].createCombatModifiers({'unit':unit,'target':target,'gameboard':gameboard})) 
            else:
                return gameboard
        
    class Oxidize:
        name = 'Oxidize'
        cost = {'Passive':'Passive'}
                    
    class Hailstorm:
        name = 'Hailstorm'
        cost = {'Turn':'Passive'}
        
        def getTargets(self,unit,gameboard):
            return list(set(self.getLOSTargets(unit,gameboard,args)).intersection(set(self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location))))            
        
        def abilityEffect(self,unit,target,gameboard):
            commons = [x for x in self.getAOETargets(3,unit) if gameboard[x].unitType == 'Common' and gameboard[x].playerID == gameboard[unit].playerID]
            availableCommon = [x for x in commons if commons[x].attributeManager.getAttribute['Attack'] > 0]
            if availableCommon:
                gameboard[availableCommon].changeAttributes('Attack',-1)
                return self.combat(unit,target,gameboard,gameboard[unit].createCombatModifiers({'unit':unit,'target':target,'gameboard':gameboard})) 
            else:
                return gameboard
            
    class LiquidShield:
        name = 'LiquidShield'
        cost = {'Reaction':'Reaction'}
        state = ['TakeDamage']
        
        def abilityEffect(self,unit,target,gameboard,damage):
            damage = damage - 2
            return gameboard,damage
            
    class Geyser:
        name = 'Geyser'
        cost = {'Reaction':'Reaction'}
        state = ['Any']
        
        def getTargets(self,unit,gameboard):
            spaces = [x for x in gameboard if type(gameboard[x]).__name__ == 'Objective' and gameboard[x].playerID == gameboard[unit].playerID]
            targetSpaces = [x for y in [adjacentSpaces(x) for x in spaces] if gameboard[y].playerID != gameboard[unit].playerID for x in y]
            
        def abilityEffect(self,unit,target,gameboard):
            for x in targetSpaces:
                self.combat(unit,target,gameboard,{'Damage':2,'Wounding':True,'Piercing':True}) 
            
    class Frostbite:
        name = 'Frostbite'
        cost = {'Passive':'Passive'}
                    
    class HarbingerOfWinter:
        name = 'HarbingerOfWinter'
        cost = {'Passive':'Passive'}
                
class Fire:
    class Fireball:
        name = 'Fireball'
        cost = {'Turn':'Special'}
        
        def getTargets(self,unit,gameboard):
            return self.getLOSTargets(unit,gameboard)
        
        def abilityEffect(self,unit,target,gameboard):
            gameboard = self.combat(unit,target,gameboard,{'Damage':4})
            spaces = [x for x in self.adjacentSpaces(target)]
            for x in spaces:
                gameboard[x].combat(unit,x,gameboard,{'Damage':1,'Piercing':True,'Wounding':True})
            
    class SearingAura:
        name = 'SearingAura'
        cost = {'Passive':'Passive'}
                    
    class Combust:
        name = 'Combust'
        cost = {'Reaction':'Passive'}
        state = ['EliminateUnit']            
        
        def abilityEffect(self,unit,target,gameboard):
            targets = [x for x in gameboard[unit].adjacentSpaces()]
            for x in targets:
                gameboard[unit].combat(unit,x,gameboard,{'Damage':3})
            return gameboard
        
    class Flare:
        name = 'Flare'
        cost = {'Passive':'Passive'}
                    
    class StepsOfCinder:
        name = 'StepsOfCinder'
        cost = {'Turn':'Special'}
        active = 0
        
        def abilityEffect(self,unit,target,gameboard):
            self.active = gameboard[unit].attunements['Fire']
            return gameboard
            
    class TraceFlames:
        name = 'TraceFlames'
        cost = {'Turn':'Special'}
        
        def getTargets(self,unit,gameboard):
            return [x for x in gameboard if gameboard[x].unitType == 'Common' and gamedboard[x].playerID == gameboard[unit].playerID]
        
        def abilityEffect(self,unit,target,gameboard):
            tempUnit = gameboard[target]
            gameboard[target] = gameboard[unit]
            gameboard[target].location = target
            gameboard[unit] = tempUnit
            gameboard[unit].location = unit
            for x in gameboard[target].adjacentSpaces():
                gameboard[target].combat(target,x,gameboard,{'Damage':3})
            
    class ThermalRadiation:
        name = 'ThermalRadiation'
        cost = {'Reaction':'Passive'}
        state = ['GiveDamage']
        
        def abilityEffect(self,unit,target,gameboard,damage):
            return gameboard, damage + gameboard[unit].attunements['Fire']
            
    class Pyre:
        name = 'Pyre'
        cost = {'Turn':'Special'}
        damage = {0:5, 1:4, 2:3}
        active = 3
        
        def __init__(self,location):
            self.location = location
        
        def getTargets(self,unit,gameboard):
            self.getAOETargets(2,unit)
        
        def abilityEffect(self,unit,target,gameboard):
            gameboard['Pyre'][target] = Pyre(target)
        
        def dealDamage(self,gameboard):
            spaces = self.getAOETargets(2,self.location)
            for x in spaces: 
                if x in gameboard and self.getDistance(x,self.location) == 2:
                    gameboard[x].attributeManager.currentAttributes['Health'] = gameboard[x].attributeManager.currentAttributes['Health'] - 3
                elif x in gameboard and self.getDistance(x,self.location) == 1:
                    gameboard[x].attributeManager.currentAttributes['Health'] = gameboard[x].attributeManager.currentAttributes['Health'] - 4                    
                elif x == self.location:
                    gameboard[x].attributeManager.currentAttributes['Health'] = gameboard[x].attributeManager.currentAttributes['Health'] - 5
                    
    class Meteor(Ability):
        name = 'Meteor'
        cost = {'Turn':'Special'}
        active = 0
        
        def getTargets(self,unit,gameboard):
            return [space for space in [(x,y) for x in range(0,20) for y in range(0,20)] if space not in boardgame]
            
        def abilityEffect(self,unit,target,gameboard):
            self.location = target
            self.active = 2
            return gameboard
        
        def dealDamage(self,gameboard):
            elite = [x for x in gameboard if gameboard[x].unitType == 'Elite' and gameboard[x].playerID == self.playerID]
            for x in [self.adjacentSpaces(self.location) + [location]]:
                if x in gameboard:
                    self.combat(elite[0],gameboard[x],gameboard,{'Wounding':True,'Damage':12})
            return gameboard
    
    class GammaBurst(Ability):
        name = 'GammaBurst'
        cost = {'Turn':'Special'}
        
        def getTargets(self,unit,gameboard):
            return getLOSTargets(unit,gameboard)
        
        def abilityEffect(self,unit,target,gameboard):
            return self.combat(unit,target,gameboard,{'Wounding':True,'Piercing':True,'Swift':True,'Damage':5})
            
class Earth(Element):
    class KineticImpulse(Ability):
        name = 'KineticImpulse'
        cost = {'Turn':'Special'}
        
        def getTargets(self,unit,gameboard):
            return [x for x in self.getMeleeTargets(unit,gameboard) if type(gameboard[x]).__name__ == 'Unit']
        
        def abilityEffect(self,unit,target,gameboard):
            gameboard = self.forcedMovement(1+gameboard[unit].attunements['Earth'],gameboard[unit].direction,target,gameboard)
            
    class Stonewrought:
        name = 'Stonewrought'
        cost = {'Passive':'Passive'}
        
        def abilityEffect(self):
            return random.choice([True,False])            
            
    class Tremor:
        name = 'Tremor'
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
        
    class Tectonics:
        name = 'Tectonics'
        cost = {'Turn':'Special'}
        
        locations = []
        
        def abilityEffect(self,unit,gameboard):
            if gameboard[unit].attunements['Earth'] < 5:
                self.locations = random.sample([x for x in self.getAOETargets(gameboard[unit].attunements['Earth'],unit)], gameboard[unit].attunements['Earth'])
            elif gameboard[unit].attunements['Earth'] >= 5: 
                self.locations = random.sample([x for x in self.getAOETargets(gameboard[unit].attunements['Earth'],unit)], 5)
                
    class Terraform:
        name = 'Terraform'
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
            
    class Fissure:
        name = 'Fissure'
        cost = {'Passive':'Passive'}
                    
    class Avalanche:
        name = 'Avalanche'
        cost = {'Passive':'Passive'}
                    
    class Gleization:
        name = 'Gleization'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            commons = [x for x in gameboard if gameboard[x].playerID == gameboard[unit].playerID and gameboard[x].unitType == 'Common']
            for x in commons:
                maxHealth = gameboard[x].levelManager.classAttributes()['Health'] + gameboard[x].permBonusAttr['Health']
                gameboard[x].bonusAttributes['Armor'] = gameboard[x].bonusAttributes['Armor'] + maxHealth - gameboard[x].attributeManager.getAttributes['Health']
                
    class Shockwave:
        name = 'Shockwave'
        cost = {'Passive':'Passive'}
                    
    class Gigalith:
        name = 'Gigalith'
        cost = {'Passive':'Passive'}
        
            
class Mana(Element):
    class ManaLeech:
        name = 'ManaLeech'
        cost = {'Turn':'Special'}
        
        def getTargets(self,unit,gameboard):
            return [x for x in self.getLOSTargets(unit,gameboard,{'Range':3})]
        
        def abilityEffect(self,unit,target,gameboard):
            gameboard = self.combat(unit,target,gameboard,{'Wounding':True,'Piercing':True,'Damage':True})
            if gameboard[unit].attributeManager.getAttributes('Health') < maxHealth:
                gameboard[unit].attributeManager.changeAttributes('Health',2)
                if gameboard[unit].attributeManager.getAttributes('Health') == maxHealth + 1:
                    gameboard[unit].attributeManager.changeAttributes('Health',-1)
            return gameboard
            
    class Phase:
        name = 'Phase'
        cost = {'Reaction':'Reaction'}
        state = ['AddEvasion']
        
        def abilityEffect(self,unit,target,gameboard,combatSteps):
            combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + 3
            if 'Wounding' in combatSteps['AttackMods']:
                combatSteps['AttackMods'].remove('Wounding')
                combatSteps['HitResults'] = 6
            return gameboard,combatSteps
            
    class Substitute:
        name = 'Substitute'
        cost = {'Reaction':'Reaction'}
        state = ['TakeDamage']
        
        def abilityEffect(self,unit,target,gameboard,damage):
            common = random.choice([x for x in gameboard if gameboard[x].playerID == gameboard[unit].playerID and gameboard[x].unitType == 'Common'])
            tempUnit = gameboard[common]
            gameboard[common] = gameboard[unit]
            gameboard[unit] = tempUnit
            return gameboard
            
            
    class AetherBeam:
        name = 'AetherBeam'
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
            
    class Channel:
        name = 'Channel'
        cost = {'Passive':'Passive'}
        # need to do this        
            
    class Reflect:
        name = 'Reflect'
        cost = {'Reaction':'Reaction'}
        state = ['TakeDamage']
        
        def abilityEffect(self,unit,target,gameboard,damage):
            gameboard = self.forcedMovement(damage,self.oppositeDirections[gameboard[target].direction],unit,target,gameboard)
            return gameboard, 0
            
    class InfusedElementals:
        name = 'InfusedElementals'
        cost = {'Passive':'Passive'}
        # need to do this            
        
    class MindFlay:
        name = 'MindFlay'
        cost = {'Turn':'Special'}

        def getTargets(self,unit,gameboard):
            return [x for x in self.getLOSTargets(unit,gameboard,{'Range':3})]
        
        def abilityEffect(self,unit,target,gameboard):
            gameboard = self.combat(unit,target,gameboard,{'Wounding':True,'Piercing':True,'Damage':gameboard[unit].attunements['Mana']})
            
    class ArcaneShield:
        name = 'ArcaneShield'
        cost = {'Turn':'Special'}
        self.stacks = 0
        
        def abilityEffect(self,unit,target,gameboard):
            self.stacks = self.stacks + 1
        
        def useStack(self):
            if self.stacks > 0:
                self.stacks = self.stacks - 1
            
    class AetherPulse:
        name = 'AetherPulse'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            targets = [x for x in self.getAOETargets(1,unit) if x in gameboard]
            for x in targets:
                gameboard = self.combat(unit,x,gameboard,{'Damage':gameboard[unit].attunements['Mana'],'Wounding':True,'AetherPulse':True})
            return gameboard
        
        def recoverHealth(self,unit,gameboard):
            gameboard[unit].attributeManager.changeAttributes('Health',1)
            return gameboard
        
class Void(Element):
    class PairedDecay:
        name = 'PairedDecay'
        cost = {'Turn':'Special'}

        def getTargets(self,unit,gameboard):
            return [x for x in self.getLOSTargets(unit,gameboard,{'Range':3})]
        
        def abilityEffect(self,unit,target,gameboard):
            damage = random.choice(range(1,gameboard[unit].attributeManager.getAttributes('Health')))
            gameboard[unit].attributeManager.changeAttributes('Health',-damage)
            self.dealDamage(unit,target,gameboard)
            
    class GravitationalCollapse:
        name = 'GravitationalCollapse'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Portal:
        name = 'Portal'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Rift:
        name = 'Rift'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class TransverseManifold:
        name = 'TransverseManifold'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Singularity:
        name = 'Singularity'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Orbitals:
        name = 'Orbitals'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class MassTeleport:
        name = 'MassTeleport'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Simulacrum:
        name = 'Simulacrum'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Duality:
        name = 'Duality'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
        