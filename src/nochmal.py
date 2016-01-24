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

import bpy

# change scene
bpy.context.screen.scene=bpy.data.scenes['Scene']

for obj in bpy.data.objects:
    if obj.name == "spieler" or obj.name == "Lampe" or obj.name == "Kamera" or obj.name == "Ziel" or obj.name == "Ursprung":
        if obj.name == "spieler":
            startBlock = obj
        if obj.name == "Lampe":
            startLampe = obj
        if obj.name == "Kamera":
            startCamera = obj
        if obj.name == "Ziel":
            endBlock = obj
        if obj.name == "Ursprung":
            startBlockHidden = obj

location = startBlockHidden.location
startBlock.location = (location[0], location[1], 0.3)
# turn around:
bpy.context.scene.objects.active = startBlock
print ("Setting location to %s" % location)
