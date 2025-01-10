import pygame

sprite_sheet = None
def get_sprite_sheet(sheet):
    global sprite_sheet
    sprite_sheet = sheet
    print(sprite_sheet)

def piece_surf(is_white, slice, size):
    global sprite_sheet
    sprite_sheet = pygame.transform.scale(sprite_sheet, (6*size, 2*size))
    return sprite_sheet.subsurface(slice*size, int(is_white == False)*size, size, size)



class piece:

    def __init__(self, is_white, size):
        self.is_white = is_white
        self.name = type(self).__name__
        self.num_moves = 0
        self.size = size/1.2
        self.pos = None

    def assign_pos(self, x, y, rect, move_increment):
        self.rect = piece_surf(self.is_white, self.slice, self.size).get_rect(center = rect.center)
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.num_moves += move_increment
        self.calc_moves()

    def is_on_board(self, point):
        if point[0] >= 0 and point[0] <= 7 and point[1] >= 0 and point[1] <= 7:
            return True
        return False
    
    def blit(self, screen, rect_center=None, transparent=True):
        surf = piece_surf(self.is_white, self.slice, self.size)
        if rect_center:
            if transparent:
                surf.set_alpha(50)
            rect = surf.get_rect(center=rect_center)
        else:
            rect = self.rect
        screen.blit(surf, rect)
    
    def set_player_piece(self, is_player_white):
        self.is_player_piece = self.is_white == is_player_white
        if self.name == 'pawn' and self.pos:
            self.calc_moves()