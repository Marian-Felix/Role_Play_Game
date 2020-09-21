from random import randint


#### weapons
## parent-class weapons
class Weapon:
    type = "weapon"
    inventory_sort = 1

    def check_if_broken(self):
        if self.durability <= 0:
            self.durability = 0
            self.is_broken = True

    def get_value(self):
        value = round(self.w_damage * 2.1 + self.durability * 0.4)
        return value

    def __repr__(self):
        return self.name


## child-classes weapons
class Spiked_club(Weapon):
    def __init__(self):
        self.w_damage = 5 + randint(0, 2)
        self.durability = 10 + randint(0, 20)
        self.is_broken = False
        self.name = "Spiked Club"


class Lumberjack_axe(Weapon):
    def __init__(self):
        self.w_damage = 10 + randint(0, 3)
        self.durability = 10 + randint(0, 20)
        self.is_broken = False
        self.name = "Lumberjack Axe"


class Sword(Weapon):
    def __init__(self):
        self.w_damage = 14 + randint(0, 5)
        self.durability = 10 + randint(0, 40)
        self.is_broken = False
        self.name = "Sword"


class Templer_hammer(Weapon):
    def __init__(self):
        self.w_damage = 23 + randint(0, 8)
        self.durability = 15 + randint(0, 40)
        self.is_broken = False
        self.name = "Templer Hammer"


#### armor
## parent-class armor
class Armor:
    type = "armor"
    inventory_sort = 2

    def check_if_broken(self):
        if self.durability <= 0:
            self.durability = 0
            self.is_broken = True

    def get_value(self):
        value = round(self.a_defense * 3.2 + self.durability * 0.6)
        return value

    def __repr__(self):
        return self.name


## child-classes armor
class Woolen_rags(Armor):
    def __init__(self):
        self.a_defense = 1 + randint(0, 1)
        self.durability = 7 + randint(0, 7)
        self.is_broken = False
        self.name = "Woolen Rags"


class Leather_tunica(Armor):
    def __init__(self):
        self.a_defense = 4 + randint(0, 3)
        self.durability = 10 + randint(0, 20)
        self.is_broken = False
        self.name = "Leather Tunica"


class Chain_mail(Armor):
    def __init__(self):
        self.a_defense = 10 + randint(0, 7)
        self.durability = 10 + randint(0, 40)
        self.is_broken = False
        self.name = "Chain Mail"


class Breast_plate_armor(Armor):
    def __init__(self):
        self.a_defense = 20 + randint(0, 10)
        self.durability = 25 + randint(0, 60)
        self.is_broken = False
        self.name = "Breast Plate Armor"


#### artefacts
## parent-class artefacts
class Artefact:
    type = "artefact"
    inventory_sort = 3

    def __repr__(self):
        return self.name


## child-classes artefacts
class Lesser_health_crystal(Artefact):
    def __init__(self):
        self.h_bonus = 8 + randint(0, 8)
        self.name = "Lesser Health Crystal"
        self.value = 50


class Health_crystal(Artefact):
    def __init__(self):
        self.h_bonus = 18 + randint(0, 20)
        self.name = "Health Crystal"
        self.value = 100


#### potions
# ## child-classes potions
# class Potion:
#     type = "potion"
#     inventory_sort = 4
#
#     def __repr__(self):
#         return self.name
#
#
# class potion(Potion):
#
#     def __init__(self):
#         self.name = "Potion"
#     ##potion should just replenish the health completely.