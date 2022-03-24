import pygame, time

aplyr = 1
turn = 0
game = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
state=True
winner=False
circle = pygame.image.load("rond.png")
cross = pygame.image.load("cross.png")


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


def player_choice(nick, game):
    col = '[' + nick + ']' + ' Indiquez la colonne: '
    rw = '\n[' + nick + ']' + ' Indiquez la ligne: '
    colomn = -1
    row = -1
    while colomn > 3 or colomn < 0:
        colomn = input(col)
        if isinstance(colomn, int):
            print('#oui')
        else:
            if colomn == '0' or colomn == '1' or colomn == '2' or colomn == '3':
                colomn = int(colomn)
            else:
                print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n[!] Donnée incorrecte')
                colomn = -1
    while row > 3 or row < 0:
        row = int(input(rw))
        if isinstance(row, int):
            variablecheck = 'oui'
        else:
            if row == '0' or row == '1' or row == '2' or row == '3':
                row = int(row)
            else:
                print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n[!] Donnée incorrecte')
                row = -1
    if game[row - 1][colomn - 1] != 0:
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n[!] Cette case a déjà été jouée !')
        print(game)
        return player_choice(nick, game)
    return row, colomn


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
                    return True
            idx = idx + 1
        pelt = 0
        idx = 0
    return False


def col_check_win(game, player):
    col = 0
    line = 0
    while col < 3:
        if game[line][col] == player:
            if game[line + 1][col] == player and game[line + 2][col] == player:
                return True
        col = col + 1
    return False


def diag_to_right_check_win(game, player):
    col = 0
    line = 0
    if game[line][col] == player:
        if game[line + 1][col + 1] == player and game[line + 2][col + 2] == player:
            return True
    return False


def diag_to_left_check_win(game, player):
    col = 0
    line = 2
    if game[line][col] == player:
        if game[line - 1][col + 1] == player and game[line - 2][col + 2] == player:
            return True
    return False


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
    if linear_check_win(game, player) or col_check_win(game, player) or diag_to_right_check_win(game,
                                                                                                player) or diag_to_left_check_win(
            game, player):
        return True
    else:
        return False


dic = {(1, 1): (335, 349)}


def graphic_change(game, indx, player, circle, cross):
    dic = {(0, 0): (47, 45), (0, 1): (343, 45), (0, 2): (647, 45), (1, 0): (47, 349), (1, 1): (335, 349),
           (1, 2): (647, 349), (2,0):(47,650), (2,1):(343,650), (2,2):(647,650)}
    if player==1:
        screen.blit(cross, dic[indx])
    else:
        screen.blit(circle, dic[indx])

def countdown(num_of_secs):
    while num_of_secs:
        m, s = divmod(num_of_secs, 60)
        min_sec_format = '{:02d}:{:02d}'.format(m, s)
        print(min_sec_format, end='/r')
        time.sleep(1)
        num_of_secs -= 1

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
        if winner==True:
            running=False
            time.sleep(5)
        if i.type == pygame.QUIT:
            running = False
            pygame.quit()
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
                    if win_checker(game, player):
                        print('Gagnant')
                        winner=True
                print(game)
                print(pos)
                print(indx)
