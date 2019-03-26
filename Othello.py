import turtle
import random

SQUARE = 50
UPPER_BOUNDARY = 200
LEFT_BOUNDARY = -200
RIGHT_BOUNDARY = 200
LOWER_BOUNDARY = -200
ORIGIN_X = 20
ORIGIN_Y = 0
HEIGHT = 8
WIDTH = 8

game_state = []

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#### Purpose:
# 
# To draw an 8X8 Board
#
#### Signature:
#
# draw_board :: void => void

def draw_board(n):
    ''' Function: draw_board
        Parameters: n, an int for # of squares
        Returns: nothing
        Does: Draws an nxn board with a green background
    '''
    
    turtle.setup(n * SQUARE + SQUARE, n * SQUARE + SQUARE)
    turtle.screensize(n * SQUARE, n * SQUARE)
    turtle.bgcolor('white')

    # Create the turtle to draw the board
    global othello
    global screen
    othello = turtle.Turtle()
    screen = turtle.Screen()
    screen.onclick(click)
    othello.penup()
    othello.speed(.5)
    othello.hideturtle()
    # screen.onclick(print("othello.setpos"))

    # Line color is black, fill color is green
    othello.color("black", "forest green")
    
    # Move the turtle to the upper left corner
    global corner
    corner = -n * SQUARE / 2
    othello.setposition(corner, corner)
  
    # Draw the green background
    othello.begin_fill()
    for i in range(4):
        othello.pendown()
        if i % 2 == 0:
            othello.forward(SQUARE * WIDTH)
        else:
            othello.forward(SQUARE * HEIGHT)
        othello.left(90)

    othello.end_fill()

    # Draw the horizontal lines
    for i in range(WIDTH):
        othello.setposition(corner, SQUARE * i + corner)
        draw_lines(othello, WIDTH)

    # Draw the vertical lines
    othello.left(90)
    for i in range(HEIGHT):
        othello.setposition(SQUARE * i + corner, corner)
        draw_lines(othello, HEIGHT)

    othello.goto(-5.0,-25.0)
    draw_circle(othello, 1)  
    game_state[3][3] = 1
    othello.goto(45.0,-25.0)
    draw_circle(othello, 0)
    game_state[3][4] = 0
    othello.goto(45.0,25.0)
    draw_circle(othello, 1)
    game_state[4][3] = 1
    othello.goto(-5.0,25.0)
    draw_circle(othello, 0)
    game_state[4][4] = 0
    print(game_state)
    

    turtle.done()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Purpose:
# 
# Flips the piecees over between the players move and the players other piece as per legal_move 
#
#### Signature:
#
# piece_flipper :: int int => bool

def peice_flipper(row,colum):
    p = game_state[row][colum]
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        row_temp, colum_temp = row, colum
        row_temp += xdirection # first step in the direction
        colum_temp += ydirection # first step in the direction
        if (game_state[row_temp][colum_temp] == (1 - p)):
            # go deeper
            diff = [row_temp - row, colum_temp - colum]
            for i in range(2, 7):
                diff_temp = [diff[0] * i, diff[1] * i]
                if (legal_move_in_bounds(row + diff_temp[0], colum + diff_temp[1])):
                    if(game_state[row + diff_temp[0]][colum + diff_temp[1]] == p):
                        for j in range(2, i):
                            # flip  (row + diff[0]*j, colum + diff[1]*j)
                            x, y = convert_cordinants_back(row + diff[0]*j, colum + diff[1]*j)
                            othello.goto(x, y)
                            draw_circle(othello,p)
                            game_state[row + diff[0]*j][colum + diff[1]*j] = p
                        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Purpose:
# 
# Allows the click if the move is legal and possible
#
#### Signature:
#
# legal_move :: int int array => bool

def legal_move(row, colum, p):
    
    if (game_state[row][colum] != None):
        return False
    if (legal_move_in_bounds(row, colum) == False):
        return False
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        row_temp, colum_temp = row, colum
        row_temp += xdirection # first step in the direction
        colum_temp += ydirection # first step in the direction
        print(row_temp, colum_temp)
        print(game_state[row_temp][colum_temp])
        if (game_state[row_temp][colum_temp] == (1 - p)):
            # go deeper
            diff = [row_temp - row, colum_temp - colum]
            for i in range(2, 7):
                diff_temp = [diff[0] * i, diff[1] * i]
                if (legal_move_in_bounds(row + diff_temp[0], colum + diff_temp[1])):
                    if(game_state[row + diff_temp[0]][colum + diff_temp[1]] == p):
                        return True
    return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Purpose:
# 
# keeps legal move function in bounds
#
#### Signature:
#
# legal_move_in_bounds :: int int => bool

def legal_move_in_bounds(row, colum):
    return 0 <= row <= 7 and 0 <= colum <= 7 
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#### Purpose:
# 
# Checks to make sure the move is within the grid
#
#### Signature:
#
# pos_in_bounds :: int, int => bool

def pos_in_bounds(x, y):
    return RIGHT_BOUNDARY > x > LEFT_BOUNDARY and LOWER_BOUNDARY < y < UPPER_BOUNDARY

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Purpose:
# 
# Board Game State, holds pieces
#
#### Signature:
#
# create_board_state :: void => void

    
def create_board_state():
    
    for x in range(0, HEIGHT):
        temp_state = []
        for y in range(0, WIDTH):
            temp_state.append(None)
            
        game_state.append(temp_state)
    # print(game_state)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#### Purpose:
# 
# tally's the score
#
#### Signature:
#
# score :: int, int, void => bool

