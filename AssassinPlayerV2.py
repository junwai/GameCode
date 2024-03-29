# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:05:33 2021

@author: bgool
"""
import random
import math
import GeneralUse as gen
import lineOfSight as LOS

# Something is overwriting the respawn

class StealthToken(gen.GeneralUse):
    
    # this is the token object
    name = 'StealthToken'
    unitName = 'StealthToken'
    unitType = 'StealthToken'
    playerClass = 'None'
    attributeManager = gen.AttributeManager({'Health':0,'Attack':0,'Movement':0,'Reaction':0,'Special':0,'Hit':0,'Evasion':0,'Armor':0})
    reactionManager = gen.ReactionManager()
    abilities = {}
    blastTrap = 0
    
    def __init__(self,playerID,location):
        self.playerID = playerID
        self.location = location
        self.boardImage = gen.MySprite('StealthToken','StealthToken')
    
    def setBlastTrap(self):
        self.blastTrap = 1    

    def stealthTokenEffect(self,unit,gameboard):
        if self.blastTrap:
            if random.randint(1,6) > gameboard[unit].attributeManager.getAttributes('Evasion'):
                self.dealIndirectDamage(self.location,unit,gameboard,5,self.playerID)
        return gameboard

class PlaceStealthToken(gen.Ability):
    name = 'StealthToken'
    cost = {'Turn':['Movement']}
    
    def getTargets(self,unit,gameboard):
        targets = [x for x in self.adjacentSpaces(unit) if x not in gameboard and x in gen.boardLocations]
        if targets:
            return random.choice(targets)
        else:
            return []
        
    def abilityEffect(self,unit,target,gameboard):
        if target:
            gameboard[target] = StealthToken(self.playerID,target)
            if 'BlastTrap' in gameboard[unit].abilities:
                gameboard[target].blastTrap = 1
        return gameboard
        

class AssassinAvoid(gen.Ability):
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
    
class AssassinAttack(gen.Ability):
    name = 'Attack'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Attack',-1)
        mods = gameboard[unit].createCombatModifiers({'unit':unit,'target':target,'gameboard':gameboard})
        if mods:
            return self.combat(unit,target,gameboard,mods)
        return self.combat(unit,target,gameboard) 
        
    def getTargets(self,unit,gameboard,*args):
        if 'PsychicScream' in gameboard[unit].abilities:
            if gameboard[unit].abilities['PsychicScream'].active:
                spaces = self.getAOETargets(1,unit,gameboard)
        else:
            spaces = list(set(self.getLOSTargets(unit,gameboard,args)).intersection(set(self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location,gameboard))))
        return spaces    

class AssassinPurposefulDodge(gen.PurposefulDodge):
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
    
class AssassinUnit(gen.Unit):
    
    name = 'Unit'
    unitClass = 'Assassin'
    damageBonus = 0
    
    def setClass(self,playerClass,playerID,captureCost):
        self.playerClass = playerClass
        self.playerID = playerID
        self.levelManager = gen.LevelManager(1,playerClass,self.unitType)
        self.unitAttributes = self.levelManager.getAttributes()
        self.attributeManager = gen.AttributeManager(self.unitAttributes)
        self.captureCost = captureCost
        self.abilities = {'Attack':AssassinAttack(playerID), 'Movement':gen.Movement(playerID), 'Reorient':gen.Reorient(playerID), 'Perception':gen.Perception(playerID),
                 'AccurateStrike': gen.AccurateStrike(playerID),'Avoid':AssassinAvoid(playerID),'PurposefulDodge':AssassinPurposefulDodge(playerID),'RedirectedStrike':gen.RedirectedStrike(playerID),
                 'Efficiency':Efficiency(playerID),'Notoriety':Notoriety(playerID),
                 'Stealth':Stealth(playerID),'Jaunt':Jaunt(playerID)}
        for x in self.abilities:
            self.abilities[x].unitName = self.unitName
        self.boardImage = gen.MySprite(self.playerClass,self.unitType)

    def createCombatModifiers(self,mods):
        target = mods['target']
        gameboard = mods['gameboard']
        mods = {}
        if self.unitType == 'Common' and 'Efficiency' in self.abilities:
            mods['Piercing'] = True
            mods['Assassin'] = 1
        if self.unitType == 'Elite' and 'Interrogate' in self.abilities:
            mods['Assassin'] = 2
        if gameboard[target].unitType in ['Elite','Common']:
            notoriety = gameboard[target].levelManager.level - self.levelManager.level
            if notoriety > 0:
                if 'AddHit' in mods:
                    mods['AddHit'] = mods['AddHit'] + notoriety
                else:
                    mods['AddHit'] = notoriety
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
        if self.location == unit and target in gameboard:
            if 'KidneyShot' in self.abilities and gameboard[target].name == 'Unit':
                if self.location in [gameboard[target].adjacentSpacesDir({'Location':self.location})[3],gameboard[target].adjacentSpacesDir({'Location':self.location})[5]]:
                    combatSteps['AddDamage'] = combatSteps['AddDamage'] + 1
            if 'BackStab' in self.abilities:
                if self.location in [gameboard[target].adjacentSpacesDir()[3],gameboard[target].adjacentSpacesDir()[5]]:
                    combatSteps['AddHit'] = combatSteps['AddHit'] + 2
            if 'FamiliarTerritory' in self.abilities:
                if [x for x in self.adjacentSpaces(target) if x in gameboard and gameboard[x].name == 'Objective']:
                    combatSteps['AddHit'] = combatSteps['AddHit'] + 3
                    combatSteps['AddDamage'] = combatSteps['AddDamage'] + 2
            if 'Killshot' in self.abilities:
                if gameboard[target].attributeManager.getAttributes('Health')/2 < self.attributeManager.getAttributes('Damage') + self.damageBonus:
                    combatSteps['AttackMods']['Wounding'] = 'True'
            if 'Phantom' in self.abilities and 'Evasion' in combatSteps['CombatResult'] and self.unitType == 'Elite':
                self.damageBonus = self.damageBonus + 1
            if [y for y in [x for x in self.adjacentSpaces(self.location) if x in gameboard] if 'Lethargy' in gameboard[y].abilities and gameboard[y].playerID != gameboard[unit].playerID] and 'Wounding' in combatSteps['AttackMods']:
                if 'Wounding' in combatSteps['AttackMods']:
                    del combatSteps['AttackMods']['Wounding']
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
                stealthtokens = [x for x in gameboard if gameboard[x].name == 'StealthToken']
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
                combatSteps['AddDamage'] = combatSteps['AddDamage'] + len([x for x in self.adjacentSpaces(self.location) if x in gameboard and gameboard[x].name == 'StealthToken' and gameboard[x].playerID == self.playerID])
            if 'Portent' in self.abilities:
                if self.abilities['Portent'].active:
                    combatSteps['CalcEvasion'] = 2
                    self.abilities['Portent'].active = False
            
        if self.location == target:
            if 'Meld' in self.abilities:
                combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + len([x for x in self.adjacentSpaces(self.location) if x in gameboard and gameboard[x].name == 'StealthToken'])
            if 'Wounding' in combatSteps['AttackMods']:
                if 'Blur' in self.abilities:
                    del combatSteps['AttackMods']['Wounding']
                    combatSteps['CalcHit'] = 0
                    combatSteps['AddHit'] = 7
            if 'Anonymity' in self.abilities:
                spaces = len([x for x in gameboard[target].adjacentSpaces(target) if x in gameboard and gameboard[x].name == 'Unit' and gameboard[x].playerID != gameboard[unit].playerID])
                combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + spaces
            if [y for y in [x for x in self.adjacentSpaces(self.location) if x in gameboard] if 'Dyskinesia' in gameboard[y].abilities and gameboard[y].playerID != gameboard[unit].playerID]:
                disadv = random.randint(1,6)
                if combatSteps['CalcEvasion'] > disadv:
                    combatSteps['CalcEvasion'] = disadv            
            if 'Portent' in self.abilities:
                if self.abilities['Portent'].active:
                    combatSteps['CalcHit'] = 2
                    self.abilities['Portent'].active = False
            if [x for x in gameboard if type(x) is tuple and 'HoarFrost' in gameboard[x].abilities]:
                elites = [x for x in gameboard if type(x) is tuple and 'HoarFrost' in gameboard[x].abilities]
                for x in elites:
                    if gameboard[x].getDistance(target) <= gameboard[x].attunement['Water']:
                        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] - 2        
        return gameboard,combatSteps
    
    def indirectPassiveMods(self,source,target,gameboard,combatSteps):
        if 'Meld' in self.abilities:
            combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + len([x for x in self.adjacentSpaces(self.location) if x in gameboard and gameboard[x].name == 'StealthToken'])
        if 'Wounding' in combatSteps['AttackMods']:
            if 'Blur' in self.abilities:
                del combatSteps['AttackMods']['Wounding']
                combatSteps['CalcHit'] = 0
                combatSteps['AddHit'] = 7
        if 'Portent' in self.abilities:
            if self.abilities['Portent'].active:
                combatSteps['CalcHit'] = 2
                self.abilities['Portent'].active = False
        if [x for x in gameboard if type(x) is tuple and 'HoarFrost' in gameboard[x].abilities]:
            elites = [x for x in gameboard if type(x) is tuple and 'HoarFrost' in gameboard[x].abilities]
            for x in elites:
                if gameboard[x].getDistance(target) <= gameboard[x].attunement['Water']:
                    combatSteps['AddEvasion'] = combatSteps['AddEvasion'] - 2    
        return gameboard, combatSteps
    
    def movementEffects(self,unit,target,gameboard):
        if 'ShadowStep' in self.abilities:
            token = random.choice([x for x in gameboard[unit].adjacentSpaces(unit) if gameboard[x].name == 'StealthToken'])
            gameboard[random.choice([x for x in gameboard[unit].adjacentSpaces(token) if x not in gameboard])] = gameboard[token]
            del gameboard[token]
        return gameboard
        
    def addMovementSpaces(self,unit,origin,gameboard,spaces):
        if 'Reaper' in self.abilities:
            if [x for x in self.adjacentSpaces(unit) if x in gameboard and gameboard[x].name in ['Objective','Respawn']]:
                spaces = [a for b in [self.adjacentSpaces(x) for x in gameboard if type(x) is tuple and gameboard[x].name in ['Objective','Respawn']] for a in b if a not in gameboard]
        return spaces

# Tier 0
class Efficiency(gen.Ability):
    name = 'Efficiency'
    cost = {'Passive':['Passive']}
    
class Notoriety(gen.Ability):
    name = 'Notoriety'
    cost = {'Passive':['Passive']}
    
class Stealth(gen.Ability):
    name = 'Stealth'
    cost = {'Turn':['Movement']}
    
    def abilityEffect(self,unit,target,gameboard):
        if 'EffectiveCover' not in gameboard[unit].abilities:
            spaces = [x for x in gameboard[unit].adjacentSpaces(unit) if x not in gameboard]
            if spaces:
                place = random.choice(spaces)
                gameboard[place] = StealthToken(gameboard[unit].playerID,place)
                if 'BlastTrap' in gameboard[unit].abilities:
                    gameboard[place].setBlastTrap()
                return gameboard
        else:
            spaces = gameboard[unit].getAOETargets(2,unit,gameboard)
            if spaces:
                place = random.choice(spaces)
                gameboard[place] = StealthToken(gameboard[unit].playerID,place)
                if 'BlastTrap' in gameboard[unit].abilities:
                    gameboard[place].setBlastTrap()
                return gameboard
        return gameboard
                
class Jaunt(gen.Ability):
    name = 'Jaunt'
    cost = {'Passive':['Passive']}
    
# Tier 1: 2+
class QuickStep(gen.Ability):
    name = 'Quickstep'
    cost = {'Reaction':['Reaction']}
    state = ['AddEvasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + 1
        gameboard = gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,{'Distance':1,'Cost':'Passive'})
        user = [x for x in gameboard if type(x) is tuple and gameboard[x].name == 'Unit' and gameboard[x].unitName == self.unitName and gameboard[x].playerID == self.playerID]
        if user:
            combatSteps['newPosition'] = user[0]
        return gameboard,combatSteps
    
class KidneyShot(gen.Ability):
    name = 'KidneyShot'
    cost = {'Passive':['Passive']}
            
class Backstab(gen.Ability):
    name = 'Backstab'
    cost = {'Passive':['Passive']}
            
class Shift(gen.Ability):
    name = 'Shift'
    cost = {'Reaction':['Passive']}
    state = ['Evasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        gameboard,newpos = gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,{'Distance':1,'Cost':'Passive'})
        combatSteps['newPosition'] = newpos
        return gameboard,combatSteps
    
class Rope(gen.Ability):
    name = 'Rope'
    cost = {'Turn':['Special'],'Reaction':['Reaction']}
    state = ['Any']
    
    def getTargets(self,unit,gameboard,*args):
        return self.getLOSTargets(unit,gameboard,args)
    
    def getLOSTargets(self,unit,gameboard,*args):
        spaces = [x for x in self.getAOETargets(3,unit,gameboard) if gameboard[x].name == 'Unit']
        LOS = gameboard[unit].lineOfSightManager.lineOfSight['Clear']+gameboard[unit].lineOfSightManager.lineOfSight['Partial']
        potentialTargets = list(set(LOS).intersection(set(spaces)))
        return potentialTargets
    
    def abilityEffect(self,unit,target,gameboard,*combatSteps):
        potentialTargets = [x for x in gameboard[target].adjacentSpaces(target) if gameboard[unit].getDistance(x) < gameboard[unit].getDistance(target) and x != unit]
        if potentialTargets:
            targetSpace = random.choice(potentialTargets)
            gameboard[targetSpace] = gameboard[target]
            gameboard[targetSpace].changeLocation(targetSpace)
            del gameboard[target]
        if combatSteps:
            return gameboard,combatSteps
        return gameboard
    
class Sabotage(gen.Ability):
    name = 'Sabotage'
    cost = {'Turn':['Attack']}
    
    def getTargets(self,unit,gameboard):
        return [x for x in self.getMeleeTargets(unit,gameboard) if gameboard[x].name in ['Obstacle','Objective']]
        
    def abilityEffect(self,unit,target,gameboard):
        if gameboard[target].name == 'Objective':
            gameboard = self.dealDamage(unit,target,gameboard,3)
        if gameboard[target].name == 'Obstacle':
            gameboard = self.dealDamage(unit,target,gameboard,4)
        return gameboard
    
class HeightenedSenses(gen.Ability):
    name = 'HeightenedSenses'
    cost = {'Passive':['Passive']}
            
class Undercover(gen.Ability):
    name = 'Undercover'
    cost = {'Turn':['Movement']}
    
    def getTargets(self,unit,gameboard):
        potentialTargets = [x for x in gameboard if type(x) is tuple and gameboard[x].name == 'StealthToken']
        if potentialTargets:
            return potentialTargets
        else:
            return [unit]
    
    def abilityEffect(self,unit,target,gameboard):
        if unit == target:
            return gameboard
        else:
            spaces = [x for x in self.adjacentSpaces(target) if x not in gameboard]
            if spaces:
                moveStealthToken = random.choice(spaces)
                gameboard[moveStealthToken] = gameboard[target]
                del gameboard[target]
            return gameboard
        
class Interrogate(gen.Ability):
    name = 'Interrogate'
    cost = {'Passive':['Passive']}
            
class Afterimage(gen.Ability):
    name = 'Afterimage'
    cost = {'Turn':['Movement'],'Reaction':['Reaction']}
    state = ['Evasion']
    
    def getTargets(self,unit,gameboard):
        return [x for x in list(set(self.getAOETargets(3,unit,gameboard)).intersection(set(gameboard))) if gameboard[x].name == 'StealthToken']
    
    def abilityEffect(self,unit,target,gameboard,*combatSteps):
        gameboard[target] = gameboard[unit]
        gameboard[target].location = target
        del gameboard[unit]
        if combatSteps:
            return gameboard,combatSteps
        return gameboard
        
class DeepStrike(gen.Ability):
    name = 'DeepStrike'
    cost = {'Turn':['Movement']}
    
    def getTargets(self,unit,gameboard):
        spaces = [x for x in gameboard if type(x) is tuple and gameboard[x].name in ['Respawn','Objective']]
        return [x for y in [self.adjacentSpaces(x) for x in spaces] for x in y if x in gameboard and gameboard[x] == 'StealthToken']            
    
    def abilityEffect(self,unit,target,gameboard):  
        gameboard[target] = gameboard[unit]
        del gameboard[unit]
        return gameboard
        
class Meld(gen.Ability):
    name = 'Meld'
    cost = {'Passive':['Passive']}
            
class Cripple(gen.Ability):
    name = 'Cripple'
    cost = {'Passive':['Passive']}
            
# Tier 2: 5+

class SurpriseAttack(gen.Ability):
    name = 'SurpriseAttack'
    cost = {'Passive':['Passive']}
    
class AssassinCounter(gen.Ability):
    name = 'Counter'
    cost = {'Reaction':['Reaction']}
    state = ['Evasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        if target in self.getMeleeTargets(target,gameboard):
            gameboard = self.combat(unit,target,gameboard,{'AddHit':3})
        return gameboard,combatSteps
    
class Blur(gen.Ability):
    name = 'Blur'
    cost = {'Reaction':['Reaction']}
    state = ['PreEvasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        advantage = random.randint(1,6)
        if advantage > combatSteps['CalcHit']:
            combatSteps['CalcHit'] < advantage
            combatSteps['CalcHit'] = advantage
        return gameboard,combatSteps
    
class FamiliarTerritory(gen.Ability):
    name = 'FamiliarTerritory'
    cost = {'Passive':['Passive']}
            
class CriticalStrike(gen.Ability):
    name = 'CriticalStrike'
    cost = {'Passive':['Passive']}
    
class BodyDouble(gen.Ability):
    name = 'BodyDouble'
    cost = {'Turn':['Special'],'Reaction':['Reaction']}
    state = ['Any']
    use = 'Elite'
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard if type(x) is tuple and gameboard[x].unitType == 'Common' and gameboard[x].playerID == gameboard[unit].playerID]
    
    def abilityEffect(self,unit,target,gameboard,*combatSteps):
        temp = gameboard[unit]
        gameboard[unit] = gameboard[target]
        gameboard[target] = temp
        if combatSteps:
            return gameboard,combatSteps
        else:
            return gameboard
    
class Shadowstep(gen.Ability):
    name = 'Shadowstep'
    cost = {'Passive':['Passive']}
            
class BlastTrap(gen.Ability):
    name = 'BlastTrap'
    cost = {'Passive':['Passive']}
            
class Anonymity(gen.Ability):
    name = 'Anonymity'
    cost = {'Passive':['Passive']}
            
class Phantom(gen.Ability):
    name = 'Phantom'
    cost = {'Passive':['Passive']}
            
# Tier 3: 9+
class Killshot(gen.Ability):
    name = 'Killshot'
    cost = {'Passive':['Passive']}
            
class Aversion(gen.Ability):
    name = 'Aversion'
    cost = {'Reaction':['Reaction']}
    state = ['Wounding']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['Damage'] = math.floor((combatSteps['Damage'] + combatSteps['AddDamage'])/2)
        return gameboard,combatSteps
    
class Vendetta(gen.Ability):
    name = 'Vendetta'
    cost = {'Reaction':['Reaction']}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        if damage >= 4:
            if unit in gameboard:
                gameboard[unit].attributeManager.setBonusAttributes('Attack',1)
        return gameboard, damage, unit
        
class Reaper(gen.Ability):
    name = 'Reaper'
    cost = {'Passive':['Passive']}

class House(gen.GeneralUse):
    houseRanks = {1:'Resident',2:'Seneschal',3:'Vizier',4:'Grand Master'}
    
class Conium(House):
    name = 'Conium'
    abilities = {
            1: ['Virulency','Infect'],
            2: ['PoisonedDagger','Lethargy'],
            3: ['Metastasis','Biohazard'],
            4: ['Plagelord','Dyskinesia']
        }
    
class Virulency(gen.Ability):
    name = 'Virulency'
    cost = {'Passive':['Passive']}
            
class Infect(gen.Ability):
    name = 'Infect'
    cost = {'Passive':['Passive']}
            
class PoisonedDagger(gen.Ability):
    name = 'PoisonedDagger'
    cost = {'Reaction':['Special']}
    state = ['MissedMeleeAttack']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['CombatResult'] = 'Hit'
        combatSteps['Damage'] = gameboard[unit].attributeManager.getAttributes['Damage']
        combatSteps['AddDamage'] = 0
        combatSteps['AttackMods'] = combatSteps['AttackMods'] + ['Wounding']
        return gameboard, combatSteps
    
class Lethargy(gen.Ability):
    name = 'Lethargy'
    cost = {'Passive':['Passive']}
            
class Metastasis(gen.Ability):
    name = 'Metastasis'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return self.getLOSTargets(unit,gameboard,{'Range':3})
    
    def abilityEffect(self,unit,target,gameboard):
        return self.dealDamage(unit,target,gameboard,3)
    
class Biohazard(gen.Ability):
    name = 'Biohazard'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return self.getAOETargets(2,unit,gameboard)
    
    def abilityEffect(self,unit,target,gameboard):
        for x in target:
            self.combat(unit,target,gameboard,{'AttackMods':'Wounding','Damage':3})
        return gameboard
    
    def execute(self,unit,gameboard,*args):
        potentialTargets = self.getTargets(unit,gameboard,*args)
        target = potentialTargets
        gameboard = self.abilityEffect(unit,target,gameboard)
        gameboard[unit].reactionManager.setState('None')
        gameboard[target].reactionManager.setState('None')
        return gameboard
    
class Plaguelord(gen.Ability):
    name = 'Plaguelord'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return self.getAOETargets(1,unit,gameboard)            
    
    def abilityEffect(self,unit,target,gameboard):
        for x in target:
            self.dealDamage(unit,target,gameboard,gameboard[unit].damageBonus)
        gameboard[unit].damageBonus = 0
        return gameboard
        
    def execute(self,unit,gameboard,*args):
        potentialTargets = self.getTargets(unit,gameboard,*args)
        target = [x for x in potentialTargets if gameboard[x].name == 'Unit']
        gameboard = self.abilityEffect(unit,target,gameboard)
        gameboard[unit].reactionManager.setState('None')
        gameboard[target].reactionManager.setState('None')
        return gameboard
        
class Dyskinesia(gen.Ability):
    name = 'Dyskinesia'
    cost = {'Passive':['Passive']}
                    
class Naal(House):
    name = 'Naal'
    
    abilities = {
            1: ['Ranger','Mark'],
            2: ['Sniper','EffectiveCover'],
            3: ['Camouflage','Communications'],
            4: ['Vantage','Spotter']
        }
    
class Ranger(gen.Ability):
    name = 'Ranger'
    cost = {'Passive':['Passive']}
    
    def __init__(self,unitName,player):
        self.unitName = unitName
        self.player = player
    
    def statEffect(self,unitObj):
        unitObj.changePermanentUpgrade('Special',-1)
        unitObj.unitRange = 3
        return unitObj
    
class Mark(gen.Ability):
    name = 'Mark'
    cost = {'Passive':['Passive']}
                
class Sniper(gen.Ability):
    name = 'Sniper'
    cost = {'Passive':['Passive']}
                
    def statEffect(self,unitObj):
        unitObj.changePermanentUpgrade('Hit',-2)
        return unitObj
    
class EffectiveCover(gen.Ability):
    name = 'EffectiveCover'
    cost = {'Passive':['Passive']}
                
class Camouflage(gen.Ability):
    name = 'Camouflage'
    cost = {'Passive':['Passive']}
    
    def abilityEffect(self,unit,gameboard):
        spaces = [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard]
        for x in spaces:
            gameboard[x] = StealthToken()
        gameboard[unit].attributeManager.currentAttributes['Movement'] = 0
        return gameboard
        
class Communications(gen.Ability):
    name = 'Communications'
    cost = {'Passive':['Passive']}
                
class Vantage(gen.Ability):
    name = 'Vantage'
    cost = {'Passive':['Passive']}
                
class Spotter(gen.Ability):
    name = 'Spotter'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard]
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = SpotterUnit(gameboard[unit].playerID)

class SpotterUnit(gen.Unit):
    
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
    
class Shadowstrike(gen.Ability):
    name = 'Shadowstrike'
    cost = {'Reaction':['Passive']}
    state = ['EliminateUnit']
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = StealthToken(gameboard[unit].playerID,target)
        return gameboard
        
class CloakAndDagger(gen.Ability):
    name = 'CloakAndDagger'
    cost = {'Passive':['Passive']}
            
class Infiltrate(gen.Ability):
    name = 'Infiltrate'
    cost = {'Passive':['Passive']}
            
class Misdirection(gen.Ability):
    name = 'Misdirection'
    cost = {'Passive':['Passive']}
            
class Stalk(gen.Ability):
    name = 'Stalk'
    cost = {'Passive':['Passive']}
                
class Smokescreen(gen.Ability):
    name = 'Smokescreen'
    cost = {'Turn':'Special'}
    
    def getTargets(self,unit,gameboard):
        self.getAOETargets(3,gameboard[unit].location,gameboard)
        
    def abilityEffect(self,unit,target,gameboard):
        spaces = [x for x in self.adjacentSpaces(target) if x not in gameboard]
        for x in spaces:
            gameboard[x] = StealthToken(gameboard[unit].playerID,gameboard[unit].location)
        return gameboard
    
class Eviscerate(gen.Ability):
    name = 'Eviscerate'
    cost = {'Passive':['Passive']}
                
class Sneak(gen.Ability):
    name = 'Sneak'
    cost = {'Passive':['Passive']}
            
class Esper(House):
    name = 'Esper'
    
    abilities = {
            1:['Levitation','TimeDilation'],
            2:['Portent','PsychicScream'],
            3:['Kineblade','Barrier'],
            4:['Crumple','Savant']
        }
    
class Levitation(gen.Ability):
    name = 'Levitation'
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].unrestrainedMovement = True
        gameboard[unit].attributeManager.changeAttribute('Evasion',2)
        gameboard[unit].attributeManager.changeAttribute('Movement',2)
        return gameboard
        
class TimeDilation(gen.Ability):
    name = 'TimeDilation'
    cost = {'Passive':['Passive']}
                
class Portent(gen.Ability):
    name = 'Portent'
    cost = {'Turn':['Special']}
    active = False
    
    def abilityEffect(self,unit,target,gameboard):
        self.active = True
        return gameboard
    
class PsychicScream(gen.Ability):
    name = 'PsychicScream'
    cost = {'Turn':['Special']}
    active = False
    
    def abilityEffect(self,unit,target,gameboard):
        self.active = True
        return gameboard
    
class Kineblade(gen.Ability):
    name = 'Kineblade'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard]
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = SpotterUnit(gameboard[unit].playerID)   
        return gameboard         
        
class KinebladeUnit(gen.Unit):
    name = 'KinebladeUnit'

    def __init__(self,playerID):
        self.playerID = playerID        

class Barrier:
    name = 'Barrier'
    cost = {'Reaction':['Reaction']}
    state = ['AddEvasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['Armor'] = combatSteps['Armor'] + 3
        combatSteps['Evasion'] = combatSteps['Evasion'] + 1
        return gameboard, combatSteps
        
class Crumple:
    name = 'Crumple'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return self.getLOSTargets(unit,gameboard,{'Range':3})
    
    def abilityEffect(self,unit,target,gameboard):
        mods = gameboard[unit].createCombatModifiers({'unit':unit,'target':target,'gameboard':gameboard})
        mods['Wounding'] = True
        mods['Piercing'] = True
        gameboard[unit].changeAttributes('Attack',-1)
        return self.combat(unit,target,gameboard,mods)               
        
class Savant(gen.Unit):
    name = 'Savant'
    cost = {'Turn':['Special']}
    
    def getTargets(self,unit,gameboard):
        return [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard]
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[target] = SpotterUnit(gameboard[unit].playerID)
        return gameboard
        
class SavantUnit(gen.Unit):
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
    
class Airborne(gen.Ability):
    name = 'Airborne'
    cost = {'Passive':['Passive']}
                
class Disengage(gen.Ability):
    name = 'Disengage'
    cost = {'Reaction':['Reaction']}
    state = ['AfterAttack']
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Movement',3)
        gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,{'Distance':3})
        return gameboard
    
class Lift(gen.Ability):
    name = 'Lift'
    cost = {'Turn':['Special','Movement']}
    
    def abilityEffect(self,unit,target,gameboard):
        space = random.choice(self.getAOETargets(6,unit,gameboard))
        gameboard[space] = gameboard[unit]
        del gameboard[unit]
        return gameboard
       
class Rush(gen.Ability):
    name = 'Rush'
    cost = {'Turn':['Movement','Attack']}
    
    def getTargets(self,unit,gameboard):
        return []
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Movement',3)
        gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,{'Distance':3})            
        return gameboard[unit].abilities['Attack'].execute(unit,gameboard)
        
class RendingStrike(gen.Ability):
    name = 'RendingStrike'
    cost = {'Reaction':['Movement']}
    state = ['AddHit']
    # add piercing and swift to an attack
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['AttackMods']['Piercing'] = True
        combatSteps['AttackMods']['Swift'] = True
        return gameboard, combatSteps
    
class Flurry(gen.Ability):
    name = 'Flurry'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard[unit].attributeManager.changeAttributes('Attack',1)            
        gameboard[unit].abilities['Attack'].execute(unit,gameboard)
        gameboard[unit].abilities['Attack'].execute(unit,gameboard)
        return gameboard
    
class ConcussiveJump(gen.Ability):
    name = 'ConcussiveJump'
    cost = {'Turn':['Special','Movement']}
    
    def abilityEffect(self,unit,target,gameboard):
        targets = self.getAOETargets(1,unit,gameboard)
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Wounding':True})
        space = random.choice(self.getAOETargets(4,unit,gameboard))
        gameboard[space] = gameboard[unit]
        del gameboard[unit]
        targets = self.getAOETargets(1,space,gameboard)
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Wounding':True})
        return gameboard
    
class Flock(gen.Ability):
    name = 'Flock'
    cost = {'Passive':['Passive']}
                
class AssassinPlayer(gen.Player):
    
    houseRank = {'Conium':0,'Naal':0,'Caecus':0,'Esper':0,'Accipiter':0}
    houses = {'Conium':Conium(),'Naal':Naal(),'Caecus':Caecus(),'Esper':Esper(),'Accipiter':Accipiter()}
    damageBonus = 0
    attackMods = []

    def __init__(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        # instantiate new units
        self.units = {'Elite':AssassinUnit('Elite','Elite'),'Common1':AssassinUnit('Common','Common1'),\
                      'Common2':AssassinUnit('Common','Common2'),'Common3':AssassinUnit('Common','Common3'),\
                      'Common4':AssassinUnit('Common','Common4')}
        for unit in self.units:
            self.units[unit].setClass(self.playerClass,self.playerID,self.captureCost)
        
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

        tokens = [x for x in gameboard if type(x) is tuple and gameboard[x].name == 'StealthToken' and self.playerID == gameboard[x].playerID]
        if 'Camouflage' in self.abilities:
            if random.choice(['Pass','Camouflage']) == 'Camouflage':
                elite = [x for x in gameboard if type(x) is tuple and gameboard[x].unitType == 'Elite' and gameboard[x].playerID == self.playerID]
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
        units = [x for x in gameboard if type(x) is tuple and gameboard[x].playerID == self.playerID and gameboard[x].unitType in ['Common','Elite']]
        commons = [x for x in units if gameboard[x].unitType == 'Common']
        elite = [x for x in units if gameboard[x].unitType == 'Elite']
        for x in commons:
            self.damageBonus = self.damageBonus + gameboard[x].damageBonus
            gameboard[x].damageBonus = 0
        for x in elite:
            gameboard[x].damageBonus = self.damageBonus
            self.units['Elite'].damageBonus = self.damageBonus

        units = [x for x in gameboard if type(x) is tuple and 'Tectonics' in gameboard[x].abilities]        
        if units:
            for unit in units:
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
            
    def tier1(self):
        return {'Quickstep':QuickStep(self.playerID),'KidneyShot':KidneyShot(self.playerID),'Backstab':Backstab(self.playerID),'Shift':Shift(self.playerID),'Rope':Rope(self.playerID),\
                'Sabotage':Sabotage(self.playerID),'HeightenedSenses':HeightenedSenses(self.playerID),'Undercover':Undercover(self.playerID),\
                'Interrogate':Interrogate(self.playerID),'Afterimage':Afterimage(self.playerID),'DeepStrike':DeepStrike(self.playerID),'Meld':Meld(self.playerID),'Cripple':Cripple(self.playerID)}
    def tier2(self):
        return {'Counter':AssassinCounter(self.playerID),'Blur':Blur(self.playerID),'FamiliarTerritory':FamiliarTerritory(self.playerID),\
                'CriticalStrike':CriticalStrike(self.playerID),'SurpriseAttack':SurpriseAttack(self.playerID),'BodyDouble':BodyDouble(self.playerID),\
                'Shadowstep':Shadowstep(self.playerID),'BlastTrap':BlastTrap(self.playerID),'Anonymity':Anonymity(self.playerID),'Phantom':Phantom(self.playerID)}
    def tier3(self):
        return {'Killshot':Killshot(self.playerID),'Aversion':Aversion(self.playerID),'Vendetta':Vendetta(self.playerID),'Reaper':Reaper(self.playerID)}

    def availableAbilities(self):
        if self.level < 5:
            return {x:self.tier1().get(x) for x in self.tier1() if x not in self.abilities}
        elif self.level >= 5 and self.level < 9:
            options = {**self.tier1(),**self.tier2()}
            return {x:options.get(x) for x in options if x not in self.abilities}
        else:
            options = {**self.tier1(),**self.tier2(),**self.tier3()}
            return {x:options.get(x) for x in options if x not in self.abilities}