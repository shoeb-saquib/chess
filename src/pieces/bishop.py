import sys
sys.path.insert(0, "../")
from piece import piece
from copy import deepcopy


class bishop(piece):

    def __init__(self, is_white, size):
        super().__init__(is_white, size)
        self.value = 3
        self.slice = 2

    def calc_moves(self):
        x = self.x
        y = self.y
        moves = [[], []]
        self.moves = deepcopy(moves)
        for i in range(8):
            moves[0].append((i, i+y-x))
            moves[1].append((i, -i+y+x))
        for i in range(2):
            for move in moves[i]:
                if self.is_on_board(move):
                    self.moves[i].append(move)

    def legal_moves(self, squares):
        moves = self.moves
        legal_moves = []
        self.powers = []
        for line in moves:
            for i in range(len(line)):
                if line[i] == self.pos:
                    if i==0:
                        part_lines = [line[i+1:]]
                    elif i==7:
                        part_lines = [reversed(line[:i])]
                    else:
                        part_lines = [line[i+1:], reversed(line[:i])]
            for part_line in part_lines:
                for move in part_line:
                    self.powers.append(move)
                    piece = squares[move[0]][move[1]].piece
                    if piece:
                        if piece.is_white != self.is_white:
                            legal_moves.append(move)
                        break
                    else:
                        legal_moves.append(move)
        return legal_moves