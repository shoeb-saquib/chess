import sys
sys.path.insert(0, "../")
from piece import piece

class pawn(piece):

    def __init__(self, is_white, size):
        super().__init__(is_white, size)
        self.value = 1
        self.slice = 5
        self.en_passant = False
        self.double_move_turn = None

    def calc_moves(self):
        if self.is_player_piece: 
            forward = 1 
        else: 
            forward = -1
        x = self.x
        y = self.y
        moves = []
        for i in range(-1, 2):
            move = (x+i, y+forward)
            if self.is_on_board(move):
                moves.append(move)
        double_forward = (x, y+forward*2)
        has_not_moved = self.num_moves == 0
        if has_not_moved and self.is_on_board(double_forward):
            moves.append(double_forward)
        self.moves = moves
    
    def legal_moves(self, squares):
        moves = self.moves
        legal_moves = []
        powers = []
        forward = True
        for move in moves:
            if move[0] == self.x:
                attack = False
            else:
                attack = True
                powers.append(move)
            piece = squares[move[0]][move[1]].piece
            if piece:
                is_enemy = piece.is_white != self.is_white
                if attack and is_enemy:
                    legal_moves.append(move)
                if attack == False:
                    forward = False
            else:
                en_passant_piece = squares[move[0]][self.y].piece
                if attack and en_passant_piece:
                    if en_passant_piece.name == 'pawn' and en_passant_piece.en_passant:
                        legal_moves.append(move)
                if attack == False and forward:
                    legal_moves.append(move)
        self.powers = powers
        return legal_moves