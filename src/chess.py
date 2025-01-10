import pygame
from copy import deepcopy
from sys import exit
import pickle
from pieces.king import king
from pieces.queen import queen
from pieces.rook import rook
from pieces.bishop import bishop
from pieces.knight import knight
from pieces.pawn import pawn
from piece import get_sprite_sheet


pygame.init()
screen_height = 1080
screen_base = 1620
screen = pygame.display.set_mode((screen_base, screen_height/40+screen_height))
screen.fill('black')
pygame.display.set_caption('Chess')
sprite_sheet = pygame.image.load('sprites\chess_pieces.png').convert_alpha()
get_sprite_sheet(sprite_sheet)

class square:

    def __init__(self, x, y, center_x, center_y, size, color):
        self.x = x
        self.y = y
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.size = size
        self.piece = None
        self.assign_pos(x, y)

    def assign_pos(self, x, y):
        self.x = x
        self.y = y
        center_x = self.center_x
        center_y = self.center_y
        size = self.size
        cor = (center_x-4*size+x*size, center_y+4*size-y*size)
        self.rect = pygame.Surface((size, size)).get_rect(bottomleft = cor)
        if self.piece:
            self.piece.assign_pos(self.x, self.y, self.rect, 0)

    def assign_piece(self, piece, move_increment = 0):
        self.piece = piece
        piece.assign_pos(self.x, self.y, self.rect, move_increment)

    def clear_piece(self):
        self.piece = None

    def blit(self):
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.color)
        screen.blit(surf, self.rect)
        if self.piece:
            self.piece.blit(screen)

class board:

    def __init__(self, center_x = screen_base/2, center_y = (screen_height/40+screen_height)/2, size = screen_height/8, color_white = 'white', color_black = 'dark gray'):
        squares = []
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        let_markings = []
        num_markings = []
        marking_color = color_white
        for x in range(8):
            if x % 2 == 0:
                marking_color = color_white
            else:
                marking_color = color_black
            pos = (center_x+(x-3)*size-size/15, center_y+4*size-size/120)
            let_markings.append((marking_color, letters[x], pos))
            pos = (center_x-4*size+size/15, center_y+(3-x)*size+size/15)
            num_markings.append((marking_color, str(x+1), pos))
            squares.append([])
            for y in range(8):
                if (y+x) % 2 == 0:
                    color = color_black
                else:
                    color = color_white
                squares[x].append(square(x, y, center_x, center_y, size, color))
        self.squares = squares
        self.let_markings = let_markings
        self.num_markings = num_markings
        self.size = size
        self.center_pos = (center_x, center_y)

    def set_board(self, start_white):
        squares = self.squares
        size = self.size
        pieces = [[], []]
        for i in range(2):
            is_white = i == int(start_white)
            if i == 0:
                row = 7
                pawn_row = 6
            else:
                row = 0
                pawn_row = 1
            king_piece = king(is_white, size)
            king_piece.set_player_piece(start_white)
            queen_piece = queen(is_white, size)
            pieces[i] = [king_piece, queen_piece]
            squares[4][row].assign_piece(king_piece)
            squares[3][row].assign_piece(queen_piece)
            for j in range(2):
                rook_piece = rook(is_white, size)
                bishop_piece = bishop(is_white, size)
                knight_piece = knight(is_white, size)
                pieces[i] += [rook_piece, bishop_piece, knight_piece]
                if j == 0:
                    squares[0][row].assign_piece(rook_piece)
                    squares[1][row].assign_piece(knight_piece)
                    squares[2][row].assign_piece(bishop_piece)
                else:
                    squares[7][row].assign_piece(rook_piece)
                    squares[6][row].assign_piece(knight_piece)
                    squares[5][row].assign_piece(bishop_piece)
            for j in range(8):
                pawn_piece = pawn(is_white, size)
                pawn_piece.set_player_piece(start_white)
                pieces[i] += [pawn_piece]
                squares[j][pawn_row].assign_piece(pawn_piece)
        self.pieces = pieces
        self.killed_pieces = [[], []]

    def reflect(self):
        squares = []
        for i in range(8):
            squares.append([])
            for j in range(8):
                squares[i].append(None)
        for x in range(8):
            for y in range(8):
                new_x = 7-x
                new_y = 7-y
                self.squares[x][y].assign_pos(new_x, new_y)
                squares[new_x][new_y] = self.squares[x][y]
        self.squares = squares

    def blit(self):
        background =  pygame.surface.Surface((self.size*12-self.size/5, self.size*8))
        background.fill('gray')
        screen.blit(background, background.get_rect(center=self.center_pos))
        background =  pygame.surface.Surface((self.size*8+self.size/5, self.size*8))
        background.fill('black')
        screen.blit(background, background.get_rect(center=self.center_pos))
        font = pygame.font.Font(None, int(self.size/3))
        for i in range(len(self.squares)):
            for square in self.squares[i]:
                square.blit()
            surf = font.render(self.let_markings[i][1], True, self.let_markings[i][0])
            screen.blit(surf, surf.get_rect(bottomright=self.let_markings[i][2]))
            surf = font.render(self.num_markings[i][1], True, self.num_markings[i][0])
            screen.blit(surf, surf.get_rect(topleft=self.num_markings[i][2]))
        for i in range(2):
            pawn_count = 0
            piece_count = 0
            if i == 0:
                offset = self.size*1.5
            else:
                offset = self.size/2
            for piece in self.killed_pieces[i]:
                if piece.name == 'pawn':
                    level = pawn_count
                    pawn_count += 1
                    side = -1
                else:
                    level = piece_count
                    piece_count += 1
                    side = 1
                pos = (self.center_pos[0]+side*(self.size*4+offset), self.center_pos[1]+self.size*4-self.size/2-self.size*level)
                piece.blit(screen, pos, False)

    def assign_turn(self, turn):
        self.pieces = turn.pieces
        self.squares = turn.squares
        self.killed_pieces = turn.killed_pieces


