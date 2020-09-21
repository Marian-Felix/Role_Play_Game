from random import randint
import time
import characters as c
import items as i


class Vertex:
    def __init__(self, value, description="Nothing to see ...", interact=None):
        self.value = value
        self.edges = []
        self.description = description
        self.interact = interact

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
        self.is_new_game = True

    def add_vertex(self, *node):
        for node in node:
            self.graph_dict[node.value] = node

    def add_edge(self, from_node, to_node):
        self.graph_dict[from_node.value].add_edge(to_node.value)
        self.graph_dict[to_node.value].add_edge(from_node.value)

    def explore_world(self):
        if self.is_new_game:
            hero_name = None
            while not hero_name:
                hero_name = input("Greetings, traveller! What is your name?\n")
            time.sleep(0.4)
            print("\nWelcome, {}! Use numbers to walk around and explore.  \n"
                  "Hint: Examine the situation before you take action.\n".format(hero_name))
            confirm()
            global hero
            hero = c.Hero(hero_name)
            current_location = "Village center"
            self.current_location_global = "Village center"
            print("\nYou find yourself at the {0}. \nGood luck, adventurer!".format(current_location))
        elif not self.is_new_game:
            current_location = "Village: Temple"
            self.current_location_global = "Village: Temple"
        confirm()
        self.is_new_game = False
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
        exp_choice = check_int_input([1,2,3,4], "\n*** Main menu ***\n(1) Travel\n(2) Examine\n(3) Interact\n"
                                                "(4) Hero menu")
        if exp_choice == 1:
            return
        if exp_choice == 2:
            print("\n", current_location.description)
            if input("\n*** Press Enter to continue ***"):
                continue
        if exp_choice == 3:
            try:
                current_location.interact()
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
          "                                               Lighthouse - - Cliff      Spring\n"
          .format(world_map.current_location_global), 113 * "*", "\n")


def check_int_input(valid_choices, terminal_prompt):
    while True:
        try:
            hero_choice = int(input(terminal_prompt))
            return hero_choice
            if hero_choice not in valid_choices:
                raise ValueError
        except ValueError:
            print("\n*** Wrong input. Enter a valid number. ***")


def hero_menu_choices():
    while True:
        hero.print_stats()
        hero_choice = check_int_input([1,2,3,4,5], "\n*** Hero ***\n(1) Equip Item\n(2) Unequip Item\n(3) Use Potion"
                                                   "\n(4) Show Map\n(5) Return\n")
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
            hero.use_potion()
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
    text = input("\n*** Press Enter to continue ***")
    if text:
        print(50*"-")
        print()
        return


def time_delay_txt(text):
    time.sleep(0.033 * len(text))


def battle(opponent):
    print("\n",35*"*"," BATTLE ", 35*"*", "\n {} vs. {}".format(hero, opponent))
    confirm()
    while True:
        print()
        battle_choice = check_int_input([1,2,3,4], "*** Battle! ***\nYou:   {}\nEnemy: {}\n(1) Attack\n(2) Risk Attack"
                                                   "\n(3) Use Potion\n(4) Retreat".format(hero.return_stats(),
                                                                                          opponent.return_stats()))
        if battle_choice == 1:
            hero.attack(opponent)
        if battle_choice == 2:
            hero.risk_attack(opponent)
        if battle_choice == 3:
            hero.use_potion()
        if battle_choice == 4:
            print("{} is trying to escape battle!".format(hero.name))
            time.sleep(0.6)
            if randint(0,10) in range(0,8):
                print("Phew! You retreated successfully.")
                return
            else:
                print("No Chance to retreat!")
        if opponent.is_knocked_out:
            print("\n{} is defeated!".format(opponent.name))
            confirm()
            return
        opponent_turn(opponent)
        if hero.is_knocked_out:
            hero_dies()


def opponent_turn(opponent):
    if randint(0,10) in range(7):
        opponent.attack(hero)
    else:
        opponent.risk_attack(hero)


def hero_dies():
    print("You have been knocked out!")
    confirm()
    time.sleep(1.5)
    print(". . . ")
    time.sleep(1.5)
    print(". . . ")
    time.sleep(1.5)
    print(". . . ")
    time.sleep(2)
    print(" You wake up at the village temple. Everything is dizzy and blurry ... ")
    hero.is_knocked_out = False
    confirm()
    hero.replenish()
    world_map.explore_world()

def print_quest(text):
    print(text)
    time_delay_txt(text)


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
            self.text = "\n'Hello, stranger ... you see, I don't have much time right now. Wait for a moment, " \
                        "will you?'"
            print_quest(self.text)
            self.nr_replies = 1
            confirm()
            return
        if self.quest == 0 and self.nr_replies == 1:
            self.text = "\n'OK. You townsfolk always come here and get killed for no reason but your own stupidity. " \
                        "\nThis is the last town before the lost mountains, so just don't go any further. \n" \
                        "I have enough problems without you already.'"
            print_quest(self.text)
            self.nr_replies = 2
            confirm()
            return
        if self.quest == 0 and self.nr_replies == 2:
            self.text = "\n'Alright!! You are one of the stubborn kind, aren't you? What's your name? {}? I'll tell you " \
                        "what.\nYou are lost or bored or whatever, and I keep losing men on the road to the north \n"\
                        "and I don't know why. Tell me what's going on in the Dark Forest and I will reward you." \
                        "\n\n Sigh ... you're completely unarmed! Here, take these ... " \
                        "the last owner has no more use for it'.\n".format(hero.name)
            print_quest(self.text)
            self.nr_replies = 0
            self.quest = 1
            hero.put_in_inventory(club1)
            hero.put_in_inventory(tunica1)
            confirm()
            print("\nHint: You can manage your items in the Hero menu! Try to equip your new items.")
            confirm()
            return
        if self.quest == 1 and self.nr_replies == 0:
            self.text = "\n'Come back if you know more about what's going on in the Dark Forest!'"
            print_quest(self.text)
            confirm()
            return
        if self.quest == 1 and self.nr_replies == 1:
            self.text = "\n'You went to the forest and came back alive? Not bad.\nWhat do you say? A cult? The big " \
                        "Tree ... the Evergreen Tree? This is where our ancestors used to bury there dead ...\n It was " \
                        "BURNING? I have to think about this. Take this and - please get back to me.'"
            print_quest(self.text)
            print()
            hero.put_in_inventory("potion")
            confirm()
            self.nr_replies = 2


