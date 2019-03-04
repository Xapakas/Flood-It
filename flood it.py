from graphics import *
from Tile import *
from random import *

def drawInitial(l_colors):
    win = GraphWin("FLOOD IT BRO",780,600)
    new_game_rectangle = Rectangle(Point(20,15),Point(180,50))
    new_game_rectangle.setFill("#001a4d") # dark navy
    new_game_rectangle.draw(win)
    new_game_text = Text(Point(100,32.5),"New Game")
    new_game_text.setSize(19)
    new_game_text.setFill("white")
    new_game_text.draw(win)
    x_base = 20
    y_base = 70
    i_num = 0
    for row in range(2): # drawing boxes on left
        for col in range(3):
            box = Rectangle(Point(x_base,y_base),Point(x_base+40,y_base+40))
            box.setFill(l_colors[i_num])
            box.draw(win)
            x_base += 60
            i_num += 1
        x_base = 20
        y_base += 60
##    turns_text = Text(Point(100,200),"Turns: 0 / 25") # i will likely replace
##    turns_text.setSize(20)                            # these later with objects
##    turns_text.draw(win)                              # that can be modified
    best_text = Text(Point(100,240),"Best: None")     # during the game
    best_text.setSize(20)
    best_text.draw(win)
    won_text = Text(Point(100,280),"Won: 0")
    won_text.setSize(20)
    won_text.draw(win)
    lost_text = Text(Point(100,320),"Lost: 0")
    lost_text.setSize(20)
    lost_text.draw(win)

    return win

def generateGrid(l_colors):
    l_tiles = []
    l_add = []
    for row in range(14):
        for col in range(14):
            t = Tile(row,col,l_colors[randint(0,5)],"uninfected")
            l_add.append(t)
        l_tiles.append(l_add)
        l_add = []
    l_tiles[0][0].set_infected("hungry")

    return l_tiles

def drawGrid(l_colors,l_tiles,win):
    x_base = 200
    y_base = 15
    for i_row in range(14):
        for i_col in range(14):
            tile = Rectangle(Point(x_base,y_base),Point(x_base+40,y_base+40))
            tile.setFill(l_tiles[i_row][i_col].get_color())
            tile.draw(win)
            x_base += 40
        x_base = 200
        y_base += 40

def updateText(win,i_turn):
    cover_box = Rectangle(Point(10,180),Point(190,220)) # will get longer
    cover_box.setFill("gray94")
    cover_box.setOutline("gray94")
    cover_box.draw(win)
    turns_text = Text(Point(100,200),"Turns: " + str(i_turn) + " / 25")
    turns_text.setSize(20)
    turns_text.draw(win)

def getClick(win):
    click = win.getMouse()
    x = click.getX()
    y = click.getY()

    return x,y