class turn():

    def __init__(self, num_turn, chess_board=None, should_reflect=False):
        self.num_turn = num_turn
        self.is_white_turn = num_turn % 2 == 0
        for piece in chess_board.pieces[self.is_white_turn]:
            if piece.name == 'pawn' and piece.en_passant:
                if num_turn > piece.double_move_turn+1:
                    piece.en_passant = False
        if chess_board.pieces[self.is_white_turn][0].is_player_piece:
            should_reflect = False
        if should_reflect and num_turn != 0:
            chess_board.reflect()
            for color_pieces in chess_board.pieces:
                for piece in color_pieces:
                    piece.set_player_piece(self.is_white_turn) 
        self.squares = deepcopy(chess_board.squares)
        self.pieces = [[None], [None]]
        for squares_x in self.squares:
            for square in squares_x:
                if square.piece:
                    if square.piece.name == 'king':
                        self.pieces[square.piece.is_white][0] = square.piece
                    else:
                        self.pieces[square.piece.is_white].append(square.piece)
        self.killed_pieces = deepcopy(chess_board.killed_pieces)
        self.true_threat_map = self.get_threat_map(chess_board.pieces, chess_board.squares, True)
        self.threat_map = self.get_threat_map(chess_board.pieces, chess_board.squares, False)
        self.check = self.is_check(self.threat_map, self.pieces[int(self.is_white_turn)][0])
        self.legal_moves = self.get_legal_moves(self.squares, self.pieces)
        
    def get_threat_map(self, pieces, squares, overlap, piece_removed=None):
        threat_map = []
        for piece in pieces[int(self.is_white_turn==False)]:
            if piece_removed and piece_removed.pos == piece.pos:
                pass
            else:
                piece.legal_moves(squares)
                if overlap:
                    threat_map.extend(piece.powers)
                else:
                    for power in piece.powers:
                        if threat_map.count(power) == 0:
                            threat_map.append(power)
        return threat_map
    
    def is_check(self, threat_map, king):
        for pos in threat_map:
            if king.pos == pos:
                return True
        return False
    
    def add_castling(self, legal_moves, castling_checks, squares):
        if castling_checks[0][0]:
            king_pos = castling_checks[0][1].pos
            for i in range(2):
                if castling_checks[1+i][0]:
                    if i == 0:
                        step = -1
                    else:
                        step = 1
                    castling = True
                    king_to = (king_pos[0]+2*step, king_pos[1])
                    check_positions = [(king_pos[0]+step, king_pos[1]), king_to]
                    king_third = (king_pos[0]+3*step, king_pos[1])
                    if castling_checks[1+i][1].pos != king_third:
                        check_positions.append(king_third)
                    for pos in check_positions:
                        if squares[pos[0]][pos[1]].piece != None:
                            castling = False
                    for threat in self.threat_map:
                        if threat == king_pos or threat == check_positions[0] or threat == king_to:
                            castling = False
                    if castling:
                        legal_moves[0][1].append(king_to)
                        self.is_empty = False
        return legal_moves

    def get_legal_moves(self, squares, pieces):
        self.is_empty = True
        legal_moves = []
        castling_checks = [[False], [False], [False]]
        for piece in pieces[int(self.is_white_turn)]:
            if piece.num_moves == 0:
                if piece.name == 'king':
                    castling_checks[0][0] = True
                    castling_checks[0].append(piece)
                if piece.name == 'rook':
                    if piece.x == 0:
                        castling_checks[1][0] = True
                        castling_checks[1].append(piece)
                    if piece.x == 7:
                        castling_checks[2][0] = True
                        castling_checks[2].append(piece)
            legal_moves.append((piece, []))
            moves = piece.legal_moves(squares)
            for move in moves:
                temp_squares = deepcopy(squares)
                temp_piece = deepcopy(piece)
                if piece.name == 'pawn' and abs(piece.x - move[0]) == 1 and temp_squares[move[0]][move[1]].piece == None:
                    piece_removed = deepcopy(temp_squares[move[0]][temp_piece.y].piece)
                    temp_squares[move[0]][temp_piece.y].clear_piece()
                else:
                    piece_removed = deepcopy(temp_squares[move[0]][move[1]].piece)
                temp_squares[temp_piece.x][temp_piece.y].clear_piece()
                temp_squares[move[0]][move[1]].assign_piece(temp_piece, 1)
                if temp_piece.name == 'king':
                    king = temp_piece
                else:
                    king = pieces[int(self.is_white_turn)][0]
                if self.is_check(self.get_threat_map(pieces, temp_squares, False, piece_removed), king) == False:
                    legal_moves[len(legal_moves)-1][1].append(move)
                    self.is_empty = False
        legal_moves = self.add_castling(legal_moves, castling_checks, squares)
        return legal_moves
        

