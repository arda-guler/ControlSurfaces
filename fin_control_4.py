# FIN CONTROL DEMO (4 FINS)

from tkinter import *

canard_max_angle = 100 # 10 degrees, not 100, it just makes
                       # visualizing easier

command_turn = [0,0]
command_roll = 0

class canard():
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle

    def get_pos(self):
        return self.pos

canard_left = canard([-20, 0], 0)
canard_right = canard([20, 0], 0)
canard_top = canard([0, 20], 0)
canard_bottom = canard([0, -20], 0)

canards = [canard_left, canard_right, canard_top, canard_bottom]

def calc_canard_angles(x, y, roll):
    
    canard_left = (y + roll)
    canard_right = (y - roll)
    canard_top = (x + roll)
    canard_bottom = (x - roll)

    return canard_left, canard_right, canard_top, canard_bottom

def space2canvas(space_coords):
    canvas_x = ((space_coords[0]) + 900/2)
    canvas_y = ((-space_coords[1] + 500/2))
    
    return [canvas_x, canvas_y]

def canvas2space(canvas_coords):
    space_x = (canvas_coords[0] - 900/2)
    space_y = -((canvas_coords[1] - 500/2))

    return [space_x, space_y]

def clicked_on_canvas(event):
    x = canvas2space([event.x,0])[0]
    y = canvas2space([0, event.y])[1]

    move_command_turn(x, y)

def right_clicked_on_canvas(event):
    x = canvas2space([event.x,0])[0]
    move_command_roll(x)

def move_command_roll(x):
    global command_roll
    command_roll = x

def move_command_turn(x, y):
    global command_turn

    command_turn[0] = x
    command_turn[1] = y

def get_max_requested_canard_angle():
    global canards

    result = None
    
    for c in canards:
        if not result or abs(c.angle) > abs(result.angle):
            result = c

    return abs(result.angle)

def limit_turn():
    global canards, canard_max_angle

    # check if any of the canards are requested to turn more than it can
    # because in that case, we need to readjust angles
    need_limiting = False
    
    for c in canards:
        if abs(c.angle) > canard_max_angle:
            need_limiting = True
            break

    if need_limiting:
        max_requested = get_max_requested_canard_angle()

        for c in canards:
            c.angle = (c.angle/max_requested)*canard_max_angle

    return need_limiting

root = Tk()
root.title("Canard Control")
root.geometry("1150x600")

tk_canvas = Canvas(root, width=900, height=500, bg="white")
tk_canvas.grid(row=0, column=1, rowspan=25, columnspan=5)

tk_canvas.bind('<Button-1>', clicked_on_canvas)
tk_canvas.bind('<Button-3>', right_clicked_on_canvas)

left_angle = IntVar()
left_angle.set(0)
right_angle = IntVar()
right_angle.set(0)
top_angle = IntVar()
top_angle.set(0)
bottom_angle = IntVar()
bottom_angle.set(0)

left_angle_name = Label(root, text="Left Canard")
left_angle_name.grid(row=0, column=0)
left_angle_label = Label(root, textvariable=left_angle)
left_angle_label.grid(row=1, column=0)

right_angle_name = Label(root, text="Right Canard")
right_angle_name.grid(row=2, column=0)
right_angle_label = Label(root, textvariable=right_angle)
right_angle_label.grid(row=3, column=0)

top_angle_name = Label(root, text="Top Canard")
top_angle_name.grid(row=4, column=0)
top_angle_label = Label(root, textvariable=top_angle)
top_angle_label.grid(row=5, column=0)

bottom_angle_name = Label(root, text="Bottom Canard")
bottom_angle_name.grid(row=6, column=0)
bottom_angle_label = Label(root, textvariable=bottom_angle)
bottom_angle_label.grid(row=7, column=0)

is_limited = StringVar()
limit_indicator = Label(root, textvariable=is_limited)
limit_indicator.grid(row=0, column=6, rowspan=3)

while True:

    # rocket body
    tk_canvas.create_oval(space2canvas([-15, -15]),
                          space2canvas([+15, +15]),
                          fill="red")
    
    canard_left.angle, canard_right.angle, canard_top.angle, canard_bottom.angle = calc_canard_angles(command_turn[0], command_turn[1], command_roll)

    limited_turn = limit_turn()
    if limited_turn:
        is_limited.set("Turn command beyond\ncanard rotation limits!\n(Canard angles adjusted to\nstay on desired vector with\nthe best turn rate possible.)")
    else:
        is_limited.set("OK")

    left_angle.set(round(canard_left.angle/10, 3))
    right_angle.set(round(canard_right.angle/10, 3))
    top_angle.set(round(canard_top.angle/10, 3))
    bottom_angle.set(round(canard_bottom.angle/10, 3))

    # canards
    tk_canvas.create_line(space2canvas([-15, 0])[0], space2canvas([-15, 0])[1],
                          space2canvas([-45, 0])[0], space2canvas([-45, 0])[1],
                          fill="hotpink")
    
    tk_canvas.create_line(space2canvas([15, 0])[0], space2canvas([15, 0])[1],
                          space2canvas([45, 0])[0], space2canvas([45, 0])[1],
                          fill="hotpink")

    tk_canvas.create_line(space2canvas([0, 15])[0], space2canvas([0, 15])[1],
                          space2canvas([0, 45])[0], space2canvas([0, 45])[1],
                          fill="hotpink")

    tk_canvas.create_line(space2canvas([0, -15])[0], space2canvas([0, -15])[1],
                          space2canvas([0, -45])[0], space2canvas([0, -45])[1],
                          fill="hotpink")
    
    # canard arrows
    tk_canvas.create_line(space2canvas(canard_left.get_pos())[0], space2canvas(canard_left.get_pos())[1],
                          space2canvas(canard_left.get_pos())[0], space2canvas([0, canard_left.get_pos()[1] + canard_left.angle])[1],
                          fill="blue", arrow=LAST)

    tk_canvas.create_line(space2canvas(canard_right.get_pos())[0], space2canvas(canard_right.get_pos())[1],
                          space2canvas(canard_right.get_pos())[0], space2canvas([0, canard_right.get_pos()[1] + canard_right.angle])[1],
                          fill="blue", arrow=LAST)

    tk_canvas.create_line(space2canvas(canard_top.get_pos())[0], space2canvas(canard_top.get_pos())[1],
                          space2canvas([canard_top.get_pos()[0] + canard_top.angle, 0])[0], space2canvas(canard_top.get_pos())[1],
                          fill="blue", arrow=LAST)

    tk_canvas.create_line(space2canvas(canard_bottom.get_pos())[0], space2canvas(canard_bottom.get_pos())[1],
                          space2canvas([canard_bottom.get_pos()[0] + canard_bottom.angle, 0])[0], space2canvas(canard_bottom.get_pos())[1],
                          fill="blue", arrow=LAST)

    # turn command
    tk_canvas.create_line(space2canvas([0,0])[0], space2canvas([0,0])[1],
                          space2canvas([command_turn[0], 0])[0], space2canvas([0, command_turn[1]])[1],
                          fill="red", arrow=LAST)

    # roll command
    tk_canvas.create_line(space2canvas([0,200])[0], space2canvas([0,200])[1],
                          space2canvas([command_roll, 200])[0], space2canvas([command_roll, 200])[1],
                          fill="orange", arrow=LAST)

    root.update()
    tk_canvas.delete("all")

root.mainloop()
