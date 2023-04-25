import random
import math
from time import time
from threading import Lock

FREQUENCY = 50  # Hertz
MOLE_RADIUS = 6
MOLE_MASS = 1
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GRID_WIDTH = 10
GRID_HEIGHT = 10
VOLUME = 49.00


class Physics:
    def __init__(self, n: int, V_global: float) -> None:
        self.lock = Lock()
        self.iter = 0
        self.lc_iter = 0 # last change iteration
        self.N = n
        self.Vg = V_global
        self.Vol = VOLUME
        self.wall_area = 2* (SCREEN_HEIGHT+SCREEN_WIDTH)
        self.wall_momentum = 0.00
        self.kT = 0
        self.Moles = []

        self.addMoles(self.N)

    def getCollisionIdx(self, mole_list: list["Mole"]) -> list[int]:
        collision = []
        for mole_i in mole_list:
            col = [
                mole_j
                for mole_j in mole_list
                if mole_i != mole_j and mole_i.x == mole_j.x and mole_i.y == mole_j.y
            ]
            if col is not []:
                collision.extend(col)
        return collision

    def checkInitCollisions(self, mole_list: list["Mole"]) -> None:
        collide = self.getCollisionIdx(mole_list)
        while len(collide) != 0:
            for colider in collide:
                colider.initPosition()
            collide = self.getCollisionIdx(mole_list)

    def getMoles(self) -> list["Mole"]:
        return self.Moles

    def setGlobalSpeed(self, v: float) -> None:
        self.Vg = v

    def addMoles(self, n: int) -> None:
        moles_init_pos = [random.sample(range(SCREEN_WIDTH), n), random.sample(range(SCREEN_WIDTH), n)]
        new_moles = [Mole(self.Vg, moles_init_pos[0][idx], moles_init_pos[1][idx]) for idx in range(n)]
        self.Moles.extend(new_moles)
        self.N += n

    def delMoles(self, n: int) -> None:
        self.N -= n
        self.Moles = self.Moles[0 : self.N]

    def setMoleCount(self, n: int) -> None:
        if n > self.N:
            self.addMoles(n - self.N)
        elif n < self.N:
            self.delMoles(self.N - n)

    def setMolesSpeed(self) -> None:
        with self.lock:
            for mole in self.Moles:
                mole.setMoleSpeed(self.Vg)

    def moveMoles(self) -> None:
        self.iter += 1
        momentum = 0
        self.kT = 0

        for mole1 in self.Moles:
            mole1.calcRoute()
        for mole1 in self.Moles:
            momentum += mole1.moveMole()
        if momentum != 0:
            self.wall_momentum = momentum
            self.lc_iter = 30
        if self.lc_iter != 0 and momentum == 0:
            self.lc_iter -= 1
        if self.lc_iter == 0 and momentum == 0:
            self.wall_momentum = momentum
        #print(self.iter)
        colliding = []
        for idx, mole1 in enumerate(self.Moles):
            for mole2 in self.Moles[idx:]:
                if mole1 is not mole2 and mole1.isClose2(mole2) and mole1.overlaps(mole2):
                    mole1.resolveMolesCollision(mole2)
                    colliding.append((mole1,mole2))    
            self.kT += mole1.getEnergy()/1.5
        
        for mole1, mole2 in colliding:
            mole1.bounce(mole2)

        self.kT *= 1e-4

    def getWallMomentum(self) -> float:
        return "{:.2f}".format(self.wall_momentum)
    
    def getKT(self) -> float:
        return "{:.2f}".format(self.kT)
    

