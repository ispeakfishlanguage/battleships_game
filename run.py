def set_grid_size(): 
    """Ask the user to enter the grid size and return the grid size."""
    while True:
        try:
            grid_size = int(input("Enter the grid size ( choose a number between 4 and 10, e.g., 8 for an 8x8 grid): "))
            if grid_size >= 4 and grid_size <= 10:
                return grid_size
            else:
                print("Invalid grid size. Please enter a number between 4 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")
def place_computer_ships():
    
def place_player_ships():
    
def play_round():
    
def check_if_hit():
    
def check_if_sunk():
    
def check_if_game_over():
    
def restart_game():
    
def main():
    print("Welcome to Battleships!")
    # Prompt the user to set the grid size
    grid_size = set_grid_size()

    # Initialize the game grid with the chosen size
    player_grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    computer_grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

    place_computer_ships()
    place_player_ships()
    play_round()
    check_if_hit()
    check_if_sunk()
    check_if_game_over()
    
