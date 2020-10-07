from random import randint
from items import *
# from world_map import confirm
import time


def confirm():
    if input("\n*** Press Enter to continue ***"):
        print()
        print()
        return


class Character:
    def return_stats(self):
        return "HP {}/{}, A {}, D {}".format(self.current_health, self.max_health, self.attack_dmg, self.defense)

    def lose_health(self, damage):
        if self.defense > round(damage):
            dam = 0
        else:
            dam = (round(damage) - self.defense)
        self.current_health -= dam
        if self.current_health <= 0:
            self.current_health = 0
        print("\n{} damage to {}. (HP: {}/{})".format(dam, self.name, self.current_health, self.max_health))
        confirm()
        if self.current_health == 0:
            self.is_knocked_out = True

    def attack(self, opponent):
        print("\n{} is attacking {}!".format(self.name, opponent.name), end="")
        time.sleep(0.4)
        random_number = randint(1, 100)
        if random_number in range(1,80):
            opponent.lose_health(self.attack_dmg + (randint(0, 35) / 100) * self.attack_dmg)
            # print("{} landed a hit!".format(self.name))
        else:
            print("\n{} missed with the attack ...".format(self.name))
            confirm()

    def risk_attack(self, opponent):
        print("\n{} is trying a Risk Attack for 2x damage!".format(self.name), end="")
        time.sleep(0.4)
        random_number = randint(1, 101)
        if random_number in range(1, 51):
            opponent.lose_health(2 * self.attack_dmg + (randint(0, 35) / 100) * self.attack_dmg) # oder 2* kompletter Schaden? Ist wrsl zu stark
        else:
            print("\n{} missed with the attack ...".format(self.name))
            confirm()


def get_item_sort_type(item):
    try:
        return item.inventory_sort
    except:
        return 1


