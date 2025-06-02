"""
Spyder Editor

This is a temporary script file.
"""

def request_location(question_str):
    """
    Prompt the user for a board location, and return that location.
    
    Takes a string parameter, which is displayed to the user as a prompt.
    
    Raises ValueError if input is not a valid integer, 
    or RuntimeError if the location typed is not in the valid range.
    
    *************************************************************
    DO NOT change this function in any way
    You MUST use this function for ALL user input in your program
    *************************************************************
    """
    loc = int(input(question_str))
    if loc<0 or loc>=24:
        raise RuntimeError("Not a valid location")
    return loc


def draw_board(g):
    """
    Display the board corresponding to the board state g to console.
    Also displays the numbering for each point on the board, and the
    number of counters left in each players hand, if any.
    A reference to remind players of the number of each point is also displayed.
    
    You may use this function in your program to display the board
    to the user, but you may also use your own similar function, or
    improve this one, to customise the display of the game as you choose
    """
    def colored(r, g, b, text):
        """
        Spyder supports coloured text! This function creates coloured
        version of the text 'text' that can be printed to the console.
        The colour is specified with red (r), green (g), blue (b) components,
        each of which has a range 0-255.
        """
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def piece_char(i):
        """
        Return the (coloured) character corresponding to player i's counter,
        or a + to indicate an unoccupied point
        """
        if i==0:
            return colored(100,100,100,'+')
        elif i==1:
            return colored(255,60,60,'X')
        elif i==2:
            return colored(60,120,255,'O')

        
    board = '''
x--------x--------x  0--------1--------2 
|        |        |  |        |        |
|  x-----x-----x  |  |  3-----4-----5  |
|  |     |     |  |  |  |     |     |  |
|  |  x--x--x  |  |  |  |  6--7--8  |  |
|  |  |     |  |  |  |  |  |     |  |  |
x--x--x     x--x--x  9-10-11    12-13-14
|  |  |     |  |  |  |  |  |     |  |  |
|  |  x--x--x  |  |  |  | 15-16-17  |  |
|  |     |     |  |  |  |     |     |  |
|  x-----x-----x  |  |  18---19----20  |
|        |        |  |        |        |
x--------x--------x  21------22-------23
'''    
    boardstr = ''
    i = 0
    for c in board:
        if c=='x':
            boardstr += piece_char(g[0][i])
            i += 1
        else:
            boardstr += colored(100,100,100,c)
    if g[1]>0 or g[2]>0:
        boardstr += '\nPlayer 1: ' + (piece_char(1)*g[1])
        boardstr += '\nPlayer 2: ' + (piece_char(2)*g[2])
    print(boardstr)
    
    
    
#############################    
# The functions for each task
    
def is_adjacent(i, j):
    """
    A function that takes two parameters, i and j, which represent the indices 
    of two points on the game board, and returns the Boolean value True if 
    those two points are adjacent to one another (connected by a line without 
    going through another point), or False otherwise. 
    A point is not adjacent to itself.
    """
    # Define the board as a list of points and their connections
    board = {
        0: [1, 9],
        1: [0, 2, 4],
        2: [1, 14],
        3: [4, 10],
        4: [1, 3, 5, 7],
        5: [4, 13],
        6: [7, 11],
        7: [4, 6, 8],
        8: [7, 12],
        9: [0, 10, 21],
        10: [3, 9, 11, 18],
        11: [6, 10, 15],
        12: [8, 13, 17],
        13: [5, 12, 14, 20],
        14: [2, 13, 23],
        15: [11, 16],
        16: [15, 17, 19],
        17: [12, 16],
        18: [10, 19],
        19: [16, 18, 20, 22],
        20: [13, 19],
        21: [9, 22],
        22: [19, 21, 23],
        23: [14, 22]
    }

    # Check if i and j are in each other's list of connections
    result = j in board[i] and i in board[j]
    return result
    
def new_game():
    """
    Initialise a new Nine Men's Morris game.

    Returns:
    list: A list representing the initial game state.
          - Element 0: The board with 24 unoccupied points.
          - Element 1: Number of counters that player 1 has in hand.
          - Element 2: Number of counters that player 2 has in hand.
          - Element 3: The active player (1 for player 1, 2 for player 2).
    """
    # Initialise the board with 24 unoccupied points
    board = [0] * 24

    # Initialise player counters to 9 for both players
    p1_counters = 9
    p2_counters = 9

    # Set the active player to player 1
    active_player = 1

    # Construct and return the game state
    game_state = [board, p1_counters, p2_counters, active_player]
    return game_state