def current_score(black, white):
    global game_state
    white = 1
    black = 0
    for row in game_state:
        for i in range(0, len(row)):
            if row[i] == 1:
                black += 1
            if row[i] == 0:
                white +=1
    # print (black,white)
    return black,white

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#### Purpose:
# 
# Centers position of the click in the center of the square
#
#### Signature:
#
# translate_position :: int, int => void

def translate_position(x, y):
        x = (x//SQUARE)*SQUARE
        y = (y//SQUARE)*SQUARE+SQUARE
        othello.goto(x+SQUARE * .9,y -SQUARE*.5)
        # print(x,y)
        return x,y

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#### Purpose:
# 
# To draw lines for the board
#
#### Signature:
#
# draw_board :: void => void

def draw_lines(turt, n):
    turt.pendown()
    turt.forward(SQUARE * n)
    turt.penup()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#### Purpose:
# 
# To make a move againt human player
#
#### Signature:
#
# AI :: int => void

def AI(p):
    legal_position_list = []
    for row in range(0,7):
        for colum in range(0,7):
            if(game_state[row][colum] != None):
                for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    row_temp, colum_temp = row, colum
                    row_temp += xdirection # first step in the direction
                    colum_temp += ydirection # first step in the direction
                    if(legal_move(row_temp, colum_temp, p)):
                        # add (row_temp, clum_temp) to legal_position_list
                        legal_position_list.append((row_temp, colum_temp))
    # randomly select
    rand = random.choice(legal_position_list)
    game_state[rand[0]][rand[1]] = p
    x, y = convert_cordinants_back(rand[0], rand[1])
    othello.goto(x, y)
    draw_circle(othello,p)
    peice_flipper(rand[0], rand[1])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Purpose:
# 
# converts othello position into 8 X 8 position
#
#### Signature:
#
# cconvert_cordinants :: float, float => int, int

def convert_cordinants(x,y):
    
    row = int((x - corner)//SQUARE)
    colum = int((y - corner)//SQUARE)
    print(row, colum, corner, SQUARE)
    return row,colum
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Purpose:
# 
# converts the quardinents back to x and y for the flipper function
#
#### Signature:
#
# convert_cordinents_back :: int int => bool

def convert_cordinants_back(row,colum):
    x = -155.0 + (row * SQUARE)
    y = -175.0 + (colum * SQUARE)
    return x, y

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Purpose:
# 
# Executes a move upon a click, updates game state grid
#
#### Signature:
#
# draw_board :: int, int => void

def click(x,y):
    global game_state
    global p 
    p = 1
    scr = current_score(black=int,white=int)
    row,colum = convert_cordinants(x,y)
    in_bounds = pos_in_bounds(x,y)
    is_legal = legal_move(row,colum,p)
    if in_bounds and is_legal:
        translate_position(x,y)
        draw_circle(othello, p)
        # row,colum = convert_cordinants(x,y)
        peice_flipper(row,colum)
        game_state[row][colum] = p
        
    AI(0)   
    print("clicked")
    
    #
    ### This is code that lets you play Human vs Human ##
    #
    # if p==0:
    #     if in_bounds and is_legal:
    #         translate_position(x,y)
    #         draw_circle(othello, p)
    #         # row,colum = convert_cordinants(x,y)
    #         game_state[row][colum] = 0
    #         # print(game_state)
    #         scr
    #         p+=1
    #         mc
    #         jk

    # else: 
    #     if in_bounds and is_legal:
    #         translate_position(x,y)
    #         draw_circle(othello, p)
    #         # row,colum = convert_cordinants(x,y)
    #         game_state[row][colum] = 1
    #         # print(game_state)
    #         scr
    #         p-=1
    #         mc
    # print(scr)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

#### Purpose:
# 
# checks for the winner
#
#### Signature:
#
# winner :: int,int,array,array,void => string

def winner(black, white, row, colum, game_state):
    
    current_score(black,white)

    if (game_state[row][colum] == None and game_state[row][colum] == 0):
        print("White Wins")
    if (game_state[row][colum] == None and game_state[row][colum] == 1):
        print("Black Wins")
    if (game_state[row][colum] != None):
        if (black > white):
            print("Black Wins")
        else:
            print("White Wins")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

#### Purpose:
# 
# Draws the circle shaped tile object
#
#### Signature:
#
# draw_board :: void => void

def draw_circle(turt, player):
    if(player > 0):
        turt.fillcolor(0,0,0)  
    else:
        turt.fillcolor("white")
    # turt.goto(x+SQUARE * .5,y -SQUARE*.9)
    turt.down()
    turt.begin_fill()
    turt.circle((SQUARE)*0.40)
    turt.end_fill()
    turt.up()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###############TESTS#################TESTS####################TESTS#############
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def tests_draw_board():
    pass
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_legal_move():
    pass
#     assert(legal_move(2,4 == None) == True)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_pos_in_bounds():
    pass
    # assert(pos_in_bounds(-201,-50) == False)
    # assert(pos_in_bounds(-199,-49) == True)
    # assert(pos_in_bounds(0,0) == True)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_create_board_state():
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_peice_flipper():
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_current_score():
    pass
    # assert(current_score(0,1) == False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_translate_position():
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_draw_lines():
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_AI():
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_convert_cordinants():
    pass
    # assert(convert_cordinants(0,0) == (0,0) == True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def testconvert_cordinants_back():
    pass
    # assert(convert_cordinants(0,0) == (0,0) == True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_click():
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_winner():
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_draw_circle():
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    create_board_state()
    draw_board(8)
    # test_pos_in_bounds()
    # test_current_score()
    # test_translate_position()
    # screen.onclick(draw_circle)
    # screen.mainloop()

main()