class Mole:
    def __init__(self, Vg: float, x: int, y: int, angle=None) -> None:
        self.r = MOLE_RADIUS
        self.mass = MOLE_MASS
        self.color_idx = 0
        self.Vg = self.Vinit = Vg
        if angle is None:
            self.angle = random.uniform(0, 2 * math.pi)
        else:
            self.angle = angle
        self.x = x
        self.y = y
        self.V = self.Vg
        self.Vy = self.V * math.sin(self.angle)
        self.Vx = self.V * math.cos(self.angle)
        self.dx = None # 1 / FREQUENCY * self.Vx
        self.dy = None # 1 / FREQUENCY * self.Vy
        self.gx = int(self.x/GRID_WIDTH)
        self.gy = int(self.y/GRID_HEIGHT)

    def setMoleSpeed(self, v: float) -> None:
        # new mole speed is fractal of its new and old speed
        self.V = (v/self.Vg)*self.V
        self.Vg = v
        self.Vy = self.V * math.sin(self.angle)
        self.Vx = self.V * math.cos(self.angle)

    def getEnergy(self):
        return 0.5 * self.mass * self.Vg * self.Vg

    def calcRoute(self) -> None:
        self.dx = 1 / FREQUENCY * self.Vx
        self.dy = 1 / FREQUENCY * self.Vy

    def isClose2(self, m1: 'Mole') -> bool:
        # if a molecule is in a grid square next to another 
        # molecule or they are in the same square
        if abs(m1.gx-self.gx) <= 1 and abs(m1.gy-self.gy) <= 1:
            return True
        return False
    
    def moveMole(self) -> float:
        '''
        Function used to hit a wall by a mole
        returns hit wall momentum
        '''
        # Molecule meets right/left wall
        hit_wall_mmnt = 0
        s = 0
        if self.x + self.dx + MOLE_RADIUS >= SCREEN_WIDTH and self.Vx > 0:
            s = abs(1 / FREQUENCY * self.Vx)
            self.dx = SCREEN_WIDTH - (self.x + MOLE_RADIUS)
            self.x = round(SCREEN_WIDTH - (s - self.dx))
            self.Vx *= -1
            self.angle = math.pi - self.angle
            hit_wall_mmnt += self.mass*self.mass*s
        elif self.x + self.dx - MOLE_RADIUS <= 0 and self.Vx < 0:
            s = abs(1 / FREQUENCY * self.Vx)
            self.dx = self.x - MOLE_RADIUS
            self.x = round(s - self.dx)
            self.Vx *= -1
            self.angle = math.pi - self.angle
            hit_wall_mmnt += self.mass*self.mass*s
        else:
            self.x += round(self.dx)
        # Molecule meets upper/lower wall
        if self.y + self.dy + MOLE_RADIUS >= SCREEN_HEIGHT and self.Vy > 0:
            s = abs(1 / FREQUENCY * self.Vy)
            self.dy = SCREEN_HEIGHT - (self.y + MOLE_RADIUS)
            self.y = round(SCREEN_HEIGHT - (s - self.dy))
            self.Vy *= -1
            self.angle = 2 * math.pi - self.angle
            hit_wall_mmnt += self.mass*self.mass*s
        elif self.y + self.dy - MOLE_RADIUS <= 0 and self.Vy < 0:
            s = abs(1 / FREQUENCY * self.Vy)
            self.dy = self.y - MOLE_RADIUS
            self.y = round(s - self.dy)
            self.Vy *= -1
            self.angle = 2 * math.pi - self.angle
            hit_wall_mmnt += self.mass*self.mass*s
        else:
            self.y += round(self.dy)

        self.gx = int(self.x/GRID_WIDTH)
        self.gy = int(self.y/GRID_HEIGHT)
        hit_wall_mmnt = self.mass*self.mass*s
        return hit_wall_mmnt

    def overlaps(self, m1: "Mole") -> None:
        return abs((self.y - m1.y)**2 + (self.x - m1.x)**2) <= (self.r + m1.r)**2

    def resolveMolesCollision(self, m1: "Mole") -> None:
        d = math.sqrt((self.y - m1.y)**2 + (self.x - m1.x)**2)
        if d == 0:
            d += .001
        overlap = 0.5 * (d-self.r-m1.r)
        self.x -= round(overlap * (self.x - m1.x) / d)
        self.y -= round(overlap * (self.y - m1.y) / d)
        m1.x += round(overlap * (self.x - m1.x) / d)
        m1.x += round(overlap * (self.y - m1.y) / d)

    def bounce(self, m1: "Mole") -> None:
        d = math.sqrt((self.y - m1.y)**2 + (self.x - m1.x)**2)
        if d == 0:
            d += .001
        nx = (m1.x - self.x) / d
        ny = (m1.y - self.y) / d
        
        tx = -ny
        ty = nx

        dTan1 = self.Vx * tx + self.Vy * ty
        dTan2 = m1.Vx * tx + m1.Vy * ty

        dNorm1 = self.Vx * nx + self.Vy * ny
        dNorm2 = m1.Vx * nx + m1.Vy * ny

        # conservation of momenmtum
        mom1 = (dNorm1 * (self.mass - m1.mass) + 2 * m1.mass * dNorm2) / (self.mass + m1.mass)
        mom2 = (dNorm2 * (m1.mass - self.mass) + 2 * self.mass * dNorm1) / (self.mass + m1.mass)

        # Update ball velocities
        self.Vx = tx * dTan1 + nx * mom1
        self.Vy = ty * dTan1 + ny * mom1
        m1.Vx = tx * dTan2 + nx * mom2
        m1.Vy = ty * dTan2 + ny * mom2

    def checkMolesCollision1(self, m1: "Mole") -> None:
        if self.dx == 0 or self.dy == 0:
            return
        # self.dx += 0.001
        sdx = self.dx - m1.dx
        sx = self.x - m1.x
        sdy = self.dy - m1.dy
        sy = self.y - m1.y
        mindist = self.r + m1.r
        a = (sdx * sdx) + (sdy * sdy)
        b = 2 * ((sx * sdx) + (sy * sdy))
        c = (sx * sx + sy * sy) - (mindist * mindist)

        if (b * b) - (4 * a * c) < 0:
           return
        t = (-b - math.sqrt((b * b) - (4 * a * c))) / a
        t2 = (-b + math.sqrt((b * b) - (4 * a * c))) / a
        if abs(t) > abs(t2):
            t = t2

        # Calculation of collision point and teleport to it
        # Now they got 1 point in a common
        self.x += t * self.dx
        self.y += t * self.dy

        # Calculation of vector centre to centre and its normal
        sx = self.x - m1.x
        sy = self.y - m1.y
        sxynorm = math.sqrt((sx * sx) + (sy * sy))
        sxn = sx / sxynorm
        syn = sy / sxynorm

        # Speed of mass center
        summass = self.mass + m1.mass
        sumdx = (self.mass * self.dx + m1.mass * m1.dx) / summass
        sumdy = (self.mass * self.dy + m1.mass * m1.dy) / summass

        # Get summary speed from moles momentum and calc vectors of
        # where they will go
        pn = (self.dx - sumdx) * sxn + (self.dy - sumdy) * syn
        px = 2 * sxn * pn
        py = 2 * syn * pn

        # Substract vec from Mole momentum
        self.dx -= px
        self.dy -= py
        self.angle = math.atan(self.dy/self.dx)

        mult = self.mass / m1.mass
        m1.dx += px * mult
        m1.dy += px * mult
        m1.angle = math.atan(m1.dy/m1.dx)

        self.color_idx = int(100*time()%10)
        m1.color_idx = int(100*time()%10)
        #print("collision btwn: ", self, " ", m1)

        # Show the mole the wae
        # if t < 0:
        #     self.x -= t * self.dx
        #     self.y -= t * self.dy
        # if self.x < self.r:
        #     self.x = self.r
        # if self.x > SCREEN_WIDTH - self.r:
        #     self.x = SCREEN_WIDTH - self.r
        # if self.y > SCREEN_HEIGHT + self.r:
        #     self.y = SCREEN_HEIGHT + self.r
        # if self.y < self.r:
        #     self.y = self.r
        
        self.x = round(self.x)
        self.y = round(self.y)
        m1.x = round(m1.x)
        m1.y = round(m1.y)

    def checkMolesCollision2(self, m1: "Mole") -> None:
        # if self.dx == 0 or self.dy == 0:
        #     return
        # A1 = ly2 - ly1; 
        # B1 = lx1 - lx2; 
        # C1 = (ly2 - ly1)*lx1 + (lx1 - lx2)*ly1; 
        # C2 = -B1*x0 + A1*y0; 
        # det = A1*A1 - -B1*B1; 
        # cx = 0; 
        # cy = 0; 
        # if det != 0:
        #     cx = (float)((A1*C1 - B1*C2)/det); 
        #     cy = (float)((A1*C2 - -B1*C1)/det); 
        # else:
        #     cx = x0 
        #     cy = y0
     
        d = math.sqrt((self.dx - m1.dx)**2 + (self.dy - m1.dy)**2)
        
        nx = (m1.dx - self.dx) / d
        ny = (m1.dy - self.dy) / d
        p = 2 * (self.Vx * nx + self.Vy * ny - m1.Vx * nx - m1.Vy * ny) / (self.mass + m1.mass)
        self.Vx = self.Vx - p * self.mass * nx
        self.Vy = self.Vy - p * self.mass * ny
        m1.Vx = m1.Vx + p * m1.mass * nx
        m1.Vy = m1.Vy + p * m1.mass * ny
        
