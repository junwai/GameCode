# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:05:33 2021

@author: bgool
"""
import random
import GeneralUse as gen
import lineOfSight as LOS

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
        
class MageUnit(gen.Unit):

    attunements = {'Air':0,'Water':0,'Fire':0,'Earth':0,'Mana':0,'Void':0}
    name = 'Unit'
    unitClass = 'Mage'
    
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
   
class ChainLightning(gen.Ability):
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
    
class Nimbus(gen.Ability):
    name = 'Nimbus'
    level = 2
    cost = {'Turn':'Passive'}
                    
class Whirlwind(gen.Ability):
    name = 'Whirlwind'
    level = 3
    cost = {'Turn':'Passive'}

    def abilityEffect(self,gameboard,playerID):
        units = [x for x in gameboard if gameboard[x].unitType == 'Common' and gameboard[x].playerID == playerID]
        for x in units:
            gameboard[x].abilities['Movement'].abilityEffect(x,[],gameboard,{'Direction':random.choice(self.directions),'Cost':'Passive','Distance':gameboard[x].attunements['Air'] + 2})
        return gameboard
    
class WindShear(gen.Ability):
    name = 'WindShear'
    level = 4
    cost = {'Turn':'Passive'}
    
class Zephyr(gen.Ability):
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
    
class Haste(gen.Ability):
    name = 'Haste'
    level = 6
    cost = {'Turn':'Passive'}
                
class ManifestAir(gen.Ability):
    name = 'ManifestAir'
    level = 7
    cost = {'Turn':'Passive'}
                
class MirrorShroud(gen.Ability):
    name = 'MirrorShroud'
    level = 8
    cost = {'Turn':'Passive'}
                
class Prismata(gen.Ability):
    name = 'Prismata'
    level = 9
    cost = {'Reaction':'Reaction'}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        for x in gameboard[unit].adjacentSpaces:
            gameboard = self.combat(unit,x,gameboard,{'Wounding':True,'Damage':damage})
        return gameboard
    
class LightningStrike(gen.Ability):
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
 
class IceBlast(gen.Ability):
    name = 'IceBlast'
    level = 1
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return self.getLOSTargets(unit,gameboard)
    
    def abilityEffect(self,unit,target,gameboard):
        return self.combat(unit,target,gameboard,{'AddHit':gameboard[unit].attunements['Water'],'Damage':1+gameboard[unit].attunements['Water']})
        
class Hoarfrost(gen.Ability):
    name = 'Hoarfrost'
    level = 2
    cost = {'Turn':'Passive'}
                
class FlashFlood(gen.Ability):
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
                
class ManifestWater(gen.Ability):
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
    
class Oxidize(gen.Ability):
    name = 'Oxidize'
    level = 5
    cost = {'Turn':'Passive'}
                
class Hailstorm(gen.Ability):
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
        
class LiquidShield(gen.Ability):
    name = 'LiquidShield'
    level = 7
    cost = {'Reaction':'Reaction'}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        damage = damage - 2
        return gameboard,damage
        
class Geyser(gen.Ability):
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
    
class Frostbite(gen.Ability):
    name = 'Frostbite'
    level = 9
    cost = {'Turn':'Passive'}
                
class HarbingerOfWinter(gen.Ability):
    name = 'HarbingerOfWinter'
    level = 10
    cost = {'Turn':'Passive'}

class Water:
    name = 'Water'
    def __init__(self,playerID):
        self.abilities = {'IceBlast':IceBlast('Elite',playerID),'Hoarfrost':Hoarfrost('Elite',playerID),'FlashFlood':FlashFlood('Elite',playerID),'ManifestWater':ManifestWater('Elite',playerID),'Oxidize':Oxidize('Elite',playerID),'Hailstorm':Hailstorm('Elite',playerID),'LiquidShield':LiquidShield('Elite',playerID),'Geyser':Geyser('Elite',playerID),'Frostbite':Frostbite('Elite',playerID),'HarbingerOfWinter':HarbingerOfWinter('Elite',playerID)}
    
class Fireball(gen.Ability):
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
    
class SearingAura(gen.Ability):
    name = 'SearingAura'
    level = 2
    cost = {'Turn':'Passive'}
                
class Combust(gen.Ability):
    name = 'Combust'
    level = 3
    cost = {'Reaction':'Passive'}
    state = ['EliminateUnit']            
    
    def abilityEffect(self,unit,target,gameboard):
        targets = [x for x in gameboard[unit].adjacentSpaces()]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Damage':3})
        return gameboard
    
class Flare(gen.Ability):
    name = 'Flare'
    level = 4
    cost = {'Passive':'Passive'}
                
class StepsOfCinder(gen.Ability):
    name = 'StepsOfCinder'
    level = 5
    cost = {'Turn':'Special'}
    active = 0
    
    def abilityEffect(self,unit,target,gameboard):
        self.active = gameboard[unit].attunements['Fire']
        return gameboard
        
class TraceFlames(gen.Ability):
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
    
class ThermalRadiation(gen.Ability):
    name = 'ThermalRadiation'
    level = 7
    cost = {'Reaction':'Passive'}
    state = ['GiveDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        return gameboard, damage + gameboard[unit].attunements['Fire']
        
class Pyre(gen.Ability):
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
    
class Meteor(gen.Ability):
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

class Incinerate(gen.Ability):
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
               
class KineticImpulse(gen.Ability):
    name = 'KineticImpulse'
    level = 1
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        return [x for x in self.getMeleeTargets(unit,gameboard) if type(gameboard[x]).__name__ == 'Unit']
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.forcedMovement(1+gameboard[unit].attunements['Earth'],gameboard[unit].direction,target,gameboard)
        return gameboard
    
class Stonewrought(gen.Ability):
    name = 'Stonewrought'
    level = 2
    cost = {'Turn':'Passive'}
    
    def abilityEffect(self):
        return random.choice([True,False])            
        
class Tremor(gen.Ability):
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
    
class Tectonics(gen.Ability):
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
    
class Terraform(gen.Ability):
    name = 'Terraform'
    level = 5
    cost = {'Turn':'Special'}
    
    def abilityEffect(self,unit,target,gameboard):
        choice = random.choice(['Create','Move'])

        if choice == 'Create':
            target = random.choice([x for x in self.getAOETargets(3,unit) if x not in gameboard])
            gameboard[target] = gen.Obstacle()
        if choice == 'Move':
            target = random.choice([x for x in self.getAOETargets(3,unit) if type(gameboard[x]).__name__ == 'Obstacle'])
            moveSpace = random.choice([x for x in self.getAOETargets(3,unit) if x not in gameboard])
            gameboard[moveSpace] = gameboard[target]
            del gameboard[target]
        return gameboard
        
class Fissure(gen.Ability):
    name = 'Fissure'
    level = 6
    cost = {'Turn':'Passive'}
                
class Avalanche(gen.Ability):
    name = 'Avalanche'
    level = 7
    cost = {'Turn':'Passive'}
                
class Gleization(gen.Ability):
    name = 'Gleization'
    level = 8
    cost = {'Turn':'Special'}
    
    def abilityEffect(self,unit,target,gameboard):
        commons = [x for x in gameboard if gameboard[x].playerID == gameboard[unit].playerID and gameboard[x].unitType == 'Common']
        for x in commons:
            maxHealth = gameboard[x].levelManager.classAttributes()['Health'] + gameboard[x].permBonusAttr['Health']
            gameboard[x].bonusAttributes['Armor'] = gameboard[x].bonusAttributes['Armor'] + maxHealth - gameboard[x].attributeManager.getAttributes['Health']
        return gameboard
    
class Shockwave(gen.Ability):
    name = 'Shockwave'
    level = 9
    cost = {'Turn':'Passive'}
                
class Gigalith(gen.Ability):
    name = 'Gigalith'
    level = 10
    cost = {'Turn':'Passive'}

class Earth:
    name = 'Earth'
    
    def __init__(self,playerID):
        self.abilities = {'KineticImpulse':KineticImpulse('Elite',playerID),'Stonewrought':Stonewrought('Elite',playerID),'Tremor':Tremor('Elite',playerID),'Tectonics':Tectonics('Elite',playerID),'Terraform':Terraform('Elite',playerID),'Fissure':Fissure('Elite',playerID),'Avalanche':Avalanche('Elite',playerID),'Gleization':Gleization('Elite',playerID),'Shockwave':Shockwave('Elite',playerID),'Gigalith':Gigalith('Elite',playerID)}  
            
class ManaLeech(gen.Ability):
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
        
class Phase(gen.Ability):
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
        
class Substitute(gen.Ability):
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
        
        
class AetherBeam(gen.Ability):
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
        
class Channel(gen.Ability):
    name = 'Channel'
    level = 5
    cost = {'Turn':'Passive'}
    # need to do this        
        
class Reflect(gen.Ability):
    name = 'Reflect'
    level = 6
    cost = {'Reaction':'Reaction'}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        gameboard = self.forcedMovement(damage,self.oppositeDirections[gameboard[target].direction],unit,target,gameboard)
        return gameboard, 0
        
class InfusedElementals(gen.Ability):
    name = 'InfusedElementals'
    level = 7
    cost = {'Turn':'Passive'}
    # need to do this            
    
class MindFlay(gen.Ability):
    name = 'MindFlay'
    level = 8
    cost = {'Turn':'Special'}

    def getTargets(self,unit,gameboard):
        return [x for x in self.getLOSTargets(unit,gameboard,{'Range':3})]
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.combat(unit,target,gameboard,{'Wounding':True,'Piercing':True,'Damage':gameboard[unit].attunements['Mana']})
        return gameboard
    
class ArcaneShield(gen.Ability):
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
        
class AetherPulse(gen.Ability):
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

class PairedDecay(gen.Ability):
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
    
class GravitationalCollapse(gen.Ability):
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
        
class Portal(gen.Ability):
    name = 'Portal'
    level = 3
    cost = {'Turn':'Passive'}
                
class Rift(gen.Ability):
    name = 'Rift'
    level = 4
    cost = {'Turn':'Passive'}
                
class TransverseManifold(gen.Ability):
    name = 'TransverseManifold'
    level = 5
    cost = {'Turn':'Passive'}
                
class Singularity(gen.Ability):
    name = 'Singularity'
    level = 6
    cost = {'Turn':'Special'}
    
    def abilityEffect(self,unit,target,gameboard):
        target = [x for x in self.getAOETargets(3,unit) if gameboard[x].name == 'Objective']
        gameboard[target].playerID = 'None'
        gameboard[target].health = 0
        return gameboard
    
class Orbitals(gen.Ability):
    name = 'Orbitals'
    level = 7
    cost = {'Turn':'Passive'}
                
class MassTeleport(gen.Ability):
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
                
class Simulacrum(gen.Ability):
    name = 'Simulacrum'
    level = 9
    cost = {'Turn':'Passive'}
        
class Duality(gen.Ability):
    name = 'Duality'
    level = 10
    cost = {'Turn':'Passive'}

class Void:
    name = 'Void'
    def __init__(self,playerID):
        self.abilities = {'PairedDecay':PairedDecay('Elite',playerID),'GravitationalCollapse':GravitationalCollapse('Elite',playerID),'Portal':Portal('Elite',playerID),'Rift':Rift('Elite',playerID),'TransverseManifold':TransverseManifold('Elite',playerID),'Singularity':Singularity('Elite',playerID),'Orbitals':Orbitals('Elite',playerID),'MassTeleport':MassTeleport('Elite',playerID),'Simulacrum':Simulacrum('Elite',playerID),'Duality':Duality('Elite',playerID)}

class MagePlayer(gen.Player):
    
    captureCost = 'Special'
    attunements = {'Air':0,'Water':0,'Fire':0,'Earth':0,'Mana':0,'Void':0}
    attunement = []

    def __init__(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        # instantiate new units
        self.units = {'Elite':MageUnit('Elite','Elite'),'Common1':MageUnit('Common','Common1'),\
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
