#Arcade Game Code Follows
from tkinter import *
import random

# make a window
window = Tk()
window.title('The Under Water Adventure')

# create a canvas to put objects on the screen
canvas = Canvas(window, width=400, height=400, bg = 'dodgerblue')
canvas.pack()

# Set up the welcome screen
title = canvas.create_text(200, 100, text = 'Underwater Adventure', fill='white', font= ('Verdana', 30))
directions = canvas.create_text(200, 200, text= 'Collect the Falling Treasure!', fill='white', font=('Verdana', 20))

#Score
score = 0
score_display = Label(window, text='Score: '+str(score))
score_display.pack()
                      
#Level Display
level = 1
level_display = Label(window, text='Level: ' + str(level))
level_display.pack()

#Images
player_image = PhotoImage(file='SCUBA.gif')
mychar= canvas.create_image(200,310, image = player_image)

#variables and lists for treasure
treasure_list = []
enemy_list = []
treasure_speed = 2
treasure_color_list = ['gold', 'crimson', 'blue', 'limegreen', 'darkviolet', 'aliceblue', 'black']

#movement
move_direction = 0 



#functions
def make_treasure():
    xposition = random.randint(1,400)
    treasure_color = random.choice(treasure_color_list)
    treasure = canvas.create_oval(xposition, 0, xposition+30, 30, fill = treasure_color, outline = treasure_color)
    treasure_list.append(treasure)
    if treasure_color =='black':
        enemy_list.append(treasure)
    window.after(1000, make_treasure)

def move_treasure():
    for treasure in treasure_list:
        canvas.move(treasure, 0, treasure_speed)
        if canvas.coords(treasure)[1] >400:
            xposition = random.randint(1,400)
            canvas.coords(treasure, xposition, 0, xposition+30,30)
    window.after(50, move_treasure)

def update_score_level():
    global score, level, treasure_speed
    score = score + 1
    score_display.config(text="Score: " + str(score))
    if score > 5 and score <= 10:
        treasure_speed = treasure_speed +1
        level =2
        level_display.config(text='Level: ' + str(level))
    elif score >10:
        treasure_speed = treasure_speed +1
        level = 3
        level_display.config(text='Level: ' + str(level))

def collision(item1, item2, distance):
    xdistance = abs(canvas.coords(item1)[0] - canvas.coords(item2)[0])
    ydistance = abs(canvas.coords(item1)[1] - canvas.coords(item2)[1])
    overlap = xdistance < distance and ydistance <distance
    return overlap

def check_hits():
    for treasure in enemy_list:
        if collision(mychar, treasure, 30):
            game_over = canvas.create_text(200, 200, text = 'Game Over', fill = 'crimson', font = ('Verdana', 30))
            window.after(2000, end_game_over)
            return
    for treasure in treasure_list:
        if collision(mychar, treasure, 30):
            canvas.delete(treasure)
            treasure_list.remove(treasure)
            update_score_level()
    window.after(100, check_hits)

def check_input(event):
    global move_direction
    key = event.keysym
    if key == "Right":
        move_direction = "Right"
    elif key == "Left":
        move_direction = "Left"

def end_input(event):
    global move_direction
    move_direction = "None"

def move_character():
    if move_direction =="Right" and canvas.coords(mychar)[0] < 400:
        canvas.move(mychar, 10, 0)
    if move_direction == "Left" and canvas.coords(mychar)[0] >0:
        canvas.move(mychar, -10,0)
    window.after(16, move_character)        

def end_game_over():
    window.destroy()

def end_title():
    canvas.delete(title)
    canvas.delete(directions)

canvas.bind_all('<KeyPress>', check_input)
canvas.bind_all('<KeyRelease>', end_input)

window.after(1000, end_title)
window.after(1000, make_treasure)
window.after(1000, move_treasure)
window.after(1000, check_hits)
window.after(1000, move_character)
window.mainloop()