def remaining_counters(g):
    """
    Calculate the total number of counters that the current player has available.

    Args:
    g (list): The game state.
          - Element 0: The board with 24 points.
          - Element 1: Number of counters that player 1 has in hand.
          - Element 2: Number of counters that player 2 has in hand.
          - Element 3: The active player (1 for player 1, 2 for player 2).

    Returns:
    integer: The total number of counters that the current player has available.
    """
    # Extract relevant information from the game state
    board, p1_counters, p2_counters, active_player = g

    # Determine the current player's counters
    if active_player == 1:
        current_player_counters = p1_counters + board.count(1)
    else:
        current_player_counters = p2_counters + board.count(2)

    return current_player_counters

def is_in_mill(g, i):
    """
    Determine if the counter at point i is in a mill.

    Parameters:
    - g (list): The game state.
    - i (int): The index of the point to check.

    Returns:
    - int: -1 if i is outside the range 0-23 inclusive or if there is no counter at point i,
           0 if the counter at point i is not in a mill,
           1 if the counter at point i belongs to player 1 and is in (one or more) mills,
           2 if the counter at point i belongs to player 2 and is in (one or more) mills.
    """
    # Extract relevant information from the game state
    board, _, _, _ = g

    # Check if i is outside the range 0-23 or if there is no counter at point i
    if i < 0 or i >= len(board) or board[i] == 0:
        return -1

    # Get the player whose counter is at point i
    player = board[i]

    # Define all possible mills on the board (without diagonal mills)
    mills = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal mills
        [9, 10, 11], [12, 13, 14], [15, 16, 17],
        [18, 19, 20], [21, 22, 23],
        [0, 9, 21], [3, 10, 18], [6, 11, 15],  # Vertical mills
        [1, 4, 7], [16, 19, 22], [8, 12, 17],
        [5, 13, 20], [2, 14, 23]
    ]

    # Check if the counter at point i is in a mill
    for mill in mills:
        if i in mill and all(board[j] == player for j in mill):
            return player

    # If i is not in a mill, return 0
    return 0


def player_can_move(g):
    """
    Check if the current player has a valid move to make.

    Args:
    g (list): The game state.
          - Element 0: The board with 24 points.
          - Element 1: Number of counters that player 1 has in hand.
          - Element 2: Number of counters that player 2 has in hand.
          - Element 3: The active player (1 for player 1, 2 for player 2).

    Returns:
    bool: True if the current player has a valid move, False otherwise.
    """
    # Extract relevant information from the game state
    board, p1_counters, p2_counters, active_player = g

    # Check if the current player has counters in hand
    if active_player == 1 and p1_counters > 0:
        return True
    elif active_player == 2 and p2_counters > 0:
        return True

    # Check if any counters on the board are next to an adjacent unoccupied space
    for i in range(24):
        if board[i] == active_player and any(is_adjacent(i, j) and board[j] == 0 for j in range(24)):
            return True

    return False


def place_counter(g, i):
    """
    Place a counter of the currently active player at point i on the board.

    Args:
    g (list): The game state.
          - Element 0: The board with 24 points.
          - Element 1: Number of counters that player 1 has in hand.
          - Element 2: Number of counters that player 2 has in hand.
          - Element 3: The active player (1 for player 1, 2 for player 2).
    i (integer): The index of the point to place the counter (0-23).

    Raises:
    RuntimeError: If there is already a counter at the specified location.

    """
    # Extract relevant information from the game state
    board, p1_counters, p2_counters, active_player = g

    # Check if there is already a counter at the specified location
    if board[i] != 0:
        raise RuntimeError("There is already a counter at this location!")

    # Place a counter of the currently active player at point i on the board
    board[i] = active_player

    # Decrement the number of counters that the current player has in their hand
    if active_player == 1:
        g[1] -= 1
    else:
        g[2] -= 1


