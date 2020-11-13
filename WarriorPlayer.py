# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:56:44 2020

@author: bgool
"""

class WarriorUnit(Unit):
    
    weaponUpgrades = {'Warhammer':0,'Spear':0,'Katana':0,'Rapier':0,'Axe':0,'Greatsword':0,'Bow':0}
    weapons = {'Warhammer':Warhammer(),'Spear':Spear(),'Katana':Katana(),'Rapier':Rapier(),'Axe':Axe(),'Greatsword':Greatsword(),'Bow':Bow}
    form = 1
    
    def __init__(self,unitType,unitName,weapons):
        super().__init__(unitType,unitName)
        
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
    
    def hitDiceMods(self,unit,target,gameboard,combatSteps):
        # 3 or 4 push
        # 1 or 4 gain reaction: could already be coded
        # 5 or 6 add hit mod to damage
        # 2 or 3 move
        # 5 or 6 add evasion to damage
        #
    
    def evasionDiceMods(self,unit,target,gameboard,combatSteps):
    
    def movementEffects(self,unit,target,gameboard):
        return gameboard
    
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
    
    # need both warriorattack and attack to differentiate a normal attack and a form attack
    # both need to access passives
    
    class WarriorAttack(Attack):
        name = 'WarriorAttack'
        cost = {'Turn':['Attack']}
        
        def abilityEffect(self,unit,target,gameboard):
            gameboard[unit].changeAttributes('Attack',-1)
            self.weapon = random.choice(['Warhammer','Spear','Katana','Rapier','Axe','Greatsword','Bow'])
            hitDice = random.randint(1,6)
            gameboard, mods = gameboard[unit].hitDiceMods(unit,target,gameboard)
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
        
    def attackPassiveEffects(self,unit,target,gameboard):
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

                
    def beginningTurnEffects(self,gameboard):
        return gameboard
        
    def endTurnEffects(self,gameboard):
        for x in self.units:
            if 'Rage' in x.abilities:
                x.abilities['Rage'].damage = 0
        return gameboard
        
    
        
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
    
    # TO DO: Update weapons to include combat
    # Create general abilities above
    class Weapon(Ability):
        def Form1(self):
            return
        def Form2(self):
            return
        def Form3(self):
            return
        def Form4(self):
            return
    
    class Warhammer(Weapon):
        name = 'Warhammer'
        def Form1(self,unit,target,gameboard):
            gameboard = self.combat(unit,target,gameboard) 
            return self.forcedMovement(2,gameboard[unit].direction,target,gameboard)
        def Form2(self,unit,target,gameboard):
            if self.oppositeSpacesDir(unit,target) in gameboard:
                return self.combat(unit,target,gameboard,{'Wounding':True}) 
            else:
                return self.combat(unit,target,gameboard) 
        def Form3(self,unit,target,gameboard):
            for x in self.getMeleeTargets(unit,gameboard):
                gameboard = self.combat(unit,target,gameboard)
                gameboard = self.forcedMovement(2,gameboard[unit].direction,target,gameboard)
            return gameboard
        def Form4(self,unit,target,gameboard):
            return self.combat(unit,target,gameboard,{'AddDamage':gameboard[target].attributeManager.getAttributes('Armor'),'Piercing':True})
        
        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):
        
    class Spear(Weapon):
        name = 'Spear'
        def Form1(self,unit,target,gameboard,combatSteps):
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':2})])
            return self.combat(unit,target,gameboard)
            
        def Form2(self,unit,target,gameboard,combatSteps):
            targets = self.getMeleeTargets(unit,gameboard)
            for x in targets:
                gameboard = self.combat(unit,target,gameboard)
            return gameboard
            
        def Form3(self,unit,target,gameboard,combatSteps):
            gameboard = self.combat(unit,target,gameboard)
            newSpace = random.choice(self.straightLine(3,random.choice(self.directions),unit,gameboard))
            gameboard[newSpace] = gameboard[unit]
            del gameboard[unit]
            return gameboard
            
        def Form4(self,unit,target,gameboard,combatSteps):
            targets = self.straightLine(3,random.choice(self.LOSDirections(gameboard[unit].direction)),unit,gameboard)
            for x in targets:
                self.combat(unit,x,gameboard)
            return gameboard
            
        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard): 
            
    class Rapier(Weapon):
        name = 'Rapier'
        
        def Form1(self,unit,target,gameboard,combatSteps):
            damage = gameboard[unit].attributeManager.getAttributes['Damage'] - 1
            self.combat(unit,target,gameboard,{'Damage':damage})
            self.combat(unit,target,gameboard,{'Damage':damage})
            
        def Form2(self,unit,target,gameboard,combatSteps):
            gameboard[unit].attributeManager.bonusAttributes['Reaction'] = gameboard[unit].attributeManager.bonusAttributes['Reaction'] + 1
            self.combat(unit,target,gameboard)
            
        def Form3(self,unit,target,gameboard,combatSteps):
            self.combat(unit,target,gameboard,{'Swift':True})
            
        def Form4(self,unit,target,gameboard,combatSteps):
            damage = gameboard[unit].attributeManager.getAttributes['Damage'] - 2
            gameboard = self.combat(unit,target,gameboard,{'Damage':damage})
            gameboard = self.combat(unit,target,gameboard,{'Damage':damage})            
            gameboard = self.combat(unit,target,gameboard,{'Damage':damage})

        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):
            
    class Katana(Weapon):
        name = 'Katana'
        self.Form4 = False
        
        def Form1(self,unit,target,gameboard,combatSteps):
            target = random.choice([x for x in gameboard[unit].getAOETargets(2,unit) if x not in gameboard])
            space = gameboard[target].adjacentSpacesDir()[1]
            if space not in gameboard:
                gameboard[space] = gameboard[unit]
                gameboard = self.combat(space,target,gameboard)
            return gameboard
            
        def Form2(self,unit,target,gameboard,combatSteps):
            target = random.choice([x for x in gameboard[unit].getAOETargets(2,unit) if x not in gameboard])
            space = gameboard[target].adjacentSpaces()[random.choice([3,4,5])]
            return self.combat(unit,target,gameboard)
            
        def Form3(self,unit,target,gameboard,combatSteps):
            gameboard = self.combat(unit,target,gameboard)
            gameboard = gameboard[unit].abilities['Movement'].abilityEffect(unit,target,gameboard,'Distance'=2,'Cost'='Passive')
            return gameboard
            
        def Form4(self,unit,target,gameboard,combatSteps):    
            self.Form4 = True
            return self.combat(unit,target,gameboard)
            
        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):
            
    class Axe(Weapon):
        name = 'Axe'
        
        def Form1(self,unit,target,gameboard,combatSteps):
            return self.combat(unit,target,gameboard,{'Axe':True})
            
        def Form2(self,unit,target,gameboard,combatSteps):
            return self.combat(unit,target,gameboard,{'AddHit':1,'Piercing':True})
            
        def Form3(self,unit,target,gameboard,combatSteps):
            cleave = self.oppositeSpacesDir(unit,target)
            gameboard = self.combat(unit,target,gameboard)
            if cleave in gameboard:
                gameboard = self.combat(unit,cleave,gameboard)
            return gameboard
        
        def Form4(self,unit,target,gameboard,combatSteps):
            damage = gameboard[target].levelManager.classAttributes()['Movement'] - gameboard[target].attributeManager.getAttribute('Movement')
            return self.combat(unit,target,gameboard,{'AddDamage':damage})

        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):
            
    class GreatSword(Weapon):
        name = 'GreatSword'
        def Form1(self,unit,target,gameboard,combatSteps):
            gameboard = self.combat(unit,target,gameboard,{'AddDamage':2})
            
        def Form2(self,unit,target,gameboard,combatSteps):
            targets = self.getMeleeTargets(unit,gameboard)
            for x in targets:
                gameboard = self.combat(unit,target,gameboard,{'AddHit',-1})
            return gameboard
            
        def Form3(self,unit,target,gameboard,combatSteps):
            targets = [x for x in self.getAOETargets(1,unit) if x in gameboard]
            for x in targets:
                gameboard = self.combat(unit,x,gameboard)
            return gameboard
            
        def Form4(self,unit,target,gameboard,combatSteps):    
            return self.combat(unit,target,gameboard,{'AddHit':4})
            
        class Upgrade1(self,unit,target,gameboard):
        class Upgrade2(self,unit,target,gameboard):
        class Upgrade3(self,unit,target,gameboard):    

    class Bow(Weapon):
        name = 'Bow'
        def Form1(self,unit,target,gameboard,combatSteps):
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
            return self.combat(unit,target,gameboard)            
            
        def Form2(self,unit,target,gameboard,combatSteps):
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
            return self.combat(unit,target,gameboard)                

        def Form3(self,unit,target,gameboard,combatSteps):
            target = random.choice([x for x in self.getLOSTargets(unit,gameboard,{'Range':3})])
            return self.combat(unit,target,gameboard)                

        def Form4(self,unit,target,gameboard,combatSteps):
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
            gameboard = self.combat(unit,gameboard[unit].adjacentSpacesDir()[1],gameboard)
            gameboard = self.forcedMovement(2,gameboard[unit].direction,self.adjacentSpacesDir()[1],gameboard)            
            
    class Contusion:
        name = 'Contusion'
        cost = {'Turn':'Passive'}
        #check
            
    class Rage:
        name = 'Rage'
        damage = 0
        cost = {'Reaction':'Passive'}
        state = ['TakeDamage']
        
        def abilityEffect(self,unit,target,gameboard,damage):
            self.damage = self.damage + 1
            return gameboard, damage
            
    class Momentum:
        name = 'Momentum'
        cost = {'Turn':'Passive'}
        
        #check
    class HeavyBolts:
        name = 'HeavyBolts'
        cost = {'Turn':'Passive'}
        #check
        
    class BladeDance:
        name = 'BladeDance'
        cost = {'Turn':'Passive'}
        #check
        
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
        #check
    
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
        #check
        
    class Rebuke:
        name = 'Rebuke'
        cost = {'Reaction':'Passive'}
        state = ['Evasion']
        
        def abilityEffect(self,unit,target,gameboard,combatSteps):
            if target in gameboard[unit].getMeleeTargets(unit,gameboard):
                gameboard = gameboard[unit].abilities['WarriorAttack'].abilityEffect(unit,target,gameboard)
                gameboard = gameboard[unit].abilities.['Movement'].execute(unit,target,gameboard,1)
            return gameboard, combatSteps
        
    class Collateral:
        name = 'Collateral'
        cost = {'Turn':'Attack'}
        
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
        hit = 0
        damage = 0
        
        def useBonuses(self, attribute):
            if attribute == 'Damage':
                dmg = self.damage
                self.damage = 0
                return self.dmg
            elif attribute == 'Hit':
                ht = self.hit
                self.hit = 0
                return self.hit
            
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
                    gameboard = self.combat(unit,target,gameboard,{'Damage':gameboard[unit].attributeManager.getAttributes('Damage')-2},'AddHit':self.useBonuses('Hit'),'AddDamage':self.useBonuses('Damage'))

    class Barter:
        name = 'Barter'
        cost = {'Reaction':'Attack'}
        state = ['TargetedMelee']
        active = False
        
        def abilityEffect(self,unit,target,gameboard,combatSteps):
            combatSteps['AttackMods']['Wounding'] = True
            self.active = True
            return 
        
    class Gardener:
        name = 'Gardener'
        cost = {'Turn':'Special'}
        active = False
        
        def abilityEffect(self,unit,target,gameboard):
            self.active = True
            
    class FleurDeLis:
        name = 'FleurDeLis'
        cost = {'Turn':'Attack'}
        
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
                
    class Sunder:
        name = 'Sunder'
        cost = {'Turn':'Passive'}
        #check
        
    class Scattershot:
        name = 'Scattershot'
        cost = {'Turn':'Passive'}
        #check
    
    class Aegis:
        name = 'Aegis'
        cost = {'Turn':'Passive'}
        #check