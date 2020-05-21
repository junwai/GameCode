# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:56:44 2020

@author: bgool
"""

class WarriorUnit(Unit):
    
    def __init__(self):
        self.form = 1
    
    def Forms(self):
        while True:
            self.form = self.form + 1
            if self.form == 5:
                self.form == 1
            yield form
            
class WarriorPlayer(Player):
    
    class Cleave:
        name = 'Cleave'
    class Sweeping:
        name = 'Sweeping'
    class Counter:
        name = 'Counter'
    class Parry:
        name = 'Parry'
    class Block:
        name = 'Block'
    class Push:
        name = 'Push'
    class Regroup:
        name = 'Regroup'
    class FocusEnergy:
        name = 'FocusEnergy'
    class Sprint:
        name = 'Sprint'
    class Assault:
        name = 'Assault'
    class Charge:
        name = 'Charge'
    class Weapon:
        def Form1:
        def Form2:
        def Form3:
        def Form4:
        
    class Warhammer(Weapon):
        name = 'Warhammer'
        def Form1:
        def Form2:
        def Form3:
        def Form4:
        class Upgrade1:
        class Upgrade2:
        class Upgrade3:
        
    class Spear(Weapon):
        name = 'Spear'
        def Form1:
        def Form2:
        def Form3:
        def Form4:
        class Upgrade1:
        class Upgrade2:
        class Upgrade3: 
            
    class Katana(Weapon):
        name = 'Katana'
        def Form1:
        def Form2:
        def Form3:
        def Form4:    
        class Upgrade1:
        class Upgrade2:
        class Upgrade3:
            
    class Rapier(Weapon):
        name = 'Rapier'
        def Form1:
        def Form2:
        def Form3:
        def Form4:    
        class Upgrade1:
        class Upgrade2:
        class Upgrade3:
            
    class Axe(Weapon):
        name = 'Axe'
        def Form1:
        def Form2:
        def Form3:
        def Form4:    
        class Upgrade1:
        class Upgrade2:
        class Upgrade3:
            
    class GreatSword(Weapon):
        name = 'GreatSword'
        def Form1:
        def Form2:
        def Form3:
        def Form4:    
        class Upgrade1:
        class Upgrade2:
        class Upgrade3:    

    class Bow(Weapon):
        name = 'Bow'
        def Form1:
        def Form2:
        def Form3:
        def Form4:    
        class Upgrade1:
        class Upgrade2:
        class Upgrade3:  
            
    class Distension:
        name = 'Distension'
    class ClearingAPath:
        name = 'ClearingAPath'
    class Contusion:
        name = 'Contusion'
    class Rage:
        name = 'Rage'
    class Momentum:
        name = 'Momentum'
    class HeavyBolts:
        name = 'HeavyBolts'
    class BladeDance:
        name = 'BladeDance'
    class PruningBranches:
        name = 'PruningBranches'
    class Incision:
        name = 'Incision'
    class Harvest:
        name = 'Harvest'
    class Tranquility:
        name = 'Tranquility
    class Rebuke:
        name = 'Rebuke'
    class Collateral:
        name = 'Collateral'
    class DescribingAnArc:
        name = 'DescribingAnArc'
    class Brushstrokes:
        name = 'Brushstrokes'
    class Barter:
        name = 'Barter'
    class Gardener:
        name = 'Gardener'
    class FleurDeLis:
        name = 'FleurDeLis'
    class Sunder:
        name = 'Sunder'
    class Scattershot:
        name = 'Scattershot'
    class Aegis:
        name = 'Aegis'