def move_counter(g, i, j):
    """
    Move a counter of the currently active player from point i to the adjacent point j on the board.

    Args:
    g (list): The game state.
          - Element 0: The board with 24 points.
          - Element 1: Number of counters that player 1 has in hand.
          - Element 2: Number of counters that player 2 has in hand.
          - Element 3: The active player (1 for player 1, 2 for player 2).
    i (integer): The index of the starting point to move the counter from (0-23).
    j (integer): The index of the destination point to move the counter to (0-23).

    Raises:
    RuntimeError: If points i and j are not adjacent, if point i doesn't contain a counter of the current player,
                  or if there is already a counter at point j.
    """
    # Extract relevant information from the game state
    board, p1_counters, p2_counters, active_player = g

    # Check if points i and j are adjacent
    if not is_adjacent(i, j):
        raise RuntimeError(f"Points {i} and {j} are not adjacent!")

    # Check if point i contains a counter of the current player
    if board[i] != active_player:
        raise RuntimeError(f"Point {i} does not contain a counter of the current player!")

    # Check if point j is unoccupied
    if board[j] != 0:
        raise RuntimeError(f"There is already a counter at point {j}!")

    # Move a counter from point i to point j
    board[j] = active_player
    board[i] = 0


def remove_opponent_counter(g, i):
    """
    Remove the counter at point i on the board if it belongs to the opposing player.
    Args:
    g (list): The game state.
    - Element 0: The board with 24 points.
    - Element 1: Number of counters that player 1 has in hand.
    - Element 2: Number of counters that player 2 has in hand.
    - Element 3: The active player (1 for player 1, 2 for player 2).
    i (integer): The index of the point to remove the opponent's counter from (0-23).
    Raises:
    RuntimeError: If point i is not occupied by a counter of the opposing player.
    """
 
    board = g[0]
    active_player = g[3]

    # Check to see if point i is unoccupied
    if board[i] == 0:
        raise RuntimeError("Invalid removal: Point {} is unoccupied.".format(i))

    # Check to see if point i is occupied by the opponent's counter
    if board[i] == active_player:
        raise RuntimeError("Invalid removal: Point {} is occupied by the current player's counter.".format(i))

    # Remove the opponent's counter at point i
    board[i] = 0

class InputError(Exception):
    pass

def turn(g):
    """
    Simulates a turn in the Nine Men's Morris game.

    Parameters:
    - g (list): The game state containing the board, unplaced counters for each player, and the active player.

    Actions:
    1. Checks if the current player is unable to move or has lost the game.
       Returns False without modifying `g` if the game is over.

    2. If the current player has counters in hand:
       - Asks the player for a location to place a counter.
       - Updates `g` to place the counter.
       - Re-prompts if the location is invalid.

    3. If the current player has no counters in hand:
       - Asks the player for the location of a counter to move.
       - Asks the player for a location to move the counter to.
       - Updates `g` to move the counter.
       - Re-prompts if the locations are invalid.

    4. If a mill is formed:
       - Asks the player for the location of an opposing counter to remove.
       - Updates `g` to remove the counter.
       - Re-prompts if the location is invalid.

    5. Updates `g` to switch the current player.

    Returns:
    bool: True if the game is not over, False if the game has ended.
    """
    p1_counters = g[1]
    p2_counters = g[2]
    active_player = g[3]

    # Display the current state of the board
    draw_board(g)

    # Check if the current player can move
    if not player_can_move(g):
        # If no valid moves, end the game
        return False
    # Check if the player has only two counters left on the board and in hand
    if g[0].count(active_player) + g[active_player] == 2:
        return False

    # Check if the current player has counters in hand
    if (active_player == 1 and p1_counters > 0) or (active_player == 2 and p2_counters > 0):
        while True:
            try:
                # Ask the player for a location to place a counter
                location_str = request_location("Player {} - Enter a position to place a counter: ".format(active_player))
                location = int(location_str)  
                place_counter(g, location)
                break
            except ValueError:
                print("Invalid input: Please enter a valid integer.")
            except RuntimeError as e:
                print(e)

        # Check if the move formed a mill
        mill_result = is_in_mill(g, location)
        if mill_result:
            draw_board(g)  # Draw the board after forming a mill
            print(f"You have formed a mill at {location}!")

            # Ask the player for the location of an opposing counter to remove
            while True:
                try:
                    remove_location = request_location("Player {} - Enter the position of an opposing counter to remove: ".format(active_player))
                    if g[0][remove_location] == 3 - active_player:
                        remove_opponent_counter(g, remove_location)
                        break
                    else:
                        print("Invalid removal: Selected position does not contain the opponent's counter.")
                except (ValueError, RuntimeError) as e:
                    print(e)

    else:
        while True:
            try:
                # Ask the player for the location of a counter to move
                from_location = request_location("Player {} - Enter the current position of the counter to move: ".format(active_player))
                to_location = request_location("Player {} - Enter the new position to move the counter to: ".format(active_player))
                move_counter(g, from_location, to_location)
                break
            except ValueError:
                print("Invalid input: Please enter valid integers.")
            except RuntimeError as e:
                print(e)

        # Check if the move formed a mill
        mill_result = is_in_mill(g, to_location)
        if mill_result:
            draw_board(g)  # Draw the board after forming a mill
            print(f"Mill detected after moving counter to {to_location}")

            # Ask the player for the location of an opposing counter to remove
            while True:
                try:
                    remove_location = request_location("Player {} - Enter the position of an opposing counter to remove: ".format(active_player))
                    if g[0][remove_location] == 3 - active_player:
                        remove_opponent_counter(g, remove_location)
                        break
                    else:
                        print("Invalid removal: Selected position does not contain the opponent's counter.")
                except (ValueError, RuntimeError) as e:
                    print(e)

    # Switch the current player
    g[3] = 3 - active_player

    return True



