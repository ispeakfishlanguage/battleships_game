import random
import subprocess
import pyfiglet
from colorama import Fore, Back, Style, init

# Initializing colorama
init(autoreset=True)


# Define the text you want to display
text_to_display = "BattleShips"

# Create a FIGlet object with a specific font
font_name = "3x5"
figlet_text = pyfiglet.Figlet()

# Generate ASCII art text using pyfiglet
ascii_text = figlet_text.renderText(text_to_display)

# Print the ASCII art text
print(ascii_text)


# Define ship lengths and icons
SHIP_LENGTHS = {'Battleship': 4, 'Cruiser': 3, 'Destroyer': 2}
SHIP_ICONS = {
    'Battleship': Fore.CYAN + 'B',
    'Cruiser': Fore.MAGENTA + 'C',
    'Destroyer': Fore.YELLOW + 'D'
}
EMPTY = '.'


def set_grid_size():
    """Ask the user to enter the grid size and return the grid size."""
    while True:
        try:
            grid_size = int(input(
                "Enter the grid size (between 4 and 10, "
                "e.g., 8 for an 8x8 grid): "
            ))
            if 4 <= grid_size <= 10:
                return grid_size
            else:
                print(
                    Fore.RED +
                    Style.BRIGHT +
                    "Invalid grid size. Please enter a number between 4"
                    " and 10."
                )
        except ValueError:
            print(
                Fore.RED +
                Style.BRIGHT +
                "Invalid input. Please enter a number."
            )


def print_grid(grid):
    """Print the grid."""
    for row in grid:
        print(" ".join([SHIP_ICONS[x] if x in SHIP_ICONS else x for x in row]))
    print()


def set_random_ship(grid_size, ship, grid):
    """Randomly place a ship on the grid."""
    while True:
        orientation = random.choice(['H', 'V'])
        if orientation == 'H':
            x = random.randint(0, grid_size - SHIP_LENGTHS[ship])
            y = random.randint(0, grid_size - 1)
            if all(grid[y][x + i] == EMPTY for i in range(SHIP_LENGTHS[ship])):
                for i in range(SHIP_LENGTHS[ship]):
                    grid[y][x + i] = ship
                return [(y, x + i) for i in range(SHIP_LENGTHS[ship])]
        elif orientation == 'V':
            x = random.randint(0, grid_size - 1)
            y = random.randint(0, grid_size - SHIP_LENGTHS[ship])
            if all(grid[y + i][x] == EMPTY for i in range(SHIP_LENGTHS[ship])):
                for i in range(SHIP_LENGTHS[ship]):
                    grid[y + i][x] = ship
                return [(y + i, x) for i in range(SHIP_LENGTHS[ship])]


def set_computer_ships(grid_size, computer_grid):
    """Randomly place all computer ships and return their positions."""
    computer_ships = {'Battleship': [], 'Cruiser': [], 'Destroyer': []}
    for ship in computer_ships:
        computer_ships[ship] = set_random_ship(grid_size, ship, computer_grid)
    return computer_ships


def get_player_ships(player_grid):
    """Ask the user to place their ships and return the player ships."""
    player_ships = {'Battleship': [], 'Cruiser': [], 'Destroyer': []}
    for ship in player_ships:
        while True:
            try:
                print(f"Place your {ship}...")
                x, y, orientation = input(
                    "Enter the starting coordinates and"
                    f" orientation for your {ship} (e.g."
                    " A 1 H for horizontal, "
                    "A 1 V for vertical): "
                ).split()
                x = ord(x.upper()) - 65
                y = int(y) - 1
                if orientation.upper() == "H":
                    for i in range(SHIP_LENGTHS[ship]):
                        if player_grid[y][x+i] != EMPTY:
                            raise ValueError
                    for i in range(SHIP_LENGTHS[ship]):
                        player_grid[y][x+i] = ship
                        player_ships[ship].append((y, x+i))
                elif orientation.upper() == "V":
                    for i in range(SHIP_LENGTHS[ship]):
                        if player_grid[y+i][x] != EMPTY:
                            raise ValueError
                    for i in range(SHIP_LENGTHS[ship]):
                        player_grid[y+i][x] = ship
                        player_ships[ship].append((y+i, x))
                else:
                    raise ValueError
                break
            except (ValueError, IndexError):
                print(
                    Fore.RED +
                    Style.BRIGHT +
                    "Invalid input. Please try again."
                )
    return player_ships


