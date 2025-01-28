from main_menu import MainMenu  # Import the MainMenu class
from fruit_catcher import Game as FruitCatcherGame  # Import the Fruit Catcher Game class
from haunted_forest_runner import Game as RunnerGame  # Import the Runner Game class
import pygame

# --- Function to run Fruit Catcher ---
def fruit_catcher_game():
    game = FruitCatcherGame()  
    game.run()  

def runner_game():
    game = RunnerGame()  
    game.run()    

# --- Main Function ---
def main():
    while True:
        menu = MainMenu()  # Show the main menu
        selected_game = menu.run()
        if selected_game == "fruit_catcher":
            fruit_catcher_game()  # run Fruit Catcher when selected
        if selected_game == "runner":
            runner_game()  # run Runner Game when selected
        else:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
