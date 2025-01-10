import sys
sys.path.insert(0, "../")
from piece import piece

class knight(piece):

    def __init__(self, is_white, size):
        super().__init__(is_white, size)
        self.value = 3
        self.slice = 3

    def calc_moves(self):
        x = self.x
        y = self.y
        moves = [(x+2, y+1), (x-2, y+1), (x+2, y-1), (x-2, y-1), (x+1, y+2), (x-1, y+2), (x+1, y-2), (x-1, y-2)]
        self.moves = []
        for move in moves:
            if self.is_on_board(move):
                self.moves.append(move)
        self.powers = self.moves.copy()

    def legal_moves(self, squares):
        moves = self.moves
        legal_moves = []
        for move in moves:
            piece = squares[move[0]][move[1]].piece
            if piece:
                if piece.is_white != self.is_white:
                    legal_moves.append(move)
            else:
                legal_moves.append(move)
        return legal_moves   