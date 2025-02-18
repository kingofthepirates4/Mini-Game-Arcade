from main_menu import MainMenu  # Import the MainMenu class
from fruit_catcher import Game as FruitCatcherGame  # Import the Fruit Catcher Game class
from haunted_forest_runner import Game as RunnerGame  # Import the Runner Game class
from tetris import Tetris  # Import the Tetris game class
import pygame

# --- Function to run Fruit Catcher ---
def fruit_catcher_game():
    game = FruitCatcherGame()  
    game.run()  

# --- Function to run Runner Game ---
def runner_game():
    game = RunnerGame()  
    game.run()    

# --- Function to run Tetris ---
def tetris_game():
    game = Tetris()
    game.run()

# --- Main Function ---
def main():
    while True:
        menu = MainMenu()  
        selected_game = menu.run()
        
        if selected_game == "fruit_catcher":
            fruit_catcher_game()  
        elif selected_game == "runner":
            runner_game()  
        elif selected_game == "tetris":
            tetris_game()  
        else:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
