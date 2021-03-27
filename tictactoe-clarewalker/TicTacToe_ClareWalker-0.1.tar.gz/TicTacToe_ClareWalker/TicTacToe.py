class Game:

    def __init__(self):
        """ Class for creating an interactive game of
        tic-tac-toe.

		Attributes:
			grid (2D list) representing entries 'X', 'O' or ' ' on board
            win (bool) representing whether the game is won yet
            winner (str) representing winning symbol, either 'X' or 'O'
		    """

        self.grid = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.win = False
        self.winner = None

    def print_grid(self):
        grid = self.grid

        row_1 = f' {grid[0][0]} | {grid[0][1]} | {grid[0][2]} \n---|---|---\n'
        row_2 = f'{grid[1][0]} | {grid[1][1]} | {grid[1][2]} \n---|---|---\n'
        row_3 = f'{grid[2][0]} | {grid[2][1]} | {grid[2][2]} '

        print(row_1, row_2, row_3)

    def reset_grid(self):
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                self.grid[i][j] = ' '


    def set_point(self, x, y, entry):
        self.grid[x][y] = entry


    def check_win(self):
        win = False
        winner = None
        grid = self.grid
        for i in [0, 1, 2]:
            # check rows for winner
            if (grid[i][0] == grid[i][1] == grid[i][2]) & (grid[i][0] != ' '):
                win = True
                winner = grid[i][0]
                break
            # check columns
            if (grid[0][i] == grid[1][i] == grid[2][0]) & (grid[0][i] != ' '):
                win = True
                winner = grid[0][i]
                break

        if not win:
            # check diagonals
            if (grid[0][0] == grid[1][1] == grid[2][2]) & (grid[0][0] != ' '):
                win = True
                winner = grid[0][0]

            if (grid[2][0] == grid[1][1] == grid[0][2]) & (grid[2][0] != ' '):
                win = True
                winner = grid[2][0]

        self.win = win
        self.winner = winner

    def play(self):
        turn = 0
        while self.win == False:
            if (turn % 2) == 0: symbol = 'X'
            if (turn % 2) == 1: symbol = 'O'

            coord = input(f'Player {symbol} enter cell co-ordinates as x y: \n')
            #if coord == 'exit': break

            assert (len(coord.split(' ')) == 2), 'Invalid input!'
            x, y = coord.split(' ')
            x = int(x)
            y = int(y)
            assert (x in [0, 1, 2]), 'X value should be 0, 1 or 2'
            assert (y in [0, 1, 2]), 'Y value should be 0, 1 or 2'
            assert (self.grid[x][y] == ' '), 'That cell is not empty'

            self.set_point(x, y, symbol)
            self.print_grid()
            self.check_win()

            turn += 1


        print(f'Congratulations! {self.winner} won the game.')
