import random
import math
import time
from threading import Lock

FREQUENCY = 50  # Hertz
MOLE_RADIUS = 15
MOLE_MASS = 1
SCREEN_WIDTH = 700 - MOLE_RADIUS
SCREEN_HEIGHT = 700 - MOLE_RADIUS
GRID_WIDTH = 10
GRID_HEIGHT = 10
VOLUME = 49.00


class Physics:
    def __init__(self, n: int, V_global: float) -> None:
        self.lock = Lock()
        self.iter = 0
        self.lc_iter = 0  # last change iteration
        self.N = n
        self.Vg = V_global
        self.Vol = VOLUME
        self.wall_area = 2 * (SCREEN_HEIGHT + SCREEN_WIDTH)
        self.wall_momentum = 32 * [0.0]
        self.kT = 0
        self.Moles = []
        self.Brownian = None
        self.BrownianPositions = []
        self.fps = 0
        self.fps_iter = 0
        self.start_time = time.time()

        self.addBrownianMole()
        self.addMoles(self.N - 1)

    def getMoles(self) -> list["Mole"]:
        return self.Moles

    def setGlobalSpeed(self, v: float) -> None:
        self.Vg = v

    def addBrownianMole(self) -> None:
        moles_init_pos = [
            random.sample(range(SCREEN_WIDTH), 1),
            random.sample(range(SCREEN_WIDTH), 1),
        ]
        mole = BrownianMole(
            Vg=self.Vg, x=moles_init_pos[0][0], y=moles_init_pos[1][0], colour=8
        )
        self.Moles.extend([mole])
        self.Brownian = mole

    def addMoles(self, n: int) -> None:
        moles_init_pos = [
            random.sample(range(SCREEN_WIDTH), n),
            random.sample(range(SCREEN_WIDTH), n),
        ]
        new_moles = [
            Mole(self.Vg, moles_init_pos[0][idx], moles_init_pos[1][idx])
            for idx in range(n)
        ]
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

    def doIter(self) -> None:
        self.iter += 1
        self.fps_iter += 1
        momentum = 0

        for mole1 in self.Moles:
            mole1.calcRoute()
        for mole1 in self.Moles:
            momentum += mole1.moveMole()
        if momentum != 0:
            self.wall_momentum[self.iter % len(self.wall_momentum)] = momentum
            self.lc_iter = 30
        if self.lc_iter != 0 and momentum == 0:
            self.lc_iter -= 1
        if self.lc_iter == 0 and momentum == 0:
            self.wall_momentum[self.iter % len(self.wall_momentum)] = momentum
        colliding = []
        for idx, mole1 in enumerate(self.Moles):
            for mole2 in self.Moles[idx:]:
                if (
                    mole1 is not mole2
                    and mole1.isClose2(mole2)
                    and mole1.overlaps(mole2)
                ):
                    mole1.resolveMolesCollision(mole2)
                    colliding.append((mole1, mole2))

        for mole1, mole2 in colliding:
            mole1.bounce(mole2)

        self.kT = self.getMolesEnergy()
        self.BrownianPositions.extend([self.Brownian.getBrownianPosition()])
        self.calcFPS()

    def getWallMomentum(self) -> float:
        return sum(self.wall_momentum) / len(self.wall_momentum)

    def getMolesEnergy(self) -> float:
        e = 0
        for mole in self.Moles:
            e += mole.getEnergy()
        return 2 / 3 * e * 1e-6

    def getVol(self) -> float:
        return self.Vol

    def getN(self) -> float:
        return self.N

    def getKT(self) -> float:
        return self.kT

    def calcFPS(self):
        if (time.time() - self.start_time) > 1:
            self.fps = self.fps_iter / (time.time() - self.start_time)
            self.fps_iter = 0
            self.start_time = time.time()

    def getFPS(self) -> float:
        return int(self.fps)

    def getBrownianPositions(self):
        return self.BrownianPositions

    def clearBrownianPositions(self):
        self.BrownianPositions = []