class Hero(Character):
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.experience = 0
        self.items = {
            "weapon": None,
            "armor": rags1,
            "artefact": None,
            "potion": 1,
            "money": 0
        }
        self.max_health_bonus = 0
        self.max_health = 50
        self.current_health = 30
        self.attack_dmg_bonus = 0
        self.defense = 0 + self.get_armor_defense()
        self.attack_dmg = 5 + self.attack_dmg_bonus + self.get_weapon_damage()
        self.inventory = []
        self.is_knocked_out = False

    # __repr__ wandelt das items-dictionary erst in eine Liste um (List comprehension),
    # die Elemente der Liste werden anschließend durch .join() in einen Sting umgewandelt
    def __repr__(self):
        return "{}, level {} (HP {}/{}, A {}, D {})".format(self.name, self.level, self.current_health, self.max_health, self.attack_dmg, self.defense)

    def print_stats(self):
        print("{a}\n Hero '{b}', level 1 (HP {c}/{d}, A {e}, D {f})\n{g}\n\t{h}\n\nInventory: {i}\n{j}"
              .format(a="\n" + 45 * "*", b=self.name, c=self.current_health, d=self.max_health, e=self.attack_dmg,
                      f=self.defense, g=45 * "*",
                      h='\n\t'.join([str(elem) for elem in ["{}: {}".format(key.title(), self.items[key])
                                                            for key in self.items.keys()]]), i=self.inventory, j=45 * "*"))

    def get_weapon_damage(self):
        try:
            weapon_damage = self.items["weapon"].w_damage
            return weapon_damage
        except AttributeError:
            return 0

    def get_armor_defense(self):
        try:
            armor_defense = self.items["armor"].a_defense
            return armor_defense
        except AttributeError:
            return 0

    def update_attack_dmg(self):
        self.attack_dmg = 5 + self.attack_dmg_bonus + self.get_weapon_damage()

    def update_armor_defense(self):
        self.defense = self.get_armor_defense()

    def replenish(self):
        self.current_health = self.max_health
        print("\nYour health has replenished.")

    def heal(self, heal_amount):
        self.current_health += self.heal_amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def equip_item(self, item_from_inventory):  # index in inventory list
        temp = self.inventory.pop(item_from_inventory)
        # self.inventory.pop(item_from_inventory)
        if self.items[temp.type] is not None:
            self.put_in_inventory(
                self.items[temp.type])  # place equipped item with the same type as new one in inventory
            self.inventory.sort(key=get_item_sort_type)  # sort inventory
        self.items[temp.type] = temp
        self.update_attack_dmg()
        self.update_armor_defense()
        print("Equipped '{}'".format(temp))

    def unequip_item(self, item_from_equipment_123):  # 1 for weapon, 2 for armor, 3 for artefact
        nothing_equipped = "You have nothing equipped on that slot!"
        if item_from_equipment_123 not in [1, 2, 3, 4]:
            print("Something went wrong ...")
            return
        if item_from_equipment_123 == 1:
            unequip_item = self.items["weapon"]
            if unequip_item is None:
                print(nothing_equipped)
                return
            self.items["weapon"] = None
            self.update_attack_dmg()
        elif item_from_equipment_123 == 2:
            unequip_item = self.items["armor"]
            if unequip_item is None:
                print(nothing_equipped)
                return
            self.items["armor"] = None
            self.update_armor_defense()
        elif item_from_equipment_123 == 3:
            unequip_item = self.items["artefact"]
            if unequip_item is None:
                print(nothing_equipped)
                return
            self.items["artefact"] = None
        elif item_from_equipment_123 == 4:
            return
        print("Unequipped '{}'".format((unequip_item)))
        self.put_in_inventory(unequip_item)

    def put_in_inventory(self, item):
        if item == "potion":
            self.items["potion"] += 1
        else:
            self.inventory.append(item)
            self.inventory.sort(key=get_item_sort_type)
        print("Added to inventory: '{}'".format(item))

    def put_out_inventory(self, item_index):
        item_lost = self.inventory.pop(item_index)
        print("Lost '{}'".format(item_lost))

    def get_money(self, money_amount):
        print("You received money ({})".format(money_amount))
        self.items["money"] += money_amount

    def use_potion(self):
        if self.items["potion"] < 1:
            print("\nYou don't have any potions!")
            confirm()
            return
        elif self.current_health == self.max_health:
            print("\nYou are already at full health!")
            confirm()
            return
        elif self.items["potion"] >= 1:
            print("\nYou used a potion.", end="")
            self.items["potion"] -= 1
            self.replenish()
            confirm()

    def gain_experience(self, experience_gained):
        self.experience += experience_gained
        if self.level == 1 and self.experience >= 100:
            self.replenish()
            self.level += 1
            self.max_health_bonus += 25
            self.attack_dmg_bonus += 5
            print("{} has now reached level 2!\nDamage +5, Health +25!".format(self.name))
        if self.level == 2 and self.experience >= 300:
            self.replenish()
            self.level += 1
            self.max_health_bonus += 40
            self.attack_dmg_bonus += 8
            print("{} has now reached level 3!\nDamage +8, Health +40!".format(self.name))
        if self.level == 3 and self.experience >= 600:
            self.replenish()
            self.level += 1
            self.max_health_bonus += 65
            self.attack_dmg_bonus += 12
            print("{} has now reached level 4!\nDamage +12, Health +65!\nYou are now at MAX. level!".format(self.name))


rags1 = Woolen_rags()


class Bandit(Character):
    def __init__(self, level):
        self.name = "Bandit"
        self.level = level
        self.max_health = randint(28, 32) * level
        self.current_health = self.max_health
        self.attack_dmg = randint(11, 13) * level
        self.defense = randint(5, 6) * level
        self.is_knocked_out = False

    def __repr__(self):
        return "Bandit, level {} (HP {}/{}, A {}, D {})".format(self.level, self.current_health, self.max_health,
                                                                self.attack_dmg, self.defense)

class Cultist(Character):
    def __init__(self, level):
        self.name = "Cultist"
        self.level = level
        self.max_health = randint(28, 33) * level
        self.current_health = self.max_health
        self.attack_dmg = randint(11, 13) * level
        self.defense = randint(2, 3) * level
        self.is_knocked_out = False

    def __repr__(self):
        return "{}, level {} (HP {}/{}, A {}, D {})".format(self.name, self.level, self.current_health, self.max_health,
                                                                self.attack_dmg, self.defense)

class Demon(Character):
    def __init__(self, level):
        self.name = "Demon Boss"
        self.level = level
        self.max_health = 150 * level
        self.current_health = self.max_health
        self.attack_dmg = randint(30, 33) * level
        self.defense = randint(0, 1) * level
        self.is_knocked_out = False

    def __repr__(self):
        return "{}, level {} (HP {}/{}, A {}, D {})".format(self.name, self.level, self.current_health, self.max_health,
                                                                self.attack_dmg, self.defense)
