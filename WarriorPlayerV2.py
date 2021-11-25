# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:04:17 2021

@author: bgool
"""

import random
import GeneralUse as gen
#########################################
        # WARRIOR DEF #
        ###############

class WarriorAttack(gen.Attack):
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
        return list(set(self.getLOSTargets(unit,gameboard,args)).intersection(set(self.getAOETargets(gameboard[unit].unitRange,gameboard[unit].location,gameboard))))
   

class Block(gen.Ability):
    name = 'Block'
    cost = {'Reaction':['Reaction']}
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        blockDamage = combatSteps['CalcHit'] + combatSteps['AddHit'] - combatSteps['CalcEvasion'] - combatSteps['AddEvasion']
        combatSteps['AddDamage'] = -blockDamage
        return gameboard, combatSteps

class Push(gen.Ability):
    name = 'Push'
    cost = {'Turn':['Special']}
    
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.forcedMovement(2,gameboard[unit].direction,target,gameboard)        
        return gameboard

class Parry(gen.Ability):
    name = 'Parry'
    cost = {'Reaction':['Reaction']}
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['AddEvasion'] = combatSteps['AddEvasion'] + gameboard[target].attributeManager.getAttributes('Hit')
        return gameboard, combatSteps

class WarriorCounter(gen.Ability):
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

        target = random.choice(gameboard[unit].getAOETargets(2,unit,gameboard))
        space = gameboard[target].adjacentSpacesDir()[1]
        if space not in gameboard:
            gameboard[space] = gameboard[unit]
            gameboard = self.combat(space,target,gameboard,combatSteps)
        self.increaseForm()
        return gameboard
        
    def Form2(self,unit,target,gameboard,combatSteps):
        gameboard,combatSteps = self.attackPassiveEffects(unit,target,gameboard,combatSteps)

        target = random.choice(gameboard[unit].getAOETargets(2,unit,gameboard))
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
        damage = gameboard[target].levelManager.classAttributes()['Movement'] - gameboard[target].attributeManager.getAttributes('Movement')
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

        targets = self.getAOETargets(1,unit,gameboard)
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
            
class Distension(gen.Ability):
    name = 'Distension'
    cost = {'Turn':['Attack']}
        
    def abilityEffect(self,unit,target,gameboard):
        gameboard = self.forcedMovement(2,gameboard[unit].direction,self.adjacentSpacesDir()[1],gameboard)
        gameboard[unit].direction = gameboard[unit].faceDirection(gameboard[unit].direction,4)
        targets = [x for x in self.getMeleeTargets(unit,gameboard) if x in gameboard]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard)
        gameboard = gameboard[unit].abilities['Movement'].abilityEffect(gameboard[unit].location,[],gameboard,{'Distance':1,'Passive':'Passive'})
    
class ClearingAPath(gen.Ability):
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
        
class Contusion(gen.Ability):
    name = 'Contusion'
    cost = {'Passive':['Passive']}
    #check
        
class Rage(gen.Ability):
    name = 'Rage'
    damage = 0
    cost = {'Reaction':['Passive']}
    state = ['TakeDamage']
    
    def abilityEffect(self,unit,target,gameboard,damage):
        self.damage = self.damage + 1
        return gameboard, damage, unit
        
class Momentum(gen.Ability):
    name = 'Momentum'
    cost = {'Passive':['Passive']}
    
    #check
class HeavyBolts(gen.Ability):
    name = 'HeavyBolts'
    cost = {'Passive':['Passive']}
    #check
    
class BladeDance(gen.Ability):
    name = 'BladeDance'
    cost = {'Passive':['Passive']}
    #check
    
class PruningBranches(gen.Ability):
    name = 'PruningBranches'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        target1 = random.choice([x for x in self.getMeleeTargets(unit,gameboard) if x in gameboard])
        gameboard = self.combat(unit,target1,gameboard)    
        gameboard = gameboard[unit].abilities['Movement'].abilityEffect(gameboard[unit].location,[],gameboard,{'Distance':1,'Passive':'Passive'})
        target2 = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':2}) if x in gameboard and x != target1])
        return self.combat(unit,target2,gameboard)    

class Incision(gen.Ability):
    name = 'Incision'
    cost = {'Passive':['Passive']}
    #check

class Harvest(gen.Ability):
    name = 'Harvest'
    cost = {'Turn':['Attack']}
    
    def abilityEffect(self,unit,target,gameboard):
        targets = self.getAOETargets(1,unit,gameboard)
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Wounding':True})
        targets = [x for x in self.getAOETargets(2,unit,gameboard) if x not in [x for x in self.getAOETargets(1,unit,gameboard)]]
        for x in targets:
            gameboard = self.combat(unit,x,gameboard,{'Wounding':True})
        return gameboard
        
class Tranquility(gen.Ability):
    name = 'Tranquility'
    cost = {'Passive':['Passive']}
    #check
    
class Rebuke(gen.Ability):
    name = 'Rebuke'
    cost = {'Reaction':['Passive']}
    state = ['Evasion']
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        if target in gameboard[unit].getMeleeTargets(unit,gameboard):
            gameboard = gameboard[unit].abilities['WarriorAttack'].abilityEffect(unit,target,gameboard)
            gameboard = gameboard[unit].abilities['Movement'].execute(unit,target,gameboard,1)
        return gameboard, combatSteps
    
class Collateral(gen.Ability):
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
                   
class DescribingAnArc(gen.Ability):
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

        
class Brushstrokes(gen.Ability):
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

class Barter(gen.Ability):
    name = 'Barter'
    cost = {'Reaction':['Attack']}
    state = ['TargetedMelee']
    active = False
    
    def abilityEffect(self,unit,target,gameboard,combatSteps):
        combatSteps['AttackMods']['Wounding'] = True
        self.active = True
        return 
    
class Gardener(gen.Ability):
    name = 'Gardener'
    cost = {'Turn':['Special']}
    active = False
    
    def abilityEffect(self,unit,target,gameboard):
        self.active = True
        
class FleurDeLis(gen.Ability):
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
            
class Sunder(gen.Ability):
    name = 'Sunder'
    cost = {'Passive':['Passive']}
    #check
    
class Scattershot(gen.Ability):
    name = 'Scattershot'
    cost = {'Passive':['Passive']}
    #check

class Aegis(gen.Ability):
    name = 'Aegis'
    cost = {'Passive':['Passive']}
    #check

class WarriorUnit(gen.Unit):
    
    name = 'Unit'
    unitClass = 'Warrior'
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
            if not [x for x in gameboard[unit].adjacentSpaces() if gameboard[unit].name == 'Unit']:
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
            if [x for x in gameboard if type(x) is tuple and 'HoarFrost' in gameboard[x].abilities]:
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
                combatSteps['Push'] = True
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
                combatSteps['Counter'] = True
        if self.weaponUpgrades['Greatsword'] >= 2:
            if combatSteps['CalcEvasion'] == 1:
                if 'Block' in gameboard[target].abilities:
                    gameboard = gameboard[target].abilities['Block'].abilityEffect(unit,target,gameboard,combatSteps)
        return gameboard,combatSteps
    
    def movementEffects(self,unit,target,gameboard):
        return gameboard

    def createOptions(self):
        # match ability costs to available points
        # excludes passives since it matches available points to cost
        options = [x.name for x in self.abilities.values() if 'Turn' in x.cost and set(x.cost['Turn']).issubset(set(self.availablePoints()))]

        return options # this is ability names
    
class WarriorPlayer(gen.Player):

    def __init__(self,playerClass,playerID):
        self.playerClass = playerClass
        self.playerID = playerID
        # instantiate new units
        self.units = {'Elite':WarriorUnit('Elite','Elite'),'Common1':WarriorUnit('Common','Common1'),\
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
     

    def levelUp(self):
        if self.level < 10:
            self.level = self.level + 1
            for unit in self.units.values():
                unit.levelManager.level = self.level
        if self.level < 5:
            for unit in self.units:
                weapon = random.choice(['Warhammer','Spear','Katana','Rapier','Axe','Greatsword','Bow'])
                self.units[unit].weaponUpgrades[weapon] = self.units[unit].weaponUpgrades[weapon] + 1

                
#    def beginningTurnEffects(self,gameboard):
#        return gameboard
#        
    def endTurnEffects(self,gameboard):
        for x in self.units:
            if 'Rage' in self.units[x].abilities:
                self.units[x].abilities['Rage'].damage = 0
        return gameboard
