import sys
sys.path.insert(0, "../")
from piece import piece

class rook(piece):

    def __init__(self, is_white, size):
        super().__init__(is_white, size)
        self.value = 5
        self.slice = 4

    def calc_moves(self):
        x = self.x
        y = self.y
        self.moves = [[], []]
        for i in range(8):
            self.moves[0].append((i, y))
            self.moves[1].append((x, i))

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