class game:

    def __init__(self, start_white, should_reflect):
        chess_board = board()
        chess_board.set_board(start_white)
        self.chess_board = chess_board
        self.num_turn = 0
        self.should_reflect = should_reflect
        self.turn = turn(self.num_turn, chess_board, should_reflect)
        self.turns = []
        self.turns.append(deepcopy(self.turn))
        self.selected_moves = None
        self.selected_square = None
        self.should_move = False
        self.blit_moves = False
        self.blit_threat_map = False
        self.promotion_info = (False, None, None)

    def get_selected_square(self, pos):
        squares = self.chess_board.squares
        for squares_x in squares:
            for square in squares_x:
                if square.rect.collidepoint(pos):
                    return square
                
    def get_selected_moves(self, square):
        for piece_info in self.turn.legal_moves:
            piece = piece_info[0]
            if piece.pos == square.piece.pos:
                legal_moves = deepcopy(piece_info[1])
                for i in range(len(legal_moves)):
                    pos = legal_moves[i]
                    legal_moves[i] = self.chess_board.squares[pos[0]][pos[1]]
                return legal_moves

    def show_legal_moves(self, pos):
        if self.promotion_info[0] == False:
            square = self.get_selected_square(pos)
            if square and self.selected_square != square:
                if square.piece and square.piece.is_white == self.turn.is_white_turn:
                    self.selected_square = square
                    self.selected_moves = self.get_selected_moves(square)
                    self.blit_moves = True
                else:
                    self.selected_square = None
                    self.selected_moves = None
                    self.blit_moves = False

    def promotion(self):
        if self.promotion_info[0]:
            name = self.promotion_piece.name
            if name == 'queen':
                self.promotion_piece = rook(self.promotion_info[2], self.chess_board.size)
            if name == 'rook':
                self.promotion_piece = bishop(self.promotion_info[2], self.chess_board.size)
            if name == 'bishop':
                self.promotion_piece = knight(self.promotion_info[2], self.chess_board.size)
            if name == 'knight':
                self.promotion_piece = queen(self.promotion_info[2], self.chess_board.size)

    def toggle_threat_map(self):
        self.blit_threat_map = self.blit_threat_map == False

    def toggle_reflect(self):
        self.should_reflect = self.should_reflect == False

    def move(self, pos):
        selected_square = self.get_selected_square(pos)
        if self.promotion_info[0]:
            if self.promotion_info[1] == selected_square:
                self.promotion_info[1].assign_piece(self.promotion_piece)
                self.chess_board.pieces[self.promotion_info[2]].append(self.promotion_piece)
                self.promotion_info = (False, None, None)
                self.num_turn += 1
                self.turn = turn(self.num_turn, self.chess_board, self.should_reflect)
                self.turns.append(deepcopy(self.turn))
        if self.selected_moves:
            for square in self.selected_moves:
                if square == selected_square:
                    self.moving_to = square
                    self.moving_from = self.selected_square
                    self.should_move = True

    def make_move(self, moving_from, moving_to, squares):
        self.should_move = False
        self.blit_moves = False
        pieces = self.chess_board.pieces[int(self.turn.is_white_turn == False)]
        killed_pieces = self.chess_board.killed_pieces[int(self.turn.is_white_turn == False)]
        if moving_from.piece.name == 'pawn' and abs(moving_from.y - moving_to.y) == 2:
            moving_from.piece.en_passant = True
            moving_from.piece.double_move_turn = self.num_turn
        if moving_from.piece.name == 'pawn' and abs(moving_from.x - moving_to.x) == 1 and moving_to.piece == None:
            en_passant_square = squares[moving_to.x][moving_from.y]
            killed_pieces.append(en_passant_square.piece)
            pieces.remove(en_passant_square.piece)
            en_passant_square.clear_piece()
        if moving_from.piece.name == 'king' and abs(moving_from.x - moving_to.x) == 2:
            if moving_to.x > moving_from.x:
                step = -1
                rook_square = squares[7][moving_to.y]
            else:
                step = 1
                rook_square = squares[0][moving_to.y]
            squares[moving_to.x+step][moving_to.y].assign_piece(rook_square.piece)
            rook_square.clear_piece()
        if moving_from.piece.name == 'pawn' and (moving_to.y == 0 or moving_to.y == 7):
            self.promotion_info = (True, moving_to, moving_from.piece.is_white)
            self.promotion_piece = queen(self.promotion_info[2], self.chess_board.size)
            moving_from.clear_piece()
        else:
            if moving_to.piece:
                killed_pieces.append(moving_to.piece)
                pieces.remove(moving_to.piece)
            moving_to.assign_piece(moving_from.piece, 1)
            moving_from.clear_piece()
            self.num_turn += 1
            self.turn = turn(self.num_turn, self.chess_board, self.should_reflect)
            self.turns.append(self.turn)

    def blit(self):
        self.chess_board.blit()
        if self.promotion_info[0]:
            self.promotion_piece.blit(screen, self.promotion_info[1].rect.center)
        if self.blit_threat_map:
            threat_map = deepcopy(self.turn.true_threat_map)
            for i in range(len(threat_map)):
                pos = threat_map[i]
                threat_map[i] = self.chess_board.squares[pos[0]][pos[1]]
            for square in threat_map:
                surf = pygame.Surface((self.chess_board.size, self.chess_board.size))
                surf.fill('red')
                surf.set_alpha(50)
                screen.blit(surf, square.rect)
        if self.blit_moves and self.selected_moves:
            for square in self.selected_moves:
                self.selected_square.piece.blit(screen, square.rect.center)

    def undo(self):
        if self.num_turn != 0:
            self.turns.pop(self.num_turn)
            self.num_turn -= 1
            self.turn = self.turns[self.num_turn]
            self.chess_board.assign_turn(self.turn)

    def update(self):
        self.blit()
        if self.should_move:
            self.make_move(self.moving_from, self.moving_to, self.chess_board.squares)
        if self.turn.is_empty:
            if self.turn.check:
                surf = pygame.font.Font(None, int(self.chess_board.size)).render('Checkmate', True, 'blue')
            else:
                surf = pygame.font.Font(None, int(self.chess_board.size)).render('Stalemate', True, 'blue')
            screen.blit(surf, surf.get_rect(center=(self.chess_board.center_pos)))

    def save(self):
        with open('save_file.txt', 'wb') as save_file:
            pickle.dump(self, save_file)

try:
    with open('save_file.txt', 'rb') as save_file:
        main_game = pickle.load(save_file)
except:
    main_game = game(True, False)

clock = pygame.time.Clock()
is_pressed = False
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_game.save()
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                is_pressed = True
                main_game.move(event.pos)
                main_game.show_legal_moves(event.pos)
        if event.type == pygame.MOUSEMOTION and is_pressed:
            main_game.show_legal_moves(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_pressed = False
        if event.type == pygame.MOUSEWHEEL:
            main_game.promotion()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                main_game.toggle_threat_map()
            if event.key == pygame.K_SPACE:
                main_game = game(True, False)
            if event.key == pygame.K_LEFT:
                main_game.undo()
            if event.key == pygame.K_r:
                main_game.toggle_reflect()

    main_game.update()
    pygame.display.update()
    clock.tick(60)                   



    




