# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:56:44 2020

@author: bgool
"""

class WarriorUnit(Unit):
    
    weaponUpgrades = {'Warhammer':0,'Spear':0,'Katana':0,'Rapier':0,'Axe':0,'Greatsword':0,'Bow':0}
    form = 1
    
    def __init__(self,unitType,unitName,weapons):
        super().__init__(unitType,unitName)
        self.weapons = weapons
        
    def increaseForm(self):
        while True:
            self.form = self.form + 1
            if self.form == 5:
                self.form == 1
            yield form
            
    def upgradeWeapon(self,weapon):
        if self.weaponUpgrades[weapon] < 3:
            self.weaponUpgrades[weapon] = self.weaponUpgrades[weapon] + 1
       
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
        return gameboard,combatSteps        
    
class WarriorPlayer(Player):
    
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
    
    class WarriorAttack(Attack):
        name = 'Attack'
        cost = {'Turn':['Attack']}
        
        def abilityEffect(self,unit,target,gameboard):
            gameboard[unit].changeAttributes('Attack',-1)
            return self.combat(unit,target,gameboard,gameboard[unit].createCombatModifiers({'unit':unit,'target':target,'gameboard':gameboard})) 
            
        def getTargets(self,unit,gameboard,*args):
            return list(set(self.getLOSTargets(unit,gameboard,args)).intersection(set(self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location))))
         
    weapons = ['Warhammer','Spear','Katana','Rapier','Axe','Greatsword','Bow']
        
    class Cleave:
        name = 'Cleave'
        cost = ['Passive']
        def abilityEffect(self,unit,target,gameboard):
    class Sweeping:
        name = 'Sweeping'
        cost = ['Passive']
        def abilityEffect(self,unit,target,gameboard):
    class Counter:
        name = 'Counter'
        cost = ['Reaction']
        def abilityEffect(self,unit,target,gameboard):
    class Parry:
        name = 'Parry'
        cost = ['Reaction']
        def abilityEffect(self,unit,target,gameboard):
    class Block:
        name = 'Block'
        cost = ['Reaction']
        def abilityEffect(self,unit,target,gameboard):
    class Push:
        name = 'Push'
        cost = ['Special']
        def abilityEffect(self,unit,target,gameboard):
    class Regroup:
        name = 'Regroup'
        cost = ['Passive']
        def abilityEffect(self,unit,target,gameboard):
    class FocusEnergy:
        name = 'FocusEnergy'
        cost = ['Special']
        def abilityEffect(self,unit,target,gameboard):
    class Sprint:
        name = 'Sprint'
        cost = ['Passive']
        def abilityEffect(self,unit,target,gameboard):
    class Assault:
        name = 'Assault'
        cost = ['Passive']
        def abilityEffect(self,unit,target,gameboard):
    class Charge:
        name = 'Charge'
        cost = ['Passive']
        def abilityEffect(self,unit,target,gameboard):
    
    class Weapon(Ability):
        def Form1:
        def Form2:
        def Form3:
        def Form4:
    
            
    class Warhammer(Weapon):
        name = 'Warhammer'
        def Form1(self,unit,target,gameboard):
            return self.forcedMovement(2,gameboard[unit].direction,target,gameboard)
        def Form2(self,unit,target,gameboard,combatSteps):
            if self.oppositeSpacesDir(unit,target) in gameboard:
                combatSteps['AttackMods']['Wounding'] = True
            return gameboard, combatSteps
        def Form3(self,unit,target,gameboard):
            for x in self.getMeleeTargets(unit,gameboard):
                self.forcedMovement(2,gameboard[unit].direction,target,gameboard)
        def Form4(self,unit,target,gameboard):
            combatSteps['AttackMods']['Piercing'] = True
            combatSteps['AddDamage'] = combatSteps['AddDamage'] + combatSteps['Armor']
        class Upgrade1(self,unit,target,gameboard):
            
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):
        
    class Spear(Weapon):
        name = 'Spear'
        def Form1(self,unit,target,gameboard):
            target = [x for x in self.getLOSTargets(unit,gameboard,{'Range':2})]
            return self.combat(unit,target,gameboard)
            
        def Form2(self,unit,target,gameboard):
            targets = self.getMeleeTargets(unit,gameboard)
            for x in targets:
                gameboard = self.combat(unit,target,gameboard)
            return gameboard
            
        def Form3(self,unit,target,gameboard):
            newSpace = random.choice(self.straightLine(3,random.choice(self.directions),unit,gameboard))
            gameboard[newSpace] = gameboard[unit]
            del gameboard[unit]
            return self.combat(unit,target,gameboard)
            
        def Form4(self,unit,target,gameboard):
            targets = self.straightLine(3,random.choice(self.LOSDirections(gameboard[unit].direction)),unit,gameboard)
            for x in targets:
                self.combat(unit,x,gameboard)
            return gameboard
            
        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard): 
            
    class Rapier(Weapon):
        name = 'Rapier'
        
        def Form1(self,unit,target,gameboard):
            damage = gameboard[unit].attributeManager.getAttributes['Damage'] - 1
            self.combat(unit,target,gameboard,{'Damage':damage})
            self.combat(unit,target,gameboard,{'Damage':damage})
            
        def Form2(self,unit,target,gameboard):
            gameboard[unit].attributeManager.bonusAttributes['Reaction'] = gameboard[unit].attributeManager.bonusAttributes['Reaction'] + 1
            self.combat(unit,target,gameboard)
            
        def Form3(self,unit,target,gameboard):
            self.combat(unit,target,gameboard,{'Swift':True})
            
        def Form4(self,unit,target,gameboard):
            damage = gameboard[unit].attributeManager.getAttributes['Damage'] - 2
            gameboard = self.combat(unit,target,gameboard,{'Damage':damage})
            gameboard = self.combat(unit,target,gameboard,{'Damage':damage})            
            gameboard = self.combat(unit,target,gameboard,{'Damage':damage})

        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):
            
    class Katana(Weapon):
        name = 'Katana'
        
        def Form1(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].getAOETargets(2,unit) if x not in gameboard])
            space = gameboard[target].adjacentSpacesDir()[1]
            if space not in gameboard:
                gameboard[space] = gameboard[unit]
                gameboard = self.combat(space,target,gameboard)
            
        def Form2(self,unit,target,gameboard):
            target = random.choice([x for x in gameboard[unit].getAOETargets(2,unit) if x not in gameboard])
            space = gameboard[target].adjacentSpaces()[random.choice([3,4,5])]
            
        def Form3(self,unit,target,gameboard):
            gameboard = self.combat(space,target,gameboard)
            gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,'Distance'=2,'Cost'='Passive')            
            
        def Form4(self,unit,target,gameboard):    
            
            
        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):
            
    class Axe(Weapon):
        name = 'Axe'
        
        def Form1(self,unit,target,gameboard):
            return self.combat(unit,target,gameboard,{'Axe':True})
            
        def Form2(self,unit,target,gameboard):
            return self.combat(unit,target,gameboard,{'AddHit':1,'Piercing':True})
            
        def Form3(self,unit,target,gameboard):
            cleave = self.oppositeSpacesDir(unit,target)
            gameboard = self.combat(unit,target,gameboard)
            if cleave in gameboard:
                gameboard = self.combat(unit,cleave,gameboard)
            return gameboard
        
        def Form4(self,unit,target,gameboard):
            damage = gameboard[target].levelManager.classAttributes()['Movement'] - gameboard[target].attributeManager.getAttribute('Movement')
            return self.combat(unit,target,gameboard,{'AddDamage':damage})

        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):
            
    class GreatSword(Weapon):
        name = 'GreatSword'
        def Form1(self,unit,target,gameboard):
            gameboard = self.combat(unit,target,gameboard,{'AddDamage':2})
            
        def Form2(self,unit,target,gameboard):
            targets = self.getMeleeTargets(unit,gameboard)
            for x in targets:
                gameboard = self.combat(unit,target,gameboard,{'AddHit',-1})
            return gameboard
            
        def Form3(self,unit,target,gameboard):
            targets = [x for x in self.getAOETargets(1,unit) if x in gameboard]
            for x in targets:
                gameboard = self.combat(unit,x,gameboard)
            return gameboard
            
        def Form4(self,unit,target,gameboard):    
            return self.combat(unit,target,gameboard,{'AddHit':4})
            
        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):    

    class Bow(Weapon):
        name = 'Bow'
        def Form1(self,unit,target,gameboard):
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
            return self.combat(unit,target,gameboard)            
            
        def Form2(self,unit,target,gameboard):
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
            return self.combat(unit,target,gameboard)                

        def Form3(self,unit,target,gameboard):
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
            return self.combat(unit,target,gameboard)                

        def Form4(self,unit,target,gameboard):
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
            return self.combat(unit,target,gameboard)
        
        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):  
            
    class Distension:
        name = 'Distension'
        cost = {'Turn':'Attack'}
            
        def abilityEffect(self,unit,target,gameboard):
            gameboard = self.forcedMovement(2,gameboard[unit].direction,self.adjacentSpacesDir()[1],gameboard)
            gameboard[unit].direction = gameboard[unit].faceDirection(gameboard[unit].direction,4)
            targets = [x for x in self.getMeleeTargets(unit,gameboard) if x in gameboard]
            for x in targets:
                gameboard = self.combat(unit,x,gameboard)
            gameboard = gameboard[unit].abilities['Movement'].abilityEffect(gameboard[unit].location,[],gameboard,{'Distance':1,'Passive':'Passive'})
        
    class ClearingAPath:
        name = 'ClearingAPath'
        cost = {'Turn':'Attack'}
        
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
            gameboard = self.combat(unit,self.adjacentSpacesDir()[1],gameboard)
            gameboard = self.forcedMovement(2,gameboard[unit].direction,self.adjacentSpacesDir()[1],gameboard)            
            
    class Contusion:
        name = 'Contusion'
        cost = {'Turn':'Passive'}
            
    class Rage:
        name = 'Rage'
        cost = {'Turn':'Passive'}
            
    class Momentum:
        name = 'Momentum'
        cost = {'Turn':'Passive'}
            
    class HeavyBolts:
        name = 'HeavyBolts'
        cost = {'Turn':'Passive'}

    class BladeDance:
        name = 'BladeDance'
        cost = {'Turn':'Passive'}
    
    class PruningBranches:
        name = 'PruningBranches'
        cost = {'Turn':'Attack'}
        
        def abilityEffect(self,unit,target,gameboard):
            target1 = random.choice([x for x in self.getMeleeTargets(unit,gameboard) if x in gameboard])
            gameboard = self.combat(unit,target1,gameboard)    
            gameboard = gameboard[unit].abilities['Movement'].abilityEffect(gameboard[unit].location,[],gameboard,{'Distance':1,'Passive':'Passive'})
            target2 = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':2}) if x in gameboard and x != target1])
            return self.combat(unit,target2,gameboard)    

    class Incision:
        name = 'Incision'
        cost = {'Turn':'Passive'}
    
    class Harvest:
        name = 'Harvest'
        cost = {'Turn':'Attack'}
        
        def abilityEffect(self,unit,target,gameboard):
            targets = [x for x in self.getAOETargets(1,unit) if x in gameboard]
            for x in targets:
                gameboard = self.combat(unit,x,gameboard,{'Wounding':True})
            targets = [x for x in self.getAOETargets(2,unit) if x in gameboard and x not in [x for x in self.getAOETargets(1,unit)]]
            for x in targets:
                gameboard = self.combat(unit,x,gameboard,{'Wounding':True})
            return gameboard
            
    class Tranquility:
        name = 'Tranquility'
        cost = {'Turn':'Passive'}
    
    class Rebuke:
        name = 'Rebuke'
        cost = {'Turn':'Passive'}
    
    class Collateral:
        name = 'Collateral'
        cost = {'Turn':'Attack'}
        
        def abilityEffect(self,unit,target,gameboard):
    
    class DescribingAnArc:
        name = 'DescribingAnArc'
        cost = {'Turn':'Attack'}
        
        def abilityEffect(self,unit,target,gameboard):
            gameboard = gameboard[unit].abilities['Movement'].abilityEffect(gameboard[unit].location,[],gameboard,{'Distance':1,'Passive':'Passive'})
            for x in range(0,3):
                target = random.choice([x for x in self.getMeleeTargets(unit,gameboard) if x in gameboard])
                gameboard = self.combat(unit,target,gameboard,{'Damage':gameboard[unit].attributeManager.getAttributes('Damage')-2})
            targets = self.getMeleeTargets(unit,gameboard)
            for x in targets:
                gameboard = self.combat(unit,target,gameboard)
                
    class Brushstrokes:
        name = 'Brushstrokes'
        cost = {'Turn':'Attack'}
        
        def abilityEffect(self,unit,target,gameboard):
    
            
    class Barter:
        name = 'Barter'
        cost = {'Reaction':'Attack'}
        
        def abilityEffect(self,unit,target,gameboard):
    
    class Gardener:
        name = 'Gardener'
        cost = {'Turn':'Special'}
        
        def abilityEffect(self,unit,target,gameboard):
            self.active = True
            
    class FleurDeLis:
        name = 'FleurDeLis'
        cost = {'Turn':'Attack'}
        
        def abilityEffect(self,unit,target,gameboard):
    
    class Sunder:
        name = 'Sunder'
        cost = {'Turn':'Passive'}

    class Scattershot:
        name = 'Scattershot'
        cost = {'Turn':'Passive'}
    
    class Aegis:
        name = 'Aegis'
        cost = {'Turn':'Passive'}
