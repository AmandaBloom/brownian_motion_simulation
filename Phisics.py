import random
import math
from threading import Lock

FREQUENCY = 30  # Hertz
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
        for mole in self.Moles:
            mole.initPosition()
        self.checkInitCollisions(self.Moles)

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
        new_moles = [Mole(self.Vg) for _ in range(n)]
        for mole in new_moles:
            mole.initPosition()
        self.checkInitCollisions(new_moles)
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
        with self.lock:
            for mole1 in self.Moles:
                mole1.moveMole()
            # for mole1 in self.Moles:
            #     for mole2 in self.Moles:
            #         if mole1 is not mole2:
            #             mole1.checkMolesCollision(mole2)


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
        self.x = random.randint(0 + MOLE_RADIUS, SCREEN_WIDTH - MOLE_RADIUS)
        self.y = random.randint(0 + MOLE_RADIUS, SCREEN_HEIGHT - MOLE_RADIUS)
        self.angle = random.uniform(0, 2 * math.pi)
        self.Vy = self.Vg * math.sin(self.angle)
        self.Vx = self.Vg * math.cos(self.angle)

    def setMoleSpeed(self, v: float) -> None:
        self.Vg = math.copysign(v, self.Vg)
        self.Vy = v * math.sin(self.angle)
        self.Vx = v * math.cos(self.angle)

    def moveMole(self) -> None:
        self.dx = 1 / FREQUENCY * self.Vx
        self.dy = 1 / FREQUENCY * self.Vy
        # Molecule meets right/left wall
        if self.x + self.dx + MOLE_RADIUS >= SCREEN_WIDTH and self.Vx > 0:
            s = abs(1 / FREQUENCY * self.Vx)
            self.dx = SCREEN_WIDTH - (self.x + MOLE_RADIUS)
            self.x = round(SCREEN_WIDTH - (s - self.dx))
            self.Vx *= -1
            self.angle = math.pi - self.angle
        elif self.x + self.dx - MOLE_RADIUS <= 0 and self.Vx < 0:
            s = abs(1 / FREQUENCY * self.Vx)
            self.dx = self.x - MOLE_RADIUS
            self.x = round(s - self.dx)
            self.Vx *= -1
            self.angle = math.pi - self.angle
        else:
            self.x += round(self.dx)
        # Molecule meets upper/lower wall
        if self.y + self.dy + MOLE_RADIUS >= SCREEN_HEIGHT and self.Vy > 0:
            s = abs(1 / FREQUENCY * self.Vy)
            self.dy = SCREEN_HEIGHT - (self.y + MOLE_RADIUS)
            self.y = round(SCREEN_HEIGHT - (s - self.dy))
            self.Vy *= -1
            self.angle = 2 * math.pi - self.angle
        elif self.y + self.dy - MOLE_RADIUS <= 0 and self.Vy < 0:
            s = abs(1 / FREQUENCY * self.Vy)
            self.dy = self.y - MOLE_RADIUS
            self.y = round(s - self.dy)
            self.Vy *= -1
            self.angle = 2 * math.pi - self.angle
        else:
            self.y += round(self.dy)

    def checkMolesCollision(self, m1: "Mole") -> None:
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

        mult = self.mass / m1.mass
        m1.dx += px * mult
        m1.dy += px * mult

        # Show the mole the wae
        if t < 0:
            self.x -= t * self.dx
            self.y -= t * self.dy
        if self.x < self.r:
            self.x = self.r
        if self.x > SCREEN_WIDTH - self.r:
            self.x = SCREEN_WIDTH - self.r
        if self.y > SCREEN_HEIGHT + self.r:
            self.y = SCREEN_HEIGHT + self.r
        if self.y < self.r:
            self.y = self.r

        self.x = round(self.x)
        self.y = round(self.y)
        m1.x = round(m1.x)
        m1.y = round(m1.y)
