# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:39:22 2020

@author: bgool
"""

import lineOfSight as LOS

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
        gameboard[unit].abilities.get('Movement').execute(unit,target,gameboard,move)
        return gameboard       
    
class AssassinUnit(Unit):

    def setClass(self,playerClass,playerID,captureCost):
        self.playerClass = playerClass
        self.playerID = playerID
        self.levelManager = LevelManager(1,playerClass,self.unitType)
        self.unitAttributes = self.levelManager.getAttributes()
        self.attributeManager = AttributeManager(self.unitAttributes)
        self.captureCost = captureCost
        self.abilities = {'Pass':Pass(),'Attack':Attack(self.unitName,playerID), 'Movement':Movement(self.unitName,playerID), 'Reorient':Reorient(self.unitName,playerID), 'Perception':Perception(self.unitName,playerID),
                 'AccurateStrike': AccurateStrike(self.unitName,playerID),'Avoid':AssassinAvoid(self.unitName,playerID),'PurposefulDodge':PurposefulDodge(self.unitName,playerID),'RedirectedStrike':RedirectedStrike(self.unitName,playerID),
                 'StealthToken':StealthToken(self.unitName,playerID),'Efficiency':Efficiency(self.unitName,playerID),'Notoriety':Notoriety(self.unitName,playerID),
                 'Stealth':Stealth(self.unitName,playerID),'Jaunt':Jaunt(self.unitName,playerID)}
    
    def createCombatModifiers(self,**kwargs):
        unit,target,gameboard = kwargs['unit'],kwargs['target'],kwargs['gameboard']
        mods = {}
        if self.unitType == 'Common' and 'Efficiency' in self.abilities:
            mods['Piercing'] = True
            mods['Assassin'] = 1
        if self.unitType == 'Elite' and 'Interrogate' in self.abilities:
            mods['Assassin'] = 2
        if 'target' in kwargs and 'gameboard' in kwargs:
            notoriety = kwargs['gameboard'][kwargs['target']].level - self.level
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
            if [y for y in [x for x in self.adjacentSpaces()] if 'Lethargy' in gameboard[y].abilities and gameboard[y].playerID != gameboard[unit].playerID] and 'Wounding' in combatSteps['AttackMods']:
                combatSteps['AttackMods'].remove('Wounding')
            if [y for y in [x for x in self.adjacentSpaces()] if 'Dyskinesia' in gameboard[y].abilities and gameboard[y].playerID != gameboard[unit].playerID]:
                disadv = random.randint(1,6)
                if combatSteps['CalcHit'] > disadv:
                    combatSteps['CalcHit'] = disadv
            if [y for y in [x for x in gameboard[target].adjacentSpaces()] if 'Mark' in gameboard[y].abilities and gameboard[y].playerID == self.playerID and self.unitType == 'Elite']:
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
                    
        if self.location == target:
            if 'Meld' in self.abilities:
                mod['AddEvasion'] = mods['AddEvasion'] + len([x for x in self.adjacentSpaces(self.location) if type(gameboard[x]).__name__ == 'StealthToken'])
            if 'Wounding' in combatSteps['AttackMods']:
                if 'Blur' in self.abilities:
                    combatSteps['AttackMods'].remove('Wounding')
                    combatSteps['CalcHit'] = 0
                    combatSteps['AddHit'] = 7
            if 'Anonymity' in self.abilities:
                spaces = len([x for x in gameboard[target].adjacentSpaces() if type(gameboard[x]).__name__ == 'Unit' and gameboard[x].playerID != gameboard[unit].playerID])
                combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + spaces
            if [y for y in [x for x in self.adjacentSpaces()] if 'Dyskinesia' in gameboard[y].abilities and gameboard[y].playerID != gameboard[unit].playerID]:
                disadv = random.randint(1,6)
                if combatSteps['CalcEvasion'] > disadv:
                    combatSteps['CalcEvasion'] = disadv            
                
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
    
class AssassinPlayer(Player):
    
    houseRank = {'Conium':0,'Naal':0,'Caecus':0,'Esper':0,'Accipiter':0}
    houses = {'Conium':Conium(),'Naal':Naal(),'Caecus':Caecus(),'Esper':Esper(),'Accipiter':Accipiter()}
    damageBonus = 0
    attackMods = []
    
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
                        self.units[x] = self.units[x].abilities[houseAbility].statEffect(units[x])
        
        
    def tier1():
        return {'Quickstep':QuickStep(),'KidneyShot':KidneyShot(),'Backstab':Backstab(),'Shift':Shift(),'Rope':Rope(),\
                'Sabotage':Sabotage(),'HeightenedSenses':HeightenedSenses(),'Undercover':Undercover(),\
                'Interrogate':Interrogate(),'Afterimage':Afterimage(),'DeepStrike':DeepStrike(),'Meld':Meld(),'Cripple':Cripple()}
    def tier2():
        return {'Counter':Counter(),'Blur':Blur(),'FamiliarTerritory':FamiliarTerritory(),\
                'CriticalStrike':CriticalStrike(),'SurpriseAttack':SurpriseAttack(),'BodyDouble':BodyDouble(),\
                'Shadowstep':Shadowstep(),'BlastTrap':BlastTrap(),'Anonymity':Anonymity(),'Phantom':Phantom()}
    def tier3():
        return {'Killshot':Killshot(),'Aversion':Aversion(),'Vendetta':Vendetta(),'Reaper':Reaper()}
 
    # Tier 0
    class Efficiency(Ability):
        name = 'Efficiency'
        cost = {'Passive':'Passive'}
        
    class Notoriety(Ability):
        name = 'Notoriety'
        cost = {'Passive':'Passive'}
        
    class Stealth(Ability):
        name = 'Stealth'
        cost = {'Turn':'Movement'}
        
        def abilityEffect(self,unit,target,gameboard):
            if 'EffectiveCover' not in gameboard[unit].abilities:
                gameboard[random.choice([x for x in gameboard[unit].adjacentSpaces() if x not in gameboard])] = StealthToken()
            else:
                gameboard[random.choice([x for x in gameboard[unit].getAOETargets(2,unit) if x not in gameboard])] = StealthToken()

    class Jaunt(Ability):
        name = 'Jaunt'
        cost = {'Passive':'Passive'}
        
    # Tier 1: 2+
    class QuickStep(Ability):
        name = 'Quickstep'
        cost = {'Reaction':'Reaction'}
        state = ['AddEvasion']
        
        def abilityEffect(self,unit,target,gameboard,combatSteps):
            combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + 1
            gameboard,newpos = gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,'Distance'=1)
            combatSteps['newPosition'] = newpos
            return gameboard,combatSteps
        
    class KidneyShot(Ability):
        name = 'KidneyShot'
        cost = {'Passive':'Passive'}
                
    class Backstab(Ability):
        name = 'Backstab'
        cost = {'Passive':'Passive'}
                
    class Shift(Ability):
        name = 'Shift'
        cost = {'Reaction':'Passive'}
        state = ['Evasion']
        
        def abilityEffect(self,unit,target,gameboard,combatSteps):
            gameboard,newpos = gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,'Distance'=1,'Cost'='Passive')
            combatSteps['newPosition'] = newpos
            return gameboard,combatSteps
        
    class Rope(Ability):
        name = 'Rope'
        cost = {'Turn':'Special','Reaction':'Reaction'}
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
        cost = {'Turn':'Attack'}
        
        def getTargets(self,unit,gameboard,*args):
            return [x for x in self.getMeleeTargets(unit,gameboard) if type(gameboard[x]) in ['Obstacle','Objective']]
            
        def abilityEffect(self,unit,target,gameboard):
            if type(gameboard[target]).__name__ == 'Objective':
                self.dealDamage(unit,target,gameboard,3)
            if type(gameboard[target]).__name__ == 'Obstacle':
                self.dealDamage(unit,target,gameboard,4)
            
    class HeightenedSenses(Ability):
        name = 'HeightenedSenses'
        cost = {'Passive':'Passive'}
                
    class Undercover(Ability):
        name = 'Undercover'
        cost = {'Turn':'Movement'}
        
        def getTargets(unit,gameboard):
            return [x for x in gameboard if type(gameboard[x]).__name__ == 'StealthToken']
        
        def abilityEffect(self,unit,target,gameboard):
            moveStealthToken = random.choice([x for x in self.adjacentSpaces(target) if x not in gameboard])
            gameboard[moveStealthToken] = gameboard[target]
            del gameboard[target]
            return gameboard
            
    class Interrogate(Ability):
        name = 'Interrogate'
        cost = {'Passive':'Passive'}
                
    class Afterimage(Ability):
        name = 'Afterimage'
        cost = {'Turn':'Movement','Reaction':'Reaction'}
        state = ['Evasion']
        
        def getTargets(unit,gameboard):
            return [x for x in set(getAOETargets(3,unit)).intersection(set(gameboard)) if type(gameboard[x]).__name__ == 'StealthToken']
        
        def abilityEffect(self,unit,target,gameboard):
            gameboard[target] = gameboard[unit]
            del gameboard[unit]
            return gameboard
            
    class DeepStrike(Ability):
        name = 'DeepStrike'
        cost = {'Turn':'Movement'}
        
        def getTargets(unit,gameboard):
            spaces = [x for x in gameboard if type(gameboard[x]).__name__ == 'Respawn' or type(gameboard[x]).__name__ == 'Objective']
            return [x for x in list(set([y for y in self.adjacentSpaces(x) for x in spaces])) if type(gameboard[x]).__name__ == 'StealthToken']
        
        def abilityEffect(self,unit,target,gameboard):  
            gameboard[target] = gameboard[unit]
            del gameboard[unit]
            return gameboard
            
    class Meld(Ability):
        name = 'Meld'
        cost = {'Passive':'Passive'}
                
    class Cripple(Ability):
        name = 'Cripple'
        cost = {'Passive':'Passive'}
                
    # Tier 2: 5+
    class Counter(Ability):
        name = 'Counter'
        name = {'Reaction':'Reaction'}
        state = ['Evasion']
        
        def abilityEffect(self,unit,target,gameboard):
            if target in self.getMeleeTargets(target,gameboard):
                return self.combat(unit,target,gameboard,{'AddHit':3})
            else:
                return gameboard
        
    class Blur(Ability):
        name = 'Blur'
        cost = {'Reaction':'Reaction'}
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
        cost = {'Turn':'Special','Reaction':'Reaction'}
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
        cost = {'Passive':'Passive'}
                
    class BlastTrap(Ability):
        name = 'BlastTrap'
        cost = {'Passive':'Passive'}
                
    class Anonymity(Ability):
        name = 'Anonymity'
        cost = {'Passive':'Passive'}
                
    class Phantom(Ability):
        name = 'Phantom'
        cost = {'Passive':'Passive'}
                
    # Tier 3: 9+
    class Killshot(Ability):
        name = 'Killshot'
        cost = {'Passive':'Passive'}
                
    class Aversion(Ability):
        name = 'Aversion'
        cost = {'Reaction':'Reaction'}
        state = ['Wounding']
        
        def abilityEffect(self,unit,target,gameboard,combatSteps):
            combatSteps['Damage'] = floor((combatSteps['Damage'] + combatSteps['AddDamage'])/2)
            return gameboard,combatSteps
        
    class Vendetta(Ability):
        name = 'Vendetta'
        cost = {'Reaction':'Reaction'}
        state = ['TakeDamage']
        
        def abilityEffect(self,unit,target,gameboard,combatSteps):
            if combatSteps['ResultingDamage'] >= 4:
                self.attributeManager.setBonusAttributes('Attack',1)
            
    class Reaper(Ability):
        name = 'Reaper'
        cost = {'Passive':'Passive'}
    
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
        
    class Virulency:
        name = 'Virulency'
        cost = {'Passive':'Passive'}
                
    class Infect:
        name = 'Infect'
        cost = {'Passive':'Passive'}
                
    class PoisonedDagger:
        name = 'PoisonedDagger'
        cost = {'Reaction':'Special'}
        state = ['MissedMeleeAttack']
        
        def abilityEffect(self,unit,target,gameboard,combatSteps):
            combatSteps['CombatResult'] = 'Hit'
            combatSteps['Damage'] = gameboard[unit].attributeManager.getAttribute['Damage']
            combatSteps['AddDamage'] = 0
            combatSteps['AttackMods'] = combatSteps['AttackMods'] + ['Wounding']
            return gameboard, combatSteps
        
    class Lethargy:
        name = 'Lethargy'
        cost = {'Passive':'Passive'}
                
    class Metastasis:
        name = 'Metastasis'
        cost = {'Turn':'Special'}
        
        def getTargets(self,unit,gameboard):
            return self.getLOSTargets(unit,gameboard,{'Range':3})
        
        def abilityEffect(self,unit,target,gameboard):
            return self.dealDamage(unit,target,gameboard,3)
        
    class Biohazard:
        name = 'Biohazard'
        cost = {'Turn':'Special'}
        
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
        
    class Plaguelord:
        name = 'Plaguelord'
        cost = {'Turn':'Special'}
        
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
            
    class Dyskinesia:
        name = 'Dyskinesia'
        cost = {'Passive':'Passive'}
                        
    class Naal(House):
        name = 'Naal'
        
        abilities = {
                1: ['Ranger','Mark'],
                2: ['Sniper','EffectiveCover'],
                3: ['Camouflage','Communications'],
                4: ['Vantage','Spotter']
            }
        
    class Ranger:
        name = 'Ranger'
        cost = {'Passive':'Passive'}
        
        def __init__(self,unitName,player):
            self.unitName = unitName
            self.player = player
        
        def statEffect(self,unitObj):
            unitObj.changePermanentUpgrade('Special',-1)
            unitObj.unitRange = 3
            return unitObj
        
    class Mark:
        name = 'Mark'
        cost = {'Passive','Passive'}
                    
    class Sniper:
        name = 'Sniper'
        cost = {'Passive':'Passive'}
                    
        def statEffect(self,unitObj):
            unitObj.changePermanentUpgrade('Hit',-2)
            return unitObj
        
    class EffectiveCover:
        name = 'EffectiveCover'
        cost = {'Passive':'Passive'}
                    
    class Camouflage:
        name = 'Camouflage'
        cost = {'Reaction':'Passive'}
        state = ['TurnStart']
        
        def abilityEffect(self,unit,target,gameboard):
            spaces = [x for x in gameboard[unit].adjacentSpaces() if x not in gameboard]
            for x in spaces:
                gameboard[x] = StealthToken()
            gameboard[unit].attributeManager.currentAttributes['Movement'] = 0
            return gameboard
            
    class Communications:
        name = 'Communications'
        cost = {'Passive':'Passive'}
                    
    class Vantage:
        name = 'Vantage'
        cost = {'Passive':'Passive'}
                    
    class Spotter(Ability):
        name = 'Spotter'
        cost = {'Turn':'Special'}
        
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
        cost = {'Reaction':'Passive'}
        state = ['EliminateUnit']
        
        def abilityEffect(self,unit,target,gameboard):
            gameboard[target] = StealthToken(gameboard[unit].playerID,target)
            
    class CloakAndDagger:
        name = 'CloakAndDagger'
        cost = {'Passive':'Passive'}
        
        def abilityEffect(self,unit,target,gameboard):
        
    class Infiltrate:
        name = 'Infiltrate'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
        
    class Misdirection:
        name = 'Misdirection'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
        
    class Stalk:
        name = 'Stalk'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Smokescreen:
        name = 'Smokescreen'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Eviscerate:
        name = 'Eviscerate'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Sneak:
        name = 'Sneak'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
        
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
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class TimeDilation:
        name = 'TimeDilation'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Portent:
        name = 'Portent'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class PsychicScream:
        name = 'PsychicScream'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Kineblade:
        name = 'Kineblade'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Barrier:
        name = 'Barrier'
        cost = ['Reaction']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Crumple:
        name = 'Crumple'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Savant(Unit):
        name = 'Savant'
        cost = ['Special']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Accipiter(House):
        
        name = 'Accipiter'
        abilities = {
                1:['Airborne','Disengage'],
                2:['Lift','Rush'],
                3:['RendingStrike','Flurry']
                4:['ConcussiveJump','Flock']
            }
        
    class Airborne:
        name = 'Airborne'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Disengage:
        name = 'Disengage'
        cost = ['Reaction']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Lift:
        name = 'Lift'
        cost = ['Special','Movement']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Rush:
        name = 'Rush'
        cost = ['Movement','Attack']
        
        def abilityEffect(self,unit,target,gameboard):
    
    class RendingStrike:
        name = 'RendingStrike'
        cost = ['Movement']
        # add piercing and swift to an attack
        def abilityEffect
        
    class Flurry:
        name = 'Flurry'
        cost = ['Attack']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class ConcussiveJump:
        name = 'ConcussiveJump'
        cost = ['Special','Movement']
        
        def abilityEffect(self,unit,target,gameboard):
            
    class Flock:
        name = 'Flock'
        cost = ['Passive']
        
        def abilityEffect(self,unit,target,gameboard):