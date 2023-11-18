import numpy as np 
def calculate_grundy_values(m, n):
    """ Calculate Grundy values for an m x n Chomp board excluding the poison square. """
    # Initialize a 2D array to store Grundy values, filled with -1 (unknown)
    grundy_values = [[-1 for _ in range(n + 1)] for _ in range(m + 1)]

    def calculate(m, n):
        """ Recursive function to calculate Grundy value for a position (m, n). """
        if m == 0 or n == 0:  # Base case: empty board
            return 0
        if grundy_values[m][n] != -1:  # Already calculated
            return grundy_values[m][n]

        mex = set()  # Set to store all reachable Grundy values
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Calculate the Grundy value for all positions that can be reached from (m, n)
                if not (i == m and j == n):  # Exclude the poison square
                    mex.add(calculate(min(i, m - i), min(j, n - j)))

        # Find the smallest non-negative integer not in the set (Minimum Excludant)
        grundy = 0
        while grundy in mex:
            grundy += 1

        grundy_values[m][n] = grundy
        return grundy

    # Calculate Grundy values for all positions
    calculate(m, n)
    return grundy_values

def select_move(grundy_values, m, n):
    """ Select the optimal move for the CPU based on the Grundy values. """
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if not (i == m and j == n):  # Avoid the poison square
                # Check if the move leads to a position with a Grundy value of 0
                if grundy_values[min(i, m - i)][min(j, n - j)] == 0:
                    return i, j
    return None  # No winning move found

def play_chomp(m, n):
    """ Simulate a game of Chomp. """
    grundy_values = calculate_grundy_values(m, n)
    board_grundy = grundy_values[m][n]

    print(f"Initial board Grundy value: {board_grundy}")
    player_turn = True

    while board_grundy != 0:
        if player_turn:
            # Player's move (can be replaced with input from a real player)
            move_row, move_col = np.random.randint(1, m + 1), np.random.randint(1, n + 1)
            print(f"Player chomps at: ({move_row}, {move_col})")
        else:
            # CPU's move
            move = select_move(grundy_values, m, n)
            if move:
                move_row, move_col = move
                print(f"CPU chomps at: ({move_row}, {move_col})")
            else:
                print("No winning move for CPU.")
                break

        # Update the board size and its Grundy value
        m, n = min(move_row, m - move_row), min(move_col, n - move_col)
        board_grundy = grundy_values[m][n]
        print(f"New board size: {m} x {n}, Grundy value: {board_grundy}")

        # Switch turns
        player_turn = not player_turn

    # Determine the winner
    if player_turn:
        print("CPU wins!")
    else:
        print("Player wins!")

if __name__ == "__main__":
    play_chomp(4, 7)
