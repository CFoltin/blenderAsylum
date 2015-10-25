import random
import bpy


class Point:
    def __init__(self, posx, posy, direction):
        self.set(posx, posy, direction)
        
    def move(self, length):
        if self.direction % 4 == 0:
            self.posx += length
        if self.direction % 4 == 1:
            self.posy += length
        if self.direction % 4 == 2:
            self.posx -= length
        if self.direction % 4 == 3:
            self.posy -= length
    
    def rotate(self, deltadirection):
        self.direction += deltadirection
        self.direction %= 4
    
    def set(self, posx, posy, direction):
        self.posx = posx
        self.posy = posy
        self.direction = direction
    
    def isInside(self, size):
        return (self.posx >= 0) and (self.posx < size) and (self.posy >= 0) and (self.posy < size)
    
    def isInBorder(self, size):
        return (self.posx == 0) or (self.posx == size-1) or (self.posy == 0) or (self.posy == size-1)
    
    def __str__(self):
        return "[%d;%d]->%d" % (self.posx, self.posy, self.direction)
    
class Asylum:
    def __init__(self, size):
        self.size = size
        self.matrix =  [[1 for x in range(size)] for x in range(size)]
              
    def move(self, point, length, setBorderPoint = True):
        for i in range(length):
            if(point.isInside(self.size)):
                self.matrix[point.posx] [point.posy] = 0
                point.move(1)
                if(point.isInBorder(self.size)):
                    if(setBorderPoint):
                        self.matrix[point.posx] [point.posy] = 0
                    return

    def isInside(self, point):
        return point.isInside(self.size)
    
    def isInBorder(self, point):
        return point.isInBorder(self.size)

    def isSelected(self, point):
        return self.isSelectedXY(point.posx,point.posy)

    def count(self):
        count = 0
        for y in range(self.size):
            for x in range(self.size):
                if self.isSelectedXY(x, y):
                    count += 1
        return count
    

    def isSelectedXY(self, x, y):
        return self.matrix[x][y] == 0

    def __str__(self):
        ret = ""
        for y in range(self.size):
            for x in range(self.size):
                if self.isSelectedXY(x, y):
                    ret += "x "
                else:  
                    ret += "  "
            ret += "\n" 
        return ret

    def createBlenderObjects(self):
        for y in range(self.size):
            print("Create row %d" % y)
            for x in range(self.size):
                if self.isSelectedXY(x, y):
                    createBase(x,y)
                for direction in range(2):
                    p = Point(x,y,direction)
                    p1 = Point(x,y,direction)
                    p.move(1)
                    if self.isInside(p) and (self.isSelected(p) != self.isSelected(p1)):
                        createSide(x, y, direction)
                        

def createBase(posx, posy):
    bpy.ops.mesh.primitive_cube_add(radius=0.5, view_align=False, enter_editmode=False, location=(posx, posy, 0.0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.resize(value=(1.0, 1.0, 0.1))

def createSide(posx, posy, direction):
    sizex = 1.0
    sizey = 1.0
    delta = 0.5
    depth = 0.1
    if direction % 4 == 0:
        posx += delta
        sizex = depth
    if direction % 4 == 1:
        posy += delta
        sizey = depth
    if direction % 4 == 2:
        posx -= delta
        sizex = depth
    if direction % 4 == 3:
        posy -= delta
        sizey = depth
    bpy.ops.mesh.primitive_cube_add(radius=0.5, view_align=False, enter_editmode=False, location=(posx , posy, 0.5), rotation=(0.0, 0.0, 0.0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.resize(value=(sizex, sizey, 1.0))

def recursion(asylum, p, schrittweite, schrittweiteMin, timeToLive):
    a.move(p, random.randint(schrittweiteMin,schrittweite), (timeToLive==0))
    if a.isInBorder(p) or not(a.isInside(p)):
        return p
    if(timeToLive>0):
        timeToLive-=1
        if(timeToLive ==0):
            return p
    pcopy = Point(p.posx, p.posy, p.direction)
    pcopy1 = Point(p.posx, p.posy, p.direction)
    p.rotate(1)
    pcopy.rotate(-1)
    lst = [p, pcopy, pcopy1]
    random.shuffle(lst)
    # randomly start other recursion(s):
    while len(lst)>1:
        nextpoint = lst.pop()
        if(random.randint(0,10)<2):
            # randomly rotate to the other side or keep running straight:
            recursion(asylum, nextpoint, schrittweite, schrittweiteMin, random.randint(1,4))
    ausgang = recursion(asylum, lst.pop(), schrittweite, schrittweiteMin, timeToLive)
    return ausgang

# labyrinth erzeugen
l = 40
schrittweite = 7
schrittweiteMin = 3
a = Asylum(l)
while True:
    a = Asylum(l)
    p = Point(int(l/2),0,1)
    random.seed()
    ausgang = recursion(a, p, schrittweite, schrittweiteMin, 0)
    print (a)
    count = a.count()
    if(count >= 3*l):
        if(ausgang.posy == 0):
            print ("Ausgang zu nah am Eingang: %s ..." % ausgang)
        else:
            print ("Asylum accepted: %d" % count)
            break;
    else:
        print ("Asylum too primitive %d, repeat..." % count)
#exit(0)

# remove all
for obj in bpy.data.objects:
    obj.select = True
bpy.ops.object.delete() 

# blender objekte erzeugen:
a.createBlenderObjects()
