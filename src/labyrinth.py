import random
import bpy
import math


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
              
    def move(self, point, length):
        for i in range(length):
            if(point.isInside(self.size)):
                self.matrix[point.posx] [point.posy] = 0
                point.move(1)
                if(point.isInBorder(self.size)):
                    self.matrix[point.posx] [point.posy] = 0
                    return

    def isInside(self, point):
        return point.isInside(self.size)
    
    def isInBorder(self, point):
        return point.isInBorder(self.size)

    def isSelected(self, point):
        return self.matrix[point.posx] [point.posy] == 0
    
    def __str__(self):
        ret = ""
        for y in range(self.size):
            for x in range(self.size):
                ret += "%d " % self.matrix [x] [y]
            ret += "\n" 
        return ret

    def createBlenderObjects(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.matrix[x] [y] == 0:
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

# start Application
l = 40
a = Asylum(l)
p = Point(int(l/2),0,1)
schrittweite = 5
random.seed()
while a.isInside(p):
    a.move(p, random.randint(2,schrittweite))
    d = random.randint(0,1)
    if(d == 1):
        p.rotate(1)
    else:
        p.rotate(-1)
    if a.isInBorder(p):
        break
print (a)

# remove all
for obj in bpy.data.objects:
    obj.select = True
bpy.ops.object.delete() 

# create bases:
a.createBlenderObjects()
