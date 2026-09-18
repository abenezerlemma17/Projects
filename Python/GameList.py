import os
import pickle
from prettytable import PrettyTable

FILE_NAME = "inventory.book.pkl"
def load_address():
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        with open(FILE_NAME, "rb") as f:
            return pickle.load(f)
    else:
        return {}
def save_address(inventory):
    with open(FILE_NAME, "wb") as f:
        pickle.dump(inventory, f)
#----------------------------------------------------------------------------------------------------------------------#
class GameList:
    def __init__(self, inventory):
        super().__init__()
        self.__name = []
        self.__genre = []

    def ask_name(self, inventory):
        name = self.__name
        user_input = input("What is the name of the game you played?: ").strip().lower()
        if user_input in name:
            print("This name already exists.")
        ask_genre = input("Enter the genre of said game: ").strip().lower()
        inventory[user_input] = ask_genre
        print("Name and genre inputted!")

    def display_list(self, inventory):
        if not inventory:
            print("There are no games listed")
            return
        table = PrettyTable(["Name", "Genre"])
        for name, genre in inventory.items():
            table.add_row([name, genre])
        print(table)
        print()

    def update_name(self, inventory):
        user_name = input("What game do you wish to update?: ").strip().lower()
        if user_name not in inventory:
            print("There are no games listed\n")
            print(user_name)
        else:
            new_user_input = input("Enter the game you wish to update?: ").strip().lower()
            inventory[new_user_input] = inventory.pop(user_name)
            print("Name updated successfully!\n")

    def update_genre(self, inventory):
        user_genre = input("What genre do you wish to update?: ").strip().lower()
        if user_genre not in inventory:
            print("There are no games listed\n")
            print(user_genre)
        else:
            new_user_input = input("Enter the genre you wish to update?: ").strip().lower()
            inventory[user_genre] = new_user_input
            print("Genre updated successfully!\n")

    def delete_item(self, inventory):
        name = input("What is the name of the game you wish to delete?: ").strip().lower()
        if len(inventory) == 0:
            print("The list is empty\n")
        if name not in inventory:
            print("There are no games listed\n")
            return
        else:
            del inventory[name]
            print("Game name deleted successfully!\n")

    def search_item(self, inventory):
        keyword = input("What is the name of the game's genre you wish to search?: ").strip().lower()
        results = {name: genre for name, genre in inventory.items() if keyword in name.lower() or genre.lower()}

        if results:
            table = PrettyTable(["Name", "Genere"])
            for name, genre in results.items():
                table.add_row([name, genre])
            print(table)
            print("\n")
        else:
            print("The item you are currently looking for is not registered.\n")
            return
#----------------------------------------------------------------------------------------------------------------------#
def menu():
    print("\nGame Lists\n"
          "The rule are fairly simple, enter any amount of games you can think of and their genres\n"
          "Menu\n"
          "-------\n"
          "1. Add a new game\n"
          "2. Display game list\n"
          "3. Delete an existing game\n"
          "4. Update a game's name\n"
          "5. Update a game's genre\n"
          "6. Search an existing game\n"
          "7. Exit\n")

def main():
    inventory = load_address()
    game = GameList(inventory)

    while True:
        menu()
        user_input = input("Enter your choice: ").strip().lower()
        if user_input == "1":
            game.ask_name(inventory)
        elif user_input == "2":
            game.display_list(inventory)
        elif user_input == "3":
            game.delete_item(inventory)
        elif user_input == "4":
            game.update_name(inventory)
        elif user_input == "5":
            game.update_genre(inventory)
        elif user_input == "6":
            game.search_item(inventory)
        elif user_input == "7":
            save_address(inventory)
        else:
            print("Invalid input")
        if user_input == "7":
            print("Thank you for playing!")
            break

main()