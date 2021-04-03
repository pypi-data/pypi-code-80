from copy import deepcopy
from functools import reduce
from .board_searcher import BoardSearcher
from .board_initializer import BoardInitializer
from prettytable import PrettyTable, NONE
from colorama import Fore, Back, Style


class Board:

	def __init__(self):
		self.player_turn = 1
		self.width = 4
		self.height = 8
		self.position_count = self.width * self.height
		self.rows_per_user_with_pieces = 3
		self.position_layout = {}
		self.piece_requiring_further_capture_moves = None
		self.previous_move_was_capture = False
		self.searcher = BoardSearcher()
		BoardInitializer(self).initialize()

	def count_movable_player_pieces(self, player_number = 1):
		return reduce((lambda count, piece: count + (1 if piece.is_movable() else 0)), self.searcher.get_pieces_by_player(player_number), 0)

	def get_possible_moves(self):
		capture_moves = self.get_possible_capture_moves()

		return capture_moves if capture_moves else self.get_possible_positional_moves()

	def get_possible_capture_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves()), self.searcher.get_pieces_in_play(), [])

	def get_possible_positional_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()), self.searcher.get_pieces_in_play(), [])

	def position_is_open(self, position):
		return not self.searcher.get_piece_by_position(position)

	def create_new_board_from_move(self, move):
		new_board = deepcopy(self)

		if move in self.get_possible_capture_moves():
			new_board.perform_capture_move(move)
		else:
			new_board.perform_positional_move(move)

		return new_board

	def perform_capture_move(self, move):
		self.previous_move_was_capture = True
		piece = self.searcher.get_piece_by_position(move[0])
		originally_was_king = piece.king
		enemy_piece = piece.capture_move_enemies[move[1]]
		enemy_piece.capture()
		self.move_piece(move)
		further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves() if move[1] == capture_move[0]]

		if further_capture_moves_for_piece and (originally_was_king == piece.king):
			self.piece_requiring_further_capture_moves = self.searcher.get_piece_by_position(move[1])
		else:
			self.piece_requiring_further_capture_moves = None
			self.switch_turn()

	def perform_positional_move(self, move):
		self.previous_move_was_capture = False
		self.move_piece(move)
		self.switch_turn()

	def switch_turn(self):
		self.player_turn = 1 if self.player_turn == 2 else 2

	def move_piece(self, move):
		self.searcher.get_piece_by_position(move[0]).move(move[1])
		self.pieces = sorted(self.pieces, key = lambda piece: piece.position if piece.position else 0)

	def is_valid_row_and_column(self, row, column):
		if row < 0 or row >= self.height:
			return False

		if column < 0 or column >= self.width:
			return False

		return True

	def __setattr__(self, name, value):
		super(Board, self).__setattr__(name, value)

		if name == 'pieces':
			[piece.reset_for_new_board() for piece in self.pieces]

			self.searcher.build(self)

	def __str__(self):
		x = PrettyTable()
		x.field_names = [" ", "a", "b", "c", "d", "e", "f", "g", "h"]
		greensq = Back.GREEN + "   " + Back.RESET
		whitesq = Back.WHITE + "   " + Back.RESET
		blackpc = Back.BLACK + "   " + Back.RESET
		redpc = Back.RED + "   " + Back.RESET
		blackkg = Back.BLACK + Fore.YELLOW + " K " + Back.RESET + Fore.RESET
		redkg = Back.RED + Fore.BLACK + " K " + Back.RESET + Fore.RESET
		brd = ["_"] * 64
		for i in range(64):
			if (i // 8) % 2 == 0:
				brd[i] = whitesq if i % 2 == 0 else greensq
			else:
				brd[i] = greensq if i % 2 == 0 else whitesq

		for player in self.searcher.player_positions.items():
			for piece in player[1]:
				if self.searcher.get_piece_by_position(piece).king:
					brd[(piece - 1) * 2 + 1 - (((piece - 1) * 2) // 8) % 2] = blackkg if player[0] == 1 else redkg
				else:
					brd[(piece - 1) * 2 + 1 - (((piece - 1) * 2) // 8) % 2] = redpc if player[0] == 1 else blackpc

		for k in range(0, 57, 8):
			x.add_row([str(k // 8 + 1)] + brd[k:k+8])
		x.padding_width = 0
		x.vrules = NONE
		return x.get_string()
