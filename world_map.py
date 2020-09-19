import time
from characters import *
from items import *


class Vertex:
    def __init__(self, value, description="Nothing to see ...", engagement=None):
        self.value = value
        self.edges = []
        self.description = description
        self.engagement = engagement

    def __repr__(self):
        return self.value

    def add_edge(self, adjacent_value):
        self.edges.append(adjacent_value)

    def get_edges(self):
        return self.edges


class Graph:
    def __init__(self):
        self.graph_dict = {}
        self.current_location_global = None

    def add_vertex(self, *node):
        for node in node:
            self.graph_dict[node.value] = node

    def add_edge(self, from_node, to_node):
        self.graph_dict[from_node.value].add_edge(to_node.value)
        self.graph_dict[to_node.value].add_edge(from_node.value)

    def explore_world(self):
        hero_name = None
        while not hero_name:
            hero_name = input("Greetings, traveller! What is your name?\n")
        time.sleep(0.4)
        print("\nWelcome, {}! Use numbers to walk around and explore.  \n"
              "Hint: Examine the situation before you take action.\n".format(hero_name))
        confirm()
        current_location = "Village center"
        self.current_location_global = "Village center"
        global hero
        hero = Hero(hero_name)
        print("\nYou find yourself at the {0}. \nGood luck, adventurer!".format(current_location))
        confirm()

        while True:
            explore_site(self.graph_dict[current_location])
            node = self.graph_dict[current_location]
            valid_choices = []
            print("\n*** Travel ***")
            for connected_location in node.edges:
                key = node.edges.index(connected_location) + 1
                print("({0}) {1}".format(key, connected_location))
                valid_choices.append(key)
                global return_var_travel_menu
                return_var_travel_menu = key + 1
            valid_choices.append(return_var_travel_menu)
            print("({0}) Return".format(return_var_travel_menu))

            while True:
                try:
                    choice = int(input())
                    if choice not in valid_choices:
                        raise ValueError
                    break
                except ValueError:
                    print("\n*** Wrong input. Enter a valid number. ***")
                # choice = int(input("\nWhere do you want to go? ")) # try except einfügen: wenn man keine Zahl einfügt

                    # print("\n*** Wrong input. Enter a valid number. ***")
            if choice == return_var_travel_menu:
                continue
            current_location = node.edges[choice-1]
            self.current_location_global = current_location
            time.sleep(0.08)
            print("\n... travelling ... ")
            time.sleep(0.2)
            print("Arriving at {0}".format(current_location))


def explore_site(current_location):
    while True:
        valid_choices = [1, 2, 3, 4]
        exp_choice = None
        time.sleep(0.4)
        try:
            exp_choice = int(input("\n*** Main menu ***\n(1) Travel\n(2) Examine\n(3) Interact\n(4) Hero menu"))
        except ValueError:
            print("\n*** Wrong input. Enter a valid number. ***")
        if exp_choice and exp_choice not in valid_choices:
            print("\n*** Wrong input. Enter a valid number. ***")
        if exp_choice == 1:
            return
        if exp_choice == 2:
            print("\n", current_location.description)
            # time.sleep(0.035*len(current_location.description))
            if input("\n*** Press Enter to continue ***"):
                continue
        if exp_choice == 3:
            try:
                current_location.engagement()
            except TypeError:
                print("\nNothing happens ... ")
                confirm()
            continue
        if exp_choice == 4:
            hero_menu_choices()


def print_map():
    print("\n", 113 * "*",
          "\n >>>>> You are at '{}'<<<<<\n                                                                            "
          "                 Dead End\n"
          "                                                                                     "
          "            |\n                                                                                "
          "               Pass - - Shelter\n                                                              "
          "                                   |\nTemple    Sherrif                       Evergreen Tree   "
          "                                  Pass Entrance\n   \\     /                                    "
          " |                                          /\n Village Center - - - - - - - - - - - - - Lower"
          " Road - - - - Upper Road - - - - Crossroads\n      |                                     /     "
          "\\              |                        \\\n Marketplace                             Cave    "
          "Altar       Encampment                    Rolling Hills\n                                      "
          "                                                       /       \\\n                            "
          "                                               Lighthouse - - Cliff      Spring\n".format(world_map.current_location_global), 113 * "*",
          "\n")


def hero_menu_choices():
    while True:
        print(hero)
        while True:
            valid_choices = [1, 2, 3, 4, 5]
            try:
                hero_choice = int(input("\n*** Hero ***\n(1) Equip Item\n(2) Unequip Item\n(3)"
                                        " Use Potion\n(4) Show Map\n(5) Return\n"))
                if hero_choice not in valid_choices:
                    raise ValueError
                break
            except ValueError:
                print("\n*** Wrong input. Enter a valid number. ***")
        if hero_choice == 1:
            if hero.inventory:
                while True:
                    valid_choices = [hero.inventory.index(item) for item in hero.inventory]
                    print("\n*** Choose item to equip ***")
                    print_inventory()

                    try:
                        inventory_choice = int(input()) - 1
                        if inventory_choice not in valid_choices:
                            raise ValueError
                        break
                    except ValueError:
                        print("\n*** Wrong input. Enter a valid number. ***")
                print()
                hero.equip_item(inventory_choice)
            else:
                print("\nYour inventory is empty!")
            confirm()
        if hero_choice == 2:
            if hero.items["weapon"] is not None or hero.items["armor"] is not None or hero.items["artefact"] is not None:
                while True:
                    valid_choices = [1, 2, 3, 4]
                    print("\n*** Choose item to unequip ***")
                    items_categories = ["Weapon", "Armor", "Artefact", "Return"]
                    for i in items_categories:
                        print("({}) {}".format(items_categories.index(i)+1, i))

                    try:
                        items_categories_choice = int(input())
                        if items_categories_choice not in valid_choices:
                            raise ValueError
                        break
                    except ValueError:
                        print("\n*** Wrong input. Enter a valid number. ***")
                print()
                hero.unequip_item(items_categories_choice)
                confirm()
            else:
                print("\nYou don't have anything equipped!")
                confirm()
        if hero_choice == 3:
            if hero.items["potion"] < 1:
                print("\nYou don't have any potions!")
                confirm()
                return
            elif hero.current_health == hero.max_health:
                print("\nYou are already at full health!")
                confirm()
                return
            elif hero.items["potion"] >= 1:
                hero.items["potion"] -= 1
                hero.replenish()
                print("\nYou used a potion. You feel replenished!")
                confirm()
        if hero_choice == 4:
            print_map()
            confirm()
        if hero_choice == 5:
            return
        continue


def return_item_stats(item):
    if item.type == "weapon":
        return "A: {}, value: {}".format(item.w_damage, item.get_value())
    if item.type == "armor":
        return "D: {}, value: {}".format(item.a_defense, item.get_value())
    if item.type == "artefact":
        return "Health bonus: {}, value: {}".format(item.h_bonus, item.value)


def print_engagement(text):
    print(text)
    # time.sleep(0.035*len(text))
    if input('\n*** Press Enter to continue ***'):
        return


def print_inventory():
    for item in hero.inventory:
        print("({}) {} ({})".format(hero.inventory.index(item)+1, item, return_item_stats(item)))


def confirm():
    if input("\n*** Press Enter to continue ***"):
        return


def time_delay_txt(text):
    time.sleep(0.033 * len(text))


def battle(opponent):
    print("\n",16*"*"," BATTLE ", 16*"*", "\n {}".format(opponent))
    # Neues Untermenü:
    # "*** Battle! ***"
    # (1) Attack
    # (2) Risk Attack
    # (3) Potion
    # (4) Retreat

    # Risk Attack = 50% Trefferchance von normaler Attack, aber dann doppelter Schaden
    # Retreat-Chance berechnet sich aus Level-Unterschied zw. Gegner und Held
    # wenn man stirbt, erwacht man wieder im Tempel


class Location_Temple():
    def interact(self):
        print("\nYou dive into the pulsing temple waters. You feel refreshed!")
        hero.replenish()
        confirm()


class Location_Sherrif():
    def __init__(self):
        self.quest = 0
        self.nr_replies = 0
        self.text = ""

    def interact(self):
        # time.sleep(0.4)
        if self.quest == 0 and self.nr_replies == 0:
            self.text = "\nHello, stranger ... you see, I don't have much time right now. Wait for a moment, will you?"
            print(self.text)
            time_delay_txt(self.text)
            self.nr_replies = 1
            confirm()
            return
        if self.quest == 0 and self.nr_replies == 1:
            self.text = "\nOK. You townsfolk always come here and get killed for no reason but your own stupidity. " \
                        "\nThis is the last town before the lost mountains, so just don't go any further. \n" \
                        "I have enough problems without you already."
            print(self.text)
            time_delay_txt(self.text)
            self.nr_replies = 2
            confirm()
            return
        if self.quest == 0 and self.nr_replies == 2:
            self.text = "\nAlright!! You are one of the stubborn kind, aren't you? What's your name? {}? I'll tell you " \
                        "what.\nYou are lost or bored or whatever, and I keep losing men on the road to the north \n"\
                        "and I don't know why. Tell me what's going on in the Dark Forest and I will reward you." \
                        "\n\n Sigh ... you're completely unarmed! Here, take these ... " \
                        "the last owner has no more use for it.\n".format(hero.name)
            print(self.text)
            time_delay_txt(self.text)
            self.replies = 0
            self.quest = 1
            hero.put_in_inventory(club1)
            hero.put_in_inventory(tunica1)
            confirm()
            print("\nHint: You can manage your items in the Hero menu! Try to equip your new items.")
            confirm()
            return


class Location_LowerRoad():
    def __init__(self):
        self.quest = 1
        self.nr_replies = 0
        self.text = ""

