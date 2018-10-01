import random


class Hero:
    # Implement battle damage priority attribute
    # Implement steal function and attributes
    def __init__(self, name, health=100):
        # All of the lists will hold objects
        self.name = name
        self.abilities = []
        self.armors = []
        self.start_health = health
        self.health = health
        self.deaths = 0
        self.kills = 0
        self.damage_priority = True
        self.steal = True

    def add_ability(self, ability_name):
        self.abilities.append(ability_name)

    # Adding all the attack strength of the Ability objects in the abilities list.
    def attack(self):
        total_strength = 0

        for ability in self.abilities:
            total_strength += ability.attack()

        return total_strength

    # Adding all the defense strength of the Armor objects that passed in.
    def defend(self):
        total_defense = 0
        if self.armors:
            for gear in self.armors:
                total_defense += gear.defend()
            return total_defense
        else:
            return 0

    def take_damage(self, damage_amnt):
        self.start_health = self.health - damage_amnt

    def add_kills(self, num_kills):
        self.kills += num_kills

    def add_armor(self, gear):
        self.armors.append(gear)


class Ability:
    def __init__(self, name, attack_strength):
        self.name = name
        self.attack_strength = int(attack_strength)

    def attack(self):

        low = self.attack_strength // 2
        return random.randint(low, self.attack_strength)

    def update_attack(self, attack_strength):

        self.attack_strength = attack_strength


class Weapon(Ability):
    def attack(self):
        return random.randint(0, self.attack_strength)


# The Team class will hold all the Hero objects have Ability and Armor objects
class Team:
    def __init__(self, team_name):
        self.name = team_name
        self.heroes = list()

    def add_hero(self, name):
        self.heroes.append(name)

    def remove_hero(self, name):
        if len(self.heroes) >= 1:
            for obj in self.heroes:
                if name == obj.name:
                    self.heroes.remove(obj)
            return 0
        else:
            return 0

    def find_hero(self, name):
        if self.heroes:
            for obj in self.heroes:
                if name == obj.name:
                    return obj
            return 0
        else:
            return 0

    def view_all_heroes(self):
        for obj in self.heroes:
            print(obj.name)

    # This take in a TEAM object and then add the number if kills from defend
    def attack(self, other_team):
        total_strength = 0

        for obj in self.heroes:
            total_strength += obj.attack()

        other_team.defend(total_strength)
        for villain in other_team.heroes:
            if villain.health <= 0:
                for hero in self.heroes:
                    hero.add_kills(1)

    # Take in the excess amount from attack function, calculate it, then return the number of kills from def deal damage
    def defend(self, damage_amnt):
        total_defense = 0
        for obj in self.heroes:
            for armor in obj.armors:
                total_defense += armor.defend()

        after_calculation = damage_amnt - total_defense

        if after_calculation > 0:
            return self.deal_damage(after_calculation)

    # Take in calculated damage from defend function, apply it to the TEAM object, return total dead for defend function
    def deal_damage(self, damage):
        spread_damage = damage/len(self.heroes)
        total_dead = 0
        for obj in self.heroes:
            obj.health -= spread_damage
            if obj.health <= 0:
                obj.deaths += 1
                total_dead += 1

        return total_dead

    def revive_heroes(self, health=100):
        if health:
            for obj in self.heroes:
                obj.health = health
        for obj in self.heroes:
            obj.health = obj.start_health

    def stats(self):
        for hero in self.heroes:
            print(hero.name + "has:\n" +
                  str(hero.kills) + " kills\n" +
                  str(hero.deaths) + " deaths")

    def update_kills(self):
        deaths = 0
        for hero in self.heroes:
            if hero.deaths != 0:
                deaths += 1
                print(hero.name + " has been killed")
        if deaths == len(self.heroes):
            print(self.name + " has been wiped out!")


class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = int(defense)

    def defend(self):
        return random.randint(0, self.defense)

class Steal:
    def __init__(self, thief, other_team):
        self.victim = random.choice(other_team.heroes)
        self.thief = thief


    # This function will allow the hero to steal from the victim
    def stealing(self):
        stolen_item = self.victim.abilities.pop(random.randint(0, len(self.victim.abilities) - 1))
        self.thief.add_abilities(stolen_item)



class Arena:

    def __init__(self):
        self.hero = None
        self.team_one = None
        self.team_two = None

    def run(self):
        self.build_team_one()
        self.build_team_two()
        self.team_battle()
        self.show_stats()

    # Function that let the user to create hero along with armors and abilities
    def hero_builder(self):
        try:
            hero_name = input("What is this hero name? ")
            hero_health = input("What is the starting numerical health of this hero?(Default 100)")

            self.hero = Hero(hero_name, int(hero_health))

            ability_number = input("How many ability does this hero have?(Numerical input) ")
            self.multiple_abilities(int(ability_number))

            armor_number = input("How many armor does this hero have?(Numerical input) ")
            self.multiple_armors(int(armor_number))

            return self.hero

        except ValueError:
            print("You didn't enter a numerical value in one of the prompts!")

        except KeyboardInterrupt:
            print("You try to interrupt that keyboard!")

    # Handle adding abilities for hero builder
    def multiple_abilities(self, number_of_abilities):
        for ability in range(0, number_of_abilities):
            ability_name = input("What is this ability name? ")
            ability_power = input("How strong is this ability?\nNumerical input: ")
            self.hero.add_ability(Ability(ability_name, ability_power))

    # Handle adding weapons
    def multiple_weapons(self, number_of_weapons):
        for weapon in range(0, number_of_weapons):
            weapon_name = input("What is this ability name? ")
            weapon_power =  input("How strong is this weapon?\n Numerical input: ")
            self.hero.add_ability(Weapon(weapon_name, weapon_power))


    # Handle adding armors for hero builder
    def multiple_armors(self, number_of_armors):
        for armor in range(0, number_of_armors):
            armor_name = input("What is the name of the gear? ")
            armor_value = input("What is the defense value?\nNumerical input: ")
            self.hero.add_armor(Armor(armor_name, armor_value))

    def build_team_one(self):
        name = input("What is the first team's name?")
        self.team_one = Team(name)
        flag = input("Add a hero? Y/N")

        if flag.upper() == "N" and len(self.team_one.heroes) == 0:
            print("There must be at least one hero in team one in order to begin!")
            self.build_team_one()

        while flag.upper() != "N":
            teammates = self.hero_builder()
            self.team_one.add_hero(teammates)
            flag = input("Add another hero? Y/N")

        return self.team_one

    def build_team_two(self):
        name = input("What is the second team's name?")
        self.team_two = Team(name)
        flag = input("Add a hero? Y/N")

        if flag.upper() == "N" and len(self.team_two.heroes) == 0:
            print("There must be at least one hero in team two in order to begin!")
            self.build_team_two()

        while flag.upper() != "N":
            teammates = self.hero_builder()
            self.team_two.add_hero(teammates)
            flag = input("Add another hero? Y/N")

        return self.team_two

    def display_team(self):
        if self.team_one.heroes:
            for hero in self.team_one.heroes:
                print(hero.name)
                for ability in hero.abilities:
                    print(ability.name + "\n" + ability.attack_strength)
                for gear in hero.armors:
                    print(gear.name + "\n" + gear.defense + "\n")

        if self.team_two.heroes:
            for hero in self.team_two.heroes:
                print(hero.name)
                for ability in hero.abilities:
                    print(ability.name + "\n" + ability.attack_strength)
                for gear in hero.armors:
                    print(gear.name + "\n" + gear.defense)

    # Simulate battle by calling attack and defend function from team object until one of the teams died
    def team_battle(self):
        team_one_died = 0
        team_two_died = 0

        # Check if the two teams can kill each other
        # if self.team_one.attack(self.team_two) and self.team_two.attack(self.team_one) != 0{}
        while team_one_died != len(self.team_one.heroes) and team_two_died != len(self.team_two.heroes):

            # Implement

            self.team_one.attack(self.team_two)

            for hero in self.team_two.heroes:
                if hero.deaths != 0:
                    team_two_died += 1

            self.team_two.attack(self.team_one)

            for hero in self.team_one.heroes:
                if hero.deaths != 0:
                    team_one_died += 1

        self.team_one.update_kills()
        self.team_two.update_kills()

        # If both them can't kill each other
        # print("Both teams can't damage each other")

    def show_stats(self):
        self.team_one.stats()
        self.team_two.stats()

# if __name__ == "__main__":
#    hero = Hero("Wonder Woman")
#    print(hero.attack())
#    ability = Ability("Divine Speed", 300)
#    hero.add_ability(ability)
#    print(hero.attack())
#    new_ability = Ability("Super Human Strength", 800)
#    hero.add_ability(new_ability)
#    print(hero.attack())

newArena = Arena()

# Running the program because Zurich told me to
newArena.run()