def save_state(g, filename):
    """
    Save the game state g to a text file.

    Args:
    g (list): The game state.
          - Element 0: The board with 24 points.
          - Element 1: Number of counters that player 1 has in hand.
          - Element 2: Number of counters that player 2 has in hand.
          - Element 3: The active player (1 for player 1, 2 for player 2).
    filename (str): The name of the text file to save the game state.

    Raises:
    RuntimeError: If the file cannot be saved.
    """
    try:
        with open(filename, 'w') as file:
            # Write the board state to the first line
            file.write(','.join(map(str, g[0])) + '\n')

            # Write the number of counters for player 1 to the second line
            file.write(str(g[1]) + '\n')

            # Write the number of counters for player 2 to the third line
            file.write(str(g[2]) + '\n')

            # Write the active player to the fourth line
            file.write(str(g[3]))
    except Exception as e:
        raise RuntimeError(f"Error saving the game state to {filename}: {e}")

def load_state(filename):
    """
    Load a game state from a text file.

    Args:
    filename (str): The name of the text file containing the game state.

    Returns:
    list: The loaded game state.
          - Element 0: The board with 24 points.
          - Element 1: Number of counters that player 1 has in hand.
          - Element 2: Number of counters that player 2 has in hand.
          - Element 3: The active player (1 for player 1, 2 for player 2).

    Raises:
    RuntimeError: If the file cannot be loaded or if the format is incorrect.
    """
    try:
        with open(filename, 'r') as file:
            # Read the board state from the first line
            board_line = file.readline().strip().split(',')
            board = [int(x) for x in board_line]

            # Read the number of counters for player 1 from the second line
            p1_counters = int(file.readline().strip())

            # Read the number of counters for player 2 from the third line
            p2_counters = int(file.readline().strip())

            # Read the active player from the fourth line
            active_player = int(file.readline().strip())

        return [board, p1_counters, p2_counters, active_player]
    except Exception as e:
        raise RuntimeError(f"Error loading the game state from {filename}: {e}")


def play_game():
    """
    Simulate an entire game by repeatedly calling turn(g).
    Display a congratulatory message for the winner at the end.
    """
    # Create a new game state
    g = new_game()

    # Continue playing the game until it's over
    while turn(g):
        pass  # Continue playing

    # Display a congratulatory message for the winner
    winner = 3 - g[3]  # Switch between player 1 (1) and player 2 (2)
    print(f"Congratulations, Player {winner}! You are the winner!")

    
def main():
    # You could add some tests to main()
    # to check your functions are working as expected

    # The main function will not be assessed. All code to
    # play the game should be in the play_game() function,
    # and so your main function should simply call this.
    # Test Case 1: Counter at point i is not in a mill


    play_game()
    
main() 