# nächstes Ziel: Kämpfe programmieren!
    def interact(self):
        if self.quest == 1 and self.nr_replies == 0:
            self.text = "\nYou are searching the surroundings for clues.\n" \
                        "Out of nowhere, a bandit is charging towards you!"
            print(self.text)
            time_delay_txt(self.text)
            self.nr_replies = 1
            battle(banditLvl1_1)
            return



# important instances
npc_temple = Location_Temple()
npc_sherrif = Location_Sherrif()
club1 = Spiked_club()
tunica1 = Leather_tunica()
lowerRoad = Location_LowerRoad()
banditLvl1_1 = Bandit(1)

# instantiate world map as graph
world_map = Graph()

# instantiate vertices of graph
# town
village = Vertex("Village center", "You're standing at the main square of this little township you found. \nYou hear"
                                   " the bells ringing. The wind is blowing leaves over the white gravel plain. "
                                   "\nAn old man is sitting under the big solitary lime tree.",
                 lambda: print_engagement("\nYou approach the old man.\n'Want to buy an apple?"
                                          "\nOh ... you are not from here. Stay in the village. Don't be stupid ... "
                                          "\nIf you came to help, the sherrif might want to talk to you'"))
marketplace = Vertex("Village: Marketplace", "A bustling, colorful marketplace with traders and craftsmen shouting and "
                                             "haggling.\nThis seems like a nice place for a bargain.")
temple = Vertex("Village: Temple", "You grasp a glimpse of the sanctity of this place, as your eyes wander \nover the "
                                   "ancient marble sculptures. \nThe waters here are said to have healing powers.", lambda: npc_temple.interact())
sherrif = Vertex('Village: Sherrif\'s Office', "The sherrif looks busy. Law and order lie in his hands.", lambda: npc_sherrif.interact())
# level1
df_lowerRoad = Vertex("Dark Forest: Lower Road", "Leaves crunch underfoot, while the sound of birds chirping dies away"
                                                 " with every step that leads you \ndeeper under the thickening "
                                                 "canopy. A scent of burned wood lies in the air."
                                                 " \nBut it's not wood alone "
                                                 "... you know this ... hair, fingernails?\nFlesh?", lambda: lowerRoad.interact())
df_cave = Vertex("Dark Forest: Spooky Cave")
df_altar = Vertex("Dark Forest: Altar")
df_burningTree = Vertex("Dark Forest: Burning Tree")
# level2
df_upperRoad = Vertex("Dark Forest: Upper Road")
df_encampment = Vertex("Dark Forest: Encampment")
df_crossroads = Vertex("Dark Forest: Crossroads")
# level3
hp_rollingHills = Vertex("High Plains: Rolling Hills")
hp_cliff = Vertex("High Plains: Breezy Cliff")
hp_lighthouse = Vertex("High Plains: Albert's Lighthouse")
hp_spring = Vertex("High Plains: Spring")
# level4
lm_pass_entrance = Vertex("Lost Mountains: Pass Entrance")
lm_pass = Vertex("Lost Mountains: Pass")
lm_shelter = Vertex("Lost Mountains: Shelter")
lm_deadEnd = Vertex("Lost Mountains: Pass Dead End")

# add vertices to map
world_map.add_vertex(village, marketplace, temple, sherrif)  # town vertices
world_map.add_vertex(df_lowerRoad, df_cave, df_altar, df_burningTree)  # level1 vertices
world_map.add_vertex(df_upperRoad, df_encampment, df_crossroads)  # level2 vertices
world_map.add_vertex(hp_rollingHills, hp_cliff, hp_lighthouse, hp_spring)  # level3 vertices
world_map.add_vertex(lm_pass_entrance, lm_pass, lm_shelter, lm_deadEnd)  # level4 vertices

# add connections between vertices
# village
world_map.add_edge(village, marketplace)
world_map.add_edge(village, temple)
world_map.add_edge(village, sherrif)
world_map.add_edge(village, df_lowerRoad)
# level1
world_map.add_edge(df_lowerRoad, df_burningTree)
world_map.add_edge(df_lowerRoad, df_cave)
world_map.add_edge(df_lowerRoad, df_altar)
world_map.add_edge(df_lowerRoad, df_upperRoad)
# level2
world_map.add_edge(df_upperRoad, df_encampment)
world_map.add_edge(df_upperRoad, df_crossroads)
world_map.add_edge(df_crossroads, hp_rollingHills)
world_map.add_edge(df_crossroads, lm_pass_entrance)
# level3
world_map.add_edge(hp_rollingHills, hp_cliff)
world_map.add_edge(hp_cliff, hp_lighthouse)
world_map.add_edge(hp_rollingHills, hp_spring)
# level4
world_map.add_edge(lm_pass_entrance, lm_pass)
world_map.add_edge(lm_pass, lm_shelter)
world_map.add_edge(lm_pass, lm_deadEnd)

world_map.explore_world()
