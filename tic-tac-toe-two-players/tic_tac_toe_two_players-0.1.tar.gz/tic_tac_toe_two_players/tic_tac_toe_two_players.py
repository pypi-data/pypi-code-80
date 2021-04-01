import sys

class Game:
	
    def __init__(self):
        """Here we initilaze the board and the win conditions"""
        self.board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.win = ((0,1,2), (3,4,5), (6,7,8), (0,4,8), (0,3,6), (1,4,7), (2,5,8), (2,4,6))
        self.moves = 0
        
    def player1(self):
        
        print("First player is X")
        numberboard_for_player1 = input("PLAYER 1: Type the number on board where you want to put X:\n")
        
        try:
        
            numberboard_for_player1 = int(numberboard_for_player1)
            if int(numberboard_for_player1) not in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                print('You enter wrong number. Please enter a number from 0 - 8.')
                self.player1()
            else:
                if self.board[numberboard_for_player1] != "X" and self.board[numberboard_for_player1] != "O":
                    self.board[numberboard_for_player1] = "X"
                    self.draw_board()
                    self.moves += 1
    
                else:
                    print("You will have to choose different place because it is already played by someone.")
                    self.player1()
                self.win_situation()
                self.check_moves()
        except ValueError:
            
                print("Enter number from 0-8")
                self.player1()
       
    def player2(self):
        print("Second player is O")
        numberboard_for_player2 = input("PLAYER 2: Type the number on board where you want to put O:\n")
        #self.check_moves()
        try:
        
            numberboard_for_player2 = int(numberboard_for_player2)
            if numberboard_for_player2 not in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                print('You enter wrong number. Please enter a number from 0 - 8.')
                self.player2()
            else:
                if self.board[numberboard_for_player2] != "O" and self.board[numberboard_for_player2] != "X":
                    self.board[numberboard_for_player2] = "O"
                    self.draw_board()
                    self.moves += 1
                    """if self.moves >= 9:
                        print('No winner')
                        self.play(playing = True)"""
                                
                else:
                    print("You will have to choose different place because it is already played by someone.")
                    self.player2()
                self.win_situation()
                self.check_moves()
        except ValueError:
            
            print("Enter number from 0-8")
            self.player2()
    def check_moves(self):
        if self.moves == 9:
            print('There is no winner')
            self.run_game(playing = True)
        
    def draw_board(self):
        
        print('____________________')
        print(self.board[6], self.board[7], self.board[8])
        print('-+-+-')
        print(self.board[3], self.board[4], self.board[5])
        print('-+-+-')
        print(self.board[0], self.board[1], self.board[2])
        print('____________________')
        
    def win_situation(self):

        for moves in self.win:
            if self.board[moves[0]] == self.board[moves[1]] == self.board[moves[2]] == "X":
                print("Player X wins the game!")
                
                self.run_game(playing = True)
            if self.board[moves[0]] == self.board[moves[1]] == self.board[moves[2]] == "O":
                print('Player O wins the game!')
                
                self.run_game(playing = True)
    
    def run_game(self, playing = False):
        
        if playing == False:
            self.draw_board()
            while True:
            
                self.player1()
            
                self.player2()
            
        if playing == True:
            
            
            
            while True:
                
                
                question = input("Want to play again? Type yes or no.\n")
                
                if question == "yes":
                    self.board = [0,1,2,3,4,5,6,7,8]
                    self.moves = 0
                    self.run_game()
                elif question == "no":
                    print("Thank you for playing. Till next time.")
                    sys.exit()
                else:
                    print("Please enter yes or no.")
                    

    


#game = Game()
#game.run_game()