def findColor(win,l_colors,l_tiles,x,y):
    s_color = "none"
    if x <= 180: # on left boxes
        x_base = 20
        y_base = 70
        for row in range(2):
            for col in range(3):
                if x >= x_base and x <= (x_base+40) and y >= y_base and y <= (y_base+40):
                    s_color = l_colors[col+(row*3)]
                x_base += 60
            x_base = 20
            y_base += 60
    if x >= 200 and x <= 760 and y >= 15 and y <= 575: # on tiles
        s_color = l_tiles[(y - 15) // 40][(x - 200) // 40].get_color()

    return s_color

def fillTiles(l_colors,l_tiles,s_color):
    b_hungry = True
    while b_hungry == True: # while hungry tiles exist
        b_hungry = False
        for i_row in range(14):
            for i_col in range(14):
                if l_tiles[i_row][i_col].get_infected() == "hungry":
                    b_hungry = True
                    if i_row > 0:
                        if l_tiles[i_row-1][i_col].get_color() == s_color and l_tiles[i_row-1][i_col].get_infected() == "uninfected":
                            l_tiles[i_row-1][i_col].set_infected("hungry")
                    if i_row < 13:
                        if l_tiles[i_row+1][i_col].get_color() == s_color and l_tiles[i_row+1][i_col].get_infected() == "uninfected":
                            l_tiles[i_row+1][i_col].set_infected("hungry")
                    if i_col > 0:
                        if l_tiles[i_row][i_col-1].get_color() == s_color and l_tiles[i_row][i_col-1].get_infected() == "uninfected":
                            l_tiles[i_row][i_col-1].set_infected("hungry")
                    if i_col < 13:
                        if l_tiles[i_row][i_col+1].get_color() == s_color and l_tiles[i_row][i_col+1].get_infected() == "uninfected":
                            l_tiles[i_row][i_col+1].set_infected("hungry")
                    l_tiles[i_row][i_col].set_infected("fed") # remember i have to set them all back from fed to hungry

def drawTiles(win,l_tiles,s_color):
    for i_row in range(14):
        for i_col in range(14):
            if l_tiles[i_row][i_col].get_infected() == "fed":
                x_base = (i_col*40) + 200
                y_base = (i_row*40) + 15
                box = Rectangle(Point(x_base,y_base),Point(x_base+40,y_base+40))
                box.setFill(s_color)
                box.draw(win)

def setToHungry(l_tiles,s_color):
    for i_row in range(14):
        for i_col in range(14):
            if l_tiles[i_row][i_col].get_infected() == "fed":
                l_tiles[i_row][i_col].set_infected("hungry")
                l_tiles[i_row][i_col].set_color(s_color)

def checkIfEnd(l_tiles,l_colors,i_turn,s_color):
    b_win = True
    b_lose = False
    for i_row in range(14):
        for i_col in range(14):
            if l_tiles[i_row][i_col].get_color() != s_color:
                b_win = False
    if i_turn == 25:
        b_lose = True
    if b_win == True and b_lose == True:
        b_lose = False # they filled all the tiles on turn 25. buzzer beater, i guess
    return b_win, b_lose

def displayEnd(win,b_win,b_lose,i_wins,i_losses):
    if b_win == True:
        i_wins += 1
        end_text = Text(Point(100,400),"You Win!")
        end_text.setFill("green1")
        end_text.setSize(20)
        end_text.draw(win)
        cover_won_box = Rectangle(Point(20,260),Point(170,300))
        cover_won_box.setFill("gray94")
        cover_won_box.setOutline("gray94")
        cover_won_box.draw(win)
        won_text = Text(Point(100,280),"Won: " + str(i_wins))
        won_text.setSize(20)
        won_text.draw(win)
    if b_lose == True:
        i_losses += 1
        end_text = Text(Point(100,400),"You Lose!")
        end_text.setFill("red1")
        end_text.setSize(20)
        end_text.draw(win)
        cover_lost_box = Rectangle(Point(20,300),Point(170,340))
        cover_lost_box.setFill("gray94")
        cover_lost_box.setOutline("gray94")
        cover_lost_box.draw(win)
        lost_text = Text(Point(100,320),"Lost: " + str(i_losses))
        lost_text.setSize(20)
        lost_text.draw(win)

    return i_wins,i_losses

def main():
    l_colors = ["blue","red","green","yellow","pink","purple"]
    win = drawInitial(l_colors)
    l_tiles = generateGrid(l_colors)
    drawGrid(l_colors,l_tiles,win)
    fillTiles(l_colors,l_tiles,l_tiles[0][0].get_color()) # these two lines account for if more than one tile is infected at the beginning
    setToHungry(l_tiles,l_tiles[0][0].get_color())
    s_color = "none"
    s_previous_color = "none"
    i_turn = 0
    i_wins = 0
    i_losses = 0
    while True: # it needs to account for more than one infected tile at the beginning - DONE
        updateText(win,i_turn)
        while s_color == "none": # validation loop
            x,y = getClick(win)
            s_color = findColor(win,l_colors,l_tiles,x,y)
##            print(s_color)
        fillTiles(l_colors,l_tiles,s_color)
        drawTiles(win,l_tiles,s_color)
        setToHungry(l_tiles,s_color)
        if s_color != s_previous_color:
            i_turn += 1 # needs to not update if the same color has been chosen - DONE
        b_win,b_lose = checkIfEnd(l_tiles,l_colors,i_turn,s_color)
##        b_lose = True # test
        if b_win == True or b_lose == True: # if b_win then it should stop playing, if b_lose it can keep playing, just the lose message stays but lost : x doesn't update
            i_wins,i_losses = displayEnd(win,b_win,b_lose,i_wins,i_losses)
        s_previous_color = s_color
        s_color = "none"

main()
