import pygame
from pygame_menu import Menu, themes
from time import sleep
from random import *

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
IMG_DIR = './images/'

digits = [pygame.image.load(f'{IMG_DIR}digit_{digit}.png') for digit in range(10)]
mine_digits = [pygame.image.load(f'{IMG_DIR}tile_{mine_digit}.png') for mine_digit in range(9)]
flag, mine_clicked, empty_tile = [pygame.image.load(f'{IMG_DIR}tile{tile_type}.png') for tile_type in ['_flag', '_mine', '']]
face_lose, face_playing, face_win = [pygame.image.load(f'{IMG_DIR}face{face_type}.png') for face_type in ['_lose', '_playing', '_win']]
digit_panel = pygame.image.load(f'{IMG_DIR}digit_panel.png')
minus = pygame.image.load(f'{IMG_DIR}minus.png')
mineUnclick = pygame.image.load(f'{IMG_DIR}mine.png')

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Minesweeper')
clock = pygame.time.Clock()

mapSize = [
    [(9, 9), 10],
    [(16, 16), 40],
    [(16, 30), 99]
]

class Minesweeper:
    def __init__(self, level: str) -> None:
        if level not in ['easy', 'medium', 'hard']:
            raise ValueError('`level` must be one of these: easy, medium, hard')
        
        self.level = ('small', *mapSize[0]) if level == 'easy' else (('medium', *mapSize[1]) if level == 'medium' else ('large', *mapSize[2]))
        self.background_img = pygame.image.load(f'{IMG_DIR}background_{self.level[0]}.png')
        self.x_coor = (SCREEN_WIDTH - self.background_img.get_width()) // 2
        self.y_coor = (SCREEN_HEIGHT - self.background_img.get_height()) // 2
        self.digits = digits
        self.mine_digits = mine_digits
        self.flag = flag
        self.mine_click = mine_clicked
        self.mine = mineUnclick
        self.empty = empty_tile
        self.lose = pygame.transform.scale(face_lose, (37, 37))
        self.playing = pygame.transform.scale(face_playing, (37, 37))
        self.win = pygame.transform.scale(face_win, (37, 37))
        self.digit_panel = digit_panel
        self.board = None
        self.ListTitle = [[self.empty] * self.level[1][1] for _ in range(self.level[1][0])]
        self.randomBoard()
    
    def randomBoard(self):
        self.board = [['0'] * self.level[1][1] for _ in range(self.level[1][0])]
        for _ in range(self.level[2]):
            x_coor, y_coor = randint(0, self.level[1][0] - 1), randint(0, self.level[1][1] - 1)
            while self.board[x_coor][y_coor] != '0':
                x_coor, y_coor = randint(0, self.level[1][0] - 1), randint(0, self.level[1][1] - 1)
            
            self.board[x_coor][y_coor] = 'X'
        
        for i in range(self.level[1][0]):
            for j in range(self.level[1][1]):
                if self.board[i][j] == 'X':
                    if i - 1 >= 0 and j - 1 >= 0 and self.board[i - 1][j - 1] != 'X':
                        self.board[i - 1][j - 1] = str(int(self.board[i - 1][j - 1]) + 1)
                    
                    if i - 1 >= 0 and self.board[i - 1][j] != 'X':
                        self.board[i - 1][j] = str(int(self.board[i - 1][j]) + 1)
                    
                    if i - 1 >= 0 and j + 1 < self.level[1][1] and self.board[i - 1][j + 1] != 'X':
                        self.board[i - 1][j + 1] = str(int(self.board[i - 1][j + 1]) + 1)
                    
                    if j + 1 < self.level[1][1] and self.board[i][j + 1] != 'X':
                        self.board[i][j + 1] = str(int(self.board[i][j + 1]) + 1)
                    
                    if i + 1 < self.level[1][0] and j + 1 < self.level[1][1] and self.board[i + 1][j + 1] != 'X':
                        self.board[i + 1][j + 1] = str(int(self.board[i + 1][j + 1]) + 1)
                    
                    if i + 1 < self.level[1][0] and self.board[i + 1][j] != 'X':
                        self.board[i + 1][j] = str(int(self.board[i + 1][j]) + 1)
                    
                    if i + 1 < self.level[1][0] and j - 1 >= 0 and self.board[i + 1][j - 1] != 'X':
                        self.board[i + 1][j - 1] = str(int(self.board[i + 1][j - 1]) + 1)
                    
                    if j - 1 >= 0 and self.board[i][j - 1] != 'X':
                        self.board[i][j - 1] = str(int(self.board[i][j - 1]) + 1)

    
    def printDigitPanel(self, nums: int, panel_x: int, panel_y: int) -> None:
        if nums < -99 or nums > 999:
            raise ValueError("`nums` must be in between -99 and 999")
        
        screen.blit(digit_panel, (panel_x, panel_y))
        time_digit = list(str(nums))
        time_digit = [0] * (3 - len(time_digit)) + time_digit
        x_coor, y_coor = 1, 2
        for idx in range(len(time_digit)):
            getDigit = digits[int(time_digit[idx])] if time_digit[idx] != '-' else minus
            screen.blit(getDigit, (panel_x + x_coor, panel_y + y_coor))
            x_coor += 22
    
    def printBoard(self, secs: int, numBomb: int, faceSurface = None):
        screen.blit(self.background_img, (self.x_coor, self.y_coor))
        self.printDigitPanel(numBomb, self.x_coor + 17, self.y_coor + 21)
        if faceSurface is None:
            faceSurface = self.playing

        screen.blit(faceSurface, (self.x_coor + (self.background_img.get_width() - self.playing.get_width()) // 2, self.y_coor + 21))
        self.printDigitPanel(secs, self.x_coor + self.background_img.get_width() - self.digit_panel.get_width() - 18, self.y_coor + 21)
        self.drawListTitle()
    
    def drawListTitle(self):
        y_coor = 81
        for i in range(self.level[1][0]):
            x_coor = 15
            for j in range(self.level[1][1]):
                screen.blit(self.ListTitle[i][j], (self.x_coor + x_coor, self.y_coor + y_coor))
                x_coor += self.empty.get_width()
            
            y_coor += self.empty.get_height()
    
    def checkWin(self):
        countBomb = 0
        for i in range(self.level[1][0]):
            for j in range(self.level[1][1]):
                if self.ListTitle[i][j] in [self.empty, self.flag] and self.board[i][j] != 'X':
                    return False
                
                if self.ListTitle[i][j] in [self.empty, self.flag] and self.board[i][j] == 'X':
                    countBomb += 1

        return countBomb == self.level[2]

    def play(self):
        visited = [[False] * self.level[1][1] for _ in range(self.level[1][0])]
        def clickCell(x: int, y: int):
            if visited[x][y] == True:
                return
            
            visited[x][y] = True
            self.ListTitle[x][y] = mine_digits[int(self.board[x][y])] if self.board[x][y] != 'X' else self.ListTitle[x][y]
            if self.board[x][y] != '0':
                return
            
            if x - 1 >= 0 and y - 1 >= 0:
                clickCell(x - 1, y - 1)
            
            if x - 1 >= 0:
                clickCell(x - 1, y)
            
            if x - 1 >= 0 and y + 1 < self.level[1][1]:
                clickCell(x - 1, y + 1)
            
            if y + 1 < self.level[1][1]:
                clickCell(x, y + 1)
            
            if x + 1 < self.level[1][0] and y + 1 < self.level[1][1]:
                clickCell(x + 1, y + 1)
            
            if x + 1 < self.level[1][0]:
                clickCell(x + 1, y)
            
            if x + 1 < self.level[1][0] and y - 1 >= 0:
                clickCell(x + 1, y - 1)
            
            if y - 1 >= 0:
                clickCell(x, y - 1)
        
        sec, numBomb = 0, self.level[2]

        running = True
        stillPlay = True
        faces = None

        pygame.mixer.Sound('./Minesweeper.mp3').play(-1, 0, 0)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                else:
                    screen.fill((246, 246, 246))
                    if self.checkWin():
                        for i in range(self.level[1][0]):
                            for j in range(self.level[1][1]):
                                if self.ListTitle[i][j] in [self.empty, self.flag] and self.board[i][j] == 'X':
                                    self.ListTitle[i][j] = self.flag
                        
                        stillPlay = False
                        faces = self.win

                    self.printBoard(sec, numBomb, faces)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            coor = event.pos
                            col_idx, row_idx = (coor[0] - self.x_coor - 15) // 20, (coor[1] - self.y_coor - 81) // 20
                            if (col_idx >= 0 and col_idx < self.level[1][1]) and (row_idx >= 0 and row_idx < self.level[1][0]) and stillPlay == True:
                                if self.board[row_idx][col_idx] == 'X':
                                    self.ListTitle[row_idx][col_idx] = self.mine_click
                                    for i in range(self.level[1][0]):
                                        for j in range(self.level[1][1]):
                                            if self.board[i][j] == 'X' and not (i == row_idx and j == col_idx):
                                                self.ListTitle[i][j] = self.mine
                                    
                                    faces = self.lose
                                    stillPlay = False


                                else:
                                    clickCell(row_idx, col_idx)
                                    self.printBoard(sec, numBomb, faces)
                            
                            else:
                                if coor[0] - (self.x_coor + (self.background_img.get_width() - self.playing.get_width()) // 2) in range(0, 38) and coor[1] - (self.y_coor + 21) in range(0, 38):
                                    sec = 0
                                    numBomb = self.level[2]
                                    faces = None
                                    self.ListTitle = [[self.empty] * self.level[1][1] for _ in range(self.level[1][0])]
                                    self.randomBoard()
                                    stillPlay = True
                                    visited = [[False] * self.level[1][1] for _ in range(self.level[1][0])]

                        elif event.button == 3:
                            coor = event.pos
                            col_idx, row_idx = (coor[0] - self.x_coor - 15) // 20, (coor[1] - self.y_coor - 81) // 20
                            if (col_idx >= 0 and col_idx < self.level[1][1]) and (row_idx >= 0 and row_idx < self.level[1][0]) and stillPlay == True:
                                if self.ListTitle[row_idx][col_idx] == self.empty:
                                    self.ListTitle[row_idx][col_idx] = self.flag
                                    numBomb -= 1
                                
                                elif self.ListTitle[row_idx][col_idx] == self.flag:
                                    self.ListTitle[row_idx][col_idx] = self.empty
                                    numBomb += 1

            if not running:
                break

            pygame.display.flip()
            clock.tick(60)
            if stillPlay:
                sec += 1
                sleep(1)

        pygame.quit()

mine = Minesweeper('easy')

def set_difficulty(value, difficulty):
    global mine
    mine = Minesweeper(difficulty)

def start_the_game():
    mine.play()

def main():
    difficulty = [
        ('Easy', 'easy'),
        ('Medium', 'medium'),
        ('Hard', 'hard')
    ]
    settings = Menu(
        "Welcome to Minesweeper",
        width = SCREEN_WIDTH,
        height = SCREEN_HEIGHT,
        theme = themes.THEME_GREEN
    )
    settings.add.dropselect("Difficulty", difficulty, onchange=set_difficulty, margin=(0, 20))
    settings.add.button('Play', start_the_game, background_color = (253, 250, 114), font_color = (0, 0, 0))
    settings.mainloop(screen)

if __name__ == '__main__':
    main()