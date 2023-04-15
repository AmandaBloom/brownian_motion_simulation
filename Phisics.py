import random
import math
from threading import Lock

FREQUENCY = 30 # Hertz
MOLE_RADIUS = 3
MOLE_MASS = 1
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GRID_WIDTH = 10
GRID_HEIGHT = 10

class Physics:
    def __init__(self, n: int, V_global: float) -> None:
        self.lock = Lock()
        self.N = n
        self.Vg = V_global
        self.Moles = [Mole(self.Vg) for _ in range(n)]
        for i in range(len(self.Moles)):
            self.Moles[i].initPosition()
        self.checkInitCollisions(self.Moles)


    def getCollisionIdx(self, mole_list: list['Mole']) -> list[int]:
        collision = []
        for i in range(len(mole_list)):
            col = [j for j in range(len(mole_list)) if i != j and mole_list[i].x == mole_list[j].x and mole_list[i].y == mole_list[j].y]
            if col is not []:
                collision.extend(col)
        return collision

    def checkInitCollisions(self, mole_list: list['Mole']) -> None:
        collide = self.getCollisionIdx(mole_list)
        while(len(collide) != 0):
            for j in range(len(collide)):
                mole_list[j].initPosition()
            collide = self.getCollisionIdx(mole_list)

    def getMoles(self) -> list['Mole']:
        return self.Moles

    def setGlobalSpeed(self, v: float) -> None:
        self.Vg = v

    def addMoles(self, n: int) -> None:
        new_moles = [Mole(self.Vg) for _ in range(n)]
        for i in range(len(new_moles)):
            new_moles[i].initPosition()       
        self.checkInitCollisions(new_moles)
        self.Moles.extend(new_moles)
        self.N += n

    def delMoles(self, n: int) -> None:
        self.Moles = self.Moles[0:self.N-n]
        self.N -= n

    def setMoleCount(self, n: int) -> None:
        if n > self.N:
            self.addMoles(n-self.N)
        elif n < self.N:
            self.delMoles(self.N-n)
            
    def setMolesSpeed(self) -> None:
        with self.lock:
            for idx in range(len(self.Moles)):
                self.Moles[idx].setMoleSpeed(self.Vg)   

    def moveMoles(self) -> None:
        with self.lock:
            for idx in range(len(self.Moles)):
                self.Moles[idx].moveMole()

#    function checkCollision(m) {

#   var gx = Math.floor(m.x/gridEltWidth);
#   var gy = Math.floor(m.y/gridEltHeight);
#   var i, j;

#   // check grid squares around the molecule for collisions
#   for (i = -1; i <= 1; i++)
#     for (j = -1; j <= 1; j++) {
# 	if (gx+i < 0 || gy+j < 0 ||
# 	    gx+i >= gridWidth || gy+j >= gridHeight)
# 	    continue;
# 	var n = checkCollisionList(m, grid[(gx+i)+(gy+j)*gridWidth]);
# 	if (n != null)
# 	    return n;
#     }
#   return null;
# }

# function checkCollisionList(m, list) {
#   var l = list.next;
#   var count = 0;
#   for (; !l.listHead; l = l.next) {
#     if (m == l)
# 	continue;
#     count++;
#     var mindist = m.r+l.r;
#     var dx = m.x-l.x;
#     var dy = m.y-l.y;
#     if (dx > mindist || dy > mindist ||
# 	dx < -mindist || dy < -mindist)
# 	continue;
#     var dist = Math.sqrt(dx*dx+dy*dy);
#     if (dist > mindist)
# 	continue;
#     return l;
#   }
#   return null;
# }


class Mole:
    def __init__(self, Vg: float) -> None:
        self.Vg = Vg
        self.x = None
        self.y = None
        self.r = MOLE_RADIUS
        self.mass = MOLE_MASS
        self.angle = None
        self.dx = None
        self.dy = None
        self.Vx = None
        self.Vy = None
    
    def initPosition(self) -> None:
        self.x = random.randint(0+MOLE_RADIUS, SCREEN_WIDTH-MOLE_RADIUS)
        self.y = random.randint(0+MOLE_RADIUS, SCREEN_HEIGHT-MOLE_RADIUS)
        self.angle = random.uniform(0, 2*math.pi)
        self.Vy = self.Vg*math.sin(self.angle)
        self.Vx = self.Vg*math.cos(self.angle)

    def setMoleSpeed(self, v: float) -> None:
        self.Vg = math.copysign(v, self.Vg)
        self.Vy = v*math.sin(self.angle)
        self.Vx = v*math.cos(self.angle)

    def moveMole(self) -> None:
        self.dx = 1/FREQUENCY*self.Vx
        self.dy = 1/FREQUENCY*self.Vy
        # Molecule meets right/left wall
        if self.x+self.dx+MOLE_RADIUS >= SCREEN_WIDTH and self.Vx > 0:
            s = abs(1/FREQUENCY*self.Vx)
            self.dx = SCREEN_WIDTH - (self.x + MOLE_RADIUS)
            self.x = round(SCREEN_WIDTH - (s-self.dx))
            self.Vx *= -1
            self.angle = math.pi - self.angle
        elif self.x+self.dx-MOLE_RADIUS <= 0 and self.Vx < 0:
            s = abs(1/FREQUENCY*self.Vx)
            self.dx = self.x-MOLE_RADIUS
            self.x = round(s-self.dx)
            self.Vx *= -1
            self.angle = math.pi - self.angle
        else:
            self.x += round(self.dx)
        # Molecule meets upper/lower wall
        if self.y+self.dy+MOLE_RADIUS >= SCREEN_HEIGHT and self.Vy > 0:
            s = abs(1/FREQUENCY*self.Vy)
            self.dy = SCREEN_HEIGHT - (self.y + MOLE_RADIUS)
            self.y = round(SCREEN_HEIGHT - (s-self.dy))
            self.Vy *= -1
            self.angle = 2*math.pi - self.angle
        elif self.y+self.dy-MOLE_RADIUS <= 0 and self.Vy < 0:
            s = abs(1/FREQUENCY*self.Vy)
            self.dy = self.y-MOLE_RADIUS
            self.y = round(s-self.dy)
            self.Vy *= -1
            self.angle = 2*math.pi - self.angle
        else:
            self.y += round(self.dy)