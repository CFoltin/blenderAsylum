# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


import random

import bpy
from mathutils import Vector, Matrix, Quaternion, Euler, Color


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
            
    def copy(self):
        return Point(self.posx, self.posy, self.direction)
    
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
                        

def createBlock(posx, posy, colorr, colorg, colorb):
    bpy.ops.mesh.primitive_cube_add(radius=0.3, view_align=False, enter_editmode=False, location=(posx, posy, 0.3), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    cube = bpy.context.object
    mat = bpy.data.materials.new("PKHG")
    mat.diffuse_color = (colorr, colorg, colorb)
    cube.active_material = mat
    return cube


def createBase(posx, posy):
    bpy.ops.mesh.primitive_cube_add(radius=0.5, view_align=False, enter_editmode=False, location=(posx, posy, 0.0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.resize(value=(1.0, 1.0, 0.1))
    return bpy.context.object

def createLamp(eingang):
    bpy.ops.object.lamp_add(view_align=False, location=(eingang.posx, eingang.posy, 0.8), radius=1.0, type='POINT', rotation=Euler((0.0, 0.0, 0.0), 'XYZ'), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    return bpy.context.object
    
def createCamera(eingang):
    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(eingang.posx, eingang.posy, 0.9), rotation=Euler((3.1415/2, 0.0, 0.0), 'XYZ'), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.resize(value=(0.1, 0.1, 0.1))
    return bpy.context.object
    

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

# create asylum
l = 10
schrittweite = 5
schrittweiteMin = 3
a = Asylum(l)

while True:
    a = Asylum(l)
    global eingang
    eingang = Point(int(l/2),0,1)
    p  = eingang.copy()
    random.seed()
    global ausgang 
    ausgang = recursion(a, p, schrittweite, schrittweiteMin, 0)
    print (a)
    count = a.count()
    if(count >= 3*l):
        if(ausgang.posy == 0):
            print ("Exit too close to entrance: %s ..." % ausgang)
        else:
            print ("Asylum accepted: %d" % count)
            break;
    else:
        print ("Asylum too primitive %d, repeat..." % count)
#exit(0)

# change scene
bpy.context.screen.scene=bpy.data.scenes['Scene']

# remove all
playerAlreadyPresent = False
for obj in bpy.data.objects:
    # retain the player, as it contains the player's logic.
    if obj.name == "spieler" or obj.name == "Lampe" or obj.name == "Kamera" or obj.name == "Ziel":
        obj.select = False
        playerAlreadyPresent = True
        if obj.name == "spieler":
            startBlock = obj
        if obj.name == "Lampe":
            startLampe = obj
        if obj.name == "Kamera":
            startCamera = obj
        if obj.name == "Ziel":
            endBlock = obj
    else:
        obj.select = True
bpy.ops.object.delete() 

# create blender objects:
a.createBlenderObjects()
# create player, lamp and camera combo
if playerAlreadyPresent == False:
    startBlock = createBlock(eingang.posx, eingang.posy, 0.0, 0.0, 1.0)
    startBlock.name = "spieler"
    startLampe = createLamp(eingang)
    startLampe.name = "Lampe"
    startCamera = createCamera(eingang)
    startCamera.name = "Kamera"
    # exit:
    endBlock = createBlock(ausgang.posx, ausgang.posy, 1.0, 0.0, 0.0)
    endBlock.name = "Ziel"
# enable blind block for storage
startBlockHidden = createBlock(eingang.posx, eingang.posy, 0.0, 0.0, 1.0)
startBlockHidden.name = "Ursprung"
startBlockHidden.hide = True
startBlockHidden.location = (eingang.posx, eingang.posy, -1.0)
#bpy.context.scene.objects.active = startBlock
#bpy.ops.transform.translate(value=(0.0, 0.0, 1.0))
startBlock.location = (eingang.posx, eingang.posy, 0.3)
startLampe.location = (eingang.posx, eingang.posy, 0.8)
startCamera.location = (eingang.posx, eingang.posy, 0.9)
endBlock.location = (ausgang.posx, ausgang.posy, 0.3)
bpy.context.scene.objects.active = startBlock
startLampe.select = True
startCamera.select = True
bpy.ops.object.parent_set(keep_transform=False, xmirror=False, type='OBJECT')