class Mole:
    def __init__(self, Vg: float, x: int, y: int, angle=None, colour=0) -> None:
        self.r = MOLE_RADIUS
        self.mass = MOLE_MASS
        self.color_idx = colour
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
        self.dx = None  # 1 / FREQUENCY * self.Vx
        self.dy = None  # 1 / FREQUENCY * self.Vy
        self.gx = int(self.x / GRID_WIDTH)
        self.gy = int(self.y / GRID_HEIGHT)

    def setMoleSpeed(self, v: float) -> None:
        # new mole speed is fractal of its new and old speed
        if self.Vg != 0:
            self.V = (v / self.Vg) * self.V
            self.Vg = v
            self.Vy = self.V * math.sin(self.angle)
            self.Vx = self.V * math.cos(self.angle)

    def getEnergy(self) -> float:
        self.Vg = math.sqrt(self.Vx**2 + self.Vy**2)
        return 0.5 * self.mass * self.Vg * self.Vg

    def calcRoute(self) -> None:
        self.dx = 1 / FREQUENCY * self.Vx
        self.dy = 1 / FREQUENCY * self.Vy

    def isClose2(self, m1: "Mole") -> bool:
        # if a molecule is in a grid square next to another
        # molecule or they are in the same square
        if abs(m1.gx - self.gx) <= 1 and abs(m1.gy - self.gy) <= 1:
            return True
        return False

    def moveMole(self) -> float:
        """
        Function used to hit a wall by a mole
        returns hit wall momentum
        """
        # Molecule meets right/left wall
        hit_wall_mmnt = 0
        s = 0
        if self.x + self.dx + MOLE_RADIUS >= SCREEN_WIDTH and self.Vx > 0:
            s = abs(1 / FREQUENCY * self.Vx)
            self.dx = SCREEN_WIDTH - (self.x + MOLE_RADIUS)
            self.x = round(SCREEN_WIDTH - (s - self.dx))
            self.Vx *= -1
            self.angle = math.pi - self.angle
            hit_wall_mmnt += self.mass * self.mass * s
        elif self.x + self.dx - MOLE_RADIUS <= 0 and self.Vx < 0:
            s = abs(1 / FREQUENCY * self.Vx)
            self.dx = self.x - MOLE_RADIUS
            self.x = round(s - self.dx)
            self.Vx *= -1
            self.angle = math.pi - self.angle
            hit_wall_mmnt += self.mass * self.mass * s
        else:
            self.x += round(self.dx)
        # Molecule meets upper/lower wall
        if self.y + self.dy + MOLE_RADIUS >= SCREEN_HEIGHT and self.Vy > 0:
            s = abs(1 / FREQUENCY * self.Vy)
            self.dy = SCREEN_HEIGHT - (self.y + MOLE_RADIUS)
            self.y = round(SCREEN_HEIGHT - (s - self.dy))
            self.Vy *= -1
            self.angle = 2 * math.pi - self.angle
            hit_wall_mmnt += self.mass * self.mass * s
        elif self.y + self.dy - MOLE_RADIUS <= 0 and self.Vy < 0:
            s = abs(1 / FREQUENCY * self.Vy)
            self.dy = self.y - MOLE_RADIUS
            self.y = round(s - self.dy)
            self.Vy *= -1
            self.angle = 2 * math.pi - self.angle
            hit_wall_mmnt += self.mass * self.mass * s
        else:
            self.y += round(self.dy)

        self.gx = int(self.x / GRID_WIDTH)
        self.gy = int(self.y / GRID_HEIGHT)
        hit_wall_mmnt = self.mass * self.mass * s
        return hit_wall_mmnt

    def overlaps(self, m1: "Mole") -> bool:
        return abs((self.y - m1.y) ** 2 + (self.x - m1.x) ** 2) <= (self.r + m1.r) ** 2

    def resolveMolesCollision(self, m1: "Mole") -> None:
        d = math.sqrt((self.y - m1.y) ** 2 + (self.x - m1.x) ** 2)
        if d == 0:
            d += 0.001
        overlap = 0.5 * (d - self.r - m1.r)
        self.x -= round(overlap * (self.x - m1.x) / d)
        self.y -= round(overlap * (self.y - m1.y) / d)
        m1.x += round(overlap * (self.x - m1.x) / d)
        m1.x += round(overlap * (self.y - m1.y) / d)

    def bounce(self, m1: "Mole") -> None:
        d = math.sqrt((self.y - m1.y) ** 2 + (self.x - m1.x) ** 2)
        if d == 0:
            d += 0.001

        # Some 300 IQ maths
        nx = (m1.x - self.x) / d
        ny = (m1.y - self.y) / d
        tx = -ny
        ty = nx
        dTan1 = self.Vx * tx + self.Vy * ty
        dTan2 = m1.Vx * tx + m1.Vy * ty
        dNorm1 = self.Vx * nx + self.Vy * ny
        dNorm2 = m1.Vx * nx + m1.Vy * ny

        # Conservation of momenmtum
        mom1 = (dNorm1 * (self.mass - m1.mass) + 2 * m1.mass * dNorm2) / (
            self.mass + m1.mass
        )
        mom2 = (dNorm2 * (m1.mass - self.mass) + 2 * self.mass * dNorm1) / (
            self.mass + m1.mass
        )

        # Update ball velocities
        self.Vx = tx * dTan1 + nx * mom1
        self.Vy = ty * dTan1 + ny * mom1
        m1.Vx = tx * dTan2 + nx * mom2
        m1.Vy = ty * dTan2 + ny * mom2


class BrownianMole(Mole):
    def __init__(self, Vg: float, x: int, y: int, angle=None, colour=0) -> None:
        super().__init__(Vg, x, y, angle, colour)

    def getBrownianPosition(self):
        return (self.x, self.y)
