import pygame, time

aplyr = 1
turn = 0
game = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
state=True
winner=False
circle = pygame.image.load("rond.png")
cross = pygame.image.load("cross.png")

poscrlc={(0,0):(144, 144), (0, 1):(440, 144),(0,2):(750,144) ,(1, 0):(144, 450), (1, 1):(440, 450), (1, 2):(750, 450), (2,0):(144, 750), (2,1):(440, 750), (2,2):(750, 750)}


def check_player(aplyr, turn):
    p1 = 1
    p2 = 2
    if turn == 9:
        return [10, 10]
    else:
        if turn % 2 == 0:
            turn += 1
            return p1, turn
        else:
            turn += 1
            return p2, turn


def convert_tab(pos):
    line = pos[0] // 300
    row = pos[1] // 300
    return row, line

def linear_check_win(game, player):
    idx = 0
    pelt = 0
    for line in game:
        for eline in line:
            if eline == player:
                for i in range(len(line)):
                    if line[i] == player:
                        pelt = pelt + 1
                if pelt == 3:
                    return True, [(idx, 0), (idx, 1), (idx, 2)]
        idx = idx + 1
        pelt = 0
    return False, (-float('inf'))

def col_check_win(game, player):
    col = 0
    line = 0
    while col < 3:
        if game[line][col] == player:
            if game[line + 1][col] == player and game[line + 2][col] == player:
                return True, [(0,col),(1,col),(2,col)]
        col = col + 1
    return False, (-float('inf'))


def diag_to_right_check_win(game, player):
    col = 0
    line = 0
    if game[line][col] == player:
        if game[line + 1][col + 1] == player and game[line + 2][col + 2] == player:
            return True, [(0,0),(1,1), (2,2)]
    return False, (-float('inf'))


def diag_to_left_check_win(game, player):
    col = 0
    line = 2
    if game[line][col] == player:
        if game[line - 1][col + 1] == player and game[line - 2][col + 2] == player:
            return True, [(2, 0), (1, 1), (0, 2)]
    return False, (-float('inf'))


def modify_game(game, pchoice, player):
    row = pchoice[0]
    line = pchoice[1]
    if game[row][line] != 0:
        return game
    game[row][line] = player
    return game


def cheat(game, pchoice, player):
    row = pchoice[0]
    line = pchoice[1]
    if game[row][line] != 0:
        return False
    else:
        return True


def win_checker(game, player):
    if linear_check_win(game, player)[0]==True:
        return True, linear_check_win(game, player)[1]
    elif col_check_win(game, player)[0]==True:
        return True, col_check_win(game, player)[1]
    elif diag_to_right_check_win(game, player)[0]==True:
        return True, diag_to_right_check_win(game, player)[1]
    elif diag_to_left_check_win(game, player)[0]==True:
        return True, diag_to_left_check_win(game, player)[1]
    else:
        return False, -float('inf')



def graphic_change(game, indx, player, circle, cross):
    dic = {(0, 0): (47, 45), (0, 1): (343, 45), (0, 2): (647, 45), (1, 0): (47, 349), (1, 1): (335, 349),
           (1, 2): (647, 349), (2,0):(47,650), (2,1):(343,650), (2,2):(647,650)}
    if player==1:
        screen.blit(cross, dic[indx])
    else:
        screen.blit(circle, dic[indx])

def see_win(poscrlc, win_locat):
   # print(win_locat)
    for cord in win_locat:
      #  print('CERCLE')
       # print(cord, win_locat)
        pygame.draw.circle(screen, (0,255,0), poscrlc[cord], 125, 8)

pygame.init()
screen = pygame.display.set_mode([900, 900])
white = [241, 233, 218]
red = [255, 106, 126]
blue = [91, 132, 208]
screen.fill(blue)
pygame.display.set_caption("Jeu du morpion")
pygame.display.flip()

running = True
while running:
    pygame.draw.line(screen, (255, 255, 255), (290, 0), (290, 900), 10)
    pygame.draw.line(screen, (255, 255, 255), (590, 0), (590, 900), 10)
    pygame.draw.line(screen, (255, 255, 255), (0, 600), (900, 600), 10)
    pygame.draw.line(screen, (255, 255, 255), (0, 300), (900, 300), 10)
    pygame.display.flip()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
            pygame.quit()
        if winner==True:
            time.sleep(2)
            screen.fill(blue)
            aplyr = 1
            turn = 0
            game = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            state=True
            winner=False
        if i.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                if state==True:
                    dat = check_player(aplyr, turn)
                    state=False
                turn = dat[1]
                player = dat[0]
                pos = pygame.mouse.get_pos()
                indx = convert_tab(pos)
                if cheat(game, indx, player):
                    game = modify_game(game, indx, player)
                    graphic_change(game, indx, player, circle, cross)
                    state=True
                    if win_checker(game, player)[0]==True:
                        win_locat=win_checker(game, player)[1]
                        print(win_locat)
                        print('Gagnant')
                        see_win(poscrlc, win_locat)
                        winner=True
                if turn==9 and winner==False:
                    print('Pas de gagnant')
                    winner=True
                print(game)
