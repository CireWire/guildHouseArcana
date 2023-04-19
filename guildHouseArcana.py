import random
import json

class Guild:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.type = None
        self.members = []
        self.hourly_rate = 10  # This is the default hourly rate per member. You can adjust it as needed.

    def display_info(self):
        print(f"\nGuild Name: {self.name}")
        print(f"Guild Type: {self.type}")
        print(f"Guild Owner: {self.owner}")

    def display_members(self):
        if len(self.members) == 0:
            print("There are no members in your guild.")
        else:
            print("Guild Members:")
            for member in self.members:
                print(f"- {member.name}, {member.skills}")

class Member:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
class Game:
    def __init__(self):
        self.guild = None
        self.resources = {"gold": 100, "wood": 50, "crystals": 10}
        self.events = ["Your guild has been robbed! Some gold has been stolen.",
                       "Your guild has been sabotaged! Some damage has been done.",
                       "A magical disaster has struck your guild! Some repairs are needed."]

    def create_guild(self):
        print("Welcome to the Guild House Registry by CireWire!")
        print("Let's start by creating your guild.")
        name = input("Enter the name of your guild: ")
        owner = input("Enter the name of the guild owner: ")
        guild_type = input("Enter the type of your guild (e.g. adventurer, mage, thief, alchemist, assassin, "
                           "monster hunters, etc.): ")
        self.guild = Guild(name, owner)
        self.guild.type = guild_type
        print(f"\nYour guild '{name}' has been created with {guild_type} type and {owner} as the owner.")

    def add_member(self):
        if self.guild is None:
            print("Please create a guild first.")
            return

        print("\n----- ADD MEMBER -----")
        name = input("Enter the name of the member: ")
        skills = input("Enter the skills of the member: ")
        self.guild.members.append(Member(name, skills))
        print(f"\n{self.guild.members[-1].name} has been added to your guild.")

    def run(self):
        self.create_guild()
        while True:
            print("\n----- RESOURCES -----")
            print(f"Gold: {self.resources['gold']}")
            print(f"Wood: {self.resources['wood']}")
            print(f"Crystals: {self.resources['crystals']}")
            print("\n----- MENU -----")
            print("1. Display Guild Info")
            print("2. Add Member")
            print("3. Display Members")
            print("4. Handle Event")
            print("5. Work")
            print("6. Save Game")
            print("7. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.guild.display_info()
            elif choice == "2":
                self.add_member()
            elif choice == "3":
                self.guild.display_members()
            elif choice == "4":
                self.handle_event()
            elif choice == "5":
                self.work()
            elif choice == "6":
                self.save_game()
            elif choice == "7":
                break
            else:
                print("Invalid choice.")

    def handle_event(self):
        event = random.choice(self.events)
        print("\n----- EVENT -----")
        print(event)
        if "stolen" in event:
            amount = random.randint(10, 30)
            self.resources["gold"] -= amount
            print(f"You have lost {amount} gold.")
        elif "sabotage" in event:
            choice = input("Do you want to hire guards to protect your guild? (y/n) ")
            if choice == "y":
                cost = 20
                if self.resources["gold"] < cost:
                    print("You don't have enough gold to hire guards.")
                else:
                    self.resources["gold"] -= cost
                    print(f"You have hired guards to protect your guild. {cost} gold has been deducted.")
            else:
                damage = random.randint(5, 15)
                self.resources["wood"] -= damage
                print(f"{damage} wood has been damaged.")
        elif "disaster" in event:
            cost = 15
            if self.resources["crystals"] < cost:
                print("You don't have enough crystals to make repairs.")
            else:
                self.resources["crystals"] -= cost
                print(f"{cost} crystals have been spent on repairs.")
        else:
            print("Nothing happened.")

    def work(self):
        if self.guild is None:
            print("Please create a guild first.")
            return

        print("\n----- WORK -----")
        hours = int(input("Enter the number of hours you want to work: "))
        total_pay = 0
        for member in self.guild.members:
            pay = hours * self.guild.hourly_rate
            total_pay += pay
            print(f"{member.name} has worked for {hours} hours and earned {pay} gold.")

        self.resources["gold"] += total_pay
        print(f"\nYou have earned a total of {total_pay} gold from work.")

        # TODO: Add a chance for the player to find resources while working.

    def save_game(self):
        data = {"guild": self.guild.__dict__, "resources": self.resources}
        with open("save.json", "w") as f:
            json.dump(data, f)
        print("Game has been saved.")

    def load_game(self):
        try:
            with open("save.json", "r") as f:
                data = json.load(f)
            self.guild = Guild(data["guild"]["name"], data["guild"]["owner"])
            self.guild.type = data["guild"]["type"]
            self.guild.members = []
            for member in data["guild"]["members"]:
                self.guild.members.append(Member(member["name"], member["skills"]))
            self.resources = data["resources"]
            print("Game has been loaded.")
        except FileNotFoundError:
            print("No saved game found.")

game = Game()
game.run()
