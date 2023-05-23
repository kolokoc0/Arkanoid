import random
import tkinter as tk

win = tk.Tk()

width = 500
height = 500

circle = 10

rect_size = 25

x = 1
y = 1

d = 5

vector = [1*d,1*d]

bricks_w = 50
bricks_h = 20
bricks_count_x = 10
bricks_count_y = 5

bricks_list = [ ]

canvas = tk.Canvas(win,width = width,height = height,bg ="white")
canvas.pack()

gulicka = canvas.create_oval(240,400,240+circle,400+circle,fill="red")

platform = canvas.create_rectangle(250,440,350,440+rect_size,fill="black")

temp = False

colors = ["green","red","blue","yellow","aquamarine"]
def prepare_bricks():
    for y in range(bricks_count_y):
        for x in range(bricks_count_x):
            bricks_list.append(canvas.create_rectangle(x*bricks_w,y*bricks_h,(x+1)*bricks_w,(y+1)*bricks_h,fill=colors[y%4],width = 2,outline= "white", tag = "none"))

def vectors():
    global vector, num
    num = random.randint(-1,1)
    coordinates = canvas.coords(gulicka)
    if coordinates[2]>=width-d-4 and vector == [1*d,1*d+num]:
        vector = [-1*d,1*d+num]
        
    elif coordinates[2]>=width-d-4 and vector ==[1*d,-1*d+num]:
        vector = [-1*d,-1*d+num]
        
    elif coordinates[0]<=0+d+1 and vector == [-1*d,-1*d+num]:
        vector = [1*d,-1*d+num]
        
    elif coordinates[0]<=0+d+1 and vector == [-1*d,1*d+num]:
        vector = [1*d,1*d+num]
        
    elif coordinates[3]>=height-d-1 and vector == [-1*d,1*d+num]:
        vector = [-1*d,-1*d+num]
        
    elif coordinates[3]>=height-d-1 and vector == [1*d,1*d+num]:
        vector = [1*d,-1*d+num]
        
    elif coordinates[1]<=0+d+1 and vector == [1*d,-1*d+num]:
        vector = [1*d,1*d+num]
        
    elif coordinates[1]<=0+d+1 and vector == [-1*d,-1*d+num]:
        vector = [-1*d,1*d+num]
    return vector

def destroy_brick():
    global vector,temp
    ball_coords = canvas.coords(gulicka)
    overlap = canvas.find_overlapping(ball_coords[0]+1,ball_coords[1]+1,ball_coords[2]-1,ball_coords[3]-1)
    former_vector,vector = vector,vector
    if len(overlap)>=2 and 2 not in overlap and temp == False:
        overlap_coords = canvas.coords(overlap[-1])
        overlap_x1 = overlap_coords[0]
        overlap_x2 = overlap_coords[2]
        overlap_y1 = overlap_coords[1]
        overlap_y2 = overlap_coords[3]
        ball_midx = (ball_coords[2]+ball_coords[0])//2
        ball_midy = (ball_coords[3]+ball_coords[1])//2
        if ball_coords[1]<=overlap_y2 and ball_midy >=overlap_y2-(1+d) or ball_coords[3]>=overlap_y1 and ball_midy <=overlap_y1+(1+d):
            if ball_coords[1]<=overlap_y2 and overlap_x1<=ball_coords[0]<=overlap_x2:
                vector = [vector[0],-1*vector[1]]
            elif ball_coords[3]>=overlap_y1 and overlap_x1<=ball_coords[2]<=overlap_x2:
                vector = [vector[0],-1*vector[1]]
        elif ball_coords[0]<=overlap_x2 and ball_midx >= overlap_x2-(1+d) or ball_coords[2]>=overlap_x1 and ball_midx <=overlap_x1+(1+d):
            if ball_coords[0]<=overlap_x2 and overlap_y1<=ball_coords[1]<=overlap_y2:
                vector = [-1*vector[0],vector[1]]
            elif ball_coords[2]>=overlap_x1 and overlap_y1<=ball_coords[3]<=overlap_y2:
                vector = [-1*vector[0],vector[1]]
    for i in overlap:
        spec = canvas.itemcget(i,"tag")
        if spec == "spec":
            temp = True
        if i in bricks_list:
            canvas.delete(i)
            bricks_list.remove(i)
    return temp

def starter(e):
    global x
    x = e.x

def plat_move(e):
    global x
    x2 = e.x
    vector = x2-x
    plat_coords = canvas.coords(platform)
    if plat_coords[0]<=0:
        if vector <=0:
            canvas.move(platform,0,0)
        elif vector >=0:
            canvas.move(platform,vector,0)
    elif plat_coords[2]>=width:
        if vector>=0:
            canvas.move(platform,0,0)
        elif vector<=0:
            canvas.move(platform,vector,0)
    else:
        canvas.move(platform,vector,0)
    x = x2

#def checkkey(e):
    #print("stlacil som")
    #print(e.char)
#def left_move(e):
    #canvas.move(platform,-10,0)
#def right_move(e):
    #canvas.move(platform,10,0)



def movement():
    global vector
    vector = vectors()
    ball_coords = canvas.coords(gulicka)
    overlap = canvas.find_overlapping(ball_coords[0],ball_coords[1],ball_coords[2],ball_coords[3])
    destroy_brick()
    if temp == True:
        vector == [vector[0],vector[1]]
    if 2 in overlap and ball_coords[3]>=(canvas.coords(overlap[1]))[3]-20:
        vector = [vector[0],-1*vector[1]]
    canvas.move(gulicka,vector[0],vector[1])
    if ball_coords[3]>=height:
        canvas.delete("all")
        canvas.create_text(width//2,height//2,text="You lost", font = ("Arial",20))
    canvas.after(10,movement)
    if len(bricks_list)==0:
        canvas.delete("all")
        canvas.create_text(width//2,height//2,text ="You won YAAAAY!!!!", font= ("Arial",40))


def special():
    ran = random.randint(40,len(bricks_list)-1)
    canvas.itemconfig(bricks_list[ran],tag = "spec")
    canvas.itemconfig(bricks_list[ran],fill = "black") 



canvas.bind("<Button-1>",starter)
canvas.bind("<B1-Motion>",plat_move)
#canvas.focus_set()
#win.bind("<Key>", checkkey)
#win.bind("<Left>",left_move)
#win.bind("<Right>",right_move)

prepare_bricks()
special()
#for i in range(5):
    #canvas.delete(bricks_list[i])
#for i in range(6,15):
    #canvas.delete(bricks_list[i])
#for i in range(16,25):
    #canvas.delete(bricks_list[i])
#for i in range(26,35):
    #canvas.delete(bricks_list[i])
#for i in range(36,45):
    #canvas.delete(bricks_list[i])
#for i in range(46,50):
    #canvas.delete(bricks_list[i])

movement()

win.mainloop()