def is_valid_coordinate(x, y, grid_size):
    return 0 <= x < grid_size and 0 <= y < grid_size


def player_turn(player_shots_grid, grid_size):
    """Function for the player's turn, ensuring shots are unique."""
    while True:
        try:
            x = int(input(f"Enter column (0-{grid_size-1}): "))
            y = int(input(f"Enter row (0-{grid_size-1}): "))

            if (
                is_valid_coordinate(x, y, len(player_shots_grid)) and
                player_shots_grid[y][x] == EMPTY
            ):
                return x, y
            else:
                print(
                    Fore.RED +
                    Style.BRIGHT +
                    "Invalid input or previously shot at this location. "
                    "Please try again."
                )
        except ValueError:
            print(
                Fore.RED +
                Style.BRIGHT +
                "Invalid input. Please enter numbers."
            )


def check_if_hit(x, y, ships, shots_grid):
    """Check if a ship has been hit."""
    for ship in ships:
        if (x, y) in ships[ship]:
            print(Back.GREEN + Style.BRIGHT + "Hit!")
            shots_grid[y][x] = 'X'
            return True
    else:
        print(Back.RED + Style.BRIGHT + "Miss!")
        shots_grid[y][x] = 'O'
        return False


def check_if_sunk(ships, shots_grid):
    """Check if a ship has been sunk."""
    for ship in ships:
        if all(shots_grid[y][x] == 'X' for x, y in ships[ship]):
            print(Fore.WHITE + Back.GREEN + f"You sunk the opponent's {ship}!")
            return True
    return False


def check_all_sunk(ships, shots_grid):
    """Check if all ships are sunk."""
    for ship in ships:
        if not all(shots_grid[y][x] == 'X' for x, y in ships[ship]):
            return False
    return True


def computer_turn(grid_size, computer_shots_grid):
    """ Computer's turn function to ensure unique shots. """
    while True:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        if computer_shots_grid[y][x] == EMPTY:
            return x, y


def main():
    print("Welcome to Battleships!")

    # Prompt the user to set the grid size
    grid_size = set_grid_size()

    # Initialize the game grids and shot grids with the chosen size
    player_grid = [
        [EMPTY for _ in range(grid_size)]
        for _ in range(grid_size)
    ]
    computer_grid = [
        [EMPTY for _ in range(grid_size)]
        for _ in range(grid_size)
    ]
    player_shots_grid = [
        [EMPTY for _ in range(grid_size)]
        for _ in range(grid_size)
    ]
    computer_shots_grid = [
        [EMPTY for _ in range(grid_size)]
        for _ in range(grid_size)
    ]

    player_ships = get_player_ships(player_grid)
    computer_ships = set_computer_ships(grid_size, computer_grid)

    while True:
        print("Your Ships:")
        print_grid(player_grid)
        print("Your Shots:")
        print_grid(player_shots_grid)

        # Player's turn
        print("Your Turn:")
        player_x, player_y = player_turn(player_shots_grid, grid_size)
        check_if_hit(player_x, player_y, computer_ships, player_shots_grid)
        if check_all_sunk(computer_ships, player_shots_grid):
            print(Fore.GREEN + Style.BRIGHT + "Congratulations! You won!")
            break

        # Computer's turn
        print("Computer's Turn:")
        computer_x, computer_y = computer_turn(grid_size, computer_shots_grid)
        check_if_hit(computer_x, computer_y, player_ships, computer_shots_grid)
        if check_all_sunk(player_ships, computer_shots_grid):
            print(
                Fore.RED + Style.BRIGHT + "Sorry, you lost. The computer won."
            )
            break

    restart = input("Do you want to play again? (Y/N): ")
    if restart.upper() == 'Y':
        main()
    elif restart.upper() == 'N':
        print("Thanks for playing!")
    else:
        print("Invalid input. Exiting the game.")


if __name__ == '__main__':
    main()
