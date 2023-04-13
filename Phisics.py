import random
import math

MOLE_RADIUS = 3
MOLE_MASS = 1
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

class Physics:
    def __init__(self, n: int, V_global: float) -> None:
        self.N = n
        self.Vg = V_global
        self.Moles = [Mole(V_global) for _ in range(n)]
        for i in range(len(self.Moles)):
            self.Moles[i].init_position()

        collide = self.get_collision_idx()
        while(len(collide) != 0):
            for j in range(len(collide)):
                self.Moles[j].init_position()
            collide = self.get_collision_idx()

    def get_collision_idx(self) -> list[int]:
        collision = []
        for i in range(len(self.Moles)):
            col = [j for j in range(len(self.Moles)) if i != j and self.Moles[i].x == self.Moles[j].x and self.Moles[i].y == self.Moles[j].y]
            if col is not []:
                collision.extend(col)
        print(collision)
        return collision

    def get_moles(self):
        return self.Moles


class Mole:
    def __init__(self, Vg: float) -> None:
        self.Vg = Vg
        self.x = None
        self.y = None
        self.r = MOLE_RADIUS
        self.mass = MOLE_MASS
        self.dx = None
        self.dy = None
        self.Vx = None
        self.Vy = None
    
    def init_position(self) -> None:
        self.x = random.randint(0+MOLE_RADIUS, SCREEN_WIDTH-MOLE_RADIUS)
        self.y = random.randint(0+MOLE_RADIUS, SCREEN_HEIGHT-MOLE_RADIUS)
        angle = random.uniform(0, 2*math.pi)
        self.Vx = self.Vg*math.sin(angle)
        self.Vy = self.Vg*math.cos(angle)