class Location_LowerRoad():
    def __init__(self):
        self.quest = 1
        self.nr_replies = 0
        self.text = ""

    def interact(self):
        if self.quest == 1 and self.nr_replies == 0:
            self.text = "\nYou are searching the surroundings for clues.\n" \
                        "Out of nowhere, some guy is charging towards you!"
            print_quest(self.text)
            battle(banditLvl1_1)
            self.nr_replies = 1
            return
        if self.quest == 1 and self.nr_replies == 1:
            self.text = "\nThe bandit you killed lies before you. " \
                        "You found some useful things in your opponent's pockets!"
            print(self.text)
            hero.put_in_inventory("potion")
            hero.put_in_inventory(tunica2)
            self.nr_replies = 2
            confirm()
            print("\nYou defended yourself, but you're none the wiser about this place. "
                  "\nYou better follow your nose - is there a fire somewhere near?")
            confirm()
            return
        # if self.quest == 1 and self.nr_replies == 2:
        #     self.text = ""
        #     print(self.text)
        #     confirm()
        #     return


class Location_BurningTree():
    def __init__(self):
        self.quest = 1
        self.nr_replies = 0
        self.text = ""

    def interact(self):
        if self.quest == 1 and self.nr_replies == 0:
            self.text = "\nYou are trying to get a closer look of what's happening at the clearing, but you blow your" \
                        " cover. \nYou're so clumsy!!\nBeing startled, most of the cult members run from you into " \
                        "the forest."
            print(self.text)
            time_delay_txt(self.text)
            confirm()
            print("\nTwo of the bigger guys don't seem to like you intruding. You can surely take them - one by one!")
            confirm()
            battle(cultistlvl1_1)
            print("\nAs the first one tumbles to the ground, the other cultist is charging at you!")
            confirm()
            battle(cultistlvl1_2)
            self.nr_replies = 1
            return
        if self.quest == 1 and self.nr_replies == 1:
            self.text = "\n'Those people are crazy!', you're whispering as you are catching your breath. " \
                        "\nYou examine the bodies ... the Sherrif might want to know of this."
            print(self.text)
            hero.put_in_inventory(rags2)
            hero.put_in_inventory((club2))
            confirm()
            self.nr_replies = 2
            return
        if self.quest ==1 and self.nr_replies == 2:
            print("\nThe Sherrif might be interested to hear what happened here ...")
            confirm()
            if location_sherrif.quest == 1 and location_sherrif.nr_replies == 0:
                location_sherrif.nr_replies = 1
            return



# instances by location
# village temple
location_temple = Location_Temple()
# village sherrif
location_sherrif = Location_Sherrif()
club1 = i.Spiked_club()
tunica1 = i.Leather_tunica()

# Dark Forest: Lower Road
location_lowerRoad = Location_LowerRoad()
banditLvl1_1 = c.Bandit(1)
tunica2 = i.Leather_tunica()

# Dark Forest: Burning Tree
location_burningTree = Location_BurningTree()
cultistlvl1_1 = c.Cultist(1)
cultistlvl1_2 = c.Cultist(1)
club2 = i.Spiked_club()
rags2 = i.Woolen_rags()



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
                                   "ancient marble sculptures. \nThe waters here are said to have healing powers.", lambda: location_temple.interact())
sherrif = Vertex('Village: Sherrif\'s Office', "The sherrif looks busy. Law and order lie in his hands.", lambda: location_sherrif.interact())
# level1
df_lowerRoad = Vertex("Dark Forest: Lower Road", "Leaves crunch underfoot, while the sound of birds chirping dies away"
                                                 " with every step that leads you \ndeeper under the thickening "
                                                 "canopy. A scent of burned wood lies in the air."
                                                 " \nBut it's not wood alone "
                                                 "... you know this ... hair, fingernails?\nFlesh?", lambda: location_lowerRoad.interact())
df_cave = Vertex("Dark Forest: Spooky Cave")
df_altar = Vertex("Dark Forest: Altar")
df_burningTree = Vertex("Dark Forest: Burning Tree", "As you follow the scent of smoke through the undergrowth, you "
                                                     "reach a clearing: \nA giant tree is bursting into flames. \nFrom "
                                                     "your hideout, you watch a group of people in shabby robes "
                                                     "chanting a strange melody in front of the fire. "
                                                     "\nThey look like trouble, although they don't seem to be armed"
                                                     " heavily.", lambda: location_burningTree.interact